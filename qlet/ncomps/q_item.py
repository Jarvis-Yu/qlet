from __future__ import annotations
import random
from typing import Callable, Sequence

import flet as ft

from .core.item import Item, ItemHandle
from .core.colour import is_light
from ._typing_shortcut import number, optional_number


__all__ = ["QItem"]


class QItemDefaultVals:
    @staticmethod
    def default_width(d: ItemHandle) -> number:
        if d.anchor_left is not None and d.anchor_right is not None:
            return d.anchor_right - d.anchor_left
        elif d.expand:
            if d.anchor_left is not None:
                return d.parent.width - d.parent.padding_right - d.anchor_left
            elif d.anchor_right is not None:
                return d.anchor_right - d.parent.padding_left
            else:
                return d.parent.width - d.parent.padding_left - d.parent.padding_right
        return d.implicit_width

    @staticmethod
    def default_height(d: ItemHandle) -> number:
        if d.anchor_top is not None and d.anchor_bottom is not None:
            return d.anchor_bottom - d.anchor_top
        elif d.expand:
            if d.anchor_top is not None:
                return d.parent.height - d.parent.padding_bottom - d.anchor_top
            elif d.anchor_bottom is not None:
                return d.anchor_bottom - d.parent.padding_top
            else:
                return d.parent.height - d.parent.padding_top - d.parent.padding_bottom
        return d.implicit_height

    default_implicit_width = 10

    default_implicit_height = 10

    @staticmethod
    def default_x(d: ItemHandle) -> number:
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
    def default_y(d: ItemHandle) -> number:
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

    default_z = 0
    default_expand = False

    default_anchor_left = None
    default_anchor_top = None
    default_anchor_right = None
    default_anchor_bottom = None

    default_align_centre_x = 0
    default_align_centre_y = 0
    default_align_x = None
    default_align_y = None

    default_padding = 0
    default_padding_left = lambda d: d.padding
    default_padding_top = lambda d: d.padding
    default_padding_right = lambda d: d.padding
    default_padding_bottom = lambda d: d.padding

    default_visible = True
    default_opacity = 1.0
    default_rotate_angle = 0.0
    default_rotate_centre_x = 0.0
    default_rotate_centre_y = 0.0
    default_scale = None
    default_scale_centre_x = 0.0
    default_scale_centre_y = 0.0
    default_scale_x = None
    default_scale_y = None
    default_border_radius = 0
    default_clip_behaviour = ft.ClipBehavior.NONE

    default_global_x = lambda d: d.parent.global_x + d.x
    default_global_y = lambda d: d.parent.global_y + d.y
    default_left = lambda d: d.global_x
    default_top = lambda d: d.global_y
    default_right = lambda d: d.global_x + d.width
    default_bottom = lambda d: d.global_y + d.height

    @staticmethod
    def default_READY_align_x(d: ItemHandle) -> number:
        d.x, d.width, d.parent.width
        d.padding_left, d.padding_right
        return random.random()

    @staticmethod
    def default_READY_align_y(d: ItemHandle) -> number:
        d.y, d.height, d.parent.height
        d.padding_top, d.padding_bottom
        return random.random()


DEFAULT_VALUES = QItemDefaultVals


