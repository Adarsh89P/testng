"""Figma-like UI renderer (1920x1080) for tutorial videos. Pure Pillow, so every frame is code-drawn."""
from PIL import Image, ImageDraw, ImageFont, ImageFilter
import os
F = os.path.join(os.path.dirname(__file__), "..", "assets", "fonts")
def font(name, size): return ImageFont.truetype(os.path.join(F, name), size)
INTER = "/usr/share/fonts/truetype/inter/Inter-Regular.ttf"
def ui(size, bold=False):
    for p in ["/usr/share/fonts/opentype/inter/Inter-%s.otf" % ("SemiBold" if bold else "Regular"),
              "/usr/share/fonts/truetype/inter/Inter-%s.ttf" % ("SemiBold" if bold else "Regular")]:
        if os.path.exists(p): return ImageFont.truetype(p, size)
    return font("Poppins-Bold.ttf" if bold else "Poppins-Bold.ttf", size)

W, H = 1920, 1080
TOP, LEFT, RIGHT = 48, 260, 300
C = dict(bar=(44,44,44), panel=(255,255,255), line=(230,230,230), canvas=(229,229,229),
         text=(30,30,30), sub=(120,120,120), blue=(13,153,255), purple=(151,71,255),
         pink=(255,0,153), sel=(222,239,255))

def chrome(d, layers, selected=None, props=None, tool="move"):
    d.rectangle([0,0,W,TOP], fill=C["bar"])
    x = 16
    for i,t in enumerate(["▲","#","□","✎","T","◯","💬"]):
        on = (i==0 and tool=="move") or (i==1 and tool=="frame")
        if on: d.rounded_rectangle([x-6,8,x+30,40], 6, fill=C["blue"])
        d.text((x+4,12), t, font=ui(18,True), fill="white")
        x += 46
    d.text((W/2-90,13), "Auto Layout Card", font=ui(17,True), fill="white")
    d.rounded_rectangle([W-120,9,W-16,39], 6, fill=C["blue"]); d.text((W-98,13),"Share",font=ui(16,True),fill="white")
    # left panel
    d.rectangle([0,TOP,LEFT,H], fill=C["panel"]); d.line([LEFT,TOP,LEFT,H], fill=C["line"])
    d.text((16,TOP+14),"Layers",font=ui(15,True),fill=C["text"])
    y = TOP+48
    for depth,name,kind in layers:
        if name == selected: d.rectangle([0,y-4,LEFT,y+24], fill=C["sel"])
        icon = {"frame":"#","al":"☰","text":"T","rect":"□","img":"▣"}[kind]
        col = C["purple"] if kind=="al" else C["sub"]
        d.text((16+depth*18,y), icon, font=ui(15,True), fill=col)
        d.text((38+depth*18,y), name, font=ui(15, name==selected), fill=C["text"])
        y += 30
    # right panel
    d.rectangle([W-RIGHT,TOP,W,H], fill=C["panel"]); d.line([W-RIGHT,TOP,W-RIGHT,H], fill=C["line"])
    d.text((W-RIGHT+16,TOP+14),"Design",font=ui(15,True),fill=C["text"])
    if props: props(d, W-RIGHT+16, TOP+56)

