import React, {useEffect,useRef,useState} from 'react';
import {FileCard,Header,Group,Closing,Callout,Photos,FileButton} from './ui';
import data from './model.json';
import {modelData} from './modelDownload';
import reference from './reference-three-quarter.jpg';
import modelPreview from './model-preview.png';
import './style.css';
const presets:any={Perspective:[-.23,-.42,0],Front:[0,0,0],Back:[0,Math.PI,0],Left:[0,-Math.PI/2,0],Bottom:[-Math.PI/2,0,0]};
export function App(){
 const canvas=useRef<HTMLCanvasElement>(null);const drag=useRef<any>(null);const [rot,setRot]=useState(presets.Perspective);const [zoom,setZoom]=useState(1);const [view,setView]=useState('Perspective');
 useEffect(()=>{const c=canvas.current;if(!c)return;let raf=0;const draw=()=>{const rect=c.getBoundingClientRect();const dpr=Math.min(devicePixelRatio||1,1.5);c.width=rect.width*dpr;c.height=rect.height*dpr;const ctx=c.getContext('2d');if(!ctx)return;ctx.scale(dpr,dpr);const W=rect.width,H=rect.height;ctx.fillStyle='#f6f5f3';ctx.fillRect(0,0,W,H);const [rx,ry,rz]=rot;const sx=Math.sin(rx),cx=Math.cos(rx),sy=Math.sin(ry),cy=Math.cos(ry),sz=Math.sin(rz),cz=Math.cos(rz);const scale=Math.min(W/17,H/13.8)*zoom;
 const pts=data.vertices.map((p:number[])=>{let [x,y,z]=p; y-=.7;let yy=y*cx-z*sx,zz=y*sx+z*cx;let xx=x*cy+zz*sy;z=-x*sy+zz*cy;x=xx*cz-yy*sz;y=xx*sz+yy*cz;const k=30/(30-z);return [W/2+x*scale*k,H/2-y*scale*k,z,x,y];});
 const rw=c.width,rh=c.height;const img=ctx.createImageData(rw,rh);const pixels=img.data;const depth=new Float32Array(rw*rh);depth.fill(-1e9);for(let i=0;i<pixels.length;i+=4){pixels[i]=246;pixels[i+1]=245;pixels[i+2]=243;pixels[i+3]=255;}
 for(const f of data.faces){const a=pts[f[0]],b=pts[f[1]],d=pts[f[2]];const u=[b[3]-a[3],b[4]-a[4],b[2]-a[2]],v=[d[3]-a[3],d[4]-a[4],d[2]-a[2]];let nx=u[1]*v[2]-u[2]*v[1],ny=u[2]*v[0]-u[0]*v[2],nz=u[0]*v[1]-u[1]*v[0];let n=Math.hypot(nx,ny,nz)||1;nx/=n;ny/=n;nz/=n;const col=data.materials[f[3]][1] as number[];const metal=Number(data.materials[f[3]][2]);const light=.50+.40*Math.abs(nx*-.35+ny*.6+nz*.72);const spec=metal*Math.pow(Math.max(0,nx*-.25+ny*.4+nz*.88),10)*.30;const rgb=col.slice(0,3).map(x=>Math.round(Math.min(1,Math.pow(x,.65)*light+spec)*255));
 const ax=a[0]*dpr,ay=a[1]*dpr,bx=b[0]*dpr,by=b[1]*dpr,dx=d[0]*dpr,dy=d[1]*dpr;const den=(by-dy)*(ax-dx)+(dx-bx)*(ay-dy);if(Math.abs(den)<.01)continue;
 const minx=Math.max(0,Math.floor(Math.min(ax,bx,dx))),maxx=Math.min(rw-1,Math.ceil(Math.max(ax,bx,dx))),miny=Math.max(0,Math.floor(Math.min(ay,by,dy))),maxy=Math.min(rh-1,Math.ceil(Math.max(ay,by,dy)));
 for(let y=miny;y<=maxy;y++)for(let x=minx;x<=maxx;x++){const wa=((by-dy)*(x+.5-dx)+(dx-bx)*(y+.5-dy))/den;const wb=((dy-ay)*(x+.5-dx)+(ax-dx)*(y+.5-dy))/den;const wc=1-wa-wb;if(wa<-.0001||wb<-.0001||wc<-.0001)continue;const z=wa*a[2]+wb*b[2]+wc*d[2],id=y*rw+x;if(z<=depth[id])continue;depth[id]=z;const j=id*4;pixels[j]=rgb[0];pixels[j+1]=rgb[1];pixels[j+2]=rgb[2];}
 }ctx.putImageData(img,0,0);
 };raf=requestAnimationFrame(draw);const ro=new ResizeObserver(draw);ro.observe(c);return()=>{cancelAnimationFrame(raf);ro.disconnect()};},[rot,zoom]);
 function preset(k:string){setView(k);setRot(presets[k]);}
 function turn(axis:number,amount:number){setView('Custom');setRot((r:number[])=>r.map((v,i)=>i===axis?v+amount:v));}
 return <FileCard><Header title="Your speaker, digitised" fact="Reference model · Detail update" intro="A first 3D study made from your speaker photos, with a raised strap and a 2½-inch body height."/>
 <Group label="Rotate and inspect" heading><div className="viewer"><img className="model-fallback" src={modelPreview} alt="First reference-modelled 3D speaker, perspective view"/><canvas ref={canvas} aria-label="Rotatable 3D speaker model. Drag to turn, or use the view and rotation buttons below." role="img" onPointerDown={e=>{e.currentTarget.setPointerCapture(e.pointerId);drag.current=[e.clientX,e.clientY,rot];}} onPointerMove={e=>{if(!drag.current)return;const [x,y,r]=drag.current;setView('Custom');setRot([r[0]+(e.clientY-y)*.012,r[1]+(e.clientX-x)*.012,r[2]]);}} onPointerUp={()=>drag.current=null} onPointerCancel={()=>drag.current=null}/><span className="hint">Drag to turn · {view}</span></div>
 <div className="views">{Object.keys(presets).map(k=><FileButton key={k} selected={view===k} compact onClick={()=>preset(k)}>{k}</FileButton>)}</div>
 <div className="axes">{['Tilt','Turn','Roll'].map((k,i)=><div key={k}><span>{k}</span><FileButton compact onClick={()=>turn(i,-Math.PI/8)} aria-label={`${k} negative`}>−</FileButton><FileButton compact onClick={()=>turn(i,Math.PI/8)} aria-label={`${k} positive`}>+</FileButton></div>)}</div>
 <div className="views"><FileButton compact onClick={()=>setZoom(z=>Math.max(.75,z-.15))}>Zoom out</FileButton><FileButton compact onClick={()=>setZoom(z=>Math.min(1.35,z+.15))}>Zoom in</FileButton><FileButton compact onClick={()=>{preset('Perspective');setZoom(1)}}>Reset</FileButton></div>
 <a className="download file-hover-underline" href={modelData} download="speaker-reference-v2.glb">Download 3D asset (.glb)</a></Group>
 <Group label="What to review" heading><Callout title="A recognisable model, not a precision scan">Body: 4½ × 2½ × 2½ inches, excluding the raised strap. The black shell, metallic trim, grille, dial, buttons, rear pattern, feet and strap are modelled. Dial numbers 00–100, radial ticks and the marks below the buttons now follow your close-ups. These are clean geometric marks, not photo textures or physically recessed engraving. Surface finish, fine strokes and strap curvature remain approximate. The underside label is a plain placeholder.</Callout><p>Check the overall shape, proportions and colour first. The controls are geometry only: there is no music, logo, pickup animation or table scene in this version.</p></Group>
 <Group label="Your source reference"><Photos items={[{src:reference,alt:'User-supplied three-quarter photo of the actual black speaker with metallic trim and reddish strap',fit:'contain'}]}/></Group>
 <Closing>Speaker asset review. No music, logo integration or room scene included.</Closing></FileCard>;
}
