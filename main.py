main_py = '''import subprocess
import sys
import yt_dlp
from pathlib import Path
from basic_pitch.inference import predict_and_save
from basic_pitch import ICASSP_2022_MODEL_PATH

def download_audio(url: str) -> str:
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
    subprocess.run([
        sys.executable, "-m", "demucs",
        "--two-stems=vocals",
        input_wav
    ], check=True)
    vocals_path = "separated/htdemucs/audio/vocals.wav"
    print(f"✅ ボーカル分離完了: {vocals_path}")
    return vocals_path

def convert_to_midi(vocals_wav: str, output_dir: str = "./output") -> None:
    Path(output_dir).mkdir(exist_ok=True)
    predict_and_save(
        [vocals_wav],
        output_directory=output_dir,
        save_midi=True,
        sonify_midi=False,
        save_model_outputs=False,
        save_notes=False,
        model_or_model_path=ICASSP_2022_MODEL_PATH,  
    )
    print(f"✅ MIDI変換完了: {output_dir} に保存されました")

if __name__ == "__main__":
    #ここにURLを入力してください。
    YOUTUBE_URL = "https://youtu.be/T5846kV8Oy4?si=I_3fq19qCH7M-4Kz"
    wav_file = download_audio(YOUTUBE_URL)
    vocals   = separate_vocals(wav_file)
    convert_to_midi(vocals)
'''

with open("main.py", "w") as f:
    f.write(main_py)

print("✅ main.py を更新しました")
