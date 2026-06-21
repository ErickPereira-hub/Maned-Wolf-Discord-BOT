import matplotlib.pyplot as plt

class Graph:

    BACKGROUND_COLOR: str = "#0E0E0E"
    FOREGROUND_COLOR: str = "#1B1B1B"
    WEAK_COLOR: str = "#138E92"
    STRONG_COLOR: str = "#14FFEC"
    EDGE_COLOR: str = "#FFFFFF"

    @classmethod
    def define_dark_style(cls) -> None:
        plt.style.use("dark_background")
        plt.rcParams["figure.facecolor"] = cls.BACKGROUND_COLOR
        plt.rcParams["axes.facecolor"] = cls.FOREGROUND_COLOR