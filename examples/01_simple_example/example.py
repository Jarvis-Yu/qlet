import flet as ft

from qlet import *

def main(page: ft.Page):
    page.padding = 10

    # sets up sizing update connection with the page
    root_item = QItem.init_page(page=page, colour="#000000")

    # adds some QItem-based children to the root item
    # note that QItem acts like a flet Stack, all items are stacked vertically by default
    root_item.add_children(QItem(
        expand=True,
        colour=ft.colors.with_opacity(0.3, "#FFFFFF"),
        children=(
            QItem(
                anchor=QAnchor(left=0, top=0, bottom=1, right=0.3),
                colour=ft.colors.with_opacity(0.3, "#FF0000"),
                children=(QImage(
                    src="https://cdn.pixabay.com/photo/2023/10/26/08/24/autumn-8342089_1280.jpg",
                    align=QAlign(0.5, 0.5),
                    width_pct=1.0,   # width of the image container is 100% of the parent's width
                    height_pct=0.7,  # height of the image container is 50% of the parent's height
                )),
            ),
            QItem(
                align=QAlign(0.5, 0.5),
                width_pct=0.33,
                height_pct=1.0,
                colour=ft.colors.with_opacity(0.3, "#00FF00"),
                children=(QText(
                    text="Hello, QText!",
                    text_colour="#000000",
                    size_rel_height=0.1,
                    anchor=QAnchor(top=0),
                    height_pct=0.3,
                    width_pct=1.0,
                    colour=ft.colors.with_opacity(0.5, "#FFFFFF"),
                )),
            ),
            QItem(
                anchor=QAnchor(left=0.7, top=0, bottom=1, right=1),
                colour=ft.colors.with_opacity(0.3, "#0000FF"),
                flets=((
                    ft.TextButton(text="Hello, Flet!", on_click=lambda _: print("Hello, Flet!")),
                ))
            ),
        ),
    ))
    page.update()

ft.app(target=main)
