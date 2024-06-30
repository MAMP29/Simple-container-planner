import time
import flet as ft
from data_manager import db
from execution_results import execution_results
from components.panel_list_area import PanelListArea
from utils.docker_utils import execute_command
from algorithms.fcfs import FCFS
from algorithms.spn import SPN
from algorithms.srt import SRT
from algorithms.hrrn import HRRN
from algorithms.round_robin import RR2Q

class ButtonRow(ft.UserControl):
    def __init__(self, content_area, panel_list_area):
        super().__init__()
        self.content_area = content_area
        self.panel_list_area = panel_list_area if panel_list_area is not None else PanelListArea([], None)
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
            bgcolor="#ffffff"
        )
        self.execute_button = ft.ElevatedButton(content=ft.Text(value="Ejecutar", color="black"), width=600, on_click=self.execute_comands, bgcolor="#aad7d9")

        self.add_button = ft.IconButton(
            icon=ft.icons.ADD,
            icon_color="black",
            icon_size=20,
            tooltip="Nuevo comando",
            bgcolor="#a2c8cc",
            on_click=self.add_command,
        )

        self.remove_button = ft.IconButton(
            icon=ft.icons.REMOVE,
            icon_color="black",
            icon_size=20,
            tooltip="Debe de haber al menos un comando",
            bgcolor="#ced4da",
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
            self.remove_button.bgcolor = "#ced4da"
            self.remove_button.tooltip = "Debe de haber al menos un comando"
        else:
            self.remove_button.disabled = False
            self.remove_button.bgcolor = "#ff8787"
            self.remove_button.tooltip = "Quitar comando"

    # Execute the commands of the user 
    def execute_comands(self, e):
        global execution_results
        data = self.content_area.get_data()
        algoritmo = self.dropdown.value
        print(data)
        results = []
        avg_turnaround_time = 0
        avg_response_time = 0

        if algoritmo == 'FCFS':
            fcfs = FCFS(data['commands'])
            results, avg_turnaround_time, avg_response_time = fcfs.run()

            for result in results:
                print(f"Resultado del comando: {result['result']}")
                print(f"Turnaround time: {result['turnaround_time']}")
                print(f"Response time: {result['response_time']}")

        elif algoritmo == 'SPN':
            spn = SPN(data['commands'])
            results, avg_turnaround_time, avg_response_time = spn.run()

            for result in results:
                print(f"Resultado del comando: {result['result']}")
                print(f"Turnaround time: {result['turnaround_time']}")
                print(f"Response time: {result['response_time']}")

        elif algoritmo == 'SRT':
            srt = SRT(data['commands'])
            results, avg_turnaround_time, avg_response_time = srt.run()

            for result in results:
                print(f"Resultado del comando: {result['result']}")
                print(f"Turnaround time: {result['turnaround_time']}")
                print(f"Response time: {result['response_time']}")

        elif algoritmo == 'HRRN':
            hrrn = HRRN(data['commands'])
            results, avg_turnaround_time, avg_response_time = hrrn.run()

            for result in results:
                print(f"Resultado del comando: {result['result']}")
                print(f"Turnaround time: {result['turnaround_time']}")
                print(f"Response time: {result['response_time']}")

        elif algoritmo == 'Round Robin 2q':
            rr2q = RR2Q(data['commands'],2)
            results, avg_turnaround_time, avg_response_time = rr2q.execute()

            for result in results:
                print(f"Resultado del comando: {result['result']}")
                print(f"Turnaround time: {result['turnaround_time']}")
                print(f"Response time: {result['response_time']}")

        print(f"Average Turnaround Time: {avg_turnaround_time}")
        print(f"Average Response Time: {avg_response_time}")

        #Create a dictionary of the execution data
        execution_data = {
            "timestamp_id": data["timestamp_id"],
            "hour_and_date": data["hour_and_date"],
            "color": data["color"],
            "nombre": data["name"],
            "algoritmo": algoritmo,
            "total_time": time.strftime("%H:%M:%S", time.gmtime(sum([r['turnaround_time'] for r in results]))),
            "avg_turnaround_time": time.strftime("%H:%M:%S", time.gmtime(avg_turnaround_time)),
            "avg_response_time": time.strftime("%H:%M:%S", time.gmtime(avg_response_time)),
            "commands": results
        }

        print("-----------------Execution data:")
        print(execution_data)

        #add execution_data to the global list
        execution_results.append(execution_data)
        print(execution_results)

        #update result panel
        #new_panel = self.panel_list_area.create_panel(execution_data)
        self.panel_list_area.add_panel(execution_data)
        self.panel_list_area.update_panels()
        
        # Save execution_results in the database
        db.save_results(execution_results)
        
        #update the panel list area
        self.content_area.clear()


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




