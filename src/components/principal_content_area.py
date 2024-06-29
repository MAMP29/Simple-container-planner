import flet as ft
from components.content_area import ContentArea
from components.button_row import ButtonRow

class PrincipalContentArea(ft.UserControl):
    def __init__(self, panel_list_area):
        super().__init__()
        self.panel_list_area = panel_list_area
        self.content_area = ContentArea()
        self.button_row = ButtonRow(self.content_area, self.panel_list_area)
        self.button_row.content_area = self.content_area

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=self.content_area,
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        width=1200,
                        height=400,
                        expand=True,
                    ),
                    ft.Container(height=20),
                    ft.Container(
                        content=self.button_row,
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        width=1200,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
            expand=True
        )