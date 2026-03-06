"""
Dibuat oleh : Darmawan Wicaksono
Kontak email: d.wicaksono@gmail.com

Video ke Text dengan OpenAI Whisper
====================================
Cara penggunaan:
  pip install openai-whisper moviepy
  python video_to_text.py --video video_saya.mp4

Atau dengan API OpenAI:
  pip install openai moviepy
  python video_to_text.py --video video_saya.mp4 --use-api --api-key sk-xxxxx
"""

import argparse
import os
import sys
import time


# ──────────────────────────────────────────────
# OPSI 1 – Whisper Lokal (gratis, offline)
# ──────────────────────────────────────────────
def transkripsi_lokal(video_path: str, model_size: str = "base", bahasa: str = None) -> dict:
    """
    Transkripsi menggunakan Whisper yang dijalankan secara lokal.

    model_size: tiny | base | small | medium | large
                (semakin besar = lebih akurat, tapi lebih lambat & butuh lebih banyak RAM)
    bahasa    : kode ISO 639-1, misal 'id' (Indonesia), 'en' (Inggris).
                None = deteksi otomatis.
    """
    try:
        import whisper
    except ImportError:
        sys.exit("❌  Whisper belum terpasang. Jalankan: pip install openai-whisper")

    # 1. Ekstrak audio dari video
    print(f"🎬  Membaca video: {video_path}")
    audio_path = _ekstrak_audio(video_path)

    # 2. Muat model Whisper
    print(f"🤖  Memuat model Whisper '{model_size}' …")
    model = whisper.load_model(model_size)

    # 3. Transkripsi
    print("✍️   Sedang mentranskripsi …")
    opsi = {}
    if bahasa:
        opsi["language"] = bahasa

    hasil = model.transcribe(audio_path, **opsi)

    # 4. Bersihkan file audio sementara
    os.remove(audio_path)

    return hasil


# ──────────────────────────────────────────────
# OPSI 2 – API OpenAI (perlu API key, berbayar)
# ──────────────────────────────────────────────
def transkripsi_api(video_path: str, api_key: str, bahasa: str = None) -> dict:
    """
    Transkripsi menggunakan endpoint Whisper di OpenAI API.
    Batas ukuran file: 25 MB.
    """
    try:
        from openai import OpenAI
    except ImportError:
        sys.exit("❌  openai belum terpasang. Jalankan: pip install openai")

    audio_path = _ekstrak_audio(video_path)

    print("🌐  Mengirim audio ke OpenAI API …")
    client = OpenAI(api_key=api_key)

    with open(audio_path, "rb") as f:
        params = {"model": "whisper-1", "file": f, "response_format": "verbose_json"}
        if bahasa:
            params["language"] = bahasa
        transkrip = client.audio.transcriptions.create(**params)

    os.remove(audio_path)

    # Samakan format dengan output Whisper lokal
    return {
        "text": transkrip.text,
        "language": getattr(transkrip, "language", "unknown"),
        "segments": getattr(transkrip, "segments", []),
    }


# ──────────────────────────────────────────────
# Fungsi Pembantu
# ──────────────────────────────────────────────
def _ekstrak_audio(video_path: str) -> str:
    """Ekstrak trek audio dari file video dan simpan sebagai .wav sementara."""
    # Support moviepy v1.x dan v2.x
    try:
        from moviepy.video.io.VideoFileClip import VideoFileClip
    except ImportError:
        try:
            from moviepy.editor import VideoFileClip
        except ImportError:
            sys.exit("❌  moviepy belum terpasang. Jalankan: pip install moviepy")

    audio_path = os.path.splitext(video_path)[0] + "_audio_temp.wav"
    print(f"🔊  Mengekstrak audio → {audio_path}")
    klip = VideoFileClip(video_path)
    klip.audio.write_audiofile(audio_path, logger=None)
    klip.close()
    return audio_path


def simpan_hasil(hasil: dict, output_path: str):
    """Simpan teks transkripsi dan, jika tersedia, stempel waktu per segmen."""
    # Teks biasa
    with open(output_path, "w", encoding="utf-8") as f:
        f.write(hasil["text"])
    print(f"✅  Transkripsi disimpan → {output_path}")

    # Stempel waktu (SRT-style sederhana)
    segmen = hasil.get("segments", [])
    if segmen:
        srt_path = os.path.splitext(output_path)[0] + ".srt"
        with open(srt_path, "w", encoding="utf-8") as f:
            for i, seg in enumerate(segmen, 1):
                mulai = _detik_ke_srt(seg["start"])
                akhir = _detik_ke_srt(seg["end"])
                f.write(f"{i}\n{mulai} --> {akhir}\n{seg['text'].strip()}\n\n")
        print(f"📄  File subtitle SRT disimpan → {srt_path}")


def _detik_ke_srt(detik: float) -> str:
    jam = int(detik // 3600)
    menit = int((detik % 3600) // 60)
    dtk = int(detik % 60)
    ms = int((detik - int(detik)) * 1000)
    return f"{jam:02d}:{menit:02d}:{dtk:02d},{ms:03d}"


def cetak_ringkasan(hasil: dict):
    print("\n" + "=" * 60)
    print("📋  HASIL TRANSKRIPSI")
    print("=" * 60)
    print(f"🌐  Bahasa terdeteksi : {hasil.get('language', '-')}")
    print(f"📝  Jumlah kata       : {len(hasil['text'].split())}")
    print(f"⏱️   Jumlah segmen    : {len(hasil.get('segments', []))}")
    print("\n--- Teks ---\n")
    print(hasil["text"])
    print("=" * 60)


# ──────────────────────────────────────────────
# Entry Point CLI
# ──────────────────────────────────────────────
def main():
    parser = argparse.ArgumentParser(
        description="Transkripsi video ke teks menggunakan OpenAI Whisper"
    )
    parser.add_argument("--video", required=True, help="Path ke file video (mp4, mkv, avi, …)")
    parser.add_argument(
        "--model",
        default="base",
        choices=["tiny", "base", "small", "medium", "large"],
        help="Ukuran model Whisper lokal (default: base)",
    )
    parser.add_argument(
        "--bahasa",
        default=None,
        help="Kode bahasa ISO 639-1, misal 'id' atau 'en' (default: deteksi otomatis)",
    )
    parser.add_argument("--output", default=None, help="Path file output .txt (opsional)")
    parser.add_argument(
        "--use-api", action="store_true", help="Gunakan OpenAI API alih-alih model lokal"
    )
    parser.add_argument("--api-key", default=None, help="OpenAI API key (wajib jika --use-api)")
    args = parser.parse_args()

    if not os.path.isfile(args.video):
        sys.exit(f"❌  File tidak ditemukan: {args.video}")

    mulai = time.time()

    if args.use_api:
        api_key = args.api_key or os.environ.get("OPENAI_API_KEY")
        if not api_key:
            sys.exit("❌  API key diperlukan. Gunakan --api-key atau set env OPENAI_API_KEY")
        hasil = transkripsi_api(args.video, api_key, args.bahasa)
    else:
        hasil = transkripsi_lokal(args.video, args.model, args.bahasa)

    cetak_ringkasan(hasil)

    # Tentukan path output
    output = args.output or os.path.splitext(args.video)[0] + "_transkripsi.txt"
    simpan_hasil(hasil, output)

    print(f"\n⏱️   Selesai dalam {time.time() - mulai:.1f} detik")


if __name__ == "__main__":
    main()
