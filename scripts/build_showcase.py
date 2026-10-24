"""Build the latest native five-view Win98 showcase and its recovery helper."""
from pathlib import Path
import struct,json,re
TEST = "--test" in __import__("sys").argv
LIMIT=2 if TEST else 34
old=Path(__file__).with_name('build_preview.py').read_text()
from capture_common import SHOWCASE_PORT
exec(old[:old.index('imp_offset=len(D)')])
# Extend the working Win98 PE builder, with independently saved live settings.
for n,v in [('mainclass','ThemeShowcaseWindow'),('inactive','Inactive window'),('tooltitle','Small tool window'),('static','STATIC'),('button','BUTTON'),('edit','EDIT'),('list','LISTBOX'),('tooltipclass','tooltips_class32'),('tiptext','Native tooltip: InfoWindow background and InfoText'),('menutitle','&Sample'),('menuopen','&Open\tCtrl+O'),('menuselected','&Selected item'),('menudisabled','&Disabled item'),('menuchecked','&Checked item'),('msgtitle','Message box sample'),('msgtext','This native message box uses the scheme message font and system colors.'),('done',('Test complete: captured Brick and Maple in five views each. Starting appearance restored.' if TEST else 'Captured 34 schemes in five views. Starting appearance restored. Files: C:\\THEMECAP. Uploads sent to host port 8003.')),('partial','Capture finished and starting appearance restored. Some uploads failed. Keep the BMP files in C:\\THEMECAP.'),('fail','Capture stopped; restoration was attempted. If needed, run restore-appearance.exe. Backup: C:\\THEMECAP\\SHOWTEST.BIN (test) or SHOWFULL.BIN (full).'),('backupfile',('C:\\THEMECAP\\SHOWTEST.BIN' if TEST else 'C:\\THEMECAP\\SHOWFULL.BIN')),('restoreok','Starting appearance restored from SHOWCASE.BIN.'),('appcaption','Windows 98 showcase')]:string(n,v)
for n in ['changed','view','hinstance','main','inactivehwnd','tool','ctrl','hfont','msgfont','statusfont','iconfont','menufont','smallfont','menu','popup','tip','thread','threadid','deadline','colorindex','currentncm','restoremode','restorefailed','closeattempts','background','backgroundctrl','dialogcaptured','timerid','stop']:
 datum(n,bytes(4))
datum('backup',struct.pack('<I',340)+bytes(512));datum('indices',struct.pack('<29I',*range(29)));datum('colorswork',bytes(116));datum('wc',bytes(40));datum('msgstruct',bytes(28));datum('toolinfo',bytes(40));datum('ncmwork',bytes(340))
font_offsets={'hfont':28,'smallfont':96,'menufont':164,'statusfont':224,'msgfont':284,'iconfont':344}
records=[];captures=[]
for i,(s,(name,slug)) in enumerate(zip(schemes,items)):
 b=bytes.fromhex(s['rawHex']);rawptr=datum('raw'+str(i),b);ncmptr=datum('ncm'+str(i),struct.pack('<I',340)+b[8:344]);rgbptr=datum('rgb'+str(i),b''.join(b[o:o+3]+b'\0' for o in range(404,520,4)))
 records.append((names['name'+str(i)],rawptr,ncmptr,rgbptr))
 for view in ['controls','menu','tooltip','message','desktop']:
  fp=string('out-'+slug+'-'+view,'C:\\THEMECAP\\'+slug+'--'+view+'.bmp');up=string('uri-'+slug+'-'+view,'/showcase/'+slug+'--'+view+'.bmp');captures.append((fp,up))
