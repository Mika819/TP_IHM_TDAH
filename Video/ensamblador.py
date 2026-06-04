from pathlib import Path
import textwrap

import numpy as np
from moviepy.editor import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoFileClip,
    concatenate_videoclips,
)

try:
    from PIL import Image, ImageDraw, ImageFont
except ImportError:
    Image = ImageDraw = ImageFont = None

BASE_DIR = Path(__file__).resolve().parent
ASSETS_DIR = BASE_DIR / "assets"
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

def crear_texto(mensaje, duracion):
    try:
        return TextClip(
            mensaje,
            fontsize=60,
            color="white",
            font="Arial-Bold",
            method="caption",
            size=(720, None),
            bg_color="black",
        ).set_duration(duracion).set_position(("center", "bottom"))
    except Exception:
        if Image is None:
            raise RuntimeError(
                "No se pudo crear el texto. Instala ImageMagick o Pillow: pip install Pillow"
            )

        lines = textwrap.wrap(mensaje, width=26)
        font = None
        if ImageFont is not None:
            for font_name in ["arial.ttf", "Arial.ttf", "DejaVuSans-Bold.ttf"]:
                try:
                    font = ImageFont.truetype(font_name, 60)
                    break
                except OSError:
                    continue
            if font is None:
                font = ImageFont.load_default()
        else:
            raise RuntimeError("Pillow no está disponible para generar texto.")

        padding = 20
        spacing = 10
        dummy = Image.new("RGB", (1, 1), color="black")
        draw = ImageDraw.Draw(dummy)
        max_width = 0
        total_height = 0
        line_sizes = []
        for line in lines:
            bbox = draw.textbbox((0, 0), line, font=font)
            width = bbox[2] - bbox[0]
            height = bbox[3] - bbox[1]
            max_width = max(max_width, width)
            line_sizes.append((width, height))
            total_height += height + spacing
        total_height -= spacing

        image_width = max(720, max_width + padding * 2)
        image_height = total_height + padding * 2
        img = Image.new("RGB", (image_width, image_height), color="black")
        draw = ImageDraw.Draw(img)

        y = padding
        for line, (width, height) in zip(lines, line_sizes):
            x = (image_width - width) // 2
            draw.text((x, y), line, font=font, fill="white")
            y += height + spacing

        return ImageClip(np.asarray(img)).set_duration(duracion).set_position(("center", "bottom"))


def ensamblar_video():
    clip1 = VideoFileClip(str(ASSETS_DIR / "escena1.mp4")).set_duration(4)
    clip2 = VideoFileClip(str(ASSETS_DIR / "escena2.mp4")).set_duration(4)
    clip3 = VideoFileClip(str(ASSETS_DIR / "escena3.mp4")).set_duration(4)

    audio1 = AudioFileClip(str(OUTPUTS_DIR / "audio1.mp3"))
    audio2 = AudioFileClip(str(OUTPUTS_DIR / "audio2.mp3"))
    audio3 = AudioFileClip(str(OUTPUTS_DIR / "audio3.mp3"))

    clip1 = clip1.set_audio(audio1)
    clip2 = clip2.set_audio(audio2)
    clip3 = clip3.set_audio(audio3)

    txt1 = crear_texto("¿No encontrás nada cuando más lo necesitás?", 4)
    txt2 = crear_texto("Organizá todo en un solo lugar.", 4)
    txt3 = crear_texto("Menos caos. Más estudio.", 4)

    video1 = CompositeVideoClip([clip1, txt1])
    video2 = CompositeVideoClip([clip2, txt2])
    video3 = CompositeVideoClip([clip3, txt3])

    video_final = concatenate_videoclips([video1, video2, video3])

    salida = OUTPUTS_DIR / "video_final_IHM.mp4"
    video_final.write_videofile(str(salida), fps=24, codec="libx264")
    print(f"Exportado: {salida}")

if __name__ == "__main__":
    ensamblar_video()
