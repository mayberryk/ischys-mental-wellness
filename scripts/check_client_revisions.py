"""Verify draft exclusion, unpublishing cleanup and insurance updates in an isolated fixture."""
from pathlib import Path
import tempfile,shutil,json,subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
with tempfile.TemporaryDirectory(prefix='ischys-check-') as tmp:
 root=Path(tmp)
 for folder in ('scripts','content','templates','static','output/pdf'):
  shutil.copytree(ROOT/folder,root/folder,ignore=shutil.ignore_patterns('__pycache__'))
 for folder in ('assets/insurance','assets/laura'):
  shutil.copytree(ROOT/folder,root/folder)
 logo=json.loads((ROOT/'content/site.json').read_text())['original_logo_path']
 (root/logo).parent.mkdir(parents=True,exist_ok=True)
 shutil.copy2(ROOT/logo,root/logo)
 def save(path,value):path.write_text(json.dumps(value))
 def build(*extra):subprocess.run([sys.executable,str(root/'scripts/build.py'),*extra],check=True,capture_output=True,text=True)
 articles_path=root/'content/articles.json';articles=json.loads(articles_path.read_text())
 draft={'key':'draft-check','path':'/learning/draft-check/','title':'Unapproved draft check','description':'Not for publication','services':[],'references':[],'source_file':'article-bodies/draft-check.json'}
 (root/'content/article-bodies').mkdir(exist_ok=True)
 save(root/'content/article-bodies/draft-check.json',{'blocks':[{'type':'p','text':'Unapproved content must stay private.'}]})
 articles.append(draft);save(articles_path,articles);build()
 assert not (root/'dist/learning/draft-check/index.html').exists()
 assert 'draft-check' not in (root/'dist/learning/index.html').read_text()
 draft.update(status='published',approved=False);save(articles_path,articles);build()
 assert not (root/'dist/learning/draft-check/index.html').exists()
 draft['approved']=True;save(articles_path,articles);build()
 assert (root/'dist/learning/draft-check/index.html').exists()
 draft['status']='draft';save(articles_path,articles);build()
 assert not (root/'dist/learning/draft-check/index.html').exists(), 'Formerly published draft remained accessible'
 build('--include-drafts','--output','.draft-preview')
 assert (root/'.draft-preview/learning/draft-check/index.html').exists()
 assert 'noindex,nofollow' in (root/'.draft-preview/learning/draft-check/index.html').read_text()
 plans_path=root/'content/insurance.json';plans=json.loads(plans_path.read_text());plans[0]['name']='Renamed insurance fixture';plans[1]['status']='inactive';save(plans_path,plans);build()
 for path in ('index.html','fees-insurance/index.html'):
  text=(root/'dist'/path).read_text()
  assert 'Renamed insurance fixture' in text
  assert plans[1]['name'] not in text
print('PASS: draft defaults, approval gate, unpublishing cleanup, draft preview, shared insurance updates.')
