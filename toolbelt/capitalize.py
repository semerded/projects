import pyperclip
text = input().split(".")
newText = []
for part in text:
    newText.append(part.split("?"))
text = []
print(newText)
for part in newText:
    text.append(part.split("!"))
newText = ""
for sentence in newText:
    newText += sentence.capitalize() + " "
    
    
pyperclip.copy(newText)
