"""
temporal file for testing
"""

import flet as ft
if __name__ == "__main__":
    def main(page: ft.Page):
        page.add(
            ft.Container(
                bgcolor="white",
                width=200,
                height=200,
                padding=ft.Padding(0, 0, 100, 100),
                # border=ft.border.all(20, "green"),
                content=ft.Container(
                    bgcolor="red",
                ),
            )
        )
        page.update()

    ft.app(target=main)
