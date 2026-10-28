"""Create a true path-only SVG from the original logo, including its original lettering.
Authoring dependencies: Pillow, NumPy, and potrace. Normal site builds need none of these.
The original PNG is retained unchanged. No fonts or embedded bitmaps are used in the SVG.
"""
from pathlib import Path
from PIL import Image
import numpy as np
import subprocess,tempfile,xml.etree.ElementTree as ET
ROOT=Path(__file__).resolve().parents[1]
im=Image.open(ROOT/'assets/ischys-original-logo.png').convert('RGBA')
a=np.asarray(im).astype(int);r,g,b,alpha=[a[:,:,i] for i in range(4)];x=np.arange(im.width)[None,:]
regions=[('omega',(x<620)&(g>r+12)&(b>r+12)),('brain',(x<620)&(r>g+6)&(g>b+10)),('lettering',(x>=620)&(r<80)&(g<100)&(b<120))]
ns='{http://www.w3.org/2000/svg}';groups=[]
with tempfile.TemporaryDirectory() as tmp:
 for name,region in regions:
  mask=region&(alpha>150)
  solid=region&(alpha>245)
  rgb=np.median(a[:,:,:3][solid],axis=0).astype(int)
  color='#'+''.join(f'{v:02x}' for v in rgb)
  path=Path(tmp)/name
  Image.fromarray(np.where(mask,0,255).astype('uint8')).convert('1').save(str(path)+'.pbm')
  subprocess.run(['potrace',str(path)+'.pbm','--svg','--turdsize','4','--opttolerance','0.15','--output',str(path)+'.svg'],check=True)
  group=ET.parse(str(path)+'.svg').getroot().find(ns+'g');group.set('fill',color)
  for el in group.iter():el.tag=el.tag.replace(ns,'')
  groups.append(ET.tostring(group,encoding='unicode'))
  print(name,color)
svg=f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {im.width} {im.height}" width="{im.width}" height="{im.height}" role="img"><title>Ischys Integrative Mental Wellness</title>'+''.join(groups)+'</svg>\n'
assert '<image' not in svg and '<text' not in svg
(ROOT/'assets/ischys-original-logo-vector.svg').write_text(svg)
