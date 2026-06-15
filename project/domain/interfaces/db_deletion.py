from abc import ABC, abstractmethod

class DatabaseDeletion(ABC):

    @abstractmethod
    def del_in_db(self) -> None:
        pass