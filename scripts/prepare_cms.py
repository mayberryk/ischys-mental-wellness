"""Package a static GitHub-backed CMS after production settings are confirmed. Never deploys."""
from pathlib import Path
from urllib.parse import urlsplit
import argparse,json,re,shutil
ROOT=Path(__file__).resolve().parents[1]
def origin(value):
    u=urlsplit(value)
    if u.scheme!='https' or not u.hostname or u.username or u.password or u.query or u.fragment or u.path not in ('','/') or u.hostname in ('localhost','127.0.0.1','::1'):
        raise ValueError('Site and OAuth URLs must be confirmed HTTPS origins')
    return value.rstrip('/')
def configuration(settings):
    if not re.fullmatch(r'[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+',settings.get('repository','')):raise ValueError('Confirm the owner/repository')
    if not re.fullmatch(r'[A-Za-z0-9_/-]+',settings.get('branch','')):raise ValueError('Confirm the deployment branch')
    endpoint=settings.get('oauth_endpoint','auth')
    if not re.fullmatch(r'[A-Za-z0-9_/-]+',endpoint) or endpoint.startswith('/') or '..' in endpoint:raise ValueError('Invalid OAuth endpoint')
    site=origin(settings.get('site_url',''));auth=origin(settings.get('oauth_url',''))
    config=json.loads((ROOT/'cms/config.yml').read_text())
    config.pop('local_backend',None)
    config['backend']={'name':'github','repo':settings['repository'],'branch':settings['branch'],'base_url':auth,'auth_endpoint':endpoint}
    config.update(site_url=site,display_url=site,logo_url=site+'/assets/ischys-original-logo-vector.svg')
    return config

def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--settings',required=True);args=parser.parse_args()
    settings=json.loads(Path(args.settings).read_text());config=configuration(settings)
    if settings.get('dependency_review_approved') is not True:raise ValueError('Resolve or explicitly approve the documented dependency review before packaging a live editor')
    vendor=ROOT/'node_modules/decap-cms/dist'
    if not (vendor/'decap-cms.js').is_file():raise ValueError('Run npm ci first')
    out=ROOT/'.cms-release/admin'
    if out.exists():raise ValueError('Archive the existing .cms-release folder before preparing a new package')
    out.mkdir(parents=True)
    (out/'config.yml').write_text(json.dumps(config,ensure_ascii=False,indent=2)+'\n')
    shutil.copy2(ROOT/'cms/preview.js',out/'preview.js')
    shutil.copytree(vendor,out/'vendor',ignore=shutil.ignore_patterns('*.map'))
    (out/'index.html').write_text('''<!doctype html><html lang="en"><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><meta name="robots" content="noindex,nofollow"><title>Ischys Content Editor</title><link href="/admin/config.yml" type="text/yaml" rel="cms-config-url"><link rel="stylesheet" href="/admin/vendor/cms.css"></head><body><script src="/admin/vendor/decap-cms.js"></script><script src="/admin/preview.js"></script></body></html>''')
    print('Prepared '+str(out)+'. Not deployed. Authentication and hosting must be configured separately.')
if __name__=='__main__':
    try:main()
    except (ValueError,KeyError) as exc:raise SystemExit(str(exc))
