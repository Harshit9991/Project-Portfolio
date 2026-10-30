import React from 'react';
export const FileCard=({children}:any)=><main className="file-card">{children}</main>;
export const Header=({title,fact,intro}:any)=><header><h1>{title}</h1><small>{fact}</small><p>{intro}</p></header>;
export const Group=({label,children}:any)=><section><h2>{label}</h2>{children}</section>;
export const Closing=({children}:any)=><footer>{children}</footer>;
export const Callout=({title,children}:any)=><aside><h3>{title}</h3><p>{children}</p></aside>;
export const Photos=({items}:any)=><div>{items.map((p:any)=><img key={p.src} src={p.src} alt={p.alt} style={{maxWidth:'100%'}}/>)}</div>;
export const FileButton=({children,selected,compact,...p}:any)=><button aria-pressed={selected} {...p}>{children}</button>;
