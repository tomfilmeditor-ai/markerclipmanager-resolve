MarkerClipManager — Trình quản lý Đánh dấu Dòng thời gian và Clip cho DaVinci Resolve
=====================================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.6
MIT License — see the script header

NÓ LÀM GÌ
---------
Một cửa sổ duy nhất để xem và quản lý tất cả các đánh dấu trong dòng thời gian Resolve:
cả đánh dấu thước (cấp dòng thời gian) và đánh dấu được đặt trên các clip riêng lẻ,
trên tất cả các bản nhạc video và âm thanh.

Đối với mỗi đánh dấu, nó hiển thị: đồ họa đánh dấu (cùng hình dạng gốc như Resolve),
bản nhạc, TC vào, TC ra, thời lượng, màu, tên, từ khóa, ghi chú.

CÁC TÍNH NĂNG
-------------
- Chọn một hoặc nhiều đánh dấu rồi đổi màu, đổi track (kể cả sang hoặc rời
  thước "TIMELINE"), hoặc xóa
- Sửa Tên, Từ khóa và Ghi chú ngay trong bảng (nhấp đúp), áp dụng cho cả
  nhiều đánh dấu đang được chọn cùng lúc
- Phím Delete làm giống nút Xóa, kèm hộp xác nhận mà bạn có thể tắt
- Hoàn tác và làm lại bằng Cmd+Z / Ctrl+Z, cùng bảng History: nhấp đúp vào một
  bước trước đó để quay thẳng về bước ấy. Chỉ áp dụng cho phiên hiện tại và bị
  xóa khi bạn đóng script
- Lọc theo màu, track, tác giả/tên hoặc từ khóa
- Xuất và nhập đánh dấu dưới dạng CSV
- Nhấp vào một hàng: đầu phát của timeline nhảy tới đánh dấu đó
- Giao diện có 12 ngôn ngữ: khởi động theo ngôn ngữ hệ thống nếu có, nếu không
  thì tiếng Anh, và bạn có thể đổi từ trình đơn ở phía trên cửa sổ (có hiệu lực
  sau khi khởi động lại script)

YÊU CẦU
-------
- DaVinci Resolve 19/20 (macOS)
- Python 3 được cài đặt trên hệ thống
- PySide6 (được cài đặt tự động bởi tập lệnh thiết lập bên dưới — không cần
  các bước thủ công)

CÀI ĐẶT (một lần)
-----------------
1. Tải trình cài đặt dành cho hệ thống của bạn
2. macOS: NHẤP CHUỘT PHẢI vào tệp .command rồi chọn "Mở" — không phải nhấp
   đúp, vì macOS sẽ chặn do tệp không được ký bằng chứng chỉ nhà phát triển
   của Apple
   Windows: nhấp đúp vào tệp .cmd; nếu SmartScreen cảnh báo, chọn "Thông tin
   thêm" rồi "Vẫn chạy"
3. Trình cài đặt sao chép các tệp rồi chuẩn bị môi trường Python mà script cần
   (phần này cần kết nối internet và mất khoảng một phút)
4. Nếu phần thứ hai không thành công — không có kết nối, hoặc thiếu Python —
   các tệp vẫn được cài đặt đúng: mở thư mục đã cài và chạy
   "MarkerClipManager_Setup.command" (macOS) hoặc
   "MarkerClipManager_Setup_Windows.cmd" (Windows) khi thuận tiện
5. Xong. Các bản cập nhật cài theo đúng cách này, đè lên bản trước, và các
   thiết lập của bạn được giữ nguyên

CÁCH SỬ DỤNG
------------
Trong DaVinci Resolve: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(tập lệnh nằm trong thư mục con "MarkerClipManager" bên trong Comp, vì vậy nó xuất hiện
trong menu dưới dạng menu con cùng tên)

CÁC GIỚI HẠN ĐƯỢC BIẾT ĐẾN
--------------------------
- Đánh dấu trong bảng là một biểu tượng được tạo lại được vẽ bởi tập lệnh, không phải
  biểu tượng chính thức của Resolve (không được hiển thị bởi API). Màu sắc là những màu
  chính xác được cung cấp bởi người dùng — chỉ hình dạng biểu tượng vẫn là một
  xấp xỉ
- "Từ khóa" không phải là trường đánh dấu gốc Resolve: nó được lưu trữ trong
  trường đánh dấu nội bộ (customData), vô hình đối với bảng Đánh dấu gốc
  Resolve — chỉ có thể đọc/ghi bởi tập lệnh này
- Timecode đọc fps và chế độ Drop Frame/Non-Drop Frame trực tiếp từ
  dòng thời gian hoạt động của dự án (29.97 và 59.94 DF được xử lý chính xác
  với thuật toán SMPTE tiêu chuẩn); trên fps không chuẩn, toán học vẫn là xấp xỉ
- Nhập/xuất EDL không được xử lý bởi tập lệnh này: sử dụng
  tính năng gốc của Resolve (Timeline > Markers > Export/Import)
- Việc di chuyển đánh dấu sang bản nhạc video/âm thanh yêu cầu một clip phải tồn tại
  tại vị trí đó

HỖ TRỢ
------
Báo cáo lỗi: sử dụng nút 🐛 trong ứng dụng (mở email được điền sẵn tới
tomfilmeditor.tools@gmail.com)
Nếu bạn muốn hỗ trợ phát triển: nút ☕ trong ứng dụng, hoặc
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
