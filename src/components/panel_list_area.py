import flet as ft
import random
from flet import colors
from data_manager import db


class PanelListArea(ft.UserControl):
    def __init__(self, execution_results, main_view):
        super().__init__()
        self.execution_results = execution_results
        self.main_view = main_view # Referencia al componente principal
        self.panels = [self.create_header_panel()]
        self.expansion_list = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            elevation=8,
            divider_color=ft.colors.AMBER,
            on_change=self.handle_change
        )
        self.panel_column = ft.Column([
            ft.Text("Panel de Registro", size=20, weight=ft.FontWeight.BOLD),
            self.expansion_list,
        ])


    def build(self):
        return self.panel_column

    def handle_change(self, e):
        print(f"Cambio en el panel con índice {e.data}")
        

    def update_panels(self):
        # Limpiar los paneles actuales y agregar nuevamente
        self.panels = [self.create_header_panel()]
        for data in self.execution_results:
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

        print("------------------------------------------------")
        print("Creating panel with data:")
        print(data)
    
        for cmd in data["commands"]:
            print("Command data:")
            print(cmd)
        print("------------------------------------------------")

        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Comando")),
                ft.DataColumn(ft.Text("Tiempo Inicio")),
                ft.DataColumn(ft.Text("Tiempo Estimado")),
                ft.DataColumn(ft.Text("Turnaround Time")),
                ft.DataColumn(ft.Text("Response Time")),
                ft.DataColumn(ft.Text("Tiempo de ejecución"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cmd["command"])),
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
            # trailing=ft.IconButton(
            #     ft.icons.DELETE, 
            #     on_click=lambda e, panel_id=data["timestamp_id"]: self.handle_delete(e, panel_id), 
            #     icon_color=ft.colors.BLACK
            # )
        )

        content = ft.Column([
            ft.Row([
                table,
                ft.VerticalDivider(width=2),
                ft.Column([
                    ft.Text(f"Algoritmo: {data['algoritmo']}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Tiempo total de ejecución: {data['total_time']}"),
                    ft.Text(f"Turnaround time promedio: {data['avg_turnaround_time']}"),
                    ft.Text(f"Response time promedio: {data['avg_response_time']}"),
                    # ElevatedButton("Exportar a JSON", on_click=lambda e: self.export_to_json(data)),
                    # ElevatedButton("Exportar a CSV", on_click=lambda e: self.export_to_csv(data)),
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
                    icon_color=ft.colors.BLACK
                ),
                ft.IconButton(
                    ft.icons.AUTORENEW,
                    on_click=lambda e, panel_data=data: self.handle_reuse(e, panel_data), 
                    icon_color=ft.colors.BLACK,
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

    #create a header panel that always gonna appear in the top panel 
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
        self.execution_results = [data for data in self.execution_results if data["timestamp_id"] != panel_id]
        db.delete_result_by_id(panel_id)  # Elimina el registro de la base de datos
        self.update_panels()

    def handle_reuse(self, e, panel_data):
        self.main_view.load_execution_data(panel_data)  # Llamada al método del componente principal para cargar los datos y redirigir
        self.page.go("/")  # Navega de vuelta al área de ejecución

    # async def handle_delete(self, e):
    #     self.panels.remove(e.control.data)
    #     self.expansion_list.controls = self.panels
    #     await self.update_async()