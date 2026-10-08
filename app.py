from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os
import time

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("Chưa tìm thấy GEMINI_API_KEY")

client = genai.Client(api_key=API_KEY)
app = Flask(__name__)


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/chat", methods=["POST"])
def chat():
    data = request.get_json()
    messages = data.get("messages", [])

    if not messages:
        return jsonify({
            "error": "Chưa có nội dung tin nhắn."
        }), 400

    # Lấy tối đa 30 tin nhắn gần nhất
    conversation = []

    for message in messages[-30:]:
        role = message.get("role", "user")
        content = message.get("content", "")

        if content:
            speaker = "Người dùng" if role == "user" else "Trợ lý AI"
            conversation.append(
                f"{speaker}: {content}"
            )

    prompt = """Bạn là một trợ lý AI thân thiện.

Hãy trả lời bằng tiếng Việt nếu người dùng hỏi bằng tiếng Việt.
Trả lời rõ ràng, tự nhiên, dễ hiểu và hữu ích.
Có thể xuống dòng khi cần.
Hãy nhớ ngữ cảnh của cuộc trò chuyện.

Lịch sử cuộc trò chuyện:
""" + "\n".join(conversation) + """

Trợ lý AI:"""

    # Thử tối đa 3 lần nếu Gemini đang quá tải
    for attempt in range(3):
        try:
            response = client.models.generate_content(
                model="gemini-3.8-flash",
                contents=prompt
            )

            if response.text:
                return jsonify({
                    "reply": response.text
                })

            return jsonify({
                "error": "AI không trả về nội dung."
            }), 500

        except Exception as e:
            error_text = str(e)

            # Nếu Gemini báo 503 / quá tải
            if "503" in error_text or "UNAVAILABLE" in error_text:

                if attempt < 2:
                    time.sleep(2)
                    continue

                return jsonify({
                    "error": "Gemini đang quá tải. Vui lòng thử lại sau vài giây."
                }), 503

            # Các lỗi khác
            return jsonify({
                "error": error_text
            }), 500

    return jsonify({
        "error": "Không thể kết nối với AI."
    }), 500


if __name__ == "__main__":
    print("🤖 AI Chatbot đang chạy tại http://127.0.0.1:5000")
    app.run(host="0.0.0.0", port=5000, debug=True)
