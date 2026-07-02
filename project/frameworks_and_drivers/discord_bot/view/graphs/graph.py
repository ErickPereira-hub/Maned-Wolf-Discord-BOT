import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import Tuple, List

class Graph:

    BACKGROUND_COLOR: str = "#0E0E0E"
    FOREGROUND_COLOR: str = "#1B1B1B"
    WEAK_COLOR: str = "#138E92"
    STRONG_COLOR: str = "#14FFEC"
    EDGE_COLOR: str = "#FFFFFF"
    REPO_PATH: str = "project/img_repo"

    @classmethod
    def define_dark_style(cls) -> None:
        plt.style.use("dark_background")
        plt.rcParams["figure.facecolor"] = cls.BACKGROUND_COLOR
        plt.rcParams["axes.facecolor"] = cls.FOREGROUND_COLOR
    
    @classmethod
    def build_dist_poisson(cls, dataset: List[Tuple[int, float]], from_qtt: int, until_qtt: int, server_id: int, author_id: int, style: str = "members") -> None:
        qtts: List[int] = [data[0] for data in dataset]
        probs: List[float] = [100 * data[1] for data in dataset]
        range_qtt: List[int] = [qtt for qtt in range(from_qtt, until_qtt + 1)]
        range_prob: List[float] = probs[from_qtt : until_qtt + 1]
        cls.define_dark_style()
        plt.bar(qtts, probs, width = 1, color = cls.WEAK_COLOR, edgecolor = cls.EDGE_COLOR, linewidth = 2.5, zorder = 0)
        plt.bar(range_qtt, range_prob, width = 1, color = cls.STRONG_COLOR, edgecolor = cls.EDGE_COLOR, linewidth = 2.5, zorder = 1)
        plt.xlabel("quantity of entrances")
        plt.ylabel("Probability (%)")
        plt.savefig(cls.REPO_PATH + f"/{style}_{server_id}{author_id}_poisson.png", dpi = 150)
        plt.clf()