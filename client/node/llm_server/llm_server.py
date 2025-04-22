from flask import Flask, request, jsonify
import requests
import socket
import psutil
from node.llm_server.get_gpu_data import get_gpu_info
app = Flask(__name__)

# === 基本設定 ===
model_name = ""
SERVER_URL = "http://localhost:5000"
PORT = 8000

# === 自分のIPアドレスを取得 ===
def get_my_ip():
    return socket.gethostbyname(socket.gethostname())

def get_gpu_usage():
    try:
        info = get_gpu_info()
        if info and "utilization.gpu" in info[0]:
            return float(info[0]["utilization.gpu"])
    except Exception as e:
        print(e)
        return -1

# === リソース情報を作成 ===
def get_node_info():
    return {
        "ip": get_my_ip(),
        "port": PORT,
        "model": model_name,
        "cpu": psutil.cpu_percent(interval=0.1),
        "memory": psutil.virtual_memory().percent,
        "gpu":get_gpu_usage()
    }

# === API: テキスト生成 ===
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    if not prompt:
        return jsonify({"error": "プロンプトがありません"}), 400

    try:
        # OllamaのAPIに投げる
        ollama_res = requests.post("http://localhost:11434/api/generate", json={
            "model": model_name,
            "prompt": prompt,
            "stream": False  # ストリームじゃなく一括取得
        })
        ollama_res.raise_for_status()

        response_data = ollama_res.json()
        return jsonify({"result": response_data.get("response", "")})
    except Exception as e:
        return jsonify({"error": f"Ollama連携失敗: {str(e)}"}), 500

# === 起動時にサーバーへ登録 ===
def register_to_server():
    info = get_node_info()
    try:
        res = requests.post(f"{SERVER_URL}/register_node", json=info)
        print("✅ サーバーに登録:", res.status_code, res.text)
    except Exception as e:
        print("❌ サーバー登録失敗:", e)

def run(selected_model):
    global model_name
    model_name = selected_model
    register_to_server()
    app.run(host="0.0.0.0", port=PORT)
