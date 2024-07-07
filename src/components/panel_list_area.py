import json
import flet as ft
from data_manager import db
from execution_results import execution_results_manager

class PanelListArea(ft.UserControl):
    def __init__(self, main_view):
        super().__init__()
        self.main_view = main_view # Referencia al componente principal
        self.panels = [self.create_header_panel()]
        self.expansion_list = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.BLACK,
            elevation=8,
            divider_color=ft.colors.BLACK,
            on_change=self.handle_change
        )
        self.panel_column = ft.Column([
            ft.Text("Panel de Registro", size=20, weight=ft.FontWeight.BOLD),
            self.expansion_list,
        ],
        scroll=ft.ScrollMode.AUTO
        )


    def build(self):
        return self.panel_column

    def handle_change(self, e):
        print(f"Cambio en el panel con índice {e.data}")
        

    def update_panels(self):
        self.panels = [self.create_header_panel()]
        for data in execution_results_manager.get_results():
            new_panel = self.create_panel(data)
            self.panels.append(new_panel)
        self.expansion_list.controls = self.panels
        if self.page:
            self.update()

    def add_panel(self, data):
        new_panel = self.create_panel(data)
        self.panels.append(new_panel)
        self.expansion_list.controls = self.panels
        if self.page:
            self.update()


    def add_new_panel(self, new_panel):
        self.panels.append(new_panel)
        self.expansion_list.controls = self.panels
        self.update()


    def create_panel(self, data):
        
        retraso_str = "Si" if data['retraso_artificial'] else 'No'

        def truncate_command(command, max_length=20):
                return command if len(command) <= max_length else command[:max_length] + '...'

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Proceso")),
                ft.DataColumn(ft.Text("Tiempo Inicio")),
                ft.DataColumn(ft.Text("Tiempo Estimado")),
                ft.DataColumn(ft.Text("Turnaround Time")),
                ft.DataColumn(ft.Text("Response Time")),
                ft.DataColumn(ft.Text("Tiempo de ejecución"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(truncate_command(cmd["command"]), tooltip=cmd["command"])),
                        ft.DataCell(ft.Text(cmd["start_time"])),
                        ft.DataCell(ft.Text(cmd["estimated_time"])),
                        ft.DataCell(ft.Text(f"{cmd['turnaround_time']:.2f}")),
                        ft.DataCell(ft.Text(f"{cmd['response_time']:.2f}")),
                        ft.DataCell(ft.Text(f"{cmd['actual_execution_time']:.2f}"))
                    ],
                ) for cmd in data["commands"]
            ],
        )

        listTitle = ft.ListTile(
            title=ft.Text(f"Panel: {data['timestamp_id']}"),
            subtitle=ft.Text(f"Fecha de creación: {data['hour_and_date']}"),
        )

        content = ft.Column([
            ft.Row([
                table,
                ft.VerticalDivider(width=2),
                ft.Column([
                    ft.Text(f"Algoritmo: {data['algoritmo']}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Tiempo total de ejecución: \n {data['total_time']}"),
                    ft.Text(f"Turnaround time promedio: \n {data['avg_turnaround_time']}"),
                    ft.Text(f"Response time promedio: \n {data['avg_response_time']}"),
                    ft.Text(f"Retraso artificial: \n {retraso_str}")
                ]),
            ]),
            ft.Row([
                ft.Container(
                    content=listTitle,
                    expand=True
                ),
                ft.IconButton(
                    ft.icons.DELETE, 
                    on_click=lambda e, panel_id=data["timestamp_id"]: self.handle_delete(e, panel_id), 
                    tooltip="Eliminar registro",
                    icon_color=ft.colors.BLACK
                ),
                ft.IconButton(
                    ft.icons.AUTORENEW,
                    on_click=lambda e, panel_data=data: self.handle_reuse(e, panel_data), 
                    tooltip="Cargar a ejecución",
                    icon_color=ft.colors.BLACK,
                ),
                ft.IconButton(
                    ft.icons.SIM_CARD_DOWNLOAD,
                    on_click=lambda e, panel_data=data: self.export_to_json(panel_data),
                    tooltip="Exportar a JSON",
                    icon_color=ft.colors.BLACK
                    
                )
            ], 
            alignment=ft.MainAxisAlignment.SPACE_BETWEEN)
        ])

        return ft.ExpansionPanel(
            bgcolor=data["color"],
            header=ft.ListTile(title=ft.Text(f"Ejecución {data['nombre']}")),
            content=content,
            data=data["timestamp_id"]
        )

    # Crear un panel principal que aparece siempre en la parte superior
    def create_header_panel(self):
        return ft.ExpansionPanel(
            bgcolor=ft.colors.BLUE_400,
            header=ft.ListTile(title=ft.Text("Area de registro",color="white")),
            content=ft.Column(
                    [   
                        ft.Text("Bievenido a al area de registro, aquí podras consultar los resultados de tus ejecuciónes", size=24, color="white")
                    ],
                    alignment=ft.MainAxisAlignment.CENTER,
                )
            )

    def handle_delete(self, e, panel_id):
        db.delete_result_by_id(panel_id)
        self.update_panels()

    def handle_reuse(self, e, panel_data):
        self.main_view.load_execution_data(panel_data)  # Llamada al método del componente principal para cargar los datos y redirigir
        self.page.go("/")  # Navega de vuelta al área de ejecución

    def export_to_json(self, panel_data):
        try:
            filename = f"registro_{panel_data['timestamp_id']}.json"
            with open(filename, 'w') as json_file:
                json.dump(panel_data, json_file, indent=4)
            print(f"Registro exportado a {filename}")
        except Exception as e:
            print(f"Error al exportar el registro: {e}")
