from pathlib import Path
import asyncio

try:
    import edge_tts
except ImportError as exc:
    raise ImportError("edge_tts no está instalado. Instala con: pip install edge-tts") from exc

BASE_DIR = Path(__file__).resolve().parent
OUTPUTS_DIR = BASE_DIR / "outputs"
OUTPUTS_DIR.mkdir(parents=True, exist_ok=True)

async def amain():
    textos = [
        ("¿No encontrás nada cuando más lo necesitás?", "audio1.mp3"),
        ("Organizá todo en un solo lugar.", "audio2.mp3"),
        ("Menos caos. Más estudio.", "audio3.mp3")
    ]
    
    voice = "es-AR-ElenaNeural"
    
    for texto, nombre in textos:
        archivo_salida = OUTPUTS_DIR / nombre
        communicate = edge_tts.Communicate(texto, voice)
        await communicate.save(str(archivo_salida))
        print(f"Generado: {archivo_salida}")

if __name__ == "__main__":
    asyncio.run(amain())
