# IDS: ADAPT — d13 folhas_final.py (quadros + rótulo de tempo), em PIL: folha de um vídeo, um quadro a cada PASSO s.
# uso: .venv-mflux/bin/python3.12 -I folha.py <video.mp4> <saida.jpg> [passo=0.75]
import sys, subprocess, tempfile, os, glob
from PIL import Image, ImageDraw, ImageFont
v, out = sys.argv[1], sys.argv[2]; passo = float(sys.argv[3]) if len(sys.argv) > 3 else 0.75
dur = float(subprocess.check_output(['ffprobe','-v','error','-show_entries','format=duration','-of','csv=p=0',v]))
ts = []; t = 0.0
while t < dur - 0.2: ts.append(round(t, 3)); t += passo
W, H = 270, 480; COLS = 5
font = ImageFont.truetype('/System/Library/Fonts/Supplemental/Arial Bold.ttf', 26)
with tempfile.TemporaryDirectory() as td:
    ims = []
    for i, t in enumerate(ts):
        p = f'{td}/{i:03d}.png'
        subprocess.run(['ffmpeg','-v','error','-y','-ss',f'{t+0.02:.3f}','-i',v,'-frames:v','1','-vf',f'scale={W}:{H}',p], check=True)
        ims.append(Image.open(p).convert('RGB'))
rows = (len(ims) + COLS - 1) // COLS
sheet = Image.new('RGB', (COLS*W + (COLS+1)*4, rows*H + (rows+1)*4), (17,17,17))
d = ImageDraw.Draw(sheet)
for i, (im, t) in enumerate(zip(ims, ts)):
    x = 4 + (i % COLS)*(W+4); y = 4 + (i // COLS)*(H+4)
    sheet.paste(im, (x, y))
    lab = f'{t:.2f}'.replace('.', ',') + ' s'
    d.rectangle([x, y+H-34, x+110, y+H], fill=(0,0,0)); d.text((x+5, y+H-31), lab, fill=(255,255,0), font=font)
sheet.save(out, quality=88)
print(out, len(ts), 'quadros')
