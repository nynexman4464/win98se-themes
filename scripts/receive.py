"""Serve guest executables and receive native Windows 98 screenshots."""
from pathlib import Path
from http.server import HTTPServer, SimpleHTTPRequestHandler
from functools import partial
from io import BytesIO
import argparse, hashlib, json, re
from PIL import Image
from capture_common import ROOT, BUILD, HOST, PREVIEW_PORT, SHOWCASE_PORT, SCHEME_ORDER

class CaptureHandler(SimpleHTTPRequestHandler):
    def __init__(self, *args, mode, repo=ROOT, build=BUILD, raw=None, crop=(91,126,446,319), **kwargs):
        self.mode, self.repo, self.raw, self.crop = mode, repo, raw or build/('raw-'+mode), crop
        super().__init__(*args, directory=str(build), **kwargs)

    def do_POST(self):
        pattern = (r'/upload/([a-z0-9-]+)\.bmp' if self.mode == 'preview' else
                   r'/showcase/([a-z0-9-]+)--(controls|menu|tooltip|message|desktop)\.bmp')
        match = re.fullmatch(pattern, self.path)
        if not match or match[1] not in SCHEME_ORDER:
            self.send_error(404, 'Unknown scheme or view'); return
        if self.headers.get('Content-Length') != '1440054':
            self.send_error(400, 'Expected 800x600, 24-bit BMP'); return
        body = self.rfile.read(1440054)
        try:
            image = Image.open(BytesIO(body)); image.load()
            if image.format != 'BMP' or image.size != (800,600): raise ValueError()
        except Exception:
            self.send_error(400, 'Invalid bitmap'); return
        slug = match[1]; self.raw.mkdir(parents=True, exist_ok=True)
        logpath = self.raw/'capture-log.json'
        log = json.loads(logpath.read_text(encoding='utf-8')) if logpath.exists() else {
            'mode': self.mode, 'guestResolution': [800,600],
            'expectedCaptures': 34 if self.mode == 'preview' else 170, 'captures': {}}
        entry = {'bmpSha256': hashlib.sha256(body).hexdigest()}
        if self.mode == 'preview':
            image.save(self.raw/(slug+'.png'))
            (self.repo/'previews').mkdir(exist_ok=True)
            image.crop(self.crop).save(self.repo/'previews'/(slug+'.png'))
            log['previewCrop'] = list(self.crop); key = slug
        else:
            view = match[2]; folder = self.raw/slug; folder.mkdir(exist_ok=True)
            image.save(folder/(view+'.png'))
            scheme = json.loads((self.repo/'themes'/(slug+'.json')).read_text(encoding='utf-8'))
            expected = scheme['colors']['Background']['rgb']
            observed = list(image.convert('RGB').getpixel((799,599)))
            entry.update(expectedBackgroundRgb=expected, observedBackgroundRgb=observed,
                         backgroundWithinDisplayQuantization=max(abs(a-b) for a,b in zip(expected,observed)) <= 8)
            key = slug+'/'+view
        log['captures'][key] = entry
        logpath.write_text(json.dumps(log,indent=2)+'\n',encoding='utf-8')
        print(f'Saved {key} ({len(log["captures"])}/{log["expectedCaptures"]})',flush=True)
        result = b'Saved\r\n'; self.send_response(200)
        self.send_header('Content-Length',str(len(result))); self.end_headers(); self.wfile.write(result)

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode',required=True,choices=['preview','showcase'])
    parser.add_argument('--bind',default='127.0.0.1')
    parser.add_argument('--port',type=int)
    parser.add_argument('--raw',type=Path)
    parser.add_argument('--crop',type=int,nargs=4,default=(91,126,446,319))
    args = parser.parse_args(); l,t,r,b = args.crop
    if not (0 <= l < r <= 800 and 0 <= t < b <= 600): parser.error('--crop must fit the 800x600 guest')
    port = args.port or (PREVIEW_PORT if args.mode == 'preview' else SHOWCASE_PORT)
    BUILD.mkdir(parents=True,exist_ok=True)
    handler = partial(CaptureHandler,mode=args.mode,raw=args.raw.resolve() if args.raw else None,crop=tuple(args.crop))
    print(f'{args.mode} receiver: http://{HOST}:{port}/',flush=True)
    HTTPServer((args.bind,port),handler).serve_forever()

if __name__ == '__main__': main()
