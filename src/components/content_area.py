import flet as ft

class ContentArea(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.TextField(label='Command', width=350),
                    ft.TextField(label='Start time', width=150),
                    ft.TextField(label='Estimated time', width=150),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=20,
            expand=True
        )
    
    def create_new_command_textfield(self, e):
        ft.TextField(label='Command', width=350),
        ft.TextField(label='Start time', width=150),
        ft.TextField(label='Estimated time', width=150),