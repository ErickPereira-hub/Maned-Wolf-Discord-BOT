import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from typing import List, Dict
from project.frameworks_and_drivers.discord_bot.view.graphs.graph import Graph
from project.application.utils.max_str_size import get_max_str_size

class MembersGraph(Graph):

    @classmethod
    def build_curve_qtt(cls, days: List[str], qtts: List[int], server_id: int, author_id: int) -> None:
        days_eq: List[int] = [pos + 1 for pos in range(len(days))]
        cls.define_dark_style()
        plt.plot(days_eq, qtts, color = cls.WEAK_COLOR, linewidth = 2) #<--- Plotting the graph
        plt.xlabel("Time (days)")
        plt.ylabel("Quantity of members")
        plt.savefig(cls.REPO_PATH + f"/members_{server_id}{author_id}.png", dpi = 150)
        plt.clf()

    @classmethod
    def build_top_members(cls, dataset: List[Dict[str, int]], server_id: int, author_id: int, option: str) -> None:
        cls.define_dark_style()
        plt.pie(
            x = [list(data.values())[0] for data in dataset],
            labels = [f"[ {list(data.values())[0]} ]  " + get_max_str_size(list(data.keys())[0]) for data in dataset],
            colors = [cls.WEAK_COLOR, cls.STRONG_COLOR, "#62FFBE", "#41FFD0", "#14BCFF"]
        )
        plt.savefig(cls.REPO_PATH + f"/best_members_by_{option}_{server_id}{author_id}.png")
        plt.clf()