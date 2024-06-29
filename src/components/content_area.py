import flet as ft
import time
import datetime
import random

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
        self.name_field = ft.TextField(label='Nombre', width=350)
        self.rows = [self.create_row()]
        self.rows_column = ft.Column(self.rows, scroll=ft.ScrollMode.AUTO, expand=True)

    def create_row(self):
        return ft.Row(
            [
                ft.TextField(label='Command', width=350),
                ft.TextField(label='Start time', width=150,hint_text="must be a integer"),
                ft.TextField(label='Estimated time', width=150, hint_text="must be a integer"),
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

    def get_data(self):
        
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
            row_data ={
                'command': row.controls[0].value,
                'start_time': int(row.controls[1].value) if row.controls[1].value else 0,
                'estimated_time': int(row.controls[2].value) if row.controls[2].value else 0,
            }
            data['commands'].append(row_data)
        return data

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
