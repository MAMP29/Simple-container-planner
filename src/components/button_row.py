import flet as ft
from components.content_area import ContentArea

class ButtonRow(ft.UserControl):
    def __init__(self, content_area):
        super().__init__()
        self.content_area = content_area
        self.dropdown = ft.Dropdown(
            label="Algoritmo",
            width=200,
            hint_text="Selecciona el algoritmo",
            options=[
                ft.dropdown.Option("FCFS"),
                ft.dropdown.Option("SPN"),
                ft.dropdown.Option("SRT"),
                ft.dropdown.Option("HRRN"),
                ft.dropdown.Option("Round Robin 2q"),
            ],
        )
        self.execute_button = ft.ElevatedButton(text="Ejecutar", width=600, on_click=self.execute_comands)

        self.add_button = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color="black",
            icon_size=20,
            tooltip="Nuevo comando",
            bgcolor="blue",
            on_click=self.add_command,
        )

        self.remove_button = ft.IconButton(
            icon=ft.icons.REMOVE,
            icon_color="black",
            icon_size=20,
            tooltip="Debe de haber al menos un comando",
            bgcolor="grey",
            on_click=self.remove_command,
            disabled=True,
        )

    def add_command(self, e):
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
            self.remove_button.tooltip = "Quitar comando"

    # execute the commands of the user 
    def execute_comands(self, e):
        data = self.content_area.get_data()
        algoritmo = self.dropdown.value

        print(f"Ejecutando data con el algoritmo: {algoritmo}")
        print(data)


    # def build(self):
    #     return ft.Container(
    #         content=ft.Row(
    #             [
    #                 self.execute_button,
    #                 # space between 
    #                 ft.Container(width=20),  # Espacio entre el botón y el dropdown
    #                 self.dropdown,
    #             ],
    #             alignment=ft.MainAxisAlignment.CENTER,
    #         ),
    #         padding=10,
    #     )
    
    def build(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        self.add_button,
                        self.remove_button,
                    ],
                    alignment=ft.MainAxisAlignment.START,
                ),
                ft.Container(height=10),
                ft.Row(
                    [
                    self.execute_button,
                    self.dropdown,
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                ),
            ],
            tight=True
        )