string('backgroundclass','ThemeShowcaseBackground')
string('desktoplabel','Sample application')
datum('desktoptext',struct.pack('<34I',*[0 if sum(c*w for c,w in zip(s['colors']['Background']['rgb'],[299,587,114]))>128000 else 0xffffff for s in schemes]))
datum('backgroundwc',bytes(40))
datum('showtable',b''.join(struct.pack('<IIII',*r) for r in records));datum('capturetable',b''.join(struct.pack('<II',*r) for r in captures))
controls=[('static','Text field and selection',16,12,280,28,0, 'msgfont','label'),('edit','Selected text sample',16,46,310,42,0x00800180,'msgfont','selection'),('button','Enabled',16,104,145,42,0,'msgfont','enabled'),('button','Disabled',173,104,145,42,0x08000000,'msgfont','disabled'),('button','Checked option',16,160,300,38,3,'msgfont','check'),('button','Radio option',16,204,300,38,9,'msgfont','radio'),('list','',350,12,350,165,0x00a00101,'msgfont','listbox'),('static','Status font sample',350,195,350,38,0,'statusfont','status'),('static','Icon label font sample',350,243,350,38,0,'iconfont','iconlabel'),('button','Default button',16,264,302,44,1,'msgfont','default')]
controls += [('static','',350,290,32,32,3,'iconfont','nativeicon'),('static','Desktop label sample',392,290,310,38,0,'iconfont','desktoplabel')]
for j,c in enumerate(controls):string('ctext'+str(j),c[1])
for j,t in enumerate(['Window text','Selected list item','Another item','Scroll to see more','Last item']):string('listtext'+str(j),t)
imports['KERNEL32.dll']+=['GetModuleHandleA','GetTickCount','CreateThread','WaitForSingleObject','ReadFile','GetCommandLineA','lstrlenA']
imports['USER32.dll']+=['SystemParametersInfoA','GetSysColor','SetSysColors','RegisterClassA','CreateWindowExA','DefWindowProcA','DestroyWindow','PeekMessageA','TranslateMessage','DispatchMessageA','CreateMenu','CreatePopupMenu','AppendMenuA','SetMenu','DrawMenuBar','TrackPopupMenu','PostMessageA','ShowWindow','UpdateWindow','SetWindowTextA','SetWindowPos','GetDesktopWindow','InvalidateRect','LoadIconA','DrawIcon','GetDlgItem']
for n,t in [('stageinit','Initializing showcase'),('stageworker','Starting menu/message capture thread'),('stagegdi','Preparing screenshot graphics'),('stageblit','Capturing display pixels'),('stagedib','Reading bitmap pixels'),('stagefile','Saving screenshot file'),('stagetip','Creating native tooltip')]:string(n,t)
datum('stage',struct.pack('<I',names['stageinit']))
string('dialogclass','#32770')
imports['KERNEL32.dll']+=['lstrcmpA','GetLastError']
imports['USER32.dll']+=['wsprintfA']
string('errorformat','Capture stopped. Stage: %s. Win32 error: %lu. Restoration was attempted; the recovery file is preserved.')
datum('errorcode',bytes(4));datum('errortext',bytes(512))
for n,t in [('stagegetncm','Reading starting window metrics'),('stagegeticon','Reading starting icon font'),('stagebackup','Saving recovery file'),('stagealloc','Allocating image buffer'),('stagemainclass','Registering sample window class'),('stagebgclass','Registering desktop window class'),('stagesetncm','Applying window metrics'),('stageseticon','Applying icon font'),('stagesetcolors','Applying colors'),('stagefont','Creating sample fonts'),('stagebgwindow','Creating desktop sample'),('stagewindows','Creating sample windows'),('stagecontrols','Creating sample controls')]:string(n,t)
imports['USER32.dll']+=['keybd_event','GetLastActivePopup','EndDialog','SetTimer','KillTimer','GetTopWindow','GetWindow','GetSysColorBrush']
imports['GDI32.dll']+=['CreateFontIndirectA','SetBkColor','SetTextColor']
imports['COMCTL32.dll']=['InitCommonControls']
imp_offset=len(D);D.extend(bytes(20*(len(imports)+1)));iat={}
for idx,(dll,funcs) in enumerate(imports.items()):
 funcs=list(dict.fromkeys(funcs));dll_rva=string('dllx'+str(idx),dll)-base
 if len(D)%2:D.append(0)
 hints=[]
 for f in funcs:
  hints.append(data_rva+len(D));D.extend(b'\0\0'+f.encode()+b'\0')
  if len(D)%2:D.append(0)
 while len(D)%4:D.append(0)
 ilt=data_rva+len(D);D.extend(struct.pack('<'+'I'*(len(hints)+1),*hints,0));irva=data_rva+len(D)
 for f,h in zip(funcs,hints):iat[f]=base+data_rva+len(D);D.extend(struct.pack('<I',h))
 D.extend(bytes(4));struct.pack_into('<IIIII',D,imp_offset+idx*20,ilt,0,0,dll_rva,irva)
