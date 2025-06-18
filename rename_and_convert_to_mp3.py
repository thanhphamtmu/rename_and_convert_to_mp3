from pathlib import Path
from pymediainfo import MediaInfo
import datetime
import subprocess
import re
import sys
from tqdm import tqdm

sys.stdout.reconfigure(encoding="utf-8")

def get_encoded_date(file_path):
    try:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "General":
                # Ưu tiên lấy file_creation_date_local trước
                if hasattr(track, 'file_creation_date'):
                    creation_date = track.file_creation_date__local
                    # Convert string "2025-06-12 20:00:52.255" thành datetime
                    return datetime.datetime.strptime(creation_date.split('.')[0], "%Y-%m-%d %H:%M:%S")
                # Nếu không có thì mới lấy encoded_date
                elif track.encoded_date:
                    return datetime.datetime.strptime(track.encoded_date, "%Y-%m-%d %H:%M:%S UTC")
    except Exception as e:
        print(f"MediaInfo error: {e}")
    return None

def convert_to_mp3(input_file: Path, output_file: Path):
    try:
        subprocess.run(
            [
                "ffmpeg",
                "-y",
                "-i",
                str(input_file),
                "-vn",
                "-acodec",
                "libmp3lame",
                "-q:a",
                "2",
                str(output_file),
            ],
            check=True,
            stdout=subprocess.DEVNULL,
            stderr=subprocess.DEVNULL,
        )
    except subprocess.CalledProcessError as e:
        print(f"Lỗi khi chuyển {input_file.name}: {e}")

def process_files():
    print("🔍 Đang kiểm tra và xử lý các file media...")

    current_dir = Path(".")
    media_files = []

    # Tìm tất cả file media
    for ext in ["m4a", "mkv", "mp4", "mp3"]:
        for media_file in current_dir.glob(f"*.{ext}"):
            media_files.append(media_file)

    to_convert = []

    for media_file in media_files:
        try:
            encoded_date = get_encoded_date(media_file)
            if encoded_date:
                date_prefix = encoded_date.strftime("%Y-%m-%d %H-%M-%S")
                current_name = media_file.stem
                current_prefix_match = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}", current_name)

                if current_prefix_match:
                    current_prefix = current_prefix_match.group()
                    if current_prefix != date_prefix:
                        # Lấy phần tên file sau prefix và bỏ khoảng trắng dư
                        base_name = media_file.name[len(current_prefix):].strip()
                        new_name = f"{date_prefix} {base_name}"
                        new_path = media_file.parent / new_name
                        media_file.rename(new_path)
                        print(f"♻️ Đổi tên: {media_file.name} ➜ {new_name}")
                        media_file = new_path
                else:
                    new_name = f"{date_prefix} {media_file.name}"
                    new_path = media_file.parent / new_name
                    media_file.rename(new_path)
                    print(f"🆕 Đổi tên: {media_file.name} ➜ {new_name}")
                    media_file = new_path

                mp3_path = media_file.with_suffix(".mp3")
                if not mp3_path.exists():
                    to_convert.append((media_file, mp3_path))
            else:
                print(f"⚠️ Không tìm thấy encoded_date cho file: {media_file.name}")
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {media_file.name}: {str(e)}")

    print(f"\n🔄 Cần chuyển MP3: {len(to_convert)} file")
    if to_convert:
        with tqdm(to_convert, desc="Đang chuyển đổi") as pbar:
            for src, dest in pbar:
                pbar.set_description(f"Đang xử lý {src.name}")
                convert_to_mp3(src, dest)

    print("✅ Hoàn tất!")

if __name__ == "__main__":
    process_files()
