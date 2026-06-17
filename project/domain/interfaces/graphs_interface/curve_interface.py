from abc import ABC, abstractmethod

class GraphCurveInterface(ABC):

    @abstractmethod
    def build_curve(self) -> None: pass