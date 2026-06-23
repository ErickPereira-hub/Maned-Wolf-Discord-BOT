from abc import ABC, abstractmethod
from typing import Any

class CacheAside(ABC):

    @abstractmethod
    def fetch_cache(self) -> Any: pass

    @abstractmethod
    def insert_into_cache(self) -> None: pass

    @abstractmethod
    def exists_in_cache(self) -> bool: pass