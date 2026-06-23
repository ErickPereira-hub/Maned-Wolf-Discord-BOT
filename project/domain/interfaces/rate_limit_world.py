from abc import ABC, abstractmethod

class RateLimitWorld(ABC):

    @abstractmethod
    def can_acces_api(self) -> bool: pass