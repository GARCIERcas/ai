from flask import Flask, render_template, request, jsonify
import requests

# Указываем Flask искать шаблоны в корневой директории
app = Flask(__name__, template_folder='.')

API_KEY = "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"
MODEL = "qwen/qwen3-next-80b-a3b-instruct:free"

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/ask', methods=['POST'])
def ask():
    user_data = request.json
    user_input = user_data.get("message")
    
    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }
    
    # Добавляем инструкцию для лучшей логики в математике/химии
    payload = {
        "model": MODEL,
        "messages": [
            {"role": "system", "content": "Решай задачи пошагово и кратко, идеально для маленького экрана."},
            {"role": "user", "content": user_input}
        ]
    }

    try:
        response = requests.post("https://openrouter.ai/api/v1/chat/completions", 
                                 headers=headers, json=payload)
        return jsonify(response.json())
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    # Запуск на порту 5000, доступно для всех устройств в сети
    app.run(host='0.0.0.0', port=5000)
