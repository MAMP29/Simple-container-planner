import flet as ft

class ButtonRow(ft.UserControl):
    def __init__(self):
        super().__init__()
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

    def build(self):
        return ft.Container(
            content=ft.Row(
                [
                    ft.ElevatedButton(text="Ejecutar", width=600, on_click=self.ejecutar_event),
                    # space between 
                    ft.Container(width=20),  # Espacio entre el botón y el dropdown
                    self.dropdown,
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            ),
            padding=10,
        )
    
    def ejecutar_event(self, e):
        print(f"El algoritmo escogido es: {self.dropdown.value}")
