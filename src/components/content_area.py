import flet as ft
import time
import datetime
import random
from components.alert_dialog import AlertDialog

light_colors = [
    ft.colors.BLUE_50,
    ft.colors.RED_50,
    ft.colors.GREEN_50,
    ft.colors.YELLOW_50,
    ft.colors.PINK_50,
    ft.colors.PURPLE_50,
    ft.colors.ORANGE_50,
    ft.colors.TEAL_50,
    ft.colors.INDIGO_50,
    ft.colors.BROWN_50,
    ft.colors.GREY_50,
]


class ContentArea(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.name_field = ft.TextField(label='Nombre', width=350, bgcolor="#ffffff", on_blur=lambda e: self.validate_command(e, "Debe de haber un nombre"))
        self.rows = [self.create_row()]
        self.rows_column = ft.Column(self.rows, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_row(self, command=""):
        return ft.Row(
            [
                ft.TextField(label='Command', width=350, bgcolor="#ffffff", value=command, on_blur=self.validate_command),
                ft.TextField(label='Start time', width=150, hint_text="must be an integer", bgcolor="#ffffff", on_blur=self.validate_time),
                ft.TextField(label='Estimated time', width=150, hint_text="must be an integer", bgcolor="#ffffff", on_blur=self.validate_time),
            ],
            alignment=ft.MainAxisAlignment.CENTER,
        )
    
    def validate_command(self, e, text="El comando es obligatorio"):
        text_field = e.control
        if not text_field.value:
            text_field.error_text = text
        else:
            text_field.error_text = None
        text_field.update()

    def validate_time(self, e):
        text_field = e.control
        try:
            int(text_field.value)
            text_field.error_text = None
        except ValueError:
            text_field.error_text = "Debe ser entero."
        text_field.update()

    def add_row(self, command=""):
        self.rows.append(self.create_row(command))
        self.update()

    def remove_row(self):
        if len(self.rows) > 1:
            self.rows.pop()
            self.update()

    def obtain_data(self): 
        timestamp_id = str(int(time.time()))
        hour_and_date = self.format_timestamp_id(timestamp_id)

        data = {
            'timestamp_id': timestamp_id,
            'hour_and_date': hour_and_date,
            'color': random.choice(light_colors),
            'name': self.name_field.value,
            'commands': []
        }
        for row in self.rows:
            row_data = {
                'command': row.controls[0].value,
                'start_time': row.controls[1].value,
                'estimated_time': row.controls[2].value,
            }
            data['commands'].append(row_data)
        return data

    def get_data(self):
        data = self.obtain_data()

        if not data['name']:
            self.show_error_message("El campo 'Nombre' es obligatorio.")
            return None

        for command in data['commands']:
            if not command['command'] or not command['start_time'] or not command['estimated_time']:
                self.show_error_message("Todos los campos de comandos son obligatorios.")
                return None
            
        try:
            for command in data['commands']:
                command['start_time'] = int(command['start_time'])
                command['estimated_time'] = int(command['estimated_time'])
        except ValueError:
            self.show_error_message("Los tiempos de inicio y estimado deben ser números enteros.")
            return None

        return data

    def show_error_message(self, message):
        def close_dialog(e):
            self.page.dialog.open = False
            self.page.update()

        dialog = ft.AlertDialog(
            title=ft.Text("Error"),
            content=ft.Text(message),
            actions=[
                ft.TextButton("OK", on_click=close_dialog)
            ]
        )
        self.page.dialog = dialog
        self.page.dialog.open = True
        self.page.update()

    #delete text of the textfields in self.rows
    def clear(self):
        self.name_field.value = ''
        for row in self.rows:
            for control in row.controls:
                control.value = ''
            self.update()
                

    def get_row_count(self):
        return len(self.rows)

    def format_timestamp_id(self, timestamp_id):
        timestamp_seconds = int(timestamp_id)
        hour_and_date = datetime.datetime.fromtimestamp(timestamp_seconds)
        format_hour_and_date = hour_and_date.strftime("%Y-%m-%d %H:%M:%S")
        return format_hour_and_date

    def load_execution_data(self, panel_data):
        self.name_field.value = panel_data["nombre"]
        self.rows = []

        for cmd in panel_data["commands"]:
            row = ft.Row(
                [
                    ft.TextField(label='Command', width=350, value=cmd["command"], bgcolor="#ffffff", on_blur=self.validate_command),
                    ft.TextField(label='Start time', width=150, hint_text="must be a integer", value=str(cmd["start_time"]), bgcolor="#ffffff", on_blur=self.validate_time),
                    ft.TextField(label='Estimated time', width=150, hint_text="must be a integer", value=str(cmd["estimated_time"]), bgcolor="#ffffff", on_blur=self.validate_time),
                ],
                alignment=ft.MainAxisAlignment.CENTER,
            )
            self.rows.append(row)

        self.rows_column.controls = self.rows
        if self.page:
            self.update()


    def build(self):
        return ft.Container(
            content=ft.Column(
                [
                    self.name_field,
                    ft.Container(height=10),
                    self.rows_column
                ],            
                #tight=True,
                expand=True,
            ),
            expand=True,
        )
