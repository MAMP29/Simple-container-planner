import flet as ft

class ButtonRow(ft.UserControl):
    def __init__(self):
        super().__init__()

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(text="Ejecutar", width=600),
                    # space between 
                    ft.Container(width=20),  # Espacio entre el botón y el dropdown
                    ft.Dropdown(
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
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
        )
    
