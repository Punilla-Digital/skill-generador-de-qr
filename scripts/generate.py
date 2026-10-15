#!/usr/bin/env python3
"""Generate and decode final raster/vector QR variants before publishing the bundle."""
import argparse, base64, io, json, re, zipfile
from pathlib import Path
import qrcode, cairosvg, zxingcpp
from PIL import Image, ImageDraw, ImageOps

ASSETS=Path(__file__).resolve().parents[1]/'assets'

def verify(im, expected):
    rgb=im.convert('RGB')
    for candidate in (rgb,ImageOps.invert(rgb)):
        if any(r.text==expected for r in zxingcpp.read_barcodes(candidate)):
            return True
    return False

def generate(url, out, logo_path=None, colors=(), scale=24, logo_mode="with"):
    if logo_mode not in ("with", "without", "both"):
        raise ValueError("Modo de logo inválido")
    if not url or scale<8 or scale>64:
        raise ValueError('Contenido vacío o escala fuera de 8–64')
    out=Path(out)
    if out.exists() and any(out.iterdir()):
        raise ValueError('Usar una carpeta de salida nueva o vacía')
    out.mkdir(parents=True,exist_ok=True)
    logo=None
    if logo_mode != "without" and logo_path:
        logo=Image.open(logo_path).convert('RGBA')
    elif logo_mode != "without":
        logo=Image.open(io.BytesIO(cairosvg.svg2png(url=str(ASSETS/'logo-qr.svg')))).convert('RGBA')
    qr=qrcode.QRCode(error_correction=qrcode.constants.ERROR_CORRECT_H,border=4)
    qr.add_data(url); qr.make(fit=True)
    matrix=qr.get_matrix(); n=len(matrix); size=n*scale
    variants=[('negro','#000000','#FFFFFF'),('blanco','#FFFFFF','#000000')]
    for i,color in enumerate(colors,1):
        if not re.fullmatch(r'#[0-9a-fA-F]{6}',color):
            raise ValueError('Color debe ser HEX #RRGGBB')
        variants.append((f'color-{i}',color,'#FFFFFF'))
    verified=[]; previews=[]
    modes = (True, False) if logo_mode == "both" else (logo_mode == "with",)
    variants = [(f"{name}-con-logo" if use_logo else f"{name}-sin-logo", fg, bg, use_logo) for use_logo in modes for name,fg,bg in variants]
    for name,fg,bg,use_logo in variants:
        for ratio in ((.15,.12,.09) if use_logo else (0,)):
            im=Image.new('RGB',(size,size),bg); draw=ImageDraw.Draw(im)
            rects=[]
            for y,row in enumerate(matrix):
                for x,value in enumerate(row):
                    if value:
                        draw.rectangle((x*scale,y*scale,(x+1)*scale-1,(y+1)*scale-1),fill=fg)
                        rects.append(f'<rect x="{x*scale}" y="{y*scale}" width="{scale}" height="{scale}"/>')
            logo_svg=""
            if use_logo:
                width=int((n-8)*scale*ratio); pad=max(scale//2,4)
                mark=logo.copy(); mark.thumbnail((width,width))
                plate=Image.new('RGBA',(width+2*pad,width+2*pad),'white')
                plate.alpha_composite(mark,((plate.width-mark.width)//2,(plate.height-mark.height)//2))
                offset=(size-plate.width)//2
                im.paste(plate,(offset,offset),plate)
                buf=io.BytesIO(); plate.save(buf,format='PNG')
                encoded=base64.b64encode(buf.getvalue()).decode()
                logo_svg=f'<image x="{offset}" y="{offset}" width="{plate.width}" height="{plate.height}" href="data:image/png;base64,{encoded}"/>'
            svg=f'<svg xmlns="http://www.w3.org/2000/svg" width="{size}" height="{size}" viewBox="0 0 {size} {size}"><rect width="{size}" height="{size}" fill="{bg}"/><g fill="{fg}">{"".join(rects)}</g>{logo_svg}</svg>'
            raster=Image.open(io.BytesIO(cairosvg.svg2png(bytestring=svg.encode())))
            if verify(im,url) and verify(raster,url):
                im.save(out/f'qr-{name}.png'); (out/f'qr-{name}.svg').write_text(svg)
                previews.append((name,im.copy()))
                verified.append({'variant':name,'png_decoded':True,'svg_raster_decoded':True,'logo_ratio':ratio,'with_logo':use_logo})
                break
        else:
            for path in out.glob('*'): path.unlink()
            raise ValueError(f'No se pudo validar {name}; cambiar color/logo o tamaño. Sin entrega.')
    cols=min(3,len(previews)); rows=(len(previews)+cols-1)//cols
    preview=Image.new('RGB',(cols*420,rows*470),'#e9e9ed'); d=ImageDraw.Draw(preview)
    for i,(name,im) in enumerate(previews):
        im.thumbnail((380,380),Image.Resampling.NEAREST)
        x=(i%cols)*420; y=(i//cols)*470
        preview.paste(im,(x+(420-im.width)//2,y+20)); d.text((x+20,y+420),name,fill='black')
    preview.save(out/'preview.png')
    (out/'validation.json').write_text(json.dumps({'content':url,'results':verified,'note':'Inverted QR compatibility varies; test physical output.'},ensure_ascii=False,indent=2))
    files=sorted(out.iterdir())
    with zipfile.ZipFile(out/'qr-completo.zip','w',zipfile.ZIP_DEFLATED) as z:
        for f in files: z.write(f,f.name)
    return verified

if __name__=='__main__':
    p=argparse.ArgumentParser(); p.add_argument('--url',required=True); p.add_argument('--out',required=True)
    p.add_argument('--logo'); p.add_argument('--color',action='append',default=[]); p.add_argument('--scale',type=int,default=24)
    p.add_argument('--logo-mode',choices=['with','without','both'],default='with')
    a=p.parse_args(); print(json.dumps(generate(a.url,a.out,a.logo,a.color,a.scale,a.logo_mode),ensure_ascii=False))