# Reuse the small assembler helpers.
exec(old[old.index('C=bytearray()'):old.index("label('entry')")])
def movimm(n,x):emit('c705');dw(names[n]);dw(x)
def absolute(labelname):emit('68');fixes.append((len(C),labelname,True));dw(0)
def sfield(off):load('index');emit('c1e004 8b80');dw(names['showtable']+off)
def outfile(off):load('index');emit('6bc005 0305');dw(names['view']);emit('c1e003 8b80');dw(names['capturetable']+off)
def stage(n):movimm('stage',names[n])
def pump(ms):push(ms);proc('pump')
def spi(action,size,ptr,flags=0):push(flags);push(ptr);push(size);push(action);call('SystemParametersInfoA')
def create(cls,text,x,y,w,h,style,parent=None,ex=0,menu=0):
 push(0);pv('hinstance');push(menu);pv(parent) if parent else push(0)
 for v in [h,w,y,x,style]:push(v)
 addr(text);addr(cls);push(ex);call('CreateWindowExA')
def writefile(filename,ptr,size):
 push(0);push(0x80);push(2);push(0);push(0);push(0x40000000);push(filename);call('CreateFileA');store('file');emit('83f8ff');jump('0f84','error');push(0);addr('written');push(size);push(ptr);pv('file');call('WriteFile');check();pv('file');call('CloseHandle');load('written');emit('3d');dw(size);jump('0f85','error')
label('entry');call('GetCommandLineA');emit('89c3');label('argscan');emit('803b00');jump('0f84','start');emit('803b2f');jump('0f84','restoreentry');emit('43');jump('e9','argscan')
label('start')
for metric,expected in [(0,800),(1,600)]:push(metric);call('GetSystemMetrics');emit('3d');dw(expected);jump('0f85','error')
push(0);call('GetModuleHandleA');store('hinstance');call('InitCommonControls')
# Snapshot live nonclient metrics, icon font, and all 29 colors before changing anything.
stage('stagegetncm');spi(0x29,340,names['backup']);check();stage('stagegeticon');spi(0x1f,60,names['backup']+340);check()
movimm('colorindex',0);label('getcolors');pv('colorindex');call('GetSysColor');emit('8b0d');dw(names['colorindex']);emit('89048d');dw(names['backup']+400);emit('ff05');dw(names['colorindex']);load('colorindex');emit('83f81d');jump('0f8c','getcolors')
push(0);addr('folder');call('CreateDirectoryA');stage('stagebackup');writefile(names['backupfile'],names['backup'],516)
stage('stagealloc');push(4);push(0x3000);push(1440054);push(0);call('VirtualAlloc');store('pixels');check();emit('56 57 fc');load('pixels');emit('89c7 be');dw(names['bmpheader']);emit('b936000000 f3a4 5f 5e')
push(0);call('GetDC');store('screen');check();pv('screen');call('CreateCompatibleDC');store('memdc');check();push(600);push(800);pv('screen');call('CreateCompatibleBitmap');store('bitmap');check();pv('bitmap');pv('memdc');call('SelectObject');store('oldobj')
push(0);push(0);push(0);push(1);addr('agent');call('InternetOpenA');store('internet');push(0);push(0);push(3);push(0);push(0);push(SHOWCASE_PORT);addr('host');pv('internet');call('InternetConnectA');store('connection')
# Register a genuine native window class using DefWindowProcA.
absolute('mainproc');emit('58 a3');dw(names['wc']+4);load('hinstance');emit('a3');dw(names['wc']+16);movimm('wc_dummy',0) if False else None
for off,val in [(28,16),(36,names['mainclass'])]:emit('c705');dw(names['wc']+off);dw(val)
stage('stagemainclass');addr('wc');call('RegisterClassA');check()
# Register both callbacks before creating sample windows.
absolute('backgroundproc');emit('58 a3');dw(names['backgroundwc']+4);load('hinstance');emit('a3');dw(names['backgroundwc']+16)
for off,val in [(28,2),(36,names['backgroundclass'])]:emit('c705');dw(names['backgroundwc']+off);dw(val)
stage('stagebgclass');addr('backgroundwc');call('RegisterClassA');check()
label('loop');stage('stagesetncm');movimm('changed',1);sfield(8);store('currentncm');push(0);pv('currentncm');push(340);push(0x2a);call('SystemParametersInfoA');check();sfield(4);emit('0558010000');emit('50');call('CreateFontIndirectA');store('iconfont')
stage('stageseticon');sfield(4);emit('0558010000');store('buf');push(0);pv('buf');push(60);push(0x22);call('SystemParametersInfoA');check();stage('stagesetcolors');sfield(12);emit('50');addr('indices');push(29);call('SetSysColors');check()
# Create scheme font objects. Font samples use their actual LOGFONTA records.
stage('stagefont')
for var,off in font_offsets.items():
 if var=='iconfont':continue
 sfield(4);emit('05');dw(off);emit('50');call('CreateFontIndirectA');store(var);check()
