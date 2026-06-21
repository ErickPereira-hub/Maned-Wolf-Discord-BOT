import matplotlib.pyplot as plt
from typing import List, Tuple
from project.frameworks_and_drivers.discord_bot.view.graphs.graph import Graph

class ChannelsGraph(Graph):

    REPO_PATH: str = "project/img_repo"

    @classmethod
    def build_top_ch_bars(cls, ch_names: List[str], msg_volume_per_channel: List[int], server_id: int, author_id: int) -> None:
        cls.define_dark_style()
        plt.bar(ch_names, msg_volume_per_channel, width = 1, color = cls.WEAK_COLOR, edgecolor = cls.EDGE_COLOR, linewidth = 2.5, zorder = 0)
        plt.xlabel("Channels")
        plt.ylabel("Message volume")
        plt.savefig(cls.REPO_PATH + f"/top_ch_{server_id}{author_id}.png", dpi = 150)
        plt.clf()
    
    @classmethod
    def build_cat_pie(cls, txt_ch_qtt: int, voice_ch_qtt: int, server_id: int, author_id: int) -> None:
        cls.define_dark_style()
        plt.pie(
            x = [txt_ch_qtt, voice_ch_qtt],
            labels = [f"Text Channels {(100 * txt_ch_qtt / (txt_ch_qtt + voice_ch_qtt)):.2f} %",f"Voice Channels {(100 * voice_ch_qtt / (txt_ch_qtt + voice_ch_qtt)):.2f} %"],
            colors = [cls.WEAK_COLOR, cls.STRONG_COLOR])
        plt.savefig(cls.REPO_PATH + f"/channels_cat_{server_id}{author_id}.png")
        plt.clf()
    
    @classmethod
    def build_nsfw_pie(cls, yes_ch_qtt: int, no_ch_qtt: int, server_id: int, author_id: int) -> None:
        cls.define_dark_style()
        plt.pie(
            x = [yes_ch_qtt, no_ch_qtt],
            labels = [f"NSFW Channels\n {(100 * yes_ch_qtt / (no_ch_qtt + yes_ch_qtt)):.2f} %",f"Non NSFW Channels\n {(100 * no_ch_qtt / (no_ch_qtt + yes_ch_qtt)):.2f} %"],
            colors = [cls.WEAK_COLOR, cls.STRONG_COLOR])
        plt.savefig(cls.REPO_PATH + f"/channels_nsfw_{server_id}{author_id}.png")
        plt.clf()