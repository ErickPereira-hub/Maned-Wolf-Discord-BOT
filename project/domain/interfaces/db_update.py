from abc import ABC, abstractmethod

class DatabaseUpdate(ABC):

    @abstractmethod
    def update_in_db(self) -> None:
        pass