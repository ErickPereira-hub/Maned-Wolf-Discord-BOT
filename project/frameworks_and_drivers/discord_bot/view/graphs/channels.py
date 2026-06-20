import matplotlib.pyplot as plt
from typing import List, Tuple
from project.frameworks_and_drivers.discord_bot.view.graphs.graph import Graph

class ChannelsGraph(Graph):

    REPO_PATH: str = "project/img_repo"

    @classmethod
    def build_top_ch_bars(cls, ch_names: List[str], msg_volume_per_channel: List[int], server_id: int, author_id: int) -> None:
        plt.style.use("dark_background")
        plt.rcParams["figure.facecolor"] = cls.BACKGROUND_COLOR
        plt.rcParams["axes.facecolor"] = cls.FOREGROUND_COLOR
        plt.bar(ch_names, msg_volume_per_channel, width = 1, color = cls.WEAK_COLOR, edgecolor = cls.EDGE_COLOR, linewidth = 2.5, zorder = 0)
        plt.xlabel("Channels")
        plt.ylabel("Message volume")
        plt.savefig(cls.REPO_PATH + f"/top_ch_{server_id}{author_id}.png", dpi = 150)
        plt.clf()