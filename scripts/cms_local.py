"""Isolated Decap trial: local Git workflow plus automatic static rebuilds. No remotes."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler,ThreadingHTTPServer
from urllib.parse import urlsplit,unquote
import io,json,os,shutil,subprocess,sys,tarfile,threading,time
ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'.cms-local';REPO=BASE/'repository';BUILD=BASE/'preview';OUT=BUILD/'dist'
def git(*args):return subprocess.check_output(['git','-C',str(REPO),*args],text=True).strip()
def initialize():
    if (REPO/'.git').exists():return
    REPO.mkdir(parents=True,exist_ok=True)
    for folder in ('content','assets'):
        shutil.copytree(ROOT/folder,REPO/folder,dirs_exist_ok=True)
    (REPO/'assets/uploads').mkdir(exist_ok=True)
    git('init','-b','main');git('config','user.name','Local CMS trial');git('config','user.email','local-cms@example.invalid')
    git('add','content','assets');git('commit','-m','Seed local CMS trial with existing content')

def rebuild():
    # Export main only. Editorial branches must never leak into the published preview.
    data=subprocess.check_output(['git','-C',str(REPO),'archive','main'])
    if (BUILD/'content').exists():shutil.rmtree(BUILD/'content')
    if (BUILD/'assets').exists():shutil.rmtree(BUILD/'assets')
    with tarfile.open(fileobj=io.BytesIO(data)) as archive:archive.extractall(BUILD,filter='data')
    subprocess.run([sys.executable,str(BUILD/'scripts/build.py')],check=True)

def watch():
    last=git('rev-parse','main')
    while True:
        time.sleep(1)
        current=git('rev-parse','main')
        if current!=last:
            try:rebuild();last=current;print('Published preview rebuilt.',flush=True)
            except subprocess.CalledProcessError:print('Build failed; review the article fields. Retrying after correction.',flush=True);last=current

class Handler(SimpleHTTPRequestHandler):
    def translate_path(self,path):
        path=unquote(urlsplit(path).path)
        if any(part.startswith('.') for part in Path(path).parts):return str(OUT/'not-found')
        if path.startswith('/admin/vendor/'):
            base=ROOT/'node_modules/decap-cms/dist';relative=path[len('/admin/vendor/'):]
        elif path.startswith('/admin/'):
            base=ROOT/'cms';relative=path[len('/admin/'):]
        else:base=OUT;relative=path.lstrip('/')
        result=(base/relative).resolve()
        return str(result if result==base or base in result.parents else OUT/'not-found')
    def list_directory(self,path):self.send_error(404);return None
    def end_headers(self):
        self.send_header('Cache-Control','no-store');self.send_header('X-Robots-Tag','noindex, nofollow');super().end_headers()

if __name__=='__main__':
    if not (ROOT/'node_modules/.bin/decap-server').exists():raise SystemExit('Run npm ci first.')
    initialize()
    if git('remote'):raise SystemExit('Local trial must not have Git remotes.')
    BUILD.mkdir(parents=True,exist_ok=True)
    for folder in ('scripts','templates','static','output/pdf'):
        shutil.copytree(ROOT/folder,BUILD/folder,dirs_exist_ok=True,ignore=shutil.ignore_patterns('__pycache__'))
    rebuild()
    env=dict(os.environ,MODE='git',GIT_REPO_DIRECTORY=str(REPO),PORT='8082',BIND_HOST='127.0.0.1',ORIGIN='http://localhost:8090')
    proxy=subprocess.Popen([str(ROOT/'node_modules/.bin/decap-server')],cwd=REPO,env=env)
    try:
        threading.Thread(target=watch,daemon=True).start()
        print('CMS trial: http://localhost:8090/admin/ — published preview: http://localhost:8090/',flush=True)
        ThreadingHTTPServer(('127.0.0.1',8090),Handler).serve_forever()
    finally:proxy.terminate();proxy.wait()
