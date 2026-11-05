"""Run: python3 server.py. Local-only development server, not production hosting."""
import argparse, json, sqlite3, uuid
from datetime import datetime, timezone
from http.server import ThreadingHTTPServer, BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from engine import Navigator

ROOT=Path(__file__).parent
NAV=Navigator()
DB=ROOT/'data/feedback.sqlite3'

def save_feedback(payload):
    if payload.get('kind') not in {'helpful','incorrect','accessibility','outdated'}: raise ValueError('Choose a feedback type')
    source=payload.get('source_id','')
    if source and source not in {r['id'] for r in NAV.records}: raise ValueError('Unknown source')
    note=payload.get('note','')
    if not isinstance(note,str) or len(note)>1000: raise ValueError('Note must be at most 1000 characters')
    identifier=uuid.uuid4().hex
    with sqlite3.connect(DB) as conn:
        conn.execute('CREATE TABLE IF NOT EXISTS feedback (id TEXT, created TEXT, kind TEXT, source_id TEXT, note TEXT)')
        conn.execute('INSERT INTO feedback VALUES (?,?,?,?,?)',(identifier,datetime.now(timezone.utc).isoformat(),payload['kind'],source,note))
    return identifier

class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass # Do not log questions or notes.
    def send(self,status,body,kind='application/json; charset=utf-8'):
        raw=json.dumps(body,ensure_ascii=False).encode() if not isinstance(body,bytes) else body
        self.send_response(status)
        for k,v in {'Content-Type':kind,'Content-Length':str(len(raw)),'Cache-Control':'no-store','X-Content-Type-Options':'nosniff','Referrer-Policy':'no-referrer','Content-Security-Policy':"default-src 'self'; script-src 'self'; style-src 'self'; connect-src 'self'; object-src 'none'; base-uri 'none'; frame-ancestors 'none'"}.items():self.send_header(k,v)
        self.end_headers();self.wfile.write(raw)
    def do_GET(self):
        path=urlparse(self.path).path
        if path=='/api/resources':return self.send(200,NAV.records)
        files={'/':('index.html','text/html; charset=utf-8'),'/app.js':('app.js','text/javascript; charset=utf-8'),'/style.css':('style.css','text/css; charset=utf-8'),'/bear.png':('bear.png','image/png')}
        if path not in files:return self.send(404,{'error':'Not found'})
        name,kind=files[path];self.send(200,(ROOT/'static'/name).read_bytes(),kind)
    def do_POST(self):
        if self.path not in {'/api/ask','/api/feedback'}:return self.send(404,{'error':'Not found'})
        # Block browser cross-origin writes, including form submissions.
        origin=self.headers.get('Origin')
        if origin and origin != 'http://'+self.headers.get('Host',''):return self.send(403,{'error':'Origin rejected'})
        if self.headers.get('Content-Type','').split(';')[0]!='application/json':return self.send(415,{'error':'JSON required'})
        try:
            size=int(self.headers.get('Content-Length','0'))
            if size<1 or size>8192:raise ValueError('Request size invalid')
            body=json.loads(self.rfile.read(size))
            if not isinstance(body,dict):raise ValueError('JSON object required')
            if self.path=='/api/ask':
                q=body.get('question')
                if not isinstance(q,str) or not 2<=len(q.strip())<=500:raise ValueError('Enter 2–500 characters')
                return self.send(200,NAV.answer(q.strip(), body.get('language', 'en')))
            return self.send(201,{'id':save_feedback(body),'message':'Saved on this computer for project review.'})
        except (ValueError,TypeError,json.JSONDecodeError) as exc:self.send(400,{'error':str(exc)})
        except Exception:self.send(500,{'error':'Something went wrong. Try browsing the resources.'})

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('--port',type=int,default=8000);args=parser.parse_args()
    print(f'Accessible AI Navigator: http://127.0.0.1:{args.port}',flush=True)
    ThreadingHTTPServer(('127.0.0.1',args.port),Handler).serve_forever()
