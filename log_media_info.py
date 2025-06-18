from pathlib import Path
from pymediainfo import MediaInfo

def log_media_info(file_path, log_file):
    try:
        media_info = MediaInfo.parse(file_path)
        log_file.write(f"\nThông tin MediaInfo cho file: {file_path}\n")
        for track in media_info.tracks:
            log_file.write(f"- Loại track: {track.track_type}\n")
            for key, value in track.to_data().items():
                log_file.write(f"  + {key}: {value}\n")
    except Exception as e:
        log_file.write(f"MediaInfo error: {e}\n")

def log_all_media_files_in_directory(directory_path="."):
    current_dir = Path(directory_path)
    log_file_path = current_dir / "media_info_log.txt"
    with open(log_file_path, "w", encoding="utf-8") as log_file:
        for file in current_dir.iterdir():
            if file.is_file() and file.suffix.lower() in [".mp4", ".mkv", ".mp3", ".m4a"]:
                log_media_info(file, log_file)
    print(f"Log đã được xuất ra file: {log_file_path}")

if __name__ == "__main__":
    print("Đang đọc thông tin tất cả các file media trong thư mục hiện tại...")
    log_all_media_files_in_directory()
