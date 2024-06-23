import flet as ft
from components.principal_content_area import PrincipalContentArea
from components.panel_list_area import PanelListArea
from components.sidebar import Sidebar
from components.docker_utils import *

def inicializar_app():
    create_image()

def main(page: ft.Page):
    inicializar_app()
    page.title = "Simple Container Planner"
    page.theme_mode = 'light'

    def route_change(route):
        sidebar = Sidebar(page)
        page.views.clear()
        if page.route == "/registro":
            page.views.append(
                ft.View(
                    "/registro",
                    [
                        ft.Row(
                            [
                                sidebar,
                                ft.VerticalDivider(width=1),
                                ft.Container(
                                    content=PanelListArea(),
                                    width=400,  # Ajusta según sea necesario
                                    height=600,  # Ajusta según sea necesario
                                    expand=True
                                )
                            ],
                            expand=True
                        )
                    ]
                )
            )
        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            [
                                sidebar,
                                ft.VerticalDivider(width=1),
                                PrincipalContentArea()
                            ],
                            expand=True
                        )
                    ]
                )
            )
        page.update()

    def view_pop(view):
        page.views.pop()
        top_view = page.views[-1]
        page.go(top_view.route)

    page.on_route_change = route_change
    page.on_view_pop = view_pop
    page.go(page.route)

ft.app(target=main)