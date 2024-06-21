import flet as ft
from components.content_area import ContentArea
from components.button_row import ButtonRow

class PrincipalContentArea(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.content_area = ContentArea()

    def add_command(self, e):
        self.content_area.add_row()
        self.update()

    def remove_command(self, e):
        self.content_area.remove_row()
        self.update()

    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.TextField(label='Nombre', width=350),
                                ft.Container(height=10),
                                self.content_area,
                            ],
                            tight=True
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        width=900,
                        height=400,
                    ),
                    ft.Container(height=20),
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.Row(
                                    [
                                        ft.IconButton(
                                            icon=ft.icons.ADD,
                                            icon_color="black",
                                            icon_size=20,
                                            tooltip="nuevo comando",
                                            bgcolor="blue",
                                            on_click=self.add_command,
                                        ),
                                        ft.IconButton(
                                            icon=ft.icons.REMOVE,
                                            icon_color="black",
                                            icon_size=20,
                                            tooltip="quitar comando",
                                            bgcolor="red",
                                            on_click=self.remove_command,
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Container(height=10),
                                ButtonRow(),
                            ],
                            tight=True
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        width=900,
                    ),
                ],
                spacing=10,
                alignment=ft.MainAxisAlignment.SPACE_BETWEEN,
            ),
            padding=20,
            expand=True
        )

    # def build(self):
    #     return ft.Container(
    #         content=ft.Column(
    #             [
    #                 ft.TextField(label='Nombre', width=350),
    #                 ContentArea(),
    #                 ft.IconButton(
    #                     icon =  ft.icons.ADD,
    #                     icon_color="black",
    #                     icon_size=20,
    #                     tooltip="nuevo comando",
    #                     bgcolor="blue",
    #                 ),
    #                 ButtonRow(),
    #             ],
    #             alignment=ft.MainAxisAlignment.SPACE_AROUND,
    #         ),
    #         padding=20,
    #         expand=True
    #     )