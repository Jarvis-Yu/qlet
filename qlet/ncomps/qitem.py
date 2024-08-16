from __future__ import annotations
from inspect import isfunction
from typing import Callable, Sequence

import flet as ft
from flet_core.event_handler import EventHandler
from typing_extensions import Self

from .core.item import _QRefHandler


__all__ = ["QItem"]


number = int | float
_id = id


class QItem:
    def __init__(
            self,
            id: str = "",
            name: str = None,

            # size
            width: number | Callable[[_QRefHandler], number] | None = None,
            height: number | Callable[[_QRefHandler], number] | None = None,
            implicit_width: number | Callable[[_QRefHandler], number] | None = None,
            implicit_height: number | Callable[[_QRefHandler], number] | None = None,
            expand: bool | Callable[[_QRefHandler], bool] = False,

            # visual
            colour: str | Callable[[_QRefHandler], str] = ft.colors.with_opacity(0, "#FFFFFF"),

            children: Sequence[QItem] = (),
    ) -> None:
        """
        :param id: identifier of the item, cannot be ``"parent"`` or ``"self"``.
        :param width: width of the item.
        :param height: height of the item.
        """
        assert id not in ("parent", "self")

        self._f_width = width
        self._f_height = height
        self._f_implicit_width = implicit_width
        self._f_implicit_height = implicit_height
        self._f_expand = expand

        self._id = id
        self._name = name if name is not None else f"{self.__class__.__name__}{_id(self)}"

        self._children = list(children)

    def _on_page_resize(self, page: ft.Page) -> Callable[[ft.ControlEvent], None]:
        self._page = page
        def f(event: ft.ControlEvent) -> None:
            print(page.width, page.height)
        self._on_resize = f
        return f

    @classmethod
    def auto_init_page(cls, page: ft.Page) -> Self:
        """
        :returns: a new QItem occupying the whole page.

        This method adds the new QItem to the page, and subscribes to page.on_resize
        with QItem's resize handler.
        """
        root_item = cls(name="root", expand=True)
        assert isinstance(page.on_resize, EventHandler)
        page.on_resize.subscribe(root_item._on_page_resize(page))
        page.add(root_item)
        return root_item

    @classmethod
    def manual_init_page(
            cls, page: ft.Page
    ) -> tuple[Self, Callable[[ft.ControlEvent]], None]:
        """
        :returns: (a new QItem, the corresponding resize handler).

        This method adds the new QItem to the page, but leaves the handler as
        a return value.
        """
        page.on_resize
    
    def __del__(self) -> None:
        if hasattr(self, "_on_resize"):
            assert hasattr(self, "_page")
            if isinstance(self._page.on_resize, EventHandler):
                self._page.on_resize.unsubscribe(self._on_resize)


if __name__ == "__main__":
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
        item = QItem(
            width={
                lambda d: (d.self.height),
                lambda: page.width / 2,
            }
        )
        page.update()

    ft.app(target=main)
