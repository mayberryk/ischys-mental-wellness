"""Check production config transformation without connecting to GitHub or an auth server."""
import json
from prepare_cms import ROOT,configuration
settings={'repository':'example/site','branch':'main','site_url':'https://site.example','oauth_url':'https://auth.example','oauth_endpoint':'auth'}
config=configuration(settings)
assert 'local_backend' not in config
assert 'localhost' not in json.dumps(config)
assert config['backend']['name']=='github'
assert config['publish_mode']=='editorial_workflow'
assert config['collections']==json.loads((ROOT/'cms/config.yml').read_text())['collections']
for bad in ('','http://site.example','https://localhost','https://user:password@site.example','https://site.example/path'):
    try:configuration(dict(settings,site_url=bad))
    except ValueError:pass
    else:raise AssertionError('Unsafe or incomplete site URL accepted: '+bad)
print('PASS: production backend, local configuration removal, collections preserved, invalid origins rejected.')
