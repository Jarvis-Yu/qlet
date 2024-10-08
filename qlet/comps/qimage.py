import flet as ft

from .qitem import QItem

__all__ = ["QImage"]

class QImage(QItem):
    def __init__(
            self,
            src: str = "",
            border_radius: float | int | None = None,
            fit: ft.ImageFit = ft.ImageFit.COVER,
            **kwargs,
        ):
        """
        :param src: The source of the image.
        :param border_radius: The border radius of the image.
        :param fit: The fit of the image.
        :param kwargs: Additional arguments to pass to the QItem constructor.
        """
        self._image = ft.Image(src=src, border_radius=border_radius, fit=fit)
        super().__init__(border_radius=border_radius, **kwargs)
        self._image.width = self.width
        self._image.height = self.height
        self.add_flet_comp(self._image)
    
    def _on_resized(self) -> None:
        super()._on_resized()
        self._image.width = self.width
        self._image.height = self.height
