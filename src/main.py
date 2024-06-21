import flet as ft
from components.sidebar import Sidebar
from components.content_area import ContentArea
from components.principal_content_area import PrincipalContentArea

def main(page: ft.Page):
    page.title = 'Simple Container planner'
    page.theme_mode = 'light'
    page.update()

    sidebar = Sidebar()
    content = ContentArea()
    principal = PrincipalContentArea()

    main_row = ft.Row(
        [
            sidebar,
            ft.VerticalDivider(width=1),
            ft.Container(height=10),
            principal,
        ],
        expand=True
    )

    page.add(main_row)

ft.app(target=main)