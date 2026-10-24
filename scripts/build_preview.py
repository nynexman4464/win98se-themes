"""Build the native Windows 98 Appearance-preview capture helper (no C compiler needed)."""
from pathlib import Path
import struct,json,re
base=0x400000;code_rva=0x1000;data_rva=0x5000
D=bytearray();names={}
def datum(n,v):names[n]=base+data_rva+len(D);D.extend(v);return names[n]
def string(n,s):return datum(n,s.encode('ascii')+b'\0')
from capture_common import BUILD, HOST, PREVIEW_PORT, OUTPUT_PREVIEW, load_schemes
BUILD.mkdir(parents=True,exist_ok=True)
schemes=load_schemes()
items=[]
for i,s in enumerate(schemes):
 slug=re.sub('[^a-z0-9]+','-',s['name'].lower()).strip('-');items.append((s['name'],slug))
 string('name'+str(i),s['name']);string('file'+str(i),'C:\\THEMECAP\\'+slug+'.bmp');string('url'+str(i),'/upload/'+slug+'.bmp')
for n,s in [('title','Display Properties'),('folder','C:\\THEMECAP'),('host',HOST),('agent','Win98ThemeCapture'),('verb','POST'),('version','HTTP/1.0'),('headers','Content-Type: application/octet-stream\r\n'),('caption','Windows 98 theme capture'),('message','Captured all 34 schemes to C:\\THEMECAP and uploaded them to the host. No scheme was applied.'),('localmessage','Captured all 34 schemes to C:\\THEMECAP. Some uploads failed; keep these BMP files and check the host server.'),('error','Capture stopped. Open Display Properties / Appearance at 800x600 and start the host capture server on port 8001. Captures already saved remain in C:\\THEMECAP.')]:string(n,s)
for n in ['found','top','buf','index','original','screen','memdc','bitmap','oldobj','pixels','file','written','internet','connection','request','failed']:
 datum(n,bytes(64 if n=='buf' else 4))
header=struct.pack('<2sIHHI',b'BM',1440054,0,0,54)+struct.pack('<IiiHHIIiiII',40,800,600,1,24,0,1440000,0,0,0,0)
datum('bmpheader',header)
while len(D)%4:D.append(0)
datum('table',b''.join(struct.pack('<III',names['name'+str(i)],names['file'+str(i)],names['url'+str(i)]) for i in range(34)))
imports={'KERNEL32.dll':['Sleep','ExitProcess','VirtualAlloc','CreateDirectoryA','CreateFileA','WriteFile','CloseHandle'],'USER32.dll':['FindWindowA','EnumChildWindows','GetClassNameA','SendMessageA','GetParent','GetDlgCtrlID','MessageBoxA','GetDC','ReleaseDC','SetForegroundWindow','GetSystemMetrics'],'GDI32.dll':['CreateCompatibleDC','CreateCompatibleBitmap','SelectObject','BitBlt','GetDIBits','DeleteObject','DeleteDC'],'WININET.dll':['InternetOpenA','InternetConnectA','HttpOpenRequestA','HttpSendRequestA','HttpQueryInfoA','InternetCloseHandle']}
imp_offset=len(D);D.extend(bytes(20*(len(imports)+1)));iat={}
for idx,(dll,funcs) in enumerate(imports.items()):
 dll_rva=string('dll'+str(idx),dll)-base
 if len(D)%2:D.append(0)
 hints=[]
 for f in funcs:
  hints.append(data_rva+len(D));D.extend(b'\0\0'+f.encode()+b'\0')
  if len(D)%2:D.append(0)
 while len(D)%4:D.append(0)
 ilt=data_rva+len(D);D.extend(struct.pack('<'+'I'*(len(hints)+1),*hints,0));irva=data_rva+len(D)
 for f,h in zip(funcs,hints):iat[f]=base+data_rva+len(D);D.extend(struct.pack('<I',h))
 D.extend(bytes(4));struct.pack_into('<IIIII',D,imp_offset+idx*20,ilt,0,0,dll_rva,irva)
