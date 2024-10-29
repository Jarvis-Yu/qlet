from __future__ import annotations
import random
from typing import Callable, Sequence

import flet as ft

from .core.item import Item, ItemHandle
from .core.colour import is_light
from ._typing_shortcut import number, optional_number
from .q_item import QItem


__all__ = ["QRect"]


class QRectDefaultVals(QItem.DEFAULT_VALUES):
    default_inset = 0
    default_inset_left = lambda d: d.inset
    default_inset_top = lambda d: d.inset
    default_inset_right = lambda d: d.inset
    default_inset_bottom = lambda d: d.inset

    default_bgcolour = "#00000000"
    default_border_width = 0
    default_border_colour = lambda d: "#000000" if is_light(d.bgcolour) else "#FFFFFF"
    default_border_width_left = lambda d: d.border_width
    default_border_colour_left = lambda d: d.border_colour
    default_border_width_top = lambda d: d.border_width
    default_border_colour_top = lambda d: d.border_colour
    default_border_width_right = lambda d: d.border_width
    default_border_colour_right = lambda d: d.border_colour
    default_border_width_bottom = lambda d: d.border_width
    default_border_colour_bottom = lambda d: d.border_colour

    @staticmethod
    def default_READY_bg_align_x(d: ItemHandle) -> number:
        d.x, d.width, d.parent.width
        d.inset_left, d.inset_right
        return random.random()

    @staticmethod
    def default_READY_bg_align_y(d: ItemHandle) -> number:
        d.y, d.height, d.parent.height
        d.inset_top, d.inset_bottom
        return random.random()

    @staticmethod
    def default_READY_border_horizontal(d: ItemHandle) -> number:
        d.width
        d.border_width_left, d.border_width_right, d.border_colour_left, d.border_colour_right
        return random.random()

    @staticmethod
    def default_READY_border_vertical(d: ItemHandle) -> number:
        d.height
        d.border_width_top, d.border_width_bottom, d.border_colour_top, d.border_colour_bottom
        return random.random()


DEFAULT_VALUES = QRectDefaultVals


