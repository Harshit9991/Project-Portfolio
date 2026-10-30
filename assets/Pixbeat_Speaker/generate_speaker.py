import math,json,struct,base64,os
from pathlib import Path
root=str(Path(__file__).resolve().parent)
V=[];F=[]
M=[('Body',[.045,.044,.058,1],.08,.4),('Trim',[.75,.45,.36,1],.88,.22),('Dark recess',[.012,.014,.019,1],.1,.6),('Strap',[.40,.11,.065,1],0,.65),('Rubber',[.025,.025,.03,1],0,.9),('Label',[.72,.71,.69,1],0,.8)]
def mesh(v,f,m):
 n=len(V);V.extend(v);F.extend([[n+a,n+b,n+c,m] for a,b,c in f])
def cylinder(x,y,z,r,d,m,N=40):
 v=[]
 for zz in (z-d/2,z+d/2):
  v.extend([[x+r*math.cos(i*2*math.pi/N),y+r*math.sin(i*2*math.pi/N),zz] for i in range(N)])
 v.extend([[x,y,z-d/2],[x,y,z+d/2]])
 f=[]
 for i in range(N):
  j=(i+1)%N;f.extend([(i,j,N+j),(i,N+j,N+i),(2*N,j,i),(2*N+1,N+i,N+j)])
 mesh(v,f,m)
def box(x,y,z,w,h,d,r,m):
 pts=[]
 for cx,cy,start in [(w/2-r,h/2-r,0),(-w/2+r,h/2-r,90),(-w/2+r,-h/2+r,180),(w/2-r,-h/2+r,270)]:
  for i in range(7):
   a=math.radians(start+i*90/6);pts.append([x+cx+r*math.cos(a),y+cy+r*math.sin(a)])
 n=len(pts);v=[[xx,yy,z+zz] for zz in (-d/2,d/2) for xx,yy in pts];v.extend([[x,y,z-d/2],[x,y,z+d/2]])
 f=[]
 for i in range(n):
  j=(i+1)%n;f.extend([(i,j,n+j),(i,n+j,n+i),(2*n,j,i),(2*n+1,n+i,n+j)])
 mesh(v,f,m)
# Body and thin front bezel.
box(0,0,0,11.43,6.35,6.35,.70,0)
box(0,0,3.18,11.46,6.38,.24,.76,1)
box(0,0,3.34,11.12,6.05,.16,.69,0)
# Grille with dark cavity and horizontal metallic bars.
cylinder(-2.40,.18,3.49,2.37,.17,1)
cylinder(-2.40,.18,3.60,2.22,.10,2)
for y in [i*.19 for i in range(-11,12)]:
 w=2*math.sqrt(max(0,2.16**2-y*y))
 if w:box(-2.40,y+.18,3.68,w,.065,.055,.025,1)
box(-2.40,.18,3.72,.055,4.32,.055,.022,1)
cylinder(-2.4,.18,3.78,.33,.12,1)
cylinder(-2.4,.18,3.86,.23,.055,1)
# Dial ring and central knob.
cylinder(3.08,1.18,3.48,1.43,.18,1)
cylinder(3.08,1.18,3.60,1.25,.08,5)
cylinder(3.08,1.18,3.76,.73,.40,1)
cylinder(3.08,1.18,4.00,.60,.08,1)
# Clean geometric dial text and markings, based on the supplied close-up.
from PIL import Image,ImageDraw,ImageFont
font=ImageFont.truetype('/usr/share/fonts/truetype/dejavu/DejaVuSansCondensed.ttf',54)
def textmesh(text,x,y,z,height,angle=0,mat=2):
 bb=font.getbbox(text);im=Image.new('L',(bb[2]-bb[0]+4,bb[3]-bb[1]+4));ImageDraw.Draw(im).text((2-bb[0],2-bb[1]),text,font=font,fill=255)
 w,h=im.size;k=height/h;ca=math.cos(angle);sa=math.sin(angle);v=[];f=[]
 for row in range(h):
  col=0
  while col<w:
   if im.getpixel((col,row))<100:col+=1;continue
   start=col
   while col<w and im.getpixel((col,row))>=100:col+=1
   pts=[((start-w/2)*k,(h/2-row)*k),((col-w/2)*k,(h/2-row)*k),((col-w/2)*k,(h/2-row-1)*k),((start-w/2)*k,(h/2-row-1)*k)]
   n=len(v);v.extend([[x+px*ca-py*sa,y+px*sa+py*ca,z] for px,py in pts]);f.extend([(n,n+1,n+2),(n,n+2,n+3)])
 mesh(v,f,mat)
