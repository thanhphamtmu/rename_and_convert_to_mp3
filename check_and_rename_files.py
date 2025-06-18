from pathlib import Path
from pymediainfo import MediaInfo
import datetime
import os
import sys
import re

sys.stdout.reconfigure(encoding="utf-8")

def get_encoded_date(file_path):
    try:
        media_info = MediaInfo.parse(file_path)
        for track in media_info.tracks:
            if track.track_type == "General":
                # Ưu tiên dùng encoded_date trước
                if track.encoded_date:
                    return datetime.datetime.strptime(track.encoded_date, "%Y-%m-%d %H:%M:%S UTC")
                # Rồi mới dùng file_creation_date nếu không có encoded_date
                elif hasattr(track, 'file_creation_date'):
                    creation_date = track.file_creation_date__local
                    return datetime.datetime.strptime(creation_date.split('.')[0], "%Y-%m-%d %H:%M:%S")
    except Exception as e:
        print(f"MediaInfo error: {e}")
    return None

def check_and_rename_files():
    print("🔍 Đang kiểm tra các file...")

    current_dir = Path(".")
    media_files = []

    # Tìm tất cả file media
    for ext in ["m4a", "mkv", "mp4", "mp3"]:
        for media_file in current_dir.glob(f"*.{ext}"):
            media_files.append(media_file)

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
                        # Lấy phần tên file sau prefix
                        base_name = media_file.name[len(current_prefix):].strip()
                        # Tạo tên mới với prefix đúng
                        new_name = f"{date_prefix} {base_name}"
                        media_file.rename(media_file.parent / new_name)
                        print(f"✅ Đã đổi tên: {media_file.name} -> {new_name}")

                        # Đổi tên các file cùng tên nhưng định dạng khác
                        for other_file in current_dir.glob(f"{current_name}.*"):
                            if other_file != media_file:
                                other_new_name = f"{date_prefix} {other_file.name}"
                                other_file.rename(other_file.parent / other_new_name)
                                print(f"✅ Đã đổi tên file liên quan: {other_file.name} -> {other_new_name}")
                    else:
                        print(f"ℹ️ File đã có tiền tố đúng: {media_file.name}")
                else:
                    new_name = f"{date_prefix} {media_file.name}"
                    media_file.rename(media_file.parent / new_name)
                    print(f"✅ Đã đổi tên: {media_file.name} -> {new_name}")
            else:
                print(f"⚠️ Không tìm thấy encoded_date cho file: {media_file.name}")
        except Exception as e:
            print(f"❌ Lỗi khi xử lý {media_file.name}: {str(e)}")

if __name__ == "__main__":
    print("Đang kiểm tra và đổi tên các file media trong thư mục hiện tại...")
    check_and_rename_files()