def auto_layout_panel(direction="vertical", gap=16, pad=24, align="top-left", hug=True, hi=None):
    def draw(d, x, y):
        def box(bx,by,bw,label,val,key):
            hl = hi==key
            d.rounded_rectangle([bx,by,bx+bw,by+32],5, fill=(255,240,250) if hl else (245,245,245),
                                outline=C["pink"] if hl else None, width=2)
            d.text((bx+8,by+7),label,font=ui(13),fill=C["sub"]); d.text((bx+30,by+6),str(val),font=ui(14,True),fill=C["text"])
        d.text((x,y),"Auto layout",font=ui(14,True),fill=C["text"]); y+=34
        for i,(sym,k) in enumerate([("↓","vertical"),("→","horizontal"),("⤶","wrap")]):
            on = k==direction; bx=x+i*40
            d.rounded_rectangle([bx,y,bx+34,y+32],5, fill=C["sel"] if on else (245,245,245),
                                outline=C["pink"] if hi=="direction" and on else None, width=2)
            d.text((bx+10,y+5),sym,font=ui(17,True),fill=C["blue"] if on else C["sub"])
        y+=44
        box(x,y,120,"⇕",gap,"gap"); box(x+130,y,120,"▢",pad,"pad"); y+=46
        # alignment grid
        d.rounded_rectangle([x,y,x+96,y+96],6,fill=(245,245,245),
                            outline=C["pink"] if hi=="align" else None, width=2)
        pos = {"top-left":(0,0),"center":(1,1),"top-center":(1,0)}[align]
        for r in range(3):
            for c in range(3):
                cx,cy=x+18+c*30,y+18+r*30
                if (c,r)==pos: d.rounded_rectangle([cx-9,cy-9,cx+9,cy+9],3,fill=C["blue"])
                else: d.ellipse([cx-2,cy-2,cx+2,cy+2],fill=(180,180,180))
        y+=112
        d.text((x,y),"Resizing",font=ui(14,True),fill=C["text"]); y+=30
        for lab in ["W","H"]:
            d.rounded_rectangle([x,y,x+250,y+32],5,fill=(245,245,245),
                                outline=C["pink"] if hi=="resize" else None, width=2)
            d.text((x+8,y+6),lab,font=ui(14,True),fill=C["sub"])
            d.text((x+34,y+6),"Hug contents" if hug else "Fixed  320",font=ui(14),fill=C["text"]); y+=40
    return draw

def card(d, x, y, w, pad=24, gap=16, show_guides=False):
    """Product card inside an auto-layout frame; returns height."""
    img_h = 180
    title, body, btn = ui(26,True), ui(17), ui(17,True)
    h = pad + img_h + gap + 34 + gap + 52 + gap + 48 + pad
    d.rounded_rectangle([x+6,y+10,x+w+6,y+h+10],18,fill=(205,205,205))
    d.rounded_rectangle([x,y,x+w,y+h],18,fill="white")
    cy = y+pad
    d.rounded_rectangle([x+pad,cy,x+w-pad,cy+img_h],12,fill=(255,214,102))
    d.ellipse([x+w/2-40,cy+50,x+w/2+40,cy+130],fill=(255,170,60))
    cy += img_h+gap; d.text((x+pad,cy),"Wireless Headphones",font=title,fill=C["text"]); cy+=34+gap
    d.text((x+pad,cy),"40h battery · Noise cancelling",font=body,fill=C["sub"])
    d.text((x+pad,cy+26),"₹4,999",font=ui(19,True),fill=C["text"]); cy+=52+gap
    d.rounded_rectangle([x+pad,cy,x+w-pad,cy+48],10,fill=C["blue"])
    tw=d.textlength("Add to cart",font=btn); d.text((x+w/2-tw/2,cy+12),"Add to cart",font=btn,fill="white")
    if show_guides:
        d.rectangle([x,y,x+w,y+h],outline=C["purple"],width=2)
        pk=(255,0,153,90)
        for gy in [y+pad+img_h, y+pad+img_h+gap+34, y+pad+img_h+2*gap+34+52]:
            d.rectangle([x+pad,gy,x+w-pad,gy+gap],fill=(255,190,225))
            d.text((x+w+12,gy-4),str(gap),font=ui(14,True),fill=C["pink"])
        d.rectangle([x,y,x+w,y+pad],fill=(255,190,225)); d.text((x+w+12,y+2),str(pad),font=ui(14,True),fill=C["pink"])
    return h

def cursor(img, x, y, scale=1.0):
    d = ImageDraw.Draw(img)
    s = 26*scale
    pts=[(x,y),(x,y+s),(x+s*0.28,y+s*0.75),(x+s*0.5,y+s*1.15),(x+s*0.65,y+s*1.08),(x+s*0.45,y+s*0.7),(x+s*0.8,y+s*0.7)]
    d.polygon(pts,fill="black",outline="white")

def caption(img, words, active, y=None):
    """Bold Hinglish caption bar at bottom; active word highlighted yellow."""
    d = ImageDraw.Draw(img); f = font("Mukta-ExtraBold.ttf", 54)
    total = sum(d.textlength(w+" ",font=f) for w in words)
    x = (W-RIGHT+LEFT)/2 - total/2; y = y or H-140
    for i,w in enumerate(words):
        col = (255,214,0) if i==active else "white"
        d.text((x,y),w,font=f,fill=col,stroke_width=7,stroke_fill="black")
        x += d.textlength(w+" ",font=f)
