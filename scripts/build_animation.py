"""Rebuild the original OCR schematic GIF. Optional artwork tool: pip install Pillow."""

from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

ROOT = Path(__file__).resolve().parents[1]
BG, PANEL, TEXT, MUTED, LINE, ACCENT = '#0D1117', '#161B22', '#E6EDF3', '#A0ADBC', '#303D4D', '#39C5CF'


def font(size):
    # Pillow's bundled font keeps this script usable on other systems.
    for name in ['DejaVuSans.ttf', '/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf']:
        try:
            return ImageFont.truetype(name, size)
        except OSError:
            pass
    return ImageFont.load_default(size=size)


def build():
    frames = []
    operations = ['Image.open(image).convert("L")', 'pytesseract.image_to_string(image)',
                  'Extract number, date, vendor, total', 'Save record and append CSV row']
    for frame in range(40):
        image = Image.new('RGB', (600, 260), BG)
        draw = ImageDraw.Draw(image)
        draw.rounded_rectangle((1,1,598,258),radius=14,outline=LINE)
        draw.text((25,20),'Inside the invoice pipeline',font=font(25),fill=TEXT)
        draw.text((25,55),'Source-based illustration / not a screen recording',font=font(15),fill=MUTED)
        active = frame // 10
        for i,label in enumerate(['Image', 'OCR', 'Fields', 'CSV']):
            x = 25+i*144
            draw.rounded_rectangle((x,100,x+116,158),radius=7,fill=PANEL,outline=ACCENT if active==i else LINE,width=2)
            draw.text((x+58,129),label,font=font(21),fill=ACCENT if active==i else TEXT,anchor='mm')
            if i<3:
                draw.line((x+118,129,x+142,129),fill=LINE,width=2)
        packet_x = 83 + frame/39*432
        draw.line((25,181,575,181),fill=LINE,width=1)
        draw.ellipse((packet_x-4,177,packet_x+4,185),fill=ACCENT)
        draw.text((25,207),operations[active],font=font(19),fill=TEXT)
        frames.append(image)
    folder=ROOT/'assets/animations'
    folder.mkdir(parents=True,exist_ok=True)
    frames[0].save(folder/'ocr-pipeline-static.png',optimize=True)
    palette=frames[0].quantize(colors=48)
    frames=[frame.quantize(palette=palette,dither=Image.Dither.NONE) for frame in frames]
    output=folder/'ocr-pipeline.gif'
    frames[0].save(output,save_all=True,append_images=frames[1:],duration=140,loop=0,optimize=True,disposal=1)
    assert output.stat().st_size<250_000, 'Animation should remain lightweight'
    print(f'Generated {output.relative_to(ROOT)} ({output.stat().st_size:,} bytes)')


if __name__=='__main__':
    build()
