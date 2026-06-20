def get_max_str_size(txt: str, max_s = 12) -> str:
    size: int = len(txt)
    if size > max_s:
        new_txt: str = ""
        for char_pos in range(max_s):
            new_txt += txt[char_pos]
        new_txt += "..."
        return new_txt
    return txt