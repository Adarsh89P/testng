from card import *
W,H=1080,1920
def frame(tag, lines, chars, manual):
    cv=Canvas(W,H); cv.clear()
    cv.pill(W/2, 210, tag, size=32, bold=True)
    cv.code_box(30, 270, W-60, 250, lines, chars)
    if manual:
        b=card_layout(270,640,540,title_rows=2,gap=16,pad=24)
        # manual: title grew but nothing moved -> overlap
        b2=card_layout(270,640,540,title_rows=1)
        b["details"]=b2["details"]; b["button"]=b2["button"]; b["card"]=b2["card"]
        draw_card(cv,b,title_rows=2,offsets={"button":(14,0),"details":(6,0)})
        cv.pill(880,950,"overlap!",size=26,fam=MONO,col=BAD)
        cv.glow(b["details"][0]+60,b["details"][1]+10,60)
    else:
        b=card_layout(270,640,540,title_rows=2)
        draw_card(cv,b,title_rows=2); measure_gap(cv,b,"gap: 16")
        cv.pill(160,1100,"hug",size=26,fam=MONO)
    cv.line(W/2, b["card"][1]+b["card"][3], W/2, 1560)
    cv.person(W/2,1610,1.0)
    cv.pill(W/2,1720,"Designer",size=28)
    return cv
frame("15 LPA",["title.text = 'Wireless Noise", "  Cancelling Headphones'","// sab manually drag..."],200,True).png("s15.png")
frame("45 LPA",["auto-layout: vertical","gap: 16","padding: 24","height: hug"],200,False).png("s45.png")
