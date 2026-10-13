from ui import *
img = Image.new("RGB",(W,H),C["canvas"]); d = ImageDraw.Draw(img)
layers=[(0,"Product Card","al"),(1,"Image","img"),(1,"Title","text"),(1,"Details","al"),(2,"Description","text"),(2,"Price","text"),(1,"Button","al"),(2,"Label","text")]
chrome(d, layers, selected="Product Card", props=auto_layout_panel(gap=16,pad=24,hi="gap"))
d.text((LEFT+430,170),"Product Card",font=ui(14),fill=C["purple"])
card(d, LEFT+430, 195, 360, show_guides=True)
# callout
f=font("Anton-Regular.ttf",64)
d.rounded_rectangle([LEFT+40,120,LEFT+390,250],18,fill=(20,20,30))
d.text((LEFT+64,130),"GAP = 16",font=f,fill=(255,214,0))
d.text((LEFT+66,205),"items ke beech ka space",font=font("Mukta-Bold.ttf",28),fill="white")
cursor(img, W-RIGHT+90, TOP+205)
caption(img, ["Gap","se","har","item","ke","beech","EQUAL","space"], 6)
img.save("sample_frame.png")
