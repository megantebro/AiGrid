import flet as ft
import requests

def client_ui(page: ft.Page):
    prompt_input = ft.TextField(label="プロンプトを入力", multiline=True, min_lines=4, max_lines=10)
    result_text = ft.Text()
    node_dropdown = ft.Dropdown(label="使用するノード")

    def load_nodes():
        try:
            res = requests.get("http://localhost:5000/get_nodes")
            res.raise_for_status()
            node_list = res.json()

            node_dropdown.options = [
                ft.dropdown.Option(f"{n['model']}:{n['ip']}:{n['port']}") for n in node_list
            ]
            if node_list:
                node_dropdown.value = f"{node_list[0]['model']}:{node_list[0]['ip']}:{node_list[0]['port']}"
            page.update()
        except Exception as e:
            result_text.value = f"ノード取得失敗: {e}"
            page.update()

    def send_prompt(e):
        if not node_dropdown.value:
            result_text.value = "⚠ ノードを選んでください"
            page.update()
            return

        model,ip, port = node_dropdown.value.split(":")
        url = f"http://{ip}:{port}/generate"

        try:
            res = requests.post(url, json={"prompt": prompt_input.value})
            result_text.value = res.json().get("result", "応答なし")
        except Exception as e:
            result_text.value = f"送信エラー: {e}"
        page.update()

    # 初期ノード読み込み
    load_nodes()

    return ft.View(
        "/client",
        controls=[
            ft.Text("🤖 プロンプト送信モード"),
            prompt_input,
            node_dropdown,
            ft.ElevatedButton("送信", on_click=send_prompt),
            result_text,
            ft.ElevatedButton("← 戻る", on_click=lambda e: page.go("/"))
        ],
        scroll="auto"
    )