class QItem(Item):
    DEFAULT_VALUES = QItemDefaultVals

    @Item.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "align_centre_x", "align_centre_y", "align_x", "align_y",
            "anchor_bottom", "anchor_left", "anchor_right", "anchor_top",
            "border_radius", "bottom",
            "clip_behaviour",
            "expand",
            "global_x", "global_y",
            "height",
            "implicit_height", "implicit_width",
            "left",
            "opacity",
            "padding", "padding_bottom", "padding_left", "padding_right", "padding_top",
            "READY_align_x", "READY_align_y", "READY_border_horizontal", "READY_border_vertical",
            "right", "rotate_angle", "rotate_centre_x", "rotate_centre_y",
            "scale", "scale_centre_x", "scale_centre_y", "scale_x", "scale_y",
            "top",
            "visible",
            "width",
            "x",
            "y",
            "z",
        }

    def __init__(
            self,
            id: str | None = None,
            children: Item | Sequence[Item] = (),
            
            # position and sizing
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

            # appearance and transformation
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
        self._root_component: ft.Stack
        self._content_container: ft.Container
        self._init_flet()

        super().__init__(
            id, False, children,
            **kwargs,
        )

        self.width: number = width
        self.height: number = height
        self.implicit_width: number = implicit_width
        self.implicit_height: number = implicit_height
        self.x: number = x
        self.y: number = y
        self.z: number = z
        self.expand: bool = expand
        self.anchor_left: optional_number = anchor_left
        self.anchor_top: optional_number = anchor_top
        self.anchor_right: optional_number = anchor_right
        self.anchor_bottom: optional_number = anchor_bottom
        self.align_centre_x: number = align_centre_x
        self.align_centre_y: number = align_centre_y
        self.align_x: number = align_x
        self.align_y: number = align_y
        self.padding: number = padding
        self.padding_left: number = padding_left
        self.padding_top: number = padding_top
        self.padding_right: number = padding_right
        self.padding_bottom: number = padding_bottom

        self.visible: bool = visible
        self.opacity: number = opacity
        self.rotate_angle: number = rotate_angle
        self.rotate_centre_x: number = rotate_centre_x
        self.rotate_centre_y: number = rotate_centre_y
        self.scale: optional_number = scale
        self.scale_centre_x: number = scale_centre_x
        self.scale_centre_y: number = scale_centre_y
        self.scale_x: optional_number = scale_x
        self.scale_y: optional_number = scale_y
        self.border_radius: number = border_radius
        self.clip_behaviour: ft.ClipBehavior = clip_behaviour

        self.global_x: number = QItemDefaultVals.default_global_x
        self.global_y: number = QItemDefaultVals.default_global_y
        self.left: number = QItemDefaultVals.default_left
        self.top: number = QItemDefaultVals.default_top
        self.right: number = QItemDefaultVals.default_right
        self.bottom: number = QItemDefaultVals.default_bottom

        self.READY_align_x: number = QItemDefaultVals.default_READY_align_x
        self.READY_align_y: number = QItemDefaultVals.default_READY_align_y

    def _init_flet(self) -> None:
        self._content_container = ft.Container(
            content=self._frame,
            rotate=ft.Rotate(0, ft.Alignment(0, 0)),
            scale=ft.Scale(alignment=ft.Alignment(0, 0)),
        )
        self._l2_content_tr_pointer = ft.TransparentPointer(
            content=self._content_container,
        )
        self._l1_content_conainter = ft.Container(
            content=self._l2_content_tr_pointer,
            padding=ft.Padding(0, 0, 0, 0),
            alignment=ft.Alignment(0, 0),
        )
        self._l1_content_tr_pointer = ft.TransparentPointer(
            content=self._l1_content_conainter,
        )
        self._root_component = ft.Stack(
            controls=[
                self._l1_content_tr_pointer,
            ],
            data=self,
        )

    def _on_width_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] width: {self.width}")
        pass

    def _on_height_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] height: {self.height}")
        pass

    def _on_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] x: {self.x}")
        pass

    def _on_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] y: {self.y}")
        pass

    def _on_visible_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] visible: {self.visible}")
        self._root_component.visible = self.visible

    def _on_opacity_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] opacity: {self.opacity}")
        self._root_component.opacity = self.opacity
        # self._content_container.opacity = self.opacity

    def _on_rotate_angle_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_angle: {self.rotate_angle}")
        self._content_container.rotate.angle = self.rotate_angle

    def _on_rotate_centre_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_centre_x: {self.rotate_centre_x}")
        self._content_container.rotate.alignment.x = self.rotate_centre_x

    def _on_rotate_centre_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_centre_y: {self.rotate_centre_y}")
        self._content_container.rotate.alignment.y = self.rotate_centre_y

    def _on_scale_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale: {self.scale}")
        self._content_container.scale.scale = self.scale

    def _on_scale_centre_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_centre_x: {self.scale_centre_x}")
        self._content_container.scale.alignment.x = self.scale_centre_x

    def _on_scale_centre_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_centre_y: {self.scale_centre_y}")
        self._content_container.scale.alignment.y = self.scale_centre_y

    def _on_scale_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_x: {self.scale_x}")
        self._content_container.scale.scale_x = self.scale_x

    def _on_scale_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_y: {self.scale_y}")
        self._content_container.scale.scale_y = self.scale_y

    def _on_border_radius_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] border_radius: {self.border_radius}")
        self._content_container.border_radius = self.border_radius

    def _on_clip_behaviour_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] clip_behaviour: {self.clip_behaviour}")
        self._content_container.clip_behavior = self.clip_behaviour

    def _on_READY_align_x_change(self) -> None:
        width = self.width - self.padding_left - self.padding_right
        self._l2_content_tr_pointer.width = width
        self._l1_content_conainter.padding.left = -width / 2
        self._l1_content_conainter.padding.right = -width / 2

        original_centre_x = self.x + self.padding_left + 0.5 * width
        parent_width = self.parent.width - self.parent.padding_left - self.parent.padding_right
        align_x = (original_centre_x / parent_width) * 2 - 1
        self._l1_content_conainter.alignment.x = align_x
    
    def _on_READY_align_y_change(self) -> None:
        height = self.height - self.padding_top - self.padding_bottom
        self._l2_content_tr_pointer.height = height
        self._l1_content_conainter.padding.top = -height / 2
        self._l1_content_conainter.padding.bottom = -height / 2

        original_centre_y = self.y + self.padding_top + 0.5 * height
        parent_height = self.parent.height - self.parent.padding_top - self.parent.padding_bottom
        align_y = (original_centre_y / parent_height) * 2 - 1
        self._l1_content_conainter.alignment.y = align_y

    def _on_children_computed(self) -> None:
        super()._on_children_computed()
        def safe_z(control: ft.Control) -> number:
            return control.data.z if hasattr(control.data, "z") else 0
        self._frame.controls.sort(key=safe_z)

    def add_child(self, new_child: QItem) -> None:
        super().add_child(new_child)
        self._frame.controls.append(new_child._root_component)