C=bytearray();labels={};fixes=[]
def emit(h):C.extend(bytes.fromhex(h))
def dw(x):C.extend(struct.pack('<I',x&0xffffffff))
def push(x):emit('68');dw(x)
def call(n):emit('ff15');dw(iat[n])
def label(n):labels[n]=len(C)
def jump(op,n):emit(op);fixes.append((len(C),n,False));dw(0)
def proc(n):jump('e8',n)
def load(n):emit('a1');dw(names[n])
def store(n):emit('a3');dw(names[n])
def addr(n):push(names[n])
def pv(n):load(n);emit('50')
def check():emit('85c0');jump('0f84','error')
def table(offset):load('index');emit('6bc00c 8b80');dw(names['table']+offset)
label('entry');addr('title');push(0);call('FindWindowA');store('top');check()
for metric,expected in [(0,800),(1,600)]:
 push(metric);call('GetSystemMetrics');emit('3d');dw(expected);jump('0f85','error')
push(0);emit('68');fixes.append((len(C),'callback',True));dw(0);pv('top');call('EnumChildWindows');load('found');check()
push(0);push(0);push(0x147);pv('found');call('SendMessageA');store('original')
push(0);addr('folder');call('CreateDirectoryA')
push(4);push(0x3000);push(1440054);push(0);call('VirtualAlloc');store('pixels');check()
# Copy BITMAPFILEHEADER + BITMAPINFOHEADER into allocation.
emit('56 57');load('pixels');emit('89c7 be');dw(names['bmpheader']);emit('b936000000 f3a4 5f 5e')
push(0);call('GetDC');store('screen');check();pv('screen');call('CreateCompatibleDC');store('memdc');check()
push(600);push(800);pv('screen');call('CreateCompatibleBitmap');store('bitmap');check();pv('bitmap');pv('memdc');call('SelectObject');store('oldobj')
push(0);push(0);push(0);push(1);addr('agent');call('InternetOpenA');store('internet')
push(0);push(0);push(3);push(0);push(0);push(PREVIEW_PORT);addr('host');pv('internet');call('InternetConnectA');store('connection')
label('loop');addr('title');push(0);call('FindWindowA');check()
# Exact scheme-name selection independent of alphabetical ordering.
table(0);emit('50');push(-1);push(0x158);pv('found');call('SendMessageA');emit('83f8ff');jump('0f84','error');emit('50');proc('select')
pv('top');call('SetForegroundWindow');push(1200);call('Sleep')
push(0xcc0020);push(0);push(0);pv('screen');push(600);push(800);push(0);push(0);pv('memdc');call('BitBlt');check()
pv('oldobj');pv('memdc');call('SelectObject')
push(0);load('pixels');emit('83c00e 50');load('pixels');emit('83c036 50');push(600);push(0);pv('bitmap');pv('screen');call('GetDIBits');emit('3d58020000');jump('0f85','error')
pv('bitmap');pv('memdc');call('SelectObject')
push(0);push(0x80);push(2);push(0);push(0);push(0x40000000);table(4);emit('50');call('CreateFileA');store('file');emit('83f8ff');jump('0f84','error')
push(0);addr('written');push(1440054);pv('pixels');pv('file');call('WriteFile');check();pv('file');call('CloseHandle');load('written');emit('3d');dw(1440054);jump('0f85','error')
# Upload the same BMP to the host capture server. Always retain the local copy.
push(0);push(0);push(0);push(0);addr('version');table(8);emit('50');addr('verb');pv('connection');call('HttpOpenRequestA');store('request');emit('85c0');jump('0f84','uploadfail')
push(1440054);pv('pixels');push(-1);addr('headers');pv('request');call('HttpSendRequestA');emit('85c0');jump('0f84','uploadclosefail')
# Require HTTP status 200 (numeric status query).
emit('c705');dw(names['written']);dw(4)
push(0);addr('written');addr('buf');push(0x20000013);pv('request');call('HttpQueryInfoA');emit('85c0');jump('0f84','uploadclosefail');emit('813d');dw(names['buf']);dw(200);jump('0f85','uploadclosefail')
pv('request');call('InternetCloseHandle');jump('e9','advance')
label('uploadclosefail');pv('request');call('InternetCloseHandle')
label('uploadfail');emit('ff05');dw(names['failed'])
label('advance');emit('ff05');dw(names['index']);load('index');emit('83f822');jump('0f8c','loop')
pv('original');proc('select');pv('oldobj');pv('memdc');call('SelectObject');pv('bitmap');call('DeleteObject');pv('memdc');call('DeleteDC');pv('screen');push(0);call('ReleaseDC');pv('connection');call('InternetCloseHandle');pv('internet');call('InternetCloseHandle')
load('failed');emit('85c0');jump('0f85','localdone');push(0);addr('caption');addr('message');push(0);call('MessageBoxA');jump('e9','exit')
label('localdone');push(0x30);addr('caption');addr('localmessage');push(0);call('MessageBoxA');jump('e9','exit')
label('error');push(0x30);addr('caption');addr('error');push(0);call('MessageBoxA')
label('exit');push(0);call('ExitProcess')
label('callback');emit('55 8bec');push(64);addr('buf');emit('ff7508');call('GetClassNameA')
for off,val in [(0,int.from_bytes(b'Comb','little')),(4,int.from_bytes(b'oBox','little'))]:
 emit('813d');dw(names['buf']+off);dw(val);jump('0f85','next')
