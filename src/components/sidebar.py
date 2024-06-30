import flet as ft


class Sidebar(ft.UserControl):
    def __init__(self, page):
        super().__init__()
        self.page = page

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(value="Simple Container Planner", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=2, color="black", thickness=3),
                    ft.ElevatedButton(content=ft.Text(value="Principal", color="black"), width=200, on_click=lambda _: self.page.go("/"),bgcolor="#aad7d9"),
                    ft.ElevatedButton(content=ft.Text(value="Registro", color="black"), width=200, on_click=lambda _: self.page.go("/registro"), bgcolor="#aad7d9"),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            width=250,
            alignment=ft.alignment.center,
            bgcolor="#ffe5b4",
        )

    def execute_clicked(self, e):
        print("Ejecutar clicked")

    def register_clicked(self, e):
        print("Registrar clicked")