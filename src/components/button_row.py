import os
import shlex
import time
import subprocess
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
        self.executed_commands = set()
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

        self.command_dropdown = ft.Dropdown(
            label="Comandos guardados",
            width=200,
            hint_text="Selecciona el comando",
            bgcolor="#ffffff",
            options=[]
        )

    def add_command(self, e):
        command = self.command_dropdown.value
        self.content_area.add_row(command if command else "")
        self.command_dropdown.value = None
        self.command_dropdown.update()
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
        self.execute_button.disabled = True

        try: 
            data = self.content_area.get_data()

            if not data:
                self.execute_button.disabled = False
                self.update()
                return

            algoritmo = self.dropdown.value

            if not algoritmo:
                self.content_area.show_error_message("Selecciona un algoritmo")
                self.execute_button.disabled = False
                self.update()
                return

            invalid_commands = self.validate_commands(data['commands'])

            if invalid_commands:
                invalid_command_names = ", ".join(invalid_commands)
                self.content_area.show_error_message(f"Comandos no válidos: {invalid_command_names}")
                self.execute_button.disabled = False
                self.update()
                return

            results = []
            avg_turnaround_time = 0
            avg_response_time = 0

            if algoritmo == 'FCFS':
                fcfs = FCFS(data['commands'])
                results, avg_turnaround_time, avg_response_time = fcfs.run()

            elif algoritmo == 'SPN':
                spn = SPN(data['commands'])
                results, avg_turnaround_time, avg_response_time = spn.run()

            elif algoritmo == 'SRT':
                srt = SRT(data['commands'])
                results, avg_turnaround_time, avg_response_time = srt.run()

            elif algoritmo == 'HRRN':
                hrrn = HRRN(data['commands'])
                results, avg_turnaround_time, avg_response_time = hrrn.run()


            elif algoritmo == 'Round Robin 2q':
                rr2q = RR2Q(data['commands'],2)
                results, avg_turnaround_time, avg_response_time = rr2q.execute()


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

            #add execution_data to the global list
            execution_results.append(execution_data)

            #update result panel
            self.panel_list_area.add_panel(execution_data)
            self.panel_list_area.update_panels()
            
            # Save execution_results in the database
            db.save_results(execution_results)

            # Update executed commands
            self.update_executed_commands(data['commands'])
            
            #update the panel list area
            self.content_area.clear()

            self.content_area.show_succed_message("La ejecución ha terminado")

        except Exception as ex:
            self.content_area.show_error_message(f"Ocurrió un error durante la ejecución: {str(ex)}")

        finally:
            self.execute_button.disabled = False




    def update_executed_commands(self, commands):
        for cmd in commands:
            self.executed_commands.add(cmd['command'])
        self.command_dropdown.options = [ft.dropdown.Option(cmd) for cmd in self.executed_commands]
        self.command_dropdown.update()

    @staticmethod
    def is_command_in_safe_directory(command_path):
        safe_directories = [
            '/bin', '/usr/bin', '/usr/local/bin',
            '/sbin', '/usr/sbin', '/usr/local/sbin',
            os.path.expanduser('~/.local/bin')  # Directorio común para comandos del usuario
        ]
        return any(command_path.startswith(directory) for directory in safe_directories)

    def validate_commands(self, commands):
        invalid_commands = []
        for command_data in commands:
            if not command_data['verify']:
                continue  # Saltar esta validación si 'verify' es falso
            command = command_data['command']
            command_name = shlex.split(command)[0]
            try:
                result = subprocess.run(['which', command_name], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
                if not self.is_command_in_safe_directory(result.stdout.strip()):
                    invalid_commands.append(command)
            except subprocess.CalledProcessError:
                invalid_commands.append(command)
        return invalid_commands


    def build(self):
        return ft.Column(
            [
                ft.Row(
                    [
                        self.add_button,
                        self.remove_button,
                        ft.Container(width=2),
                        self.command_dropdown,
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




