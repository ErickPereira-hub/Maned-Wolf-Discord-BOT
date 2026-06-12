class BaseEntity:

    @staticmethod
    def empty_is_none(txt: str) -> None | str:
        if not isinstance(txt, str):
            raise TypeError("The input must be a string!")
        return txt if txt != "" else None