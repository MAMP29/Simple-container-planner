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
                    ft.ElevatedButton(text="Principal", width=200, on_click=lambda _: self.page.go("/")),
                    ft.ElevatedButton(text="Registro", width=200, on_click=lambda _: self.page.go("/registro")),
                ],
                alignment=ft.MainAxisAlignment.START,
                horizontal_alignment=ft.CrossAxisAlignment.CENTER,
                spacing=30,
            ),
            width=250,
            alignment=ft.alignment.center,
            bgcolor="yellow",
        )

    def execute_clicked(self, e):
        print("Ejecutar clicked")

    def register_clicked(self, e):
        print("Registrar clicked")