stage('stagebgwindow');create('backgroundclass','desktoplabel',0,0,800,600,0x90000000);store('background');check()
create('static','ctext10',48,42,32,32,0x50000003,'background');store('backgroundctrl');push(32512);push(0);call('LoadIconA');push(0);emit('50');push(0x170);pv('backgroundctrl');call('SendMessageA')
create('static','desktoplabel',8,86,152,90,0x50000001,'background');store('backgroundctrl');push(1);pv('iconfont');push(0x30);pv('backgroundctrl');call('SendMessageA')
stage('stagewindows');create('mainclass','inactive',20,15,480,190,0x10cf0000);store('inactivehwnd');check()
create('mainclass','tooltitle',530,15,250,100,0x10c80000,ex=0x80);store('tool');check()
create('mainclass','appcaption',8,115,784,450,0x10cf0000);store('main');check();sfield(0);emit('50');pv('main');call('SetWindowTextA')
stage('stagecontrols')
for j,c in enumerate(controls):
 cls,txt,x,y,w,h,style,fontvar,role=c
 create(cls,'ctext'+str(j),x,y,w,h,style|0x50000000,'main',ex=0x200 if cls in ['edit','list'] else 0,menu=100+j);store('ctrl');check()
 push(1);pv(fontvar);push(0x30);pv('ctrl');call('SendMessageA')
 if role=='nativeicon':
  push(32512);push(0);call('LoadIconA');push(0);emit('50');push(0x170);pv('ctrl');call('SendMessageA')
 if role=='selection':push(-1);push(0);push(0xb1);pv('ctrl');call('SendMessageA')
 if role in ['check','radio']:push(0);push(1);push(0xf1);pv('ctrl');call('SendMessageA')
 if role=='listbox':
  for k in range(5):addr('listtext'+str(k));push(0);push(0x180);pv('ctrl');call('SendMessageA')
  push(0);push(1);push(0x186);pv('ctrl');call('SendMessageA')
