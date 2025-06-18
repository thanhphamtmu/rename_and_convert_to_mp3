# 🛠️ Media Renamer & MP3 Converter

Một bộ công cụ Python giúp tự động đổi tên và chuyển đổi định dạng file media một cách chính xác và hiệu quả.

## 🎯 Tính năng chính

1. **Tự động đổi tên file `.m4a`, `.mkv`, `.mp4`, `.mp3`** dựa trên thời gian tạo (metadata) theo định dạng `YYYY-MM-DD HH-MM-SS`.
2. **Đồng bộ tiền tố (prefix) cho tất cả các file liên quan**, đảm bảo thống nhất tên file giữa các định dạng.
3. **Chuyển đổi file âm thanh/video sang `.mp3`** sử dụng `ffmpeg`, ưu tiên sử dụng `libmp3lame` chất lượng cao.

## 🧱 Cấu trúc thư mục

```
├── check_and_rename_files.py      # Kiểm tra và đổi tên file media
├── rename_and_convert_to_mp3.py   # Đổi tên và chuyển đổi sang MP3
├── log_media_info.py              # Ghi log thông tin metadata các file
├── requirements.txt               # Thư viện phụ thuộc
└── README.md                      # Tài liệu hướng dẫn
```

## 🔧 Yêu cầu hệ thống

- Python 3.7 trở lên
- `ffmpeg` đã cài sẵn trong hệ điều hành
- Các thư viện trong `requirements.txt`

## 🚀 Cài đặt

```bash
pip install -r requirements.txt
```

## ▶️ Sử dụng

### 1. Đổi tên file media
```bash
python check_and_rename_files.py
```

### 2. Đổi tên + chuyển đổi sang MP3
```bash
python rename_and_convert_to_mp3.py
```

### 3. Ghi log metadata của file media
```bash
python log_media_info.py
```

## 📦 Định dạng hỗ trợ

- Đầu vào: `.m4a`, `.mkv`, `.mp4`, `.mp3`
- Đầu ra: `.mp3`

## 📝 Ghi chú

- Nếu file không có metadata `encoded_date` hoặc `file_creation_date`, chương trình sẽ bỏ qua và ghi chú cảnh báo.
- Các file đã có prefix hợp lệ sẽ không bị đổi tên.

## © Bản quyền

Tác giả: [@thanhphamtmu](https://github.com/thanhphamtmu)  
License: MIT
