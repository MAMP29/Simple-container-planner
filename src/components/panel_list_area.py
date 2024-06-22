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
            ft.ElevatedButton("Agregar Panel", on_click=self.add_panel)
        ])

    def handle_change(self, e):
        print(f"Cambio en el panel con índice {e.data}")

    def add_panel(self, e):
        new_panel = ft.ExpansionPanel(
            bgcolor=ft.colors.BLUE_400,
            header=ft.Text(f"Panel {len(self.panels) + 1}"),
            content=ft.Text(f"Contenido del panel {len(self.panels) + 1}")
        )
        self.panels.append(new_panel)
        self.expansion_list.controls = self.panels
        self.update()

    #create a header panel that always gonna appear in the top panel 
    def create_header_panel(self):
        return ft.ExpansionPanel(
            bgcolor=ft.colors.BLUE_400,
            header=ft.Text("Area de registros"),
            content=ft.Text("Bievenido a al area de registro, aquí podras consultar los resultados de tus ejecuciónes")
            )


    async def handle_delete(self, e):
        self.panels.remove(e.control.data)
        self.expansion_list.controls = self.panels
        await self.update_async()