# Real menu bar and popup menu with native selected/disabled/checked rendering.
call('CreateMenu');store('menu');call('CreatePopupMenu');store('popup')
for key,flags,ident in [('menuopen',0,501),('menuselected',0,502),('menudisabled',1,503),('menuchecked',8,504)]:addr(key);push(ident);push(flags);pv('popup');call('AppendMenuA')
addr('menutitle');pv('popup');push(0x10);pv('menu');call('AppendMenuA');pv('menu');pv('main');call('SetMenu');pv('main');call('DrawMenuBar');pv('main');call('SetForegroundWindow');pump(700)
movimm('view',0);proc('capture')
# Capture while TrackPopupMenu runs its normal modal message loop.
movimm('view',1);proc('workerstart');push(0);pv('main');push(0);push(185);push(60);push(0x100);pv('popup');call('TrackPopupMenu');proc('workerwait')
# Native tracking tooltip.
stage('stagetip');create('tooltipclass','tiptext',0,0,0,0,0x80000003,'main',ex=8);store('tip');check()
for off,val in [(0,40),(4,0xa0),(12,1),(36,names['tiptext'])]:emit('c705');dw(names['toolinfo']+off);dw(val)
load('main');emit('a3');dw(names['toolinfo']+8);addr('toolinfo');push(0);push(0x404);pv('tip');call('SendMessageA');push((375<<16)|190);push(0);push(0x412);pv('tip');call('SendMessageA');addr('toolinfo');push(1);push(0x411);pv('tip');call('SendMessageA');pump(500);movimm('view',2);proc('capture');pv('tip');call('DestroyWindow')
# Native message box and scheme-specific message font.
# End the modal on its owning UI thread, via a timer inside the dialog loop.
movimm('view',3);movimm('dialogcaptured',0);absolute('dialogtimer');push(200);push(0);push(0);call('SetTimer');store('timerid');check();proc('workerstart');push(0x10040);addr('msgtitle');addr('msgtext');pv('main');call('MessageBoxA');pv('timerid');push(0);call('KillTimer');proc('workerwait')
# Fifth view: the actual COLOR_BACKGROUND field and icon-title font, unobscured.
for var in ['main','tool','inactivehwnd']:push(0);pv(var);call('ShowWindow')
pv('background');call('SetForegroundWindow');pump(500);movimm('view',4);proc('capture')
for var in ['main','tool','inactivehwnd','background']:pv(var);call('DestroyWindow')
for var in font_offsets:pv(var);call('DeleteObject')
emit('ff05');dw(names['index']);load('index');emit('83f8'+f'{LIMIT:02x}');jump('0f8c','loop')
proc('restore');load('restorefailed');emit('85c0');jump('0f85','errorbox');load('failed');emit('85c0');jump('0f85','partialdone');push(0x50040);addr('appcaption');addr('done');push(0);call('MessageBoxA');jump('e9','exit')
label('partialdone');push(0x50030);addr('appcaption');addr('partial');push(0);call('MessageBoxA');jump('e9','exit')
label('error');call('GetLastError');store('errorcode');pv('errorcode');pv('stage');addr('errorformat');addr('errortext');call('wsprintfA');emit('83c410');load('changed');emit('85c0');jump('0f84','errorbox');proc('restore')
label('errorbox');push(0x50030);pv('stage');addr('errortext');push(0);call('MessageBoxA');jump('e9','exit')
label('restoreentry');push(0);push(0x80);push(3);push(0);push(1);push(0x80000000);addr('backupfile');call('CreateFileA');store('file');emit('83f8ff');jump('0f84','error');push(0);addr('written');push(516);addr('backup');pv('file');call('ReadFile');check();pv('file');call('CloseHandle');load('written');emit('3d04020000');jump('0f85','error');proc('restore');push(0x50040);addr('appcaption');addr('restoreok');push(0);call('MessageBoxA')
label('exit');push(0);call('ExitProcess')
label('restore');movimm('restorefailed',0)
for labelid,(action,size,ptr) in enumerate([(0x2a,340,names['backup']),(0x22,60,names['backup']+340)]):
 spi(action,size,ptr);emit('85c0');jump('0f85','restorenext'+str(labelid));emit('ff05');dw(names['restorefailed']);label('restorenext'+str(labelid))
