"""CMS content adapter. Mistune is vendored (BSD-3-Clause) for offline static builds."""
from pathlib import Path
import json,re,sys
from html import unescape
sys.path.insert(0,str(Path(__file__).parent/'vendor'))
import mistune

def load_articles(root):
    articles=[json.loads(p.read_text()) for p in sorted((root/'content/articles').glob('*.json'))]
    keys=set();paths=set()
    for article in articles:
        key=article['key']
        article.setdefault('path','/learning/'+key+'/')
        if not re.fullmatch(r'[a-z0-9]+(?:-[a-z0-9]+)*',key):raise ValueError('Invalid article key: '+key)
        if not re.fullmatch(r'/learning/[a-z0-9]+(?:-[a-z0-9]+)*/',article['path']):raise ValueError('Invalid article URL')
        if key in keys or article['path'] in paths:raise ValueError('Duplicate article key or URL')
        keys.add(key);paths.add(article['path'])
        for field in ('image','attachment'):
            value=article.get(field)
            if value and (not value.startswith('/assets/uploads/') or '..' in value):raise ValueError('Article uploads must use /assets/uploads/')
        if article.get('image') and not article.get('image_alt'):raise ValueError('Article cover image needs descriptive alt text')
        for ref in article.get('references',[]):
            if not ref['url'].startswith('https://'):raise ValueError('References must use HTTPS')
        article.setdefault('references',[]);article.setdefault('services',[])
    return sorted(articles,key=lambda a:(a.get('order',999),a['key']))

class Renderer(mistune.HTMLRenderer):
    def __init__(self):super().__init__(escape=True);self.toc=[]
    def heading(self,text,level,**attrs):
        level=max(2,level)
        anchor='section-'+str(len(self.toc))
        self.toc.append((anchor,unescape(re.sub('<[^>]+>','',text))))
        return f'<h{level} id="{anchor}">{text}</h{level}>\n'

def render_article(article):
    renderer=Renderer()
    html=mistune.create_markdown(renderer=renderer)(article['body'])
    return html,renderer.toc


def load_insurance(root):
    plans=json.loads((root/'content/insurance.json').read_text())['plans']
    ids=set()
    for plan in plans:
        if not plan.get('id') or plan['id'] in ids:raise ValueError('Insurance plans need unique IDs')
        ids.add(plan['id'])
        if not plan.get('name') or plan.get('status') not in ('active','pending','inactive'):raise ValueError('Invalid insurance plan')
        plan.setdefault('logo','');plan.setdefault('details','')
        if plan['logo'] and (not plan['logo'].startswith(('/assets/insurance/','/assets/uploads/')) or '..' in plan['logo']):raise ValueError('Insurance logos must be local uploaded assets')
    return plans
