import flet as ft
from components.content_area import ContentArea
from components.button_row import ButtonRow

class PrincipalContentArea(ft.UserControl):
    def __init__(self):
        super().__init__()


    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    # Nombre y área de contenido en un contenedor
                    ft.Container(
                        content=ft.Column(
                            [
                                ft.TextField(label='Nombre', width=350),
                                ft.Container(height=10),  # Espacio entre nombre y contenido
                                ContentArea(),
                            ],
                            tight=True
                        ),
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        width=900,
                        height=200,
                    ),
                    ft.Container(height=20),  # Espacio entre el contenedor y el botón de añadir
                    # Botón de añadir y fila de botones en otro contenedor
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
                                        ),

                                        ft.IconButton(
                                            icon=ft.icons.REMOVE,
                                            icon_color="black",
                                            icon_size=20,
                                            tooltip="quitar comando",
                                            bgcolor="red",
                                        ),
                                    ],
                                    alignment=ft.MainAxisAlignment.START,
                                ),
                                ft.Container(height=10),  # Espacio entre el botón de añadir y la fila de botones
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