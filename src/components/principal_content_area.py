import flet as ft
from components.content_area import ContentArea
from components.button_row import ButtonRow

class PrincipalContentArea(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.content_area = ContentArea()
        self.button_row = ButtonRow(self.content_area)
        self.button_row.content_area = self.content_area
        '''self.remove_button = ft.IconButton(
            icon=ft.icons.REMOVE,
            icon_color="black",
            icon_size=20,
            tooltip="Debe de haber al menos un comando",
            bgcolor="grey",
            on_click=self.remove_command,
            disabled=True,
        )'''

    '''def add_command(self, e):
        self.content_area.add_row()
        self.update_remove_button()
        self.update()

    def remove_command(self, e):
        self.content_area.remove_row()
        self.update_remove_button()
        self.update()

    def update_remove_button(self):
        if (self.content_area.get_row_count() <= 1):
            self.remove_button.disabled = True
            self.remove_button.bgcolor = "grey"
            self.remove_button.tooltip = "Debe de haber al menos un comando"
        else:
            self.remove_button.disabled = False
            self.remove_button.bgcolor = "red"
            self.remove_button.tooltip = "Quitar comando"'''

    



    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    ft.Container(
                        content=self.content_area,
                        padding=10,
                        border=ft.border.all(1, ft.colors.GREY_400),
                        border_radius=10,
                        width=900,
                        height=400,
                        expand=True,
                    ),
                    ft.Container(height=20),
                    ft.Container(
                        content=self.button_row,
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