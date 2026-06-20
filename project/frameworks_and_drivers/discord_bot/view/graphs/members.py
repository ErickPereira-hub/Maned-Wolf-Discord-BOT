import matplotlib.pyplot as plt
from project.domain.interfaces.graphs_interface.curve_interface import GraphCurveInterface
from typing import List, Tuple

class MembersGraph(GraphCurveInterface):

    REPO_PATH: str = "project/img_repo"
    
    @classmethod
    def build_curve_qtt(cls, days: List[str], qtts: List[int], server_id: int, author_id: int) -> None:
        days_eq: List[int] = [pos + 1 for pos in range(len(days))]
        plt.style.use("dark_background") #<--- setting the style of the graph
        plt.plot(days_eq, qtts, color = "#86BBFF", linewidth = 2) #<--- Plotting the graph
        plt.xlabel("Time (days)")
        plt.ylabel("Quantity of members")
        plt.savefig(cls.REPO_PATH + f"/members_{server_id}{author_id}.png", dpi = 150)
        plt.clf()
    
    @classmethod
    def build_dist_poisson(cls, dataset: List[Tuple[int, float]], from_qtt: int, until_qtt: int, server_id: int, author_id: int) -> None:
        qtts: List[int] = [data[0] for data in dataset]
        probs: List[float] = [100 * data[1] for data in dataset]
        range_qtt: List[int] = [qtt for qtt in range(from_qtt, until_qtt + 1)]
        range_prob: List[float] = probs[from_qtt : until_qtt + 1]
        plt.style.use("dark_background")
        plt.bar(qtts, probs, width = 1, color = "#86BBFF", edgecolor = "#AFF6FF", linewidth = 2.5, zorder = 0)
        plt.bar(range_qtt, range_prob, width = 1, color = "#A100C9", edgecolor = "#AFF6FF", linewidth = 2.5, zorder = 1)
        plt.xlabel("quantity of entrances")
        plt.ylabel("Probability (%)")
        plt.savefig(cls.REPO_PATH + f"/members_{server_id}{author_id}_poisson.png", dpi = 150)
        plt.clf()