class QRect(QItem):
    DEFAULT_VALUES = QRectDefaultVals

    @QItem.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "bgcolour", "border_colour", "border_colour_bottom", "border_colour_left",
            "border_colour_right", "border_colour_top", "border_width", "border_width_bottom",
            "border_width_left", "border_width_right", "border_width_top",
            "inset", "inset_bottom", "inset_left", "inset_right", "inset_top",
            "READY_border_horizontal", "READY_border_vertical",
            "READY_bg_align_x", "READY_bg_align_y",
        }

    def __init__(
            self,
            id: str | None = None,
            children: Item | Sequence[Item] = (),
            
            # position and sizing
            inset: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset,
            inset_left: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_left,
            inset_top: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_top,
            inset_right: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_right,
            inset_bottom: number | Callable[[ItemHandle], number] = DEFAULT_VALUES.default_inset_bottom,

            # appearance and transformation
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
        self._bg_frame = ft.Stack()
        self._bg_container: ft.Container

        super().__init__(
            id, children,
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

        self.inset: number = inset
        self.inset_left: number = inset_left
        self.inset_top: number = inset_top
        self.inset_right: number = inset_right
        self.inset_bottom: number = inset_bottom

        self.bgcolour: str = bgcolour
        self.border_width: number = border_width
        self.border_colour: str = border_colour
        self.border_width_left: number = border_width_left
        self.border_colour_left: str = border_colour_left
        self.border_width_top: number = border_width_top
        self.border_colour_top: str = border_colour_top
        self.border_width_right: number = border_width_right
        self.border_colour_right: str = border_colour_right
        self.border_width_bottom: number = border_width_bottom
        self.border_colour_bottom: str = border_colour_bottom

        self.READY_bg_align_x: number = QRectDefaultVals.default_READY_bg_align_x
        self.READY_bg_align_y: number = QRectDefaultVals.default_READY_bg_align_y
        self.READY_border_horizontal: number = QRectDefaultVals.default_READY_border_horizontal
        self.READY_border_vertical: number = QRectDefaultVals.default_READY_border_vertical

    def _init_flet(self) -> None:
        super()._init_flet()
        self._bg_container = ft.Container(
            content=self._bg_frame,
            border=ft.Border(),
            rotate=ft.Rotate(0, ft.Alignment(0, 0)),
            scale=ft.Scale(alignment=ft.Alignment(0, 0)),
        )
        self._l2_bg_tr_pointer = ft.TransparentPointer(
            content=self._bg_container,
        )
        self._l1_bg_conainter = ft.Container(
            content=self._l2_bg_tr_pointer,
            padding=ft.Padding(0, 0, 0, 0),
            alignment=ft.Alignment(0, 0),
        )
        self._l1_bg_tr_pointer = ft.TransparentPointer(
            content=self._l1_bg_conainter,
        )

        self._root_component.controls.insert(0, self._l1_bg_tr_pointer)

    def _on_bgcolour_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] bgcolour: {self.bgcolour}")
        self._bg_container.bgcolor = self.bgcolour

    def _on_rotate_angle_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_angle: {self.rotate_angle}")
        super()._on_rotate_angle_change()
        self._bg_container.rotate.angle = self.rotate_angle

    def _on_rotate_centre_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_centre_x: {self.rotate_centre_x}")
        super()._on_rotate_centre_x_change()
        self._bg_container.rotate.alignment.x = self.rotate_centre_x

    def _on_rotate_centre_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_centre_y: {self.rotate_centre_y}")
        super()._on_rotate_centre_y_change()
        self._bg_container.rotate.alignment.y = self.rotate_centre_y

    def _on_scale_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale: {self.scale}")
        super()._on_scale_change()
        self._bg_container.scale.scale = self.scale

    def _on_scale_centre_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_centre_x: {self.scale_centre_x}")
        super()._on_scale_centre_x_change()
        self._bg_container.scale.alignment.x = self.scale_centre_x

    def _on_scale_centre_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_centre_y: {self.scale_centre_y}")
        super()._on_scale_centre_y_change()
        self._bg_container.scale.alignment.y = self.scale_centre_y

    def _on_scale_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_x: {self.scale_x}")
        super()._on_scale_x_change()
        self._bg_container.scale.scale_x = self.scale_x

    def _on_scale_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_y: {self.scale_y}")
        super()._on_scale_y_change()
        self._bg_container.scale.scale_y = self.scale_y

    def _on_border_radius_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] border_radius: {self.border_radius}")
        super()._on_border_radius_change()
        self._bg_container.border_radius = self.border_radius

    def _on_clip_behaviour_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] clip_behaviour: {self.clip_behaviour}")
        super()._on_clip_behaviour_change()
        self._bg_container.clip_behavior = self.clip_behaviour

    def _on_READY_bg_align_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] READY_bg_align_x: {self.x=}, {self.width=}")
        width = self.width - self.inset_left - self.inset_right
        self._l2_bg_tr_pointer.width = width
        self._l1_bg_conainter.padding.left = -width / 2
        self._l1_bg_conainter.padding.right = -width / 2

        original_centre_x = self.x + self.inset_left + 0.5 * width
        parent_width = self.parent.width - self.parent.padding_left - self.parent.padding_right
        align_x = (original_centre_x / parent_width) * 2 - 1
        self._l1_bg_conainter.alignment.x = align_x

    def _on_READY_bg_align_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] READY_bg_align_y: {self.y=}, {self.height=}")
        height = self.height - self.inset_top - self.inset_bottom
        self._l2_bg_tr_pointer.height = height
        self._l1_bg_conainter.padding.top = -height / 2
        self._l1_bg_conainter.padding.bottom = -height / 2

        original_centre_y = self.y + self.inset_top + 0.5 * height
        parent_height = self.parent.height - self.parent.padding_top - self.parent.padding_bottom
        align_y = (original_centre_y / parent_height) * 2 - 1
        self._l1_bg_conainter.alignment.y = align_y

    def _on_READY_border_horizontal_change(self) -> None:
        border_width_left = self.border_width_left if self.border_width_left > 0 else 0
        border_width_right = self.border_width_right if self.border_width_right > 0 else 0
        horizontal_total = border_width_left + border_width_right
        if horizontal_total > self.width:
            # scale down border widths to fit within the width
            border_width_left = border_width_left * self.width / horizontal_total
            border_width_right = border_width_right * self.width / horizontal_total

        if border_width_left <= 0:
            self._bg_container.border.left = None
        else:
            self._bg_container.border.left = ft.BorderSide(border_width_left, self.border_colour_left)
        if border_width_right <= 0:
            self._bg_container.border.right = None
        else:
            self._bg_container.border.right = ft.BorderSide(border_width_right, self.border_colour_right)
    
    def _on_READY_border_vertical_change(self) -> None:
        border_width_top = self.border_width_top if self.border_width_top > 0 else 0
        border_width_bottom = self.border_width_bottom if self.border_width_bottom > 0 else 0
        vertical_total = border_width_top + border_width_bottom
        if vertical_total > self.height:
            border_width_top = border_width_top * self.height / vertical_total
            border_width_bottom = border_width_bottom * self.height / vertical_total
        if border_width_top <= 0:
            self._bg_container.border.top = None
        else:
            self._bg_container.border.top = ft.BorderSide(border_width_top, self.border_colour_top)
        if border_width_bottom <= 0:
            self._bg_container.border.bottom = None
        else:
            self._bg_container.border.bottom = ft.BorderSide(border_width_bottom, self.border_colour_bottom)


