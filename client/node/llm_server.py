from flask import Flask, request, jsonify
import requests
import socket
import psutil
from pynvml import nvmlInit,nvmlDeviceGetHandleByIndex,nvmlDeviceGetUtilizationRates

app = Flask(__name__)

# === 基本設定 ===
MODEL_NAME = "mistral"
SERVER_URL = "http://localhost:5000"
PORT = 8000

# === 自分のIPアドレスを取得 ===
def get_my_ip():
    return socket.gethostbyname(socket.gethostname())

def get_gpu_usage():
    try:
        nvmlInit()
        handle = nvmlDeviceGetHandleByIndex(0)
        util = nvmlDeviceGetUtilizationRates(handle)
        return util.gpu
    except Exception as e:
        return -1

# === リソース情報を作成 ===
def get_node_info():
    return {
        "ip": get_my_ip(),
        "port": PORT,
        "model": MODEL_NAME,
        "cpu": psutil.cpu_percent(),
        "memory": psutil.virtual_memory().percent,
        "gpu":get_gpu_usage()
    }

# === API: テキスト生成 ===
@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    prompt = data.get("prompt")
    return jsonify({"result": f"（仮）モデル[{MODEL_NAME}]で生成: {prompt}"})

# === 起動時にサーバーへ登録 ===
def register_to_server():
    info = get_node_info()
    try:
        res = requests.post(f"{SERVER_URL}/register_node", json=info)
        print("✅ サーバーに登録:", res.status_code, res.text)
    except Exception as e:
        print("❌ サーバー登録失敗:", e)

if __name__ == "__main__":
    register_to_server()
    app.run(host="0.0.0.0", port=PORT)
