from pyperclip import copy

comment = input("give your comment: ")
comment = "# " + comment.strip() + " #"
bigComment = f"{"#" * len(comment)}\n{comment}\n{"#" * len(comment)}" 
copy(bigComment)

