import flet as ft

class Sidebar(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Text(value="Simple Container Planner", size=24, weight=ft.FontWeight.BOLD),
                    ft.Divider(height=2, color="black", thickness=3),
                    ft.ElevatedButton(text="Ejecutar", width=200, on_click=self.execute_clicked),
                    ft.ElevatedButton(text="Registrar", width=200, on_click=self.register_clicked),
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