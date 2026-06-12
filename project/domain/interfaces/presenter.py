from abc import ABC, abstractmethod
from typing import Any

class Presenter(ABC):

    @abstractmethod
    def get_data(self) -> Any:
        pass