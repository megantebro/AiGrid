import flet as ft
import requests

def client_ui(page: ft.Page):  # ← ここに引数 page を追加！
    prompt_input = ft.TextField(label="プロンプトを入力")
    result_text = ft.Text()

    def send_prompt(e):
        prompt = prompt_input.value
        try:
            res = requests.get("http://localhost:5000/get_best_node").json()
            result_text.value = f"送信完了！使用ノード: {res.get('best_node')}"
        except Exception as ex:
            result_text.value = f"エラー: {str(ex)}"
        page.update()

    return ft.View(
        "/client",
        controls=[
            ft.Text("🤖 AIに依頼を送るモード"),
            prompt_input,
            ft.ElevatedButton("送信", on_click=send_prompt),
            result_text,
            ft.ElevatedButton("← 戻る", on_click=lambda e: page.go("/"))
        ]
    )
