from pyperclip import copy
import msvcrt

commentPrefixes = ("#", "//")
commentFills = ("#", "/")



while True:
    print("1. Python comment (#)")
    print("2. slash comment (//)")
    # TODO add more comment support (example: html)
    
    prompt = msvcrt.getch()
    try:
        prompt = int(prompt)
    except ValueError:
        continue
    if prompt in range(1,3):
        break
    
    
commentPrefix = commentPrefixes[prompt - 1]
commentFill = commentFills[prompt - 1]

comment = input("give your comment: ")
comment = f"{commentPrefix} {comment.strip()} {commentPrefix}"
bigComment = f"{commentFill * len(comment)}\n{comment}\n{commentFill * len(comment)}" 
copy(bigComment)

