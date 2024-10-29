from __future__ import annotations
import random
from typing import Callable, Literal, Sequence

import flet as ft

from .core.item import Item, ItemHandle
from .core.colour import contrast_bw
from ._typing_shortcut import number, optional_number
from .q_rect import QRect


__all__ = ["QText"]


class QTextDefaultVals(QRect.DEFAULT_VALUES):
    default_text = "example text"
    default_text_colour = lambda d: contrast_bw(d.bgcolour)
    default_text_alignment = "left"


DEFAULT_VALUES = QTextDefaultVals


QTextAlign = Literal["left", "right", "centre", "justify", "start", "end"]


class QText(QRect):
    DEFAULT_VALUES = QTextDefaultVals

    @QRect.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "text", "text_colour", "text_alignment",
        }

    def __init__(
            self,
            id: str | None = None,
            children: Item | Sequence[Item] = (),
            
            text: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_text,
            text_colour: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_text_colour,
            text_alignment: QTextAlign | Callable[[ItemHandle], QTextAlign] = DEFAULT_VALUES.default_text_alignment,

            # from super: QRect
            inset: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset,
            inset_left: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_left,
            inset_top: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_top,
            inset_right: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_right,
            inset_bottom: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_bottom,
            bgcolour: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_bgcolour,
            border_width: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_border_width,
            border_colour: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_border_colour,
            border_width_left: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_border_width_left,
            border_colour_left: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_border_colour_left,
            border_width_top: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_border_width_top,
            border_colour_top: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_border_colour_top,
            border_width_right: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_border_width_right,
            border_colour_right: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_border_colour_right,
            border_width_bottom: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_border_width_bottom,
            border_colour_bottom: str | Callable[[ItemHandle], str] = DEFAULT_VALUES.default_border_colour_bottom,

            # from super: QItem
            width: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_width,
            height: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_height,
            implicit_width: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_implicit_width,
            implicit_height: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_implicit_height,
            x: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_x,
            y: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_y,
            z: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_z,
            expand: bool | Callable[[ItemHandle], bool] = DEFAULT_VALUES.default_expand,
            anchor_left: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_anchor_left,
            anchor_top: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_anchor_top,
            anchor_right: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_anchor_right,
            anchor_bottom: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_anchor_bottom,
            align_centre_x: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_align_centre_x,
            align_centre_y: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_align_centre_y,
            align_x: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_align_x,
            align_y: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_align_y,
            padding: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_padding,
            padding_left: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_padding_left,
            padding_top: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_padding_top,
            padding_right: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_padding_right,
            padding_bottom: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_padding_bottom,
            visible: bool | Callable[[ItemHandle], bool] = DEFAULT_VALUES.default_visible,
            opacity: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_opacity,
            rotate_angle: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_rotate_angle,
            rotate_centre_x: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_rotate_centre_x,
            rotate_centre_y: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_rotate_centre_y,
            scale: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_scale,
            scale_centre_x: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_scale_centre_x,
            scale_centre_y: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_scale_centre_y,
            scale_x: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_scale_x,
            scale_y: optional_number | Callable[[ItemHandle], optional_number] = DEFAULT_VALUES.default_scale_y,
            border_radius: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_border_radius,
            clip_behaviour: ft.ClipBehavior | Callable[[ItemHandle], ft.ClipBehavior] = DEFAULT_VALUES.default_clip_behaviour,

            **kwargs
    ) -> None:
        """
        :param id: The id of the item, used to reference the item by its peers or offspring.
        :param children: The children of the item, which are items that are contained within the item.

        :param bgcolour: The background colour of the item.
        :param border_width: The border width of the item.
        :param border_colour: The border colour of the item.
        :param border_width_left: The border width of the left side of the item.
        :param border_colour_left: The border colour of the left side of the item.
        :param border_width_top: The border width of the top side of the item.
        :param border_colour_top: The border colour of the top side of the item.
        :param border_width_right: The border width of the right side of the item.
        :param border_colour_right: The border colour of the right side of the item.
        :param border_width_bottom: The border width of the bottom side of the item.
        :param border_colour_bottom: The border colour of the bottom side of the item.

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
        :param padding: The padding for all child items.
        :param padding_left: The padding for the left side of the item.
        :param padding_top: The padding for the top side of the item.
        :param padding_right: The padding for the right side of the item.
        :param padding_bottom: The padding for the bottom side of the item.
        :param visible: Whether the item is visible.
        :param opacity: The opacity of the item (affects children opacity).
        :param rotate_angle: The angle of rotation of the item.
        :param rotate_centre_x: The centre of rotation of the item on the x axis. -1 to 1 from left to right.
        :param rotate_centre_y: The centre of rotation of the item on the y axis. -1 to 1 from top to bottom.
        :param scale: The scale of the item.
        :param scale_centre_x: The centre of scaling of the item on the x axis. -1 to 1 from left to right.
        :param scale_centre_y: The centre of scaling of the item on the y axis. -1 to 1 from top to bottom.
        :param scale_x: The scale of the item on the x axis.
        :param scale_y: The scale of the item on the y axis.
        :param border_radius: The border radius of the item.
        :param clip_behaviour: The clip behaviour of the item.
        """
        self._frame = ft.Stack()
        self._ft_text = ft.Text()
        self._bg_container: ft.Container
        self._content_container: ft.Container
        self._ft_text: ft.Text

        super().__init__(
            id, children,

            inset=inset, inset_left=inset_left, inset_top=inset_top, inset_right=inset_right, inset_bottom=inset_bottom,
            border_width=border_width, border_colour=border_colour,
            border_width_left=border_width_left, border_colour_left=border_colour_left,
            border_width_top=border_width_top, border_colour_top=border_colour_top,
            border_width_right=border_width_right, border_colour_right=border_colour_right,
            border_width_bottom=border_width_bottom, border_colour_bottom=border_colour_bottom,

            width=width, height=height, implicit_width=implicit_width, implicit_height=implicit_height,
            x=x, y=y, z=z, expand=expand, anchor_left=anchor_left, anchor_top=anchor_top,
            anchor_right=anchor_right, anchor_bottom=anchor_bottom, align_centre_x=align_centre_x,
            align_centre_y=align_centre_y, align_x=align_x, align_y=align_y, padding=padding,
            padding_left=padding_left, padding_top=padding_top, padding_right=padding_right,
            padding_bottom=padding_bottom, visible=visible, opacity=opacity, rotate_angle=rotate_angle,
            rotate_centre_x=rotate_centre_x, rotate_centre_y=rotate_centre_y, scale=scale,
            scale_centre_x=scale_centre_x, scale_centre_y=scale_centre_y, scale_x=scale_x, scale_y=scale_y,
            border_radius=border_radius, clip_behaviour=clip_behaviour, bgcolour=bgcolour,

            **kwargs,
        )

        self.text = text
        self.text_colour = text_colour

    def _init_flet(self) -> None:
        super()._init_flet()
        self._bg_container.content = ft.TransparentPointer(
            ft.Container(
                self._ft_text,
                alignment=ft.Alignment(0, 0),
            ),
        )

    def _on_text_change(self) -> None:
        self._ft_text.value = self.text

    def _on_text_colour_change(self) -> None:
        self._ft_text.color = self.text_colour

    __TEXT_ALIGN_MAP = {
        "left": ft.TextAlign.LEFT,
        "right": ft.TextAlign.RIGHT,
        "centre": ft.TextAlign.CENTER,
        "justify": ft.TextAlign.JUSTIFY,
        "start": ft.TextAlign.START,
        "end": ft.TextAlign.END,
    }
    def _on_text_alignment_change(self) -> None:
        self._ft_text.text_align = self.__TEXT_ALIGN_MAP.get(self.text_alignment, None)


if __name__ == "__main__":
    from .q_root_item import QRootItem
    from .q_rect import QRect

    def main(page: ft.Page):
        page.padding = 0
        root_item = QRootItem.auto_init_page(page=page, wrap=True, wrap_colour="#2F2F2F")
        root_item.add_children([
            QRect(
                id="r1",
                expand=True,
                bgcolour="#777777",
                children=[
                    QText(
                        id="r1_t1",
                        text="Hello, World!",
                        text_alignment="centre",

                        width=20,
                        height=20,
                        align_x=0,
                        align_y=0,
                        border_colour="#FF0000",
                        border_width=1,
                        children=[
                            QRect(
                                id="r1_t1_r1",
                                width=50,
                                height=50,
                                bgcolour="#11000000",
                            ),
                        ],
                    ),
                ],
            ),
        ])
        root_item.compute()
        page.update()

    ft.app(target=main)
