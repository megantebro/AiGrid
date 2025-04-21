import flet as ft
from client_mode import client_ui
from node.node_mode import node_ui

def main(page: ft.Page):
    page.title = "分散AIアプリ"

    def route_change(e):
        page.views.clear()

        if page.route == "/":
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Text("どちらのモードで参加しますか？", size=20, weight="bold"),
                        ft.ElevatedButton("🤖 AIを使いたい", on_click=lambda e: page.go("/client")),
                        ft.ElevatedButton("🖥 リソースを提供する", on_click=lambda e: page.go("/node")),
                    ]
                )
            )
        elif page.route == "/client":
            page.views.append(client_ui(page))  # ← 追加！
        elif page.route == "/node":
            page.views.append(node_ui(page))
        page.update()

    page.on_route_change = route_change
    page.go(page.route)  # 初回読み込み時のルート処理

ft.app(target=main)
