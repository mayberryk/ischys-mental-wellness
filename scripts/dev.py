"""Build, serve, and rebuild static preview content. Bound to localhost only."""
from pathlib import Path
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import urlsplit
import functools,subprocess,sys,threading,time,os
ROOT=Path(__file__).resolve().parents[1];OUT=ROOT/'dist'
def build():return subprocess.run([sys.executable,str(ROOT/'scripts/build.py')],cwd=ROOT).returncode
if build():raise SystemExit(1)
class Handler(SimpleHTTPRequestHandler):
 def __init__(self,*a,**kw):super().__init__(*a,directory=str(OUT),**kw)
 def end_headers(self):
  self.send_header('Referrer-Policy','no-referrer');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Cache-Control','no-store');super().end_headers()
 def do_GET(self):
  path=urlsplit(self.path).path
  redirects={}
  for line in (OUT/'_redirects').read_text().splitlines():
   old,new,status=line.split();redirects[old]=(new,int(status))
  if path in redirects:
   dest,status=redirects[path];self.send_response(status);self.send_header('Location',dest);self.end_headers();return
  super().do_GET()
 def list_directory(self,path):self.send_error(404);return None
 def send_error(self,code,message=None,explain=None):
  if code==404 and (OUT/'404.html').exists():
   data=(OUT/'404.html').read_bytes();self.send_response(404);self.send_header('Content-Type','text/html; charset=utf-8');self.send_header('Content-Length',str(len(data)));self.end_headers()
   if self.command!='HEAD':self.wfile.write(data)
  else:super().send_error(code,message,explain)
def fingerprint():
 files=[p for folder in ('content','templates','static','scripts','output/pdf') for p in (ROOT/folder).rglob('*') if p.is_file() and '__pycache__' not in str(p)]
 return tuple((str(p),p.stat().st_mtime_ns) for p in sorted(files))
def watch():
 prev=fingerprint()
 while True:
  time.sleep(1);current=fingerprint()
  if current!=prev:build();prev=current
threading.Thread(target=watch,daemon=True).start()
port=int(os.environ.get('PORT','8080'))
print(f'Ischys preview: http://localhost:{port} (watching content and templates)',flush=True)
ThreadingHTTPServer(('127.0.0.1',port),Handler).serve_forever()