def stroke(points,width=.035,z=3.435,mat=2):
 v=[];f=[]
 for (x1,y1),(x2,y2) in zip(points,points[1:]):
  dx=x2-x1;dy=y2-y1;n=math.hypot(dx,dy)
  if not n:continue
  ox=-dy/n*width/2;oy=dx/n*width/2;j=len(v)
  v.extend([[x1+ox,y1+oy,z],[x2+ox,y2+oy,z],[x2-ox,y2-oy,z],[x1-ox,y1-oy,z]]);f.extend([(j,j+1,j+2),(j,j+2,j+3)])
 mesh(v,f,mat)
for i,label in enumerate(['00']+[str(j) for j in range(10,101,10)]):
 a=math.radians(230-i*28)
 textmesh(label,3.08+1.0*math.cos(a),1.18+1.0*math.sin(a),3.648,.30,a-math.pi/2)
 stroke([(3.08+r*math.cos(a),1.18+r*math.sin(a)) for r in (1.20,1.34)],.028,3.65)
for x in (1.84,3.01,4.18):
 cylinder(x,-1.66,3.55,.43,.30,2,24)
 cylinder(x,-1.66,3.78,.34,.22,1,24)
 cylinder(x,-1.66,3.91,.25,.04,1,24)
# Engraving-like marks below the three buttons. Dark grooves, no photo reflections.
y=-2.48
for x,direction in [(1.84,-1),(4.18,1)]:
 for off in (-.13,.10):
  tip=x+direction*(off+.08);tail=x+direction*(off-.10)
  stroke([(tail,y+.18),(tip,y),(tail,y-.18)],.045)
 bar=x+direction*.34;stroke([(bar,y+.21),(bar,y-.21)],.045)
# Power icon and M, followed by the play/pause-shaped mark visible in source.
x=2.45
stroke([(x+.16*math.cos(math.radians(a)),y+.16*math.sin(math.radians(a))) for a in range(125,417,9)],.035)
stroke([(x,y+.07),(x,y+.24)],.038)
textmesh('M',2.97,y,3.435,.39,0,2)
stroke([(3.30,y-.18),(3.48,y),(3.30,y+.18),(3.30,y-.18)],.032)
for x in (3.55,3.63):stroke([(x,y-.18),(x,y+.18)],.028)
# Back rim and perforated surface.
box(0,0,-3.20,11.1,6.03,.12,.65,0)
for row in range(-8,9):
 for col in range(-16,17):
  x=col*.31+(row%2)*.15;y=row*.31
  if abs(x)>5 or abs(y)>2.6:continue
  # radial density on right matches the photographed speaker area.
  if (x-2.0)**2+y*y<1.6**2 and (row+col)%2:continue
  cylinder(x,y,-3.285,.047,.026,2,6)
# Rubber feet and plain label on underside: rotate local geometry.
start=len(V)
box(-3.6,0,0,.75,2.8,.12,.07,4);box(3.6,0,0,.75,2.8,.12,.07,4);box(0,0,0,2.3,1.45,.025,.08,5)
for i in range(start,len(V)):
 x,y,z=V[i];V[i]=[x,-3.24-z,y]
