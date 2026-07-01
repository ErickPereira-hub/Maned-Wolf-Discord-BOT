from typing import List

def get_date_in_EN(date: str) -> str:
    pieces: List[str] = date.split("-")
    new_date: str = pieces[1] + "/" + pieces[2] + "/" + pieces[0]
    return new_date

if __name__ == "__main__":
    print(get_date_in_EN("2010-02-12"))