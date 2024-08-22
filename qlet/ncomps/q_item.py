from __future__ import annotations
from typing import Callable, Sequence

import flet as ft

from .core.item import Item, _ItemHandle
from ._typing_shortcut import number, optional_number


__all__ = ["QItem"]


class QItemDefaultVals:
    @staticmethod
    def default_width(d: _ItemHandle) -> number:
        if (
                d.anchor_left is not None
                and d.anchor_right is not None
        ):
            return d.anchor_right - d.anchor_left
        return d.implicit_width

    @staticmethod
    def default_height(d: _ItemHandle) -> number:
        if (
                d.anchor_top is not QItemDefaultVals.default_top
                and d.anchor_bottom is not QItemDefaultVals.default_bottom
        ):
            return d.anchor_bottom - d.anchor_top
        return d.implicit_height

    default_implicit_width = 10

    default_implicit_height = 10

    @staticmethod
    def default_x(d: _ItemHandle) -> number:
        if d.anchor_left is not None:
            return d.anchor_left - d.parent.global_x
        elif d.anchor_right is not None:
            return d.anchor_right - d.width - d.parent.global_x
        if d.align_x is not None:
            align_x = d.align_x / 2 + 0.5
            align_centre_x = d.align_centre_x / 2 + 0.5
            centre_offset = align_centre_x * d.width
            off_set = align_x * d.parent.width
            return off_set - centre_offset
        return 0

    @staticmethod
    def default_y(d: _ItemHandle) -> number:
        if d.anchor_top is not None:
            return d.anchor_top - d.parent.global_y
        elif d.anchor_bottom is not None:
            return d.anchor_bottom - d.height - d.parent.global_y
        if d.align_y is not None:
            align_y = d.align_y / 2 + 0.5
            align_centre_y = d.align_centre_y / 2 + 0.5
            centre_offset = align_centre_y * d.height
            off_set = align_y * d.parent.height
            return off_set - centre_offset
        return 0

    default_anchor_left = None
    default_anchor_top = None
    default_anchor_right = None
    default_anchor_bottom = None

    default_align_centre_x = 0
    default_align_centre_y = 0
    default_align_x = None
    default_align_y = None

    default_bgcolour = "#00000000"

    @staticmethod
    def default_global_x(d: _ItemHandle) -> number:
        return d.parent.global_x + d.x

    @staticmethod
    def default_global_y(d: _ItemHandle) -> number:
        return d.parent.global_y + d.y

    @staticmethod
    def default_left(d: _ItemHandle) -> number:
        return d.global_x

    @staticmethod
    def default_top(d: _ItemHandle) -> number:
        return d.global_y

    @staticmethod
    def default_right(d: _ItemHandle) -> number:
        return d.global_x + d.width
    
    @staticmethod
    def default_bottom(d: _ItemHandle) -> number:
        return d.global_y + d.height


class QItem(Item):
    DEFAULT_VALUES = QItemDefaultVals

    @Item.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "align_centre_x", "align_centre_y", "align_x", "align_y",
            "anchor_bottom", "anchor_left", "anchor_right", "anchor_top",
            "bgcolour", "bottom",
            "global_x", "global_y",
            "height",
            "implicit_height", "implicit_width",
            "left",
            "right",
            "top",
            "visible",
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
            anchor_left: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_left,
            anchor_top: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_top,
            anchor_right: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_right,
            anchor_bottom: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_bottom,
            align_centre_x: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_align_centre_x,
            align_centre_y: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_align_centre_y,
            align_x: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_align_x,
            align_y: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_align_y,

            # appearance
            bgcolour: str | Callable[[_ItemHandle], str] = QItemDefaultVals.default_bgcolour,
            visible: bool | Callable[[_ItemHandle], bool] = True,

            **kwargs
    ) -> None:
        """
        :param id: The id of the item, used to reference the item by its peers or offspring.
        :param children: The children of the item, which are items that are contained within the item.
        :param width: The width of the item.
        :param height: The height of the item.
        :param implicit_width: The width of the item if width is not defined by any means.
        :param implicit_height: The height of the item if height is not defined by any means.
        :param x: The x coordinate of the item.
        :param y: The y coordinate of the item.
        :param anchor_left: The global x coordinate of the left side of the item.
        :param anchor_top: The global y coordinate of the top side of the item.
        :param anchor_right: The global x coordinate of the right side of the item.
        :param anchor_bottom: The global y coordinate of the bottom side of the item.
        :param align_centre_x: The centre of alignment of the item on the x axis. -1 to 1 from left to right.
        :param align_centre_y: The centre of alignment of the item on the y axis. -1 to 1 from top to bottom.
        :param align_x: The alignment of the item in its parent. -1 to 1 from left to right.
        :param align_y: The alignment of the item in its parent. -1 to 1 from top to bottom.
        :param bgcolour: The background colour of the item.
        """
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
        self.anchor_left: optional_number = anchor_left
        self.anchor_top: optional_number = anchor_top
        self.anchor_right: optional_number = anchor_right
        self.anchor_bottom: optional_number = anchor_bottom
        self.align_centre_x: number = align_centre_x
        self.align_centre_y: number = align_centre_y
        self.align_x: number = align_x
        self.align_y: number = align_y

        self.bgcolour: str = bgcolour
        self.visible: bool = visible

        self.global_x: number = QItemDefaultVals.default_global_x
        self.global_y: number = QItemDefaultVals.default_global_y
        self.left: number = QItemDefaultVals.default_left
        self.top: number = QItemDefaultVals.default_top
        self.right: number = QItemDefaultVals.default_right
        self.bottom: number = QItemDefaultVals.default_bottom

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
        # print(f"{self.__class__.__name__}[{self.displayed_id}] bgcolour: {self.bgcolour}")
        self._container.bgcolor = self.bgcolour

    def _on_visible_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] visible: {self.visible}")
        self._container.visible = self.visible

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
        root_item.add_children((
            QItem(
                id="l1",
                width=lambda d: d.parent.width / 1,
                height=lambda d: d.parent.height / 1,
                bgcolour="#FFFFFF",
                children=(
                    QItem(
                        id="l1_1",
                        width=lambda d: d.parent.width / 2,
                        height=lambda d: d.parent.height / 2,
                        x=lambda d: d.width / 2,
                        y=lambda d: d.height / 2,
                        bgcolour="#FF0000",
                        children=(
                            QItem(
                                id="l1_1_1",
                                width=lambda d: d.parent.width / 2,
                                height=lambda d: d.parent.height / 2,
                                x=lambda d: d.width / 2,
                                y=lambda d: d.height / 2,
                                bgcolour="#00FF00",
                                visible=lambda d: d.width > 50,
                            )
                        ),
                    ),
                    QItem(
                        id="l1_2",
                        width=lambda d: d.parent.width / 2,
                        anchor_right=lambda d: d.parent.right,
                        anchor_top=lambda d: d.l1_1.bottom,
                        anchor_bottom=lambda d: d.parent.bottom,
                        bgcolour="#00FF00",
                    ),
                    QItem(
                        id="l1_3",
                        width=lambda d: d.parent.width / 4,
                        height=lambda d: d.parent.height / 4,
                        align_centre_x=0.5,
                        align_centre_y=0.5,
                        align_x=1,
                        align_y=1,
                        bgcolour="#0000FF",
                    )
                ),
            ),
        ))
        root_item.compute()
        page.update()

    ft.app(target=main)