# Side strap fasteners (cylinder axes rotated to X).
for side in (-1,1):
 start=len(V);cylinder(0,1.68,0,.43,.16,1,28)
 for i in range(start,len(V)):
  x,y,z=V[i];V[i]=[side*(5.74+z),y,x]
# Raised strap arcing across X, fixed pose, broad ribbon in Z.
v=[];n=49
for i in range(n):
 t=i/(n-1)*math.pi;x=-5.74*math.cos(t);y=1.68+3.7*math.sin(t)
 for dz,dy in [(-.65,0),(.65,0),(-.65,.10),(.65,.10)]:v.append([x,y+dy,dz])
f=[]
for i in range(n-1):
 a=i*4;b=(i+1)*4
 for u,w in [(0,1),(2,3),(0,2),(1,3)]:f.extend([(a+u,b+u,b+w),(a+u,b+w,a+w)])
mesh(v,f,3)
# Right ports, small dark inset slots shown in three-quarter reference.
start=len(V)
box(0,-.8,0,.18,1.1,.03,.05,2);box(.5,-1.9,0,.65,.2,.03,.04,2)
for i in range(start,len(V)):
 x,y,z=V[i];V[i]=[5.76+z,y,x]
# Retail hang tag: original geometry, logo reconstructed from supplied source.
tag_start=len(V)
M.extend([('Tag paper',[.94,.91,.84,1],0,.9),('Cotton cord',[.78,.74,.64,1],0,.95)])
cardmat=len(M)-2;cordmat=len(M)-1
# Flat card slightly clockwise, clear of the front controls.
TC=(7.75,-.05,2.25);ANG=-.12
ca=math.cos(ANG);sa=math.sin(ANG)
def tagp(x,y,z):return [TC[0]+x*ca-y*sa,TC[1]+x*sa+y*ca,TC[2]+z]
start=len(V);box(0,0,0,1.85,2.65,.07,.10,cardmat)
for i in range(start,len(V)):V[i]=tagp(*V[i])
# Eyelet sits in the top edge, visible from either face.
for side in (-1,1):
 vv=[];ff=[]
 for r in (.105,.055):
  vv.extend([tagp(r*math.cos(i*math.tau/24),1.11+r*math.sin(i*math.tau/24),side*.041) for i in range(24)])
 for i in range(24):
  j=(i+1)%24;ff.extend([(i,j,24+j),(i,24+j,24+i)])
 mesh(vv,ff,cordmat)
 cylinder(TC[0]-1.11*sa,TC[1]+1.11*ca,TC[2],.054,.084,2,24)
def cord(a,b,r=.027):
 # Tube segment, arbitrary direction.
 d=[b[i]-a[i] for i in range(3)];l=math.sqrt(sum(x*x for x in d));d=[x/l for x in d]
 u=[-d[1],d[0],0];ul=math.hypot(*u);u=[x/ul for x in u];v=[d[1]*u[2]-d[2]*u[1],d[2]*u[0]-d[0]*u[2],d[0]*u[1]-d[1]*u[0]]
 vv=[[p[i]+r*(u[i]*math.cos(j*math.tau/8)+v[i]*math.sin(j*math.tau/8)) for i in range(3)] for p in (a,b) for j in range(8)]
 ff=[]
 for j in range(8):k=(j+1)%8;ff.extend([(j,k,8+k),(j,8+k,8+j)])
 mesh(vv,ff,cordmat)
points=[[5.78,1.72,.1],[6.42,2.05,.75],[7.4,1.72,1.6],tagp(0,1.11,.07)]
for a,b in zip(points,points[1:]):cord(a,b)
# Two outward-reading logos, no photo reflection or stock reference texture.
im=Image.open(root+'/logo-reference.jpg').convert('RGB')
# Supplied mark is circular within a near-square white field.
w,h=im.size;im=im.crop((int(w*.06),int(h*.06),int(w*.94),int(h*.94))).resize((128,128)).quantize(colors=48,method=2)
pal=im.getpalette();mats={}
for ix in set(im.getdata()):
 rgb=pal[ix*3:ix*3+3];mats[ix]=len(M);M.append(('Logo ink '+str(ix),[(c/255)**2.2 for c in rgb]+[1],0,.85))
