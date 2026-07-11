from random import randint

class TokenFactory:

    @classmethod
    def gen_token(cls, bytes: int = 8) -> str:
        hex_chars: str =  "0123456789abcdef"
        token: str = ""
        for _ in range(bytes):
            token += hex_chars[randint(0, 15)] + hex_chars[randint(0, 15)]
        return token

if __name__ == "__main__":
    print(TokenFactory.gen_token())