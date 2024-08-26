from __future__ import annotations
import random
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

    default_z = 0

    default_anchor_left = None
    default_anchor_top = None
    default_anchor_right = None
    default_anchor_bottom = None

    default_align_centre_x = 0
    default_align_centre_y = 0
    default_align_x = None
    default_align_y = None

    default_bgcolour = "#00000000"
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

    @staticmethod
    def default_ready_align_x(d: _ItemHandle) -> number:
        d.x, d.width, d.align_centre_x, d.parent.width
        return random.random()

    @staticmethod
    def default_ready_align_y(d: _ItemHandle) -> number:
        d.y, d.height, d.align_centre_y, d.parent.height
        return random.random()


class QItem(Item):
    DEFAULT_VALUES = QItemDefaultVals

    @Item.cached_classproperty
    def _RESERVED_PROPERTY_NAMES(cls) -> set[str]:
        return super()._RESERVED_PROPERTY_NAMES | {
            "align_centre_x", "align_centre_y", "align_x", "align_y",
            "anchor_bottom", "anchor_left", "anchor_right", "anchor_top",
            "bgcolour", "border_radius", "bottom",
            "clip_behaviour",
            "global_x", "global_y",
            "height",
            "implicit_height", "implicit_width",
            "left",
            "opacity",
            "ready_align_x", "ready_align_y",
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
            width: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_width,
            height: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_height,
            implicit_width: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_implicit_width,
            implicit_height: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_implicit_height,
            x: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_x,
            y: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_y,
            z: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_z,
            anchor_left: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_left,
            anchor_top: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_top,
            anchor_right: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_right,
            anchor_bottom: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_anchor_bottom,
            align_centre_x: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_align_centre_x,
            align_centre_y: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_align_centre_y,
            align_x: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_align_x,
            align_y: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_align_y,

            # appearance and transformation
            bgcolour: str | Callable[[_ItemHandle], str] = QItemDefaultVals.default_bgcolour,
            visible: bool | Callable[[_ItemHandle], bool] = QItemDefaultVals.default_visible,
            opacity: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_opacity,
            rotate_angle: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_rotate_angle,
            rotate_centre_x: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_rotate_centre_x,
            rotate_centre_y: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_rotate_centre_y,
            scale: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_scale,
            scale_centre_x: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_scale_centre_x,
            scale_centre_y: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_scale_centre_y,
            scale_x: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_scale_x,
            scale_y: optional_number | Callable[[_ItemHandle], optional_number] = QItemDefaultVals.default_scale_y,
            border_radius: number | Callable[[_ItemHandle], number] = QItemDefaultVals.default_border_radius,
            clip_behaviour: ft.ClipBehavior | Callable[[_ItemHandle], ft.ClipBehavior] = QItemDefaultVals.default_clip_behaviour,

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
        """
        # self._frame = ft.Stack(clip_behavior=ft.ClipBehavior.HARD_EDGE)
        self._frame = ft.Stack()

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
        self.z: number = z
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

        self.ready_align_x: number = QItemDefaultVals.default_ready_align_x
        self.ready_align_y: number = QItemDefaultVals.default_ready_align_y

    def _init_flet(self) -> None:
        self._container = ft.Container(
            content=self._frame,
            rotate=ft.Rotate(0, ft.Alignment(0, 0)),
            scale=ft.Scale(alignment=ft.Alignment(0, 0)),
        )
        self._l2_tr_pointer = ft.TransparentPointer(
            content=self._container,
        )
        self._l1_conainter = ft.Container(
            content=self._l2_tr_pointer,
            padding=ft.Padding(0, 0, 0, 0),
            alignment=ft.Alignment(0, 0),
        )
        self._root_component = ft.TransparentPointer(
            content=self._l1_conainter,
            data=self,
        )

    def _on_width_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] width: {self.width}")
        self._l2_tr_pointer.width = self.width
        self._l1_conainter.padding.left = -self.width / 2
        self._l1_conainter.padding.right = -self.width / 2

    def _on_height_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] height: {self.height}")
        self._l2_tr_pointer.height = self.height
        self._l1_conainter.padding.top = -self.height / 2
        self._l1_conainter.padding.bottom = -self.height / 2

    def _on_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] x: {self.x}")
        pass

    def _on_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] y: {self.y}")
        pass

    def _on_bgcolour_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] bgcolour: {self.bgcolour}")
        self._container.bgcolor = self.bgcolour

    def _on_visible_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] visible: {self.visible}")
        self._container.visible = self.visible

    def _on_opacity_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] opacity: {self.opacity}")
        self._container.opacity = self.opacity

    def _on_rotate_angle_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_angle: {self.rotate_angle}")
        self._container.rotate.angle = self.rotate_angle

    def _on_rotate_centre_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_centre_x: {self.rotate_centre_x}")
        self._container.rotate.alignment.x = self.rotate_centre_x

    def _on_rotate_centre_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] rotate_centre_y: {self.rotate_centre_y}")
        self._container.rotate.alignment.y = self.rotate_centre_y

    def _on_scale_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale: {self.scale}")
        self._container.scale.scale = self.scale

    def _on_scale_centre_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_centre_x: {self.scale_centre_x}")
        self._container.scale.alignment.x = self.scale_centre_x

    def _on_scale_centre_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_centre_y: {self.scale_centre_y}")
        self._container.scale.alignment.y = self.scale_centre_y

    def _on_scale_x_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_x: {self.scale_x}")
        self._container.scale.scale_x = self.scale_x

    def _on_scale_y_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] scale_y: {self.scale_y}")
        self._container.scale.scale_y = self.scale_y

    def _on_border_radius_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] border_radius: {self.border_radius}")
        self._container.border_radius = self.border_radius

    def _on_clip_behaviour_change(self) -> None:
        # print(f"{self.__class__.__name__}[{self.displayed_id}] clip_behaviour: {self.clip_behaviour}")
        self._container.clip_behavior = self.clip_behaviour

    def _on_ready_align_x_change(self) -> None:
        centre_x = self.x + self.width * (self.align_centre_x / 2 + 0.5)
        self._l1_conainter.alignment.x = (centre_x / self.parent.width - 0.5) * 2
    
    def _on_ready_align_y_change(self) -> None:
        centre_y = self.y + self.height * (self.align_centre_y / 2 + 0.5)
        self._l1_conainter.alignment.y = (centre_y / self.parent.height - 0.5) * 2

    def _on_children_computed(self) -> None:
        super()._on_children_computed()
        self._frame.controls.sort(key=lambda c: c.data.z)

    def add_child(self, new_child: QItem) -> None:
        super().add_child(new_child)
        self._frame.controls.append(new_child._root_component)


if __name__ == "__main__":
    from .q_root_item import QRootItem

    def main(page: ft.Page):
        page.padding = 0
        root_item = QRootItem.auto_init_page(page=page, wrap=True, wrap_colour="#2F2F2F")
        root_item.add_children([
            QItem(
                id="q",
                width=lambda d: d.parent.width,
                height=lambda d: d.parent.height,
                bgcolour="#7FFFFFFF",
                children=(
                    QItem(
                        id="q1",
                        width=lambda d: d.parent.width / 3,
                        height=lambda d: d.parent.height / 3,
                        bgcolour="#FFFFFF",
                        border_radius=lambda d: d.height / 5,
                        children=(
                            QItem(
                                id="q1_1",
                                width=lambda d: d.parent.width * 2,
                                height=lambda d: d.parent.height / 2,
                                bgcolour="#FF0000",
                            ),
                        ),
                    ),
                    QItem(
                        id="q2",
                        width=lambda d: d.parent.width * 0.85,
                        height=lambda d: d.parent.height * 0.1,
                        anchor_bottom=lambda d: d.parent.bottom,
                        anchor_left=lambda d: d.parent.left,
                        bgcolour="#00FF00",
                    ),
                ),
            ),
        ])
        root_item.compute()
        page.update()

    ft.app(target=main)
