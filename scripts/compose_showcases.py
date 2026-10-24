"""Composite real Win98 screenshot pixels; do not rescale, redraw, or pad crop bounds."""
from pathlib import Path
from PIL import Image,ImageChops
import numpy as np
from collections import deque
import json
import argparse
from capture_common import ROOT, BUILD
parser=argparse.ArgumentParser(description='Arrange five native captures per scheme into one 960-pixel-wide scene.')
parser.add_argument('--input',type=Path,default=BUILD/'raw-showcase')
parser.add_argument('--output',type=Path,default=ROOT/'showcases')
args=parser.parse_args()
src=args.input.resolve();out=args.output.resolve();out.mkdir(parents=True,exist_ok=True)
def bbox_for(base,pic,kind):
 a=np.array(base.convert('RGB')).astype(np.int16);b=np.array(pic.convert('RGB')).astype(np.int16);mask=np.max(np.abs(a-b),axis=2)>8
 if kind=='menu':mask[:180]=False;mask[500:]=False;mask[:,:45]=False;mask[:,600:]=False
 elif kind=='tooltip':mask[:300]=False;mask[510:]=False
 else:mask[:175]=False;mask[540:]=False
 components=[]
 for y,x in zip(*np.nonzero(mask)):
  if not mask[y,x]:continue
  q=deque([(int(x),int(y))]);mask[y,x]=False;minx=maxx=int(x);miny=maxy=int(y);count=0
  while q:
   xx,yy=q.popleft();count+=1;minx=min(minx,xx);maxx=max(maxx,xx);miny=min(miny,yy);maxy=max(maxy,yy)
   for nx,ny in [(xx-1,yy),(xx+1,yy),(xx,yy-1),(xx,yy+1)]:
    if 0<=nx<800 and 0<=ny<600 and mask[ny,nx]:mask[ny,nx]=False;q.append((nx,ny))
  w=maxx-minx+1;h=maxy-miny+1
  if w>=50 and h>=10:components.append((w*h,count,(minx,miny,maxx+1,maxy+1)))
 assert components,kind
 components.sort(reverse=True);box=components[0][2]
 if kind=='message':
  # Recover a large-font title bar above the difference-search region from its continuous native border.
  photo=np.array(pic.convert('RGB'));original=np.array(base.convert('RGB'));mid=(box[1]+box[3])//2;tops=[]
  for xx in [box[0],box[0]+1,box[0]+2,box[2]-1,box[2]-2,box[2]-3]:
   if not np.any(photo[mid,xx]!=original[mid,xx]):continue
   color=photo[mid,xx];yy=mid
   while yy>120 and np.array_equal(photo[yy-1,xx],color):yy-=1
   if 120<yy<box[1] and mid-yy>30:tops.append(yy)
  if tops:box=(box[0],min(tops),box[2],box[3])
 # Connected-component bounds already include the native outer border.
 # Do not pad them: padding copies pixels from the window underneath.
 return box
report={}
for folder in sorted(src.iterdir()):
 if not folder.is_dir() or not (folder/'controls.png').is_file():continue
 base=Image.open(folder/'controls.png').convert('RGB');desktop=Image.open(folder/'desktop.png').convert('RGB');preboxes={kind:bbox_for(base,Image.open(folder/(kind+'.png')).convert('RGB'),kind) for kind in ['menu','message','tooltip']};canvas_h=max(630+preboxes['menu'][3]-preboxes['menu'][1],620+preboxes['message'][3]-preboxes['message'][1])+48+preboxes['tooltip'][3]-preboxes['tooltip'][1];scene=Image.new('RGB',(960,canvas_h),desktop.getpixel((799,599)))
 scene.paste(desktop.crop((0,0,175,175)),(0,0))
 scene.paste(base.crop((20,15,500,115)),(180,70))
 scene.paste(base.crop((530,15,780,115)),(690,40))
 scene.paste(base.crop((8,115,792,565)),(24,160))
 boxes={}
 for kind in ['menu','message','tooltip']:
  pic=Image.open(folder/(kind+'.png')).convert('RGB');box=preboxes[kind];patch=pic.crop(box);w,h=patch.size;boxes[kind]=box
  if kind=='menu':pos=(24,630)
  elif kind=='message':pos=(960-w-24,620)
  else:pos=(24,canvas_h-24-h)
  scene.paste(patch,pos)
 scene.save(out/(folder.name+'.png'));report[folder.name]=boxes
manifest={'layout':'Unified desktop-style scene','width':960,'nativeScale':'1:1','sourceCrops':report}
(out/'crop-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
print('Built',len(report),'unified scenes. Default crops:',report.get('windows-standard-default'))
