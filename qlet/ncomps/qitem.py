from __future__ import annotations
from inspect import isfunction
from typing import Callable, Sequence

import flet as ft
from flet_core.event_handler import EventHandler
from typing_extensions import Self

from .core.item import Item, _ItemHandle


__all__ = ["QItem"]


number = int | float
_id = id


class QItem(Item):
    @Item.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES + {
            "height",
            "implicit_height", "implicit_width",
            "width",
        }

    def __init__(
            self,
            id: str | None = None,
            root: bool = False,
            children: Item | Sequence[Item] = (),
            width: number | Callable[[_ItemHandle], number] = lambda d: d.implicit_width,
            height: number | Callable[[_ItemHandle], number] = lambda d: d.implicit_height,
            implicit_width: number | Callable[[_ItemHandle], number] = 10,
            implicit_height: number | Callable[[_ItemHandle], number] = 10,
            **kwargs
    ) -> None:
        super().__init__(id, root, children, **kwargs)

    @staticmethod
    def default_width(d: _ItemHandle) -> number:
        return d.implicit_width

    @staticmethod
    def default_height(d: _ItemHandle) -> number:
        return d.implicit_height


if __name__ == "__main__":
    exit(0)
    def main(page: ft.Page):
        page.padding = 10
        page.add(
            ft.Stack(
                [
                    ft.TransparentPointer(
                        content=ft.Container(
                            content=ft.Container(
                                expand=True,
                                bgcolor="#114514",
                            ),
                            padding=ft.Padding(0, -100, 0, 0),
                            # bgcolor="#114514",
                        ),
                        expand=True,
                    ),
                ],
                expand=True,
            ),
        )
        # root_item = QItem.auto_init_page(page=page)
        # item = QItem(
        #     width={
        #         lambda d: (d.self.height),
        #         lambda: page.width / 2,
        #     }
        # )
        page.update()

    ft.app(target=main)