if __name__ == "__main__":
    from .q_root_item import QRootItem

    def main(page: ft.Page):
        page.padding = 0
        root_item = QRootItem.auto_init_page(page=page, wrap=True, wrap_colour="#00CC00")
        root_item.add_children([
            QRect(
                id="q",
                width=lambda d: d.parent.width,
                height=lambda d: d.parent.height,
                bgcolour="#7FFFFFFF",
                children=[
                    QRect(
                        id="q1",
                        width=lambda d: d.parent.width / 3,
                        height=lambda d: d.parent.height / 3,
                        x = 50,
                        y = 50,
                        bgcolour="#000000",
                        border_radius=lambda d: d.height / 5,
                        children=[
                            QRect(
                                id="q1_1",
                                width=lambda d: d.parent.width * 0.8,
                                height=lambda d: d.parent.height * 0.8,
                                bgcolour="#FF0000",
                                border_width=30,
                                border_width_left=-20,
                                border_width_right=10,
                                border_radius=10,
                                children=[
                                    QRect(
                                        id="q1_1_1",
                                        width=lambda d: 50,
                                        height=lambda d: 50,
                                        bgcolour="#0000FF",
                                        align_centre_x=-1,
                                        align_centre_y=-1,
                                        align_x=-1,
                                        align_y=1,
                                        padding=15,
                                        children=[
                                            QRect(
                                                id="q1_1_1_1",
                                                expand=True,
                                                opacity=0.5,
                                                inset=5,
                                                bgcolour="#FFFFFF",
                                                children=[
                                                    QRect(
                                                        id="q1_1_1_1_1",
                                                        expand=True,
                                                        opacity=0.3,
                                                        bgcolour="#000000",
                                                    ),
                                                ],
                                            ),
                                        ],
                                    ),
                                ],
                            ),
                        ],
                    ),
                    QRect(
                        id="q2",
                        width=lambda d: d.parent.width * 0.85,
                        height=lambda d: d.parent.height * 0.1,
                        anchor_bottom=lambda d: d.parent.bottom,
                        anchor_left=lambda d: d.parent.left,
                        bgcolour="#00FF00",
                        children=[
                            QRect(
                                id="q2_1",
                                anchor_left=lambda d: d.parent.left + 50,
                                expand=True,
                                bgcolour="#3FFF00FF",
                            ),
                        ],
                    ),
                ],
            ),
            QRect(
                id="other_q",
                width=lambda d: d.parent.width * 0.4,
                height=lambda d: d.parent.height * 0.6,
                x=100,
                y=100,
                bgcolour="#00FF00",
                opacity=0.3,
            ),
        ])
        root_item.compute()
        page.update()

    ft.app(target=main)