push(names['backup']+400);addr('indices');push(29);call('SetSysColors');emit('85c0');jump('0f85','restoreend');emit('ff05');dw(names['restorefailed'])
label('restoreend');movimm('changed',0);emit('c3')
label('workerstart');stage('stageworker');addr('threadid');push(0);push(0);absolute('worker');push(0);push(0);call('CreateThread');store('thread');check();emit('c3')
label('workerwait');push(-1);pv('thread');call('WaitForSingleObject');pv('thread');call('CloseHandle');emit('c3')
label('worker');emit('53');push(650);call('Sleep');load('view');emit('83f801');jump('0f85','workercapture');push(0);push(0);push(0);push(0x28);call('keybd_event');push(0);push(2);push(0);push(0x28);call('keybd_event');push(200);call('Sleep');label('workercapture');proc('capture');load('view');emit('83f801');jump('0f85','closebox');push(0);push(0);push(0x1f);pv('main');call('PostMessageA');emit('5b 33c0 c20400')
# Capture worker only signals completion; it never ends the UI-thread modal.
label('closebox');movimm('dialogcaptured',1);emit('5b 33c0 c20400')
# TIMERPROC executes on the owning thread while MessageBox runs its modal loop.
label('dialogtimer');emit('55 8bec 53');load('dialogcaptured');emit('85c0');jump('0f84','timerdone');push(0);call('GetTopWindow');emit('89c3')
label('timerfind');emit('85db');jump('0f84','timerdone');push(4);emit('53');call('GetWindow');emit('3b05');dw(names['main']);jump('0f85','timernext');push(64);addr('buf');emit('53');call('GetClassNameA');addr('dialogclass');addr('buf');call('lstrcmpA');emit('85c0');jump('0f85','timernext');push(1);emit('53');call('EndDialog');emit('85c0');jump('0f84','timernext');movimm('dialogcaptured',0);jump('e9','timerdone')
label('timernext');push(2);emit('53');call('GetWindow');emit('89c3');jump('e9','timerfind')
label('timerdone');emit('5b c9 c21000')
# Background static controls use COLOR_BACKGROUND and a contrasting label color.
label('backgroundproc');emit('55 8bec 53');emit('817d0c38010000');jump('0f85','bgdefault');push(1);call('GetSysColor');emit('50 ff7510');call('SetBkColor');load('index');emit('8b0485');dw(names['desktoptext']);emit('50 ff7510');call('SetTextColor');push(1);call('GetSysColorBrush');emit('5b c9 c21000')
label('bgdefault');emit('ff7514 ff7510 ff750c ff7508');call('DefWindowProcA');emit('5b c9 c21000')
# The sample close button requests an orderly stop and restoration.
label('mainproc');emit('55 8bec');emit('837d0c10');jump('0f85','maindefault');movimm('stop',1);emit('33c0 c9 c21000')
label('maindefault');emit('ff7514 ff7510 ff750c ff7508');call('DefWindowProcA');emit('c9 c21000')
label('pump');emit('55 8bec 53');call('GetTickCount');emit('034508');store('deadline')
label('pumpnext');push(1);push(0);push(0);push(0);addr('msgstruct');call('PeekMessageA');emit('85c0');jump('0f84','pumptime');addr('msgstruct');call('TranslateMessage');addr('msgstruct');call('DispatchMessageA');jump('e9','pumpnext')
label('pumptime');load('stop');emit('85c0');jump('0f85','error');call('GetTickCount');emit('3b05');dw(names['deadline']);jump('0f83','pumpdone');push(10);call('Sleep');jump('e9','pumpnext')
label('pumpdone');emit('5b c9 c20400')
label('capture');load('stop');emit('85c0');jump('0f85','error');stage('stagegdi');push(0);call('GetDC');store('screen');check();pv('screen');call('CreateCompatibleDC');store('memdc');check();push(600);push(800);pv('screen');call('CreateCompatibleBitmap');store('bitmap');check();pv('bitmap');pv('memdc');call('SelectObject');store('oldobj')
cap=old[old.index('push(0xcc0020)'):old.index("label('advance')")]
cap=cap.replace('table(4)','outfile(0)').replace('table(8)','outfile(4)').replace("'advance'","'capturedone'")
cap=cap.replace('push(0xcc0020)',"stage('stageblit');push(0xcc0020)").replace("pv('oldobj');pv('memdc');call('SelectObject')","stage('stagedib');pv('oldobj');pv('memdc');call('SelectObject')").replace("push(0);push(0x80);push(2)","stage('stagefile');push(0);push(0x80);push(2)")
exec(cap)
label('capturedone');pv('oldobj');pv('memdc');call('SelectObject');pv('bitmap');call('DeleteObject');pv('memdc');call('DeleteDC');pv('screen');push(0);call('ReleaseDC');emit('c3')
# Emit an x86 PE, keeping the same Win95-compatible optional header.
exec(old[old.index('for p,n,absolute in fixes:'):old.index("OUTPUT_PREVIEW.write_bytes")])
binary=h.ljust(512,b'\0')+C.ljust(rc,b'\0')+D.ljust(rd,b'\0')
(BUILD / ('showcase-test.exe' if TEST else 'showcase.exe')).write_bytes(binary)
recovery=bytearray(binary);recovery[512:517]=b'\xe9'+struct.pack('<i',labels['restoreentry']-5);(BUILD / ('restore-test-appearance.exe' if TEST else 'restore-appearance.exe')).write_bytes(recovery)
print('Built', 'showcase-test.exe (10 captures)' if TEST else 'showcase.exe (170 captures)', 'and recovery helper in', BUILD)
