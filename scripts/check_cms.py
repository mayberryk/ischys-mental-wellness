"""Exercise CMS migration fidelity, draft gating, uploads and safe Markdown rendering."""
from pathlib import Path
import json,subprocess,sys,tempfile,shutil
from html.parser import HTMLParser
from cms_content import load_articles,render_article
ROOT=Path(__file__).resolve().parents[1]
class Text(HTMLParser):
    def __init__(self):super().__init__();self.words=[]
    def handle_data(self,data):self.words.append(data)
source=json.loads((ROOT/'content/source-sections.json').read_text())
archive=json.loads((ROOT/'docs/content-before-cms/articles.json').read_text())
articles=load_articles(ROOT)
by_key={a['key']:a for a in articles}
for old in archive:
    new=by_key[old['key']]
    for field,value in old.items():assert new[field]==value,(old['key'],field)
    html,_=render_article(new);text=Text();text.feed(html)
    actual=' '.join(' '.join(text.words).split())
    for block in source[old['key']]['blocks']:assert ' '.join(block['text'].split()) in actual
html,_=render_article({'body':'<script>alert(1)</script>\n\n[bad](javascript:alert(1))\n\n# Heading'})
assert '<script>' not in html and 'href="javascript:' not in html and '<h1' not in html
with tempfile.TemporaryDirectory(prefix='ischys-cms-test-') as tmp:
    root=Path(tmp)
    for folder in ('scripts','content','templates','static','assets','output/pdf'):
        shutil.copytree(ROOT/folder,root/folder,ignore=shutil.ignore_patterns('__pycache__'))
    file=root/'content/articles/cms-test.json'
    item={'key':'cms-test','title':'CMS workflow test','description':'Test introduction','body':'## Test section\n\n**Formatted text** and a [link](/learning/).','references':[],'services':[]}
    def save():file.write_text(json.dumps(item))
    def build(*args):subprocess.run([sys.executable,str(root/'scripts/build.py'),*args],check=True,capture_output=True)
    save();build();page=root/'dist/learning/cms-test/index.html';assert not page.exists()
    item['status']='published';save();build();assert not page.exists()
    item['approved']=True;save();build();assert '<strong>Formatted text</strong>' in page.read_text()
    uploads=root/'assets/uploads';uploads.mkdir(exist_ok=True)
    (uploads/'test.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1" height="1"/>')
    (uploads/'attachment.txt').write_text('Attachment test')
    item.update(image='/assets/uploads/test.svg',image_alt='Test image',attachment='/assets/uploads/attachment.txt');save();build()
    assert (root/'dist/assets/uploads/attachment.txt').exists()
    assert 'alt="Test image"' in page.read_text()
    item['status']='draft';save();build();assert not page.exists()
    build('--include-drafts','--output','.draft-preview');assert (root/'.draft-preview/learning/cms-test/index.html').exists()
print('PASS: all ten articles retain metadata, URLs and wording; CMS drafts, approval, unpublishing, Markdown safety and uploads.')
