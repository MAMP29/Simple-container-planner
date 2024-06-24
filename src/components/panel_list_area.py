import flet as ft

class PanelListArea(ft.UserControl):
    def __init__(self):
        super().__init__()
        self.panels = [self.create_header_panel()]


    def build(self):
        self.expansion_list = ft.ExpansionPanelList(
            expand_icon_color=ft.colors.AMBER,
            elevation=8,
            divider_color=ft.colors.AMBER,
            on_change=self.handle_change,
            controls=self.panels
        )

        

        return ft.Column([
            ft.Text("Panel de Registro", size=20, weight=ft.FontWeight.BOLD),
            self.expansion_list,
            ft.ElevatedButton("Agregar Panel", on_click=self.add_example_panel)
        ])

    def handle_change(self, e):
        print(f"Cambio en el panel con índice {e.data}")


    def add_example_panel(self, e):
        # Simulando datos de una ejecución
        ejecucion_data = {
            "id": len(self.panels) + 1,
            "algoritmo": "FCFS",
            "tiempo_total": "00:05:30",
            "avg_turnaround_time": "00:00:50",
            "avg_response_time": "00:00:30",
            "comandos": [
                {"comando": "echo Hello", "tiempo_inicio": "00:00:00", "tiempo_fin": "00:00:01", "turnaround_time": "00:00:04", "response_time":"00:00:05"},
                {"comando": "ls -l", "tiempo_inicio": "00:00:02", "tiempo_fin": "00:00:03","turnaround_time": "00:00:02", "response_time":"00:00:02"},
                {"comando": "sleep 5", "tiempo_inicio": "00:00:04", "tiempo_fin": "00:00:09","turnaround_time": "00:00:05", "response_time":"00:00:05"}
            ]
        }
        new_panel = self.create_panel(ejecucion_data)
        self.panels.append(new_panel)
        self.expansion_list.controls = self.panels
        self.update()


    def create_panel(self, data):
        # Crear una tabla para los comandos
        table = ft.DataTable(
            columns=[
                ft.DataColumn(ft.Text("Comando")),
                ft.DataColumn(ft.Text("Tiempo Inicio")),
                ft.DataColumn(ft.Text("Tiempo Fin")),
                ft.DataColumn(ft.Text("Turnaround Time")),
                ft.DataColumn(ft.Text("Response Time"))
            ],
            rows=[
                ft.DataRow(
                    cells=[
                        ft.DataCell(ft.Text(cmd["comando"])),
                        ft.DataCell(ft.Text(cmd["tiempo_inicio"])),
                        ft.DataCell(ft.Text(cmd["tiempo_fin"])),
                        ft.DataCell(ft.Text(cmd["turnaround_time"])),
                        ft.DataCell(ft.Text(cmd["response_time"]))
                    ],
                ) for cmd in data["comandos"]
            ],
        )

        content = ft.Row([
                table,
                ft.VerticalDivider(width=2),
                ft.Column([
                    ft.Text(f"Algoritmo: {data['algoritmo']}", weight=ft.FontWeight.BOLD),
                    ft.Text(f"Tiempo total de ejecución: {data['tiempo_total']}"),
                    ft.Text(f"Turnaround time promedio: {data['avg_turnaround_time']}"),
                    ft.Text(f"Response time promedio: {data['avg_response_time']}")
                ])
            ])
            

        return ft.ExpansionPanel(
            bgcolor=ft.colors.BLUE_50,
            header=ft.ListTile(title=ft.Text(f"Ejecución {data['id']}")),
            content=content
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


    async def handle_delete(self, e):
        self.panels.remove(e.control.data)
        self.expansion_list.controls = self.panels
        await self.update_async()