for side in (-1,1):
 for row in range(128):
  col=0
  while col<128:
   ix=im.getpixel((col,row));end=col+1
   while end<128 and im.getpixel((end,row))==ix:end+=1
   rgb=pal[ix*3:ix*3+3]
   if min(rgb)<220:
    x0=(col/128-.5)*1.58;x1=(end/128-.5)*1.58;y0=(.5-row/128)*1.58-.12;y1=(.5-(row+1)/128)*1.58-.12
    vv=[tagp(side*x0,y0,side*.042),tagp(side*x1,y0,side*.042),tagp(side*x1,y1,side*.042),tagp(side*x0,y1,side*.042)]
    mesh(vv,[(0,1,2),(0,2,3)],mats[ix])
   col=end
# Tag face outlines used for depth-aware hit testing.
tag_corners=[tagp(x,y,z) for z in (-.046,.046) for x,y in [(-.925,-1.325),(.925,-1.325),(.925,1.325),(-.925,1.325)]]

data={'vertices':V,'faces':F,'materials':M,'tagStart':tag_start,'tagCorners':tag_corners}
open(root+'/model.json','w').write(json.dumps(data,separators=(',',':')))
# Standard glTF binary in metres, material meshes separated.
blob=bytearray();views=[];acc=[];prims=[]
def add(raw,target):
 while len(blob)%4:blob.append(0)
 o=len(blob);blob.extend(raw);views.append({'buffer':0,'byteOffset':o,'byteLength':len(raw),'target':target});return len(views)-1
pos=[c*.01 for p in V for c in p]
pv=add(struct.pack('<%sf'%len(pos),*pos),34962)
acc.append({'bufferView':pv,'componentType':5126,'count':len(V),'type':'VEC3','min':[min(p[i] for p in V)*.01 for i in range(3)],'max':[max(p[i] for p in V)*.01 for i in range(3)]})
for m in range(len(M)):
 inds=[i for a,b,c,mi in F if mi==m for i in (a,b,c)]
 if not inds:continue
 iv=add(struct.pack('<%sI'%len(inds),*inds),34963);ai=len(acc);acc.append({'bufferView':iv,'componentType':5125,'count':len(inds),'type':'SCALAR'})
 prims.append({'attributes':{'POSITION':0},'indices':ai,'material':m})
g={'asset':{'version':'2.0','generator':'Speaker reference study'},'scene':0,'scenes':[{'nodes':[0]}],'nodes':[{'mesh':0,'name':'Speaker - reference model'}],'meshes':[{'primitives':prims}],'materials':[{'name':name,'pbrMetallicRoughness':{'baseColorFactor':color,'metallicFactor':metal,'roughnessFactor':rough},'doubleSided':True} for name,color,metal,rough in M],'buffers':[{'byteLength':len(blob)}],'bufferViews':views,'accessors':acc}
j=json.dumps(g,separators=(',',':')).encode();j+=b' '*((-len(j))%4);blob+=b'\0'*((-len(blob))%4)
glb=struct.pack('<III',0x46546c67,2,12+8+len(j)+8+len(blob))+struct.pack('<II',len(j),0x4e4f534a)+j+struct.pack('<II',len(blob),0x004e4942)+blob
open(root+'/speaker-reference-v3-tag.glb','wb').write(glb)
open(root+'/modelDownload.ts','w').write('export const modelData="data:model/gltf-binary;base64,'+base64.b64encode(glb).decode()+'";')
print('vertices',len(V),'triangles',len(F),'GLB bytes',len(glb))
