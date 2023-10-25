def run():
    from pyperclip import copy
    def capitalizeSentence(mark: str, prompt: str):
        prompt = prompt.split(mark)
        newText = []
        for index, sentence in enumerate(prompt):
            if sentence[0] == " ":
                sentence = " " +  sentence[1].upper() + sentence[2:]
            else:
                sentence = " " + sentence[0].upper() + sentence[1:]
            if index != len(sentence):
                sentence += mark
            newText.append(sentence)
        string =  ''.join(newText)
        return string

    prompt = input("sentence: ")
    if prompt == "<<<":
        return
    prompt = capitalizeSentence(".", prompt)
    prompt = capitalizeSentence("?", prompt)
    prompt = capitalizeSentence("!", prompt)
    prompt = prompt[:-3]
    prompt = prompt[1:]
    copy(prompt)
