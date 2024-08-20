from __future__ import annotations
from functools import partial
from typing import Callable, Sequence, TYPE_CHECKING

import flet as ft
from flet_core.control_event import ControlEvent

from .core.item import Item, _ItemHandle
from ._typing_shortcut import number


if TYPE_CHECKING:
    from .q_item import QItem


class QRootItem(Item):
    @Item.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "height",
            "width", "wrap", "wrap_colour",
        }

    def __init__(
            self,
            id: str | None = None,
            children: Item | Sequence[Item] = (),
            
            wrap: bool | Callable[[_ItemHandle], bool] = False,
            wrap_colour: str | Callable[[_ItemHandle], str] = "#FF000000",

            **kwargs
    ) -> None:
        self._frame = ft.Stack(expand=True)

        super().__init__(
            id, True, children,
            **kwargs,
        )

        self._page: ft.Page
        self._page_padding_l = 10
        self._page_padding_r = 10
        self._page_padding_t = 10
        self._page_padding_b = 10

        self._padding = ft.Padding(
            left=-self._page_padding_l,
            right=-self._page_padding_r,
            top=-self._page_padding_t,
            bottom=-self._page_padding_b,
        )

        self._root_component: ft.Stack
        self._container: ft.TransparentPointer
        self._init_flet()

        # Properties
        self.width: number = 10
        self.height: number = 10
        self.wrap: bool = wrap
        self.wrap_colour: str = wrap_colour

    def _init_flet(self) -> None:
        self._container = ft.TransparentPointer(
            content=ft.Container(
                content=self._frame,
                padding=self._padding,
            ),
            expand=True,
        )
        self._wrap_right_inner = ft.Container(expand=True)
        self._wrap_right = (
            ft.Container(
                content=self._wrap_right_inner,
                padding=ft.Padding(left=0, right=-10000, top=0, bottom=-10000),
            )
        )
        self._wrap_bottom_inner = ft.Container(expand=True)
        self._wrap_bottom = (
            ft.Container(
                content=self._wrap_bottom_inner,
                padding=ft.Padding(left=0, right=-10000, top=0, bottom=-10000),
            )
        )
        self._root_component = ft.Stack(
            controls=[
                self._container,
                self._wrap_right,
                self._wrap_bottom,
            ],
            expand=True,
        )

    def _on_width_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] width: {self.width}")
        pass

    def _on_height_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] height: {self.height}")
        pass

    def _on_wrap_change(self) -> None:
        self._wrap_right.visible = self.wrap
        self._wrap_bottom.visible = self.wrap

    def _on_wrap_colour_change(self) -> None:
        self._wrap_right_inner.bgcolor = self.wrap_colour
        self._wrap_bottom_inner.bgcolor = self.wrap_colour

    def __read_new_page_padding(self) -> bool:
        """ :returns: True if padding has changed. """
        if self._page.padding is None:
            ret_val = (
                self._page_padding_l != 10
                or self._page_padding_r != 10
                or self._page_padding_t != 10
                or self._page_padding_b != 10
            )
            self._page_padding_l = 10
            self._page_padding_r = 10
            self._page_padding_t = 10
            self._page_padding_b = 10
            return ret_val
        elif isinstance(self._page.padding, int | float):
            ret_val = (
                self._page_padding_l != self._page.padding
                or self._page_padding_r != self._page.padding
                or self._page_padding_t != self._page.padding
                or self._page_padding_b != self._page.padding
            )
            self._page_padding_l = self._page.padding
            self._page_padding_r = self._page.padding
            self._page_padding_t = self._page.padding
            self._page_padding_b = self._page.padding
            return ret_val
        elif isinstance(self._page.padding, ft.Padding):
            ret_val = (
                self._page_padding_l != self._page.padding.left
                or self._page_padding_r != self._page.padding.right
                or self._page_padding_t != self._page.padding.top
                or self._page_padding_b != self._page.padding.bottom
            )
            self._page_padding_l = self._page.padding.left
            self._page_padding_r = self._page.padding.right
            self._page_padding_t = self._page.padding.top
            self._page_padding_b = self._page.padding.bottom
            return ret_val
        else:
            raise TypeError(f"Unexpected padding type: {type(self._page.padding)}")

    def __apply_read_page_padding(self) -> None:
        self._padding.left = -self._page_padding_l
        self._padding.right = -self._page_padding_r
        self._padding.top = -self._page_padding_t
        self._padding.bottom = -self._page_padding_b

    def __on_page_resize(self, _: ControlEvent) -> None:
        self._wrap_right.padding.left = self._page.width - self._page_padding_l
        self._wrap_right.padding.top = -self._page_padding_t
        self._wrap_bottom.padding.left = -self._page_padding_l
        self._wrap_bottom.padding.top = self._page.height - self._page_padding_t

        self.width = self._page.width
        self.height = self._page.height
        self.compute()
        self._root_component.update()

    def add_child(self, new_child: QItem) -> None:
        super().add_child(new_child)
        self._frame.controls.append(new_child._root_component)

    def __on_update_monitor(self, update: Callable, *controls) -> None:
        if len(controls) == 0:
            if self.__read_new_page_padding():
                self.__apply_read_page_padding()
        update(*controls)

    @classmethod
    def auto_init_page(
            cls, page: ft.Page,
            id: str = "q_root_item",
            wrap: bool = False,
            wrap_colour: str = "#FF000000",
    ) -> QRootItem:
        """
        :param id: the id of the root item.
        :param wrap: whether to wrap the outer area of the root item with a colour.
        :param wrap_colour: the colour of the wrap.
        :returns: a root item attached to the page. Do not modify width, height of the root item.
        """
        item = QRootItem(id=id, wrap=wrap, wrap_colour=wrap_colour)
        item._page = page
        page.add(item._root_component)
        page.on_resize.subscribe(item.__on_page_resize)
        page.update = partial(item.__on_update_monitor, page.update)
        item.__read_new_page_padding()
        item.__apply_read_page_padding()
        item.__on_page_resize(None)
        return item

