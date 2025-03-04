import os
import qrcode

img = qrcode.make("https://youtu.be/mIxa0hAa1BY?si=Dv-Dp02Og-PkLCFm")

img.save("qr.png", "PNG")

os.system("open qr.png")
