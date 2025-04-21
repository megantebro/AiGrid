import os
import subprocess
import requests
import shutil

OLLAMA_INSTALLER_URL = "https://ollama.com/download/OllamaSetup.exe"
OLLAMA_EXE_NAME = "OllamaSetup.exe"
OLLAMA_LOCAL_PATH = os.path.join(os.getcwd(), OLLAMA_EXE_NAME)

def is_ollama_installed():

    try:
        result = subprocess.run(["ollama","--version"])
        return result.returncode == 0
    except Exception:
        return False

def install_ollama_if_needed(status_text, page):
    if is_ollama_installed():
        status_text.value = "✅ Ollama はすでにインストールされています"
        page.update()
        return
    status_text.value = "⬇️ Ollama をダウンロードしています..."
    page.update()

    try:
        r = requests.get(OLLAMA_INSTALLER_URL)
        with open(OLLAMA_LOCAL_PATH, "wb") as f:
            f.write(r.content)

        status_text.value = "📦 インストーラを実行中..."
        page.update()

        subprocess.Popen(OLLAMA_LOCAL_PATH, shell=True)  # ← ユーザーが手動で「次へ」で進める

        status_text.value = "🛠 インストールを完了してください。その後アプリを再起動してください"
        page.update()
    except Exception as e:
        status_text.value = f"❌ インストール失敗: {e}"
        page.update()
