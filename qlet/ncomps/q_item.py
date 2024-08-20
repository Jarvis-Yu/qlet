from __future__ import annotations
from typing import Callable, Sequence

import flet as ft

from .core.item import Item, _ItemHandle
from ._typing_shortcut import number


__all__ = ["QItem"]


class QItemDefaultVals:
    @staticmethod
    def default_width(d: _ItemHandle) -> number:
        return d.implicit_width

    @staticmethod
    def default_height(d: _ItemHandle) -> number:
        return d.implicit_height

    default_implicit_width = 10

    default_implicit_height = 10

    @staticmethod
    def default_x(d: _ItemHandle) -> number:
        return 0

    @staticmethod
    def default_y(d: _ItemHandle) -> number:
        return 0

    default_bgcolour = "#FF000000"

    @staticmethod
    def default_global_x(d: _ItemHandle) -> number:
        return d.parent.global_x + d.x

    @staticmethod
    def default_global_y(d: _ItemHandle) -> number:
        return d.parent.global_y + d.y


class QItem(Item):
    _DEFAULT_VALUES = QItemDefaultVals

    @Item.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "bgcolour",
            "global_x", "global_y",
            "height",
            "implicit_height", "implicit_width",
            "width",
            "x",
            "y",
        }

    def __init__(
            self,
            id: str | None = None,
            children: Item | Sequence[Item] = (),
            
            # position and sizing
            width: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_width,
            height: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_height,
            implicit_width: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_implicit_width,
            implicit_height: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_implicit_height,
            x: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_x,
            y: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_y,

            # appearance
            bgcolour: str | Callable[[_ItemHandle], str] = QItemDefaultVals.default_bgcolour,

            **kwargs
    ) -> None:
        self._frame = ft.Stack(expand=True)

        super().__init__(
            id, False, children,
            **kwargs,
        )

        self._root_component: ft.TransparentPointer
        self._container: ft.Container
        self._init_flet()

        self.width: number = width
        self.height: number = height
        self.implicit_width: number = implicit_width
        self.implicit_height: number = implicit_height
        self.x: number = x
        self.y: number = y

        self.bgcolour: str = bgcolour

        self.global_x = QItemDefaultVals.default_global_x
        self.global_y = QItemDefaultVals.default_global_y

    def _init_flet(self) -> None:
        self._container = ft.Container(
            content=self._frame,
            expand=True,
        )
        self._l2_tr_pointer = ft.TransparentPointer(
            content=self._container,
        )
        self._l1_conainter = ft.Container(
            content=self._l2_tr_pointer,
            padding=ft.Padding(0, 0, 0, 0),
        )
        self._root_component = ft.TransparentPointer(
            content=self._l1_conainter,
            expand=True,
        )

    def _on_width_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] width: {self.width}")
        self._l2_tr_pointer.width = self.width

    def _on_height_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] height: {self.height}")
        self._l2_tr_pointer.height = self.height

    def _on_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] x: {self.x}")
        self._l1_conainter.padding.left = self.x

    def _on_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] y: {self.y}")
        self._l1_conainter.padding.top = self.y

    def _on_bgcolour_change(self) -> None:
        self._container.bgcolor = self.bgcolour

    def add_child(self, new_child: QItem) -> None:
        super().add_child(new_child)
        self._frame.controls.append(new_child._root_component)


if __name__ == "__main__":
    from .q_root_item import QRootItem

    def main(page: ft.Page):
        page.padding = 100
        # page.padding = ft.Padding(10, 20, 30, 40)
        if False:
            ct1 = ft.Container(
                content=ft.TransparentPointer(
                        content=ft.Container(
                        # expand=True,
                        width=100,
                        height=100,
                        bgcolor="#FFFFFF",
                    ),
                ),
                bgcolor="#FF0000",
                # width=500,
                # height=500,
                # expand=True,
                # alignment=ft.Alignment(1.6, 1.6),
                # padding=ft.Padding(-50, -40, -30, -20),
                expand=True,
                padding=ft.Padding(75, 50, 0, 0),
            )
            tp = ft.TransparentPointer(
                content=ct1,
                expand=True,
            )
            page.add(
                ft.Stack(
                    [tp],
                    expand=True,
                )
            )
            page.update()
            exit()
        root_item = QRootItem.auto_init_page(page=page, wrap=True, wrap_colour="#2F2F2F")
        root_item.add_child(
            QItem(
                id="l1",
                width=lambda d: d.parent.width / 1,
                height=lambda d: d.parent.height / 1,
                bgcolour="#FFFFFF",
                children=(
                    QItem(
                        id="l2",
                        width=lambda d: d.parent.width / 2,
                        height=lambda d: d.parent.height / 2,
                        x=lambda d: d.width / 2,
                        y=lambda d: d.height / 2,
                        bgcolour="#FF0000",
                    ),
                ),
            )
        )
        root_item.compute()
        page.update()

    ft.app(target=main)
