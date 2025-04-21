import flet as ft
import requests

SERVER_URL = "http://localhost:5000"
MODEL_NAME = "mistral"

def client_ui(page: ft.Page):
    prompt_input = ft.TextField(label="プロンプトを入力", multiline=True)
    result_text = ft.Text()
    loading_text = ft.Text()

    def send_prompt(e):
        prompt = prompt_input.value.strip()
        if not prompt:
            result_text.value = "⚠ プロンプトを入力してください。"
            page.update()
            return

        loading_text.value = "⏳ ノード選択中..."
        page.update()

        try:
            # 1. 最適なノードを取得
            node_res = requests.get(f"{SERVER_URL}/get_best_node", params={"model": MODEL_NAME})
            if node_res.status_code != 200:
                result_text.value = f"❌ ノード取得失敗: {node_res.json().get('error', '不明')}"
                loading_text.value = ""
                page.update()
                return

            node = node_res.json()
            ip, port = node["ip"], node["port"]
            loading_text.value = f"✅ 使用ノード: {ip}:{port} に接続中..."

            # 2. 選ばれたノードにプロンプト送信
            generate_url = f"http://{ip}:{port}/generate"
            response = requests.post(generate_url, json={"prompt": prompt})

            if response.status_code == 200:
                result = response.json().get("result", "（空の返答）")
                result_text.value = f"💬 AIの返答:\n{result}"
            else:
                result_text.value = f"❌ 生成失敗: {response.status_code} {response.text}"
        except Exception as ex:
            result_text.value = f"❌ 通信エラー: {str(ex)}"
        finally:
            loading_text.value = ""
            page.update()

    return ft.View(
        "/client",
        controls=[
            ft.Text("🤖 AIに依頼を送るモード"),
            prompt_input,
            ft.ElevatedButton("送信", on_click=send_prompt),
            loading_text,
            result_text,
            ft.ElevatedButton("← 戻る", on_click=lambda e: page.go("/"))
        ]
    )
