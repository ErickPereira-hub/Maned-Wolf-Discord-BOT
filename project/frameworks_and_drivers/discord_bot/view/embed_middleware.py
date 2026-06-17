from discord import Embed, File
from typing import Tuple

def get_emb_without_author(
        title: str,
        desc: str,
        footer_txt: str,
        img_path: str
        ) -> Tuple[Embed, File]:
    emb: Embed = Embed()
    emb.title = title
    emb.description = desc
    emb.set_footer(text = footer_txt)
    name: str = img_path.split("/")[-1]
    emb.set_image(url = "attachment://" + name)
    file: File = File(img_path, filename = name)
    return emb, file