from pydoc import text
import flet as ft
import subprocess
import threading
import os
from node.llm_server import llm_server
from node.ollima_install import install_ollama_if_needed
OLLAMA_INSTALLER_URL = "https://ollama.com/download/OllamaSetup.exe"
OLLAMA_EXE_NAME = "OllamaSetup.exe"
OLLAMA_LOCAL_PATH = os.path.join(os.getcwd(), OLLAMA_EXE_NAME)


def node_ui(page: ft.Page):
    status_text = ft.Text("Ollama チェック中...")
    page.update()



    threading.Thread(target=lambda: install_ollama_if_needed(status_text, page), daemon=True).start()



    # モデル選択や起動UIなど続き
    model_dropdown = ft.Dropdown(
        label="使用するAIモデルを選択",
        options=[
            ft.dropdown.Option("mistral",text="mistral:4.1GB"),
            ft.dropdown.Option("phi",text="phi:1.8GB"),
            ft.dropdown.Option("mixtral",text="mixtral:26GB"),
            ft.dropdown.Option("llama2",text="llama2:3.8GB"),
            ft.dropdown.Option("llama3",text="llama3"),
            ft.dropdown.Option("chatdolphin2",text="chatdolphin2:4.7GB")
        ]
    )


    def start_model(e):
        
        selected_model = model_dropdown.value
        if not selected_model:
            status_text.value = "⚠ モデルを選択してください"
            page.update()
            return

        def install_and_run_model():
            status_text.value = f"📥 {selected_model} をインストール中..."
            page.update()
            subprocess.run(f"ollama pull {selected_model}", shell=True)
            status_text.value = f"🚀 {selected_model} を起動中..."
            page.update()
            subprocess.Popen(f"ollama run {selected_model}", shell=True)
            status_text.value = f"✅ {selected_model} 起動完了！"
            page.update()
            llm_server.run(selected_model)

        threading.Thread(target=install_and_run_model, daemon=True).start()

    start_button = ft.ElevatedButton("モデルを起動", on_click=start_model)

    return ft.View(
        "/node",
        controls=[
            ft.Text("🖥 リソース提供モード"),
            model_dropdown,
            start_button,
            status_text,
            ft.ElevatedButton("← 戻る", on_click=lambda e: page.go("/"))
        ]
    )
