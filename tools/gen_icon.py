#!/usr/bin/env python3
"""Generate assets/images/site-icon.png (512px record) with stdlib only."""
import zlib, struct, math, os
S=512; m=S/2; LABEL=0.22
def cov(d,r): return max(0.0,min(1.0,r-d+0.5))
def mix(a,b,t): return tuple(a[i]*(1-t)+b[i]*t for i in range(3))
rows=[]
for y in range(S):
    row=bytearray([0])
    for x in range(S):
        px=x+.5-m; py=y+.5-m; d=math.hypot(px,py)
        col=(11,11,11); a=cov(d,m-6)
        if d<m-14 and d>S*LABEL+8:
            g=max(0,1-abs(((m-14-d)%6.5)-3.25)/1.4); col=mix(col,(34,34,34),g)
        rim=max(0,1-abs(d-(m-7.5))/1.6); col=mix(col,(70,70,70),rim*.9)
        # soft light sheen on the vinyl
        ang=math.atan2(py,px); sheen=max(0,math.cos(2*(ang+0.8)))**8*0.10
        if S*LABEL+8<d<m-14: col=mix(col,(255,255,255),sheen)
        lr=S*LABEL
        if d<lr+1:
            t=min(1,max(0,(px+py)/(lr*2)+.5)); col=mix(col,mix((255,138,79),(244,96,36),t),cov(d,lr))
        col=mix(col,(6,9,10),cov(d,S*0.022))
        row+=bytes([round(c) for c in col]+[round(255*a)])
    rows.append(bytes(row))
def ch(t,d):
    c=struct.pack('>I',len(d))+t+d; return c+struct.pack('>I',zlib.crc32(t+d)&0xffffffff)
png=b'\x89PNG\r\n\x1a\n'+ch(b'IHDR',struct.pack('>IIBBBBB',S,S,8,6,0,0,0))+ch(b'IDAT',zlib.compress(b''.join(rows),9))+ch(b'IEND',b'')
out=os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))),'assets/images/site-icon.png')
open(out,'wb').write(png); print(out,len(png))
