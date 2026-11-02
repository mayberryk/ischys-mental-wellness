"""Content/build regression checks; no network requests or external packages."""
from pathlib import Path
from html.parser import HTMLParser
from urllib.parse import urlsplit,unquote
import json,subprocess,sys,re
from cms_content import load_articles
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],check=True)
class Page(HTMLParser):
 def __init__(self):super().__init__(convert_charrefs=True);self.refs=[];self.ids=[];self.h1=0;self.title='';self.in_title=False;self.jsons=[];self.in_json=False;self.buf='';self.description=None;self.all_text=[]
 def handle_starttag(self,t,attrs):
  a=dict(attrs)
  if t=='h1':self.h1+=1
  if t=='title':self.in_title=True
  if t=='script' and a.get('type')=='application/ld+json':self.in_json=True;self.buf=''
  if 'id'in a:self.ids.append(a['id'])
  if t=='meta' and a.get('name')=='description':self.description=a.get('content')
  for key in ('href','src'):
   if key in a:self.refs.append(a[key])
 def handle_endtag(self,t):
  if t=='title':self.in_title=False
  if t=='script' and self.in_json:self.jsons.append(json.loads(self.buf));self.in_json=False
 def handle_data(self,s):
  if self.in_title:self.title+=s
  if self.in_json:self.buf+=s
  if not self.in_json:self.all_text.append(s)
errors=[];parsed={}
for path in OUT.rglob('*.html'):
 p=Page();p.feed(path.read_text());parsed[path]=p
for path,p in parsed.items():
 for ref in p.refs:
  url=urlsplit(ref)
  if url.scheme or url.netloc:continue
  if not url.path:
   if url.fragment and unquote(url.fragment) not in p.ids:errors.append(f'{path}: missing anchor {ref}')
   continue
  target=OUT/url.path.lstrip('/') if url.path.startswith('/') else path.parent/url.path
  if target.is_dir():target=target/'index.html'
  if not target.exists():errors.append(f'{path}: broken link {ref}')
  if url.fragment and target in parsed and unquote(url.fragment) not in parsed[target].ids:errors.append(f'{path}: broken fragment {ref}')
 if len(p.ids)!=len(set(p.ids)):errors.append(f'{path}: duplicate IDs')
manifest=json.loads((OUT/'page-manifest.json').read_text());titles=[];descriptions=[]
for entry in manifest:
 p=parsed[OUT/entry['file']]
 if p.h1!=1:errors.append(f'{entry["path"]}: expected one H1, got {p.h1}')
 if not p.description:errors.append(f'{entry["path"]}: missing description')
 if not p.jsons:errors.append(f'{entry["path"]}: missing schema')
 titles.append(p.title);descriptions.append(p.description)
 text=' '.join(p.all_text)
 for forbidden in ['90-minute','90-Minute','$350','$175','$225','href="#"','QR CODE:','Texas','California','TX & CA','Salt Lake City','Ischys Mental Wellness','privacy@ischysmentalwellness.com','legal@ischysmentalwellness.com']:
  if forbidden in text:errors.append(f'{entry["path"]}: stale content {forbidden}')
 if entry['path'] not in ('/404.html',) and '802 E Bamberger Dr, Suite D' not in text:errors.append(f'{entry["path"]}: address missing')
 if 'cdn.tailwindcss.com' in (OUT/entry['file']).read_text():errors.append('Runtime Tailwind remains')
if len(titles)!=len(set(titles)):errors.append('Duplicate page titles')
if len(descriptions)!=len(set(descriptions)):errors.append('Duplicate page descriptions')
# All source content is retained in article output, after documented whitespace/encoding repairs.
source=json.loads((ROOT/'content/source-sections.json').read_text())
for item in load_articles(ROOT):
 if item.get('status')!='published' or item.get('approved') is not True:continue
 if item.get('source_file'):source[item['key']]=json.loads((ROOT/'content'/item['source_file']).read_text())
 text=' '.join(parsed[OUT/item['path'].lstrip('/')/'index.html'].all_text)
 norm=lambda v:re.sub(r'\s+',' ',v).strip()
 for block in source.get(item['key'],{}).get('blocks',[]):
  if norm(block['text']) not in norm(text):errors.append(f'{item["key"]}: missing source block {block["text"][:60]}')
if len(list((OUT/'downloads').glob('*.pdf')))!=13:errors.append('Expected 13 downloadable PDFs')
# The web toolkit may regroup print lines, but must retain the supplied wording.
resource_keys=('welcome','starting-point','wellness-plan','hard-day','resources')
resource_norm=lambda value:re.sub(r'[^\w]+',' ',value).strip().casefold()
for key in resource_keys:
 page=parsed[OUT/'patient-resources'/key/'index.html']
 visible=resource_norm(' '.join(page.all_text))
 for block in source[key]['blocks']:
  text=block['text']
  if text.startswith('QR CODE:') or '→' in text or text=='Area of My Life My Rating':continue
  if re.fullmatch(r'[\d\s]+',text):continue
  text=re.sub(r'\s+0 1 2 3 4 5 6 7 8 9$','',text)
  if resource_norm(text) not in visible:errors.append(f'{key}: missing resource wording {text[:70]}')
for pdf in (OUT/'downloads').glob('*.pdf'):
 if not pdf.read_bytes().startswith(b'%PDF-'):errors.append(f'Invalid PDF {pdf}')
# The incomplete live configuration must not accidentally pass a production build.
r=subprocess.run([sys.executable,str(ROOT/'scripts/build.py'),'--production'],capture_output=True,text=True)
config=json.loads((ROOT/'content/site.json').read_text())
if not config['production_url'] and r.returncode==0:errors.append('Production build should reject missing domain')
# Regression checks for the client-requested routes and shared insurance list.
booking=config['scheduling_url']
for service in json.loads((ROOT/'content/services.json').read_text()):
 page=parsed[OUT/service['slug']/'index.html']
 if booking not in page.refs:errors.append('Service missing exact scheduling link: '+service['slug'])
 if config['phone_href'] not in page.refs:errors.append('Service missing phone consultation: '+service['slug'])
for route in ('portal','referral','consultation'):
 page=parsed[OUT/route/'index.html']
 target=config[{'portal':'portal_url','referral':'referral_url','consultation':'consultation_url'}[route]]
 if not target and 'http-equiv="refresh"' in (OUT/route/'index.html').read_text():errors.append(route+' must not redirect before independent verification')
 if target and target not in page.refs:errors.append(route+' missing verified destination')
 if config['phone_href'] not in page.refs:errors.append(route+' missing phone assistance')
for plan in json.loads((ROOT/'content/insurance.json').read_text())['plans']:
 for file in ('index.html','fees-insurance/index.html'):
  text=' '.join(parsed[OUT/file].all_text)
  if plan['status']=='active' and plan['name'] not in text:errors.append('Active insurance missing: '+plan['name'])
  if plan['status']!='active' and plan['name'] in text:errors.append('Pending insurance exposed: '+plan['name'])
if errors:
 print('\n'.join(errors));raise SystemExit(1)
print(f'PASS: {len(manifest)} pages; local assets/links/fragments, unique metadata, schema, source article coverage, 13 PDFs, and production configuration gate.')
