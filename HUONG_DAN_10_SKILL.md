# Autoskill Hominhtuan95 — 10 Skill, HWID, F1 theo cửa sổ

## Tính năng
- Tab, Space và 10 Skill (1,2,3,4,5,6,7,8,9,0).
- Mỗi phím có bật/tắt và chu kỳ 50–180000 ms.
- Chọn cửa sổ Chiến Quốc theo HWND; mỗi EXE mở là một phiên Auto độc lập.
- **F1 chỉ bật/tắt phiên AutoSkill đang có focus**. Bấm vào cửa sổ Auto cần điều khiển trước rồi bấm F1. Khi focus ở cửa sổ game, F1 không điều khiển Auto.
- Kích hoạt HWID qua chữ ký số Ed25519, lưu license tại `%LOCALAPPDATA%\\AutoskillHominhtuan95\\license.txt`; các phiên Auto trên cùng tài khoản Windows dùng chung license.

## 1. Tạo khóa quản trị trên máy Windows
1. Giải nén toàn bộ file ZIP.
2. Cài Python 3.11+ (đánh dấu Add Python to PATH nếu có).
3. Mở CMD tại thư mục đã giải nén và chạy:
   ```bat
   py -m pip install cryptography
   py setup_license.py
   ```
4. Lệnh tạo `PRIVATE_LICENSE_KEY.pem` và tự ghi public key vào `Autoskill_Hominhtuan95.py`.
5. **Giữ PRIVATE_LICENSE_KEY.pem chỉ trên máy quản trị, không đưa lên GitHub hoặc gửi cho khách.** Sao lưu riêng an toàn. Nếu mất private key sẽ không thể cấp mã mới cho public key cũ.

## 2. Đẩy lên GitHub và build
- Tải lên repository: `Autoskill_Hominhtuan95.py`, `issue_license.py` (tùy chọn, không chứa private key), `setup_license.py` (tùy chọn).
- Tạo `.github/workflows/build.yml` với nội dung của `build.yml` trong ZIP.
- Không upload `PRIVATE_LICENSE_KEY.pem`, `license.txt`, hoặc thư mục `__pycache__`.
- Vào Actions → Build Autoskill Hominhtuan95 EXE → Run workflow.
- Tải EXE ở Artifacts sau khi build thành công.

## 3. Cấp mã HWID
- Người dùng mở EXE, sao chép HWID trong cửa sổ kích hoạt và gửi cho người quản trị.
- Trên máy quản trị, trong cùng thư mục có `PRIVATE_LICENSE_KEY.pem`, chạy:
  ```bat
  py issue_license.py MA_HWID_CUA_NGUOI_DUNG
  ```
- Sao chép toàn bộ dòng license được in ra và gửi cho người dùng.
- Người dùng dán license, bấm Kích hoạt. Các lần sau sẽ tự xác minh license đã lưu.

## 4. Mở nhiều Auto
- Chạy EXE nhiều lần, mỗi cửa sổ Auto chọn một HWND khác nhau.
- Bấm vào cửa sổ Auto muốn điều khiển rồi bấm F1; chỉ cửa sổ Auto đang có focus nhận F1.
- Mỗi Auto có bộ thời gian và nút Chạy/Dừng riêng.

## Lưu ý
- Đây là mã nguồn đã kiểm tra cú pháp, chưa kiểm thử thực tế với game Chiến Quốc trên Windows.
- Gửi phím nền bằng `PostMessageW` có thể không hoạt động nếu game dùng DirectInput/raw input hoặc có giới hạn bảo vệ.
- HWID ở đây dựa trên MachineGuid Windows (băm SHA-256); có thể thay đổi sau cài lại Windows và không phải định danh phần cứng tuyệt đối.
- Không có giới hạn số phiên Auto trên cùng máy.
