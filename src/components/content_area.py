import flet as ft

class ContentArea(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.rows = [self.create_row()]

    def create_row(self):
        return ft.Row(
            [
                ft.TextField(label='Command', width=350),
                ft.TextField(label='Start time', width=150),
                ft.TextField(label='Estimated time', width=150),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )

    def add_row(self):
        self.rows.append(self.create_row())
        self.update()

    def remove_row(self):
        if len(self.rows) > 1:
            self.rows.pop()
            self.update()


    def build(self):
        return ft.Container(
            ft.Column(self.rows, scroll=ft.ScrollMode.AUTO),
            height=250,
        )
    
