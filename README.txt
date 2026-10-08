AI CHATBOT - HƯỚNG DẪN CHẠY

1. Cài Python 3.14 hoặc phiên bản mới.
2. Mở CMD trong thư mục dự án.
3. Cài thư viện:
   python -m pip install -r requirements.txt

4. Tạo file tên ".env" trong thư mục chính.
5. Dán dòng sau vào .env:
   GEMINI_API_KEY=API_KEY_CUA_BAN

   Thay API_KEY_CUA_BAN bằng API key Gemini của bạn.
   KHÔNG chia sẻ file .env.

6. Chạy:
   python app.py

7. Mở trình duyệt:
   http://127.0.0.1:5000

CHỨC NĂNG:
- Chat với AI online.
- AI nhận lịch sử hội thoại để hiểu ngữ cảnh.
- Enter để gửi.
- Shift + Enter để xuống dòng.
- Nút "Cuộc trò chuyện mới" để xóa lịch sử hiện tại.
- Giao diện responsive.

LƯU Ý:
API key không được đưa lên GitHub hoặc gửi cho người khác.
