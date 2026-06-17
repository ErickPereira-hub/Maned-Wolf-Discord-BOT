import matplotlib.pyplot as plt
from project.domain.interfaces.graphs_interface.curve_interface import GraphCurveInterface
from typing import List

class MembersGraph(GraphCurveInterface):

    REPO_PATH: str = "project/img_repo"
    
    @classmethod
    def build_curve(cls, days: List[str], qtts: List[int], server_id: int) -> None:
        days_eq: List[int] = [pos + 1 for pos in range(len(days))]
        plt.style.use("dark_background") #<--- setting the style of the graph
        plt.plot(days_eq, qtts, color = "#86BBFF", linewidth = 2) #<--- Plotting the graph
        plt.xlabel("Time (days)")
        plt.ylabel("Quantity of members")
        plt.savefig(cls.REPO_PATH + f"/members_{server_id}.png", dpi = 150)