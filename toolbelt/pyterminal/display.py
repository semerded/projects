def title(text: str, decoration: str | None = "#"):
    if decoration != None:
        textLength = len(text)
        print(decoration * (textLength + 4))
        print(f"{decoration} {text} {decoration}")
        print(decoration * (textLength + 4))
        
    else:
        print(text)
    print("\n") # add 2 newlines
    