import flet as ft
from components.principal_content_area import PrincipalContentArea
from components.panel_list_area import PanelListArea
from components.sidebar import Sidebar
from utils.docker_utils import *
from data_manager import db

def inicializar_app():
    create_image()
    db.connect()
    db.load_results()

def main(page: ft.Page):
    inicializar_app()
    page.title = "Simple Container Planner"
    page.theme_mode = 'light'
    page.window.width = 1550
    page.window.height = 800
    page.bgcolor = "#fbf9f1"

    page.on_close = lambda e: stop_database_container()

    panel_list_area = PanelListArea(None)  # Inicialmente sin main_view
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
                        ft.Container(
                            content=ft.Row(
                                [
                                    sidebar,
                                    ft.VerticalDivider(width=1),
                                    ft.Container(
                                        content=panel_list_area,
                                        expand=True,
                                        alignment=ft.alignment.center,
                                    )
                                ],
                                expand=True,
                            ),
                            width=page.window.width,
                            height=page.window.height,
                            bgcolor=page.bgcolor,
                            expand=True,
                        )
                    ],
                    bgcolor=page.bgcolor,
                )
            )
            page.update()
            panel_list_area.update_panels()
        else:
            page.views.append(
                ft.View(
                    "/",
                    [
                        ft.Container(
                            content=ft.Row(
                                [
                                    sidebar,
                                    ft.VerticalDivider(width=1),
                                    principal_content_area
                                ],
                                expand=True
                            ),
                            width=page.window.width,
                            height=page.window.height,
                            bgcolor=page.bgcolor,
                            expand=True,
                        )
                    ],
                    bgcolor=page.bgcolor,
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