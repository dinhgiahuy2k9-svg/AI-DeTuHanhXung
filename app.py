from flask import Flask, render_template, request, jsonify
from google import genai
from dotenv import load_dotenv
import os

load_dotenv()

API_KEY = os.getenv("GEMINI_API_KEY")

if not API_KEY:
    raise RuntimeError("Chưa tìm thấy GEMINI_API_KEY trong file .env")

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
        return jsonify({"error": "Chưa có nội dung tin nhắn."}), 400

    # Gửi toàn bộ lịch sử hội thoại để AI có thể nhớ ngữ cảnh.
    conversation = []
    for message in messages[-30:]:
        role = message.get("role", "user")
        content = message.get("content", "")
        if content:
            speaker = "Người dùng" if role == "user" else "Trợ lý AI"
            conversation.append(f"{speaker}: {content}")

    prompt = """Bạn là một trợ lý AI thân thiện. Hãy trả lời bằng tiếng Việt nếu người dùng hỏi bằng tiếng Việt.
Trả lời rõ ràng, tự nhiên và hữu ích. Bạn có thể dùng xuống dòng khi cần.

Lịch sử cuộc trò chuyện:
""" + "\n".join(conversation) + "\n\nTrợ lý AI:"

    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return jsonify({"reply": response.text})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    print("🤖 AI Chatbot đang chạy tại http://127.0.0.1:5000")
    app.run(debug=True)
