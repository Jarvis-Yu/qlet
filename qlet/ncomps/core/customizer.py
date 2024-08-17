from abc import ABC, abstractmethod
from warnings import warn

from .item import Item, _PARENT, _SELF

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
            assert id not in {_PARENT, _SELF}
            assert not id.startswith("_"), f"id cannot start with '_': {id}"
            assert not id.endswith("_"), f"id cannot end with '_': {id}"
            assert id.isidentifier(), f"id is not a valid identifier: {id}"
            item._adopt_id = id
        else:
            item._adopt_id = item.id
        return item