emit('803d');dw(names['buf']+8);emit('00');jump('0f85','next');push(0);push(0);push(0x146);emit('ff7508');call('SendMessageA');emit('83f81e');jump('0f8c','next');emit('8b4508');store('found');emit('33c0 c9 c20800')
label('next');emit('b801000000 c9 c20800')
label('select');emit('55 8bec 53 56');push(0);emit('ff7508');push(0x14e);pv('found');call('SendMessageA');pv('found');call('GetDlgCtrlID');emit('0d00000100 89c3');pv('found');call('GetParent');emit('89c6');pv('found');emit('53');push(0x111);emit('56');call('SendMessageA');emit('5e 5b c9 c20400')
for p,n,absolute in fixes:struct.pack_into('<I',C,p,(base+code_rva+labels[n] if absolute else labels[n]-p-4)&0xffffffff)
def align(n,a):return (n+a-1)//a*a
rc=align(len(C),512);rd=align(len(D),512);dos=bytearray(128);dos[:2]=b'MZ';struct.pack_into('<I',dos,60,128);coff=struct.pack('<HHIIIHH',0x14c,2,0,0,0,224,0x0103)
o=bytearray(224);struct.pack_into('<H',o,0,0x10b);struct.pack_into('<III',o,4,rc,rd,0);struct.pack_into('<III',o,16,code_rva,code_rva,data_rva);struct.pack_into('<III',o,28,base,4096,512);struct.pack_into('<HHHHHH',o,40,4,0,0,0,4,0);struct.pack_into('<III',o,56,align(data_rva+len(D),4096),512,0);struct.pack_into('<HH',o,68,2,0);struct.pack_into('<IIIIII',o,72,0x100000,4096,0x100000,4096,0,16);struct.pack_into('<II',o,104,data_rva+imp_offset,20*(len(imports)+1))
def section(n,v,r,l,p,f):return struct.pack('<8sIIIIIIHHI',n.encode().ljust(8,b'\0'),v,r,l,p,0,0,0,0,f)
h=dos+b'PE\0\0'+coff+o+section('.text',len(C),code_rva,rc,512,0x60000020)+section('.data',len(D),data_rva,rd,512+rc,0xc0000040)
assert len(h)<=512 and len(C)<data_rva-code_rva
OUTPUT_PREVIEW.write_bytes(h.ljust(512,b'\0')+C.ljust(rc,b'\0')+D.ljust(rd,b'\0'))
print('Built capture-preview.exe:',len(C),'code bytes;',len(D),'data bytes;',len(items),'exact scheme names. Native API implementation used for the verified Appearance capture run.')
