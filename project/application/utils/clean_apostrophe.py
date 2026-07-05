def clean_apostrophe(input: str, replace_by: str = "!") -> str:
    
    if not isinstance(input, str): return input

    output: str = ""
    
    for char in input:
        if char == "'" or char == '"' or char == "`":
            output += replace_by
            continue
        output += char
    
    return output

if __name__ == "__main__":
    print(clean_apostrophe(None))