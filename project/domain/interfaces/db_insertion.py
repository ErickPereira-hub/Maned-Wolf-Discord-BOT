from abc import ABC, abstractmethod

class DatabaseInsertion(ABC):

    @abstractmethod
    def send_to_db(self) -> None:
        pass