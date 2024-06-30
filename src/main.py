import flet as ft
from components.principal_content_area import PrincipalContentArea
from components.panel_list_area import PanelListArea
from components.sidebar import Sidebar
from utils.docker_utils import *
from data_manager import db
from execution_results import execution_results

def inicializar_app():
    create_image()
    db.connect()
    db.load_results()
    db.print_results()

def main(page: ft.Page):
    global execution_results
    inicializar_app()
    page.title = "Simple Container Planner"
    page.theme_mode = 'light'
    page.window.width = 1200
    page.window.height = 800



    panel_list_area = PanelListArea(execution_results, None)  # Inicialmente sin main_view
    principal_content_area = PrincipalContentArea(panel_list_area)  # Pasar panel_list_area al principal_content_area
    panel_list_area.main_view = principal_content_area  # Establece principal_content_area en panel_list_area

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
                                    content=panel_list_area,
                                    width=400,  # Ajusta según sea necesario
                                    height=600,  # Ajusta según sea necesario
                                    expand=True
                                )
                            ],
                            expand=True,
                        )
                    ]
                )
            )
            page.update()
            panel_list_area.update_panels()
        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Row(
                            [
                                sidebar,
                                ft.VerticalDivider(width=1),
                                principal_content_area
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