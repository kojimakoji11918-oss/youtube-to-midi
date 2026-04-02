import subprocess
import sys
import yt_dlp
from pathlib import Path
from basic_pitch.inference import predict_and_save

def download_audio(url: str) -> str:
    """YouTubeから音声をWAVでダウンロード"""
    ydl_opts = {
        'format': 'bestaudio/best',
        'outtmpl': 'audio.%(ext)s',
        'postprocessors': [{
            'key': 'FFmpegExtractAudio',
            'preferredcodec': 'wav',
        }],
    }
    with yt_dlp.YoutubeDL(ydl_opts) as ydl:
        ydl.download([url])
    print("✅ 音声ダウンロード完了")
    return "audio.wav"

def separate_vocals(input_wav: str) -> str:
    """demucsでボーカル（主旋律）を分離"""
    subprocess.run([
        sys.executable, "-m", "demucs",
        "--two-stems=vocals",
        input_wav
    ], check=True)
    vocals_path = "separated/htdemucs/audio/vocals.wav"
    print(f"✅ ボーカル分離完了: {vocals_path}")
    return vocals_path

def convert_to_midi(vocals_wav: str, output_dir: str = "./output") -> None:
    """basic-pitchでMIDIに変換"""
    Path(output_dir).mkdir(exist_ok=True)
    predict_and_save(
        [vocals_wav],
        output_directory=output_dir,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
    )
    print(f"✅ MIDI変換完了: {output_dir} に保存されました")

if __name__ == "__main__":
    # ★ここにYouTubeのURLを入力★
    YOUTUBE_URL = "https://www.youtube.com/watch?v=T5846kV8Oy4&list=RDT5846kV8Oy4&start_radio=1"

    wav_file = download_audio(YOUTUBE_URL)
    vocals   = separate_vocals(wav_file)
    convert_to_midi(vocals)
