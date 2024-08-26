"""
temporal file for testing
"""

import flet as ft
if __name__ == "__main__":
    def main(page: ft.Page):
        def container(with_radius: bool) -> ft.Container:
            c = ft.Container(
                width=200,
                height=200,
                bgcolor="#FFFFFF",
                alignment=ft.Alignment(1.3, 0),
                content=ft.Container(
                    width=100,
                    height=100,
                    bgcolor="#FF0000",
                ),
            )
            if with_radius:
                c.border_radius = 0
            return c

        page.add(
            container(False),
            container(True),
        )
        page.update()

    ft.app(target=main)
