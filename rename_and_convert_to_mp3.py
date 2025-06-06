import os
import re
import subprocess
import sys
from datetime import datetime
from pathlib import Path

import ffmpeg
import win32com.client
from mutagen import File
from tqdm import tqdm


def is_date_prefixed(filename):
    return bool(re.match(r"^\d{4}-\d{2}-\d{2}", filename))


def get_file_creation_time(file_path):
    try:
        meta = ffmpeg.probe(str(file_path))
        if "format" in meta and "tags" in meta["format"]:
            tags = meta["format"]["tags"]
            if "creation_time" in tags:
                return datetime.strptime(tags["creation_time"], "%Y-%m-%dT%H:%M:%S.%fZ")
        for stream in meta.get("streams", []):
            tags = stream.get("tags", {})
            for tag in ["creation_time", "date", "date_time"]:
                if tag in tags:
                    try:
                        return datetime.strptime(tags[tag], "%Y-%m-%dT%H:%M:%S.%fZ")
                    except ValueError:
                        continue
    except Exception:
        pass

    try:
        audio = File(str(file_path))
        if audio is not None:
            for key in ["date", "TDRC", "TYER", "TDAT"]:
                if key in audio:
                    date_str = str(audio[key][0])
                    try:
                        return datetime.strptime(date_str, "%Y-%m-%d")
                    except ValueError:
                        try:
                            return datetime.strptime(date_str, "%Y")
                        except ValueError:
                            continue
    except Exception:
        pass

    try:
        shell = win32com.client.Dispatch("Shell.Application")
        folder = shell.NameSpace(str(file_path.parent))
        item = folder.ParseName(file_path.name)
        for i in range(500):
            column_name = folder.GetDetailsOf(None, i)
            if "media created" in column_name.lower():
                value = folder.GetDetailsOf(item, i)
                match = re.search(r"(\d{2}/\d{2}/\d{4}\s+\d{2}:\d{2})", value)
                if match:
                    return datetime.strptime(match.group(1), "%d/%m/%Y %H:%M")
                break
    except Exception:
        pass

    stats = os.stat(file_path)
    return datetime.fromtimestamp(min(stats.st_ctime, stats.st_mtime))


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


def process_files(folder_path: str):
    input_dir = Path(folder_path)
    allowed_exts = (".m4a", ".mkv")

    files = [f for f in input_dir.iterdir() if f.suffix.lower() in allowed_exts and f.is_file()]
    print(f"🔍 Tổng cộng {len(files)} file cần xử lý")

    to_convert = []

    for file in files:
        creation_time = get_file_creation_time(file)
        prefix = creation_time.strftime("%Y-%m-%d %H-%M-%S")
        base_name = file.name
        current_prefix_match = re.match(r"^\d{4}-\d{2}-\d{2} \d{2}-\d{2}-\d{2}", base_name)

        if current_prefix_match:
            current_prefix = current_prefix_match.group()
            if current_prefix != prefix:
                new_name = prefix + base_name[len(current_prefix):]
                new_path = file.with_name(new_name)
                mp3_old = file.with_suffix(".mp3")
                mp3_new = new_path.with_suffix(".mp3")
                file.rename(new_path)
                if mp3_old.exists():
                    mp3_old.rename(mp3_new)
                print(f"♻️ Đổi tên: {file.name} ➜ {new_name}")
                file = new_path
        else:
            new_name = f"{prefix} {base_name}"
            new_path = file.with_name(new_name)
            file.rename(new_path)
            print(f"🆕 Đổi tên: {file.name} ➜ {new_name}")
            file = new_path

        mp3_path = file.with_suffix(".mp3")
        if not mp3_path.exists():
            to_convert.append((file, mp3_path))

    print(f"\n🔄 Cần chuyển MP3: {len(to_convert)} file")
    if to_convert:
        with tqdm(to_convert, desc="Đang chuyển đổi") as pbar:
            for src, dest in pbar:
                pbar.set_description(f"Đang xử lý {src.name}")
                convert_to_mp3(src, dest)

    print("✅ Hoàn tất!")


if __name__ == "__main__":
    sys.stdout.reconfigure(encoding="utf-8")
    folder = str(Path.cwd())
    process_files(folder)
