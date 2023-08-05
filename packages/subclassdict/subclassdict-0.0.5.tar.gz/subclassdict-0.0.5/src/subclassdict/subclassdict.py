from typedict import TypeDict
from typing import Any, Hashable


class HashableType(Hashable, type):
    ...


class SubclassDict(TypeDict):
    def __getitem__(self, value: HashableType) -> Any:
        try:
            return super().__getitem__(value)
        except KeyError as e:
            super_key = self._get_super_key(value)
            if super_key is not None:
                return super().__getitem__(super_key)
            raise e

    def __setitem__(self, key: HashableType, value: Any) -> None:
        try:
            super().__getitem__(key)
        except KeyError as e:
            super_key = self._get_super_key(key)
            if super_key is not None:
                super().__setitem__(super_key, value)
                return
        super().__setitem__(key, value)
        
    def _get_super_key(self, value) -> HashableType | None:
        for key in self.keys():
            if issubclass(value, key):
                return key
        return None
