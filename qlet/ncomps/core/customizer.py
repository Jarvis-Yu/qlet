from abc import ABC, abstractmethod
from warnings import warn

from .item import Item

class ItemCustomizer(ABC):
    @abstractmethod
    def item(self, **kwargs) -> Item:
        pass

    def __call__(
            self,
            id: str | None = None,
            **kwargs,
    ) -> Item:
        if "adopt_id" in kwargs:
            warn("adopt_id should not be passed as a keyword argument.")
            del kwargs["adopt_id"]
        item = self.item(**kwargs)
        assert item._adopt_id is None, "Item should not have been adopted yet."
        if id is not None:
            item._adopt_id = id
        else:
            item._adopt_id = item.id
        return item
