from doctest import Example
import json
import re

JPN_LETTERS = "一-龯ぁ-んァ-ン０-９"
first_letter_jpn = re.compile(f"^[{JPN_LETTERS}]")

def format(s):
    # formatting the ** part 
    s = re.sub("\*(.*)\*", "<u>\\1</u>", s)
    # HTML 
    s = s.replace("\n", "<br>")
    # escape doublequote to use doublequotes in ANKI
    s = s.replace('"', '""')
    return s

if __name__ == "__main__":
    with open("flashcards.txt") as r:
        text = r.read()
    flashcards = json.loads(text)["flashcards"]
    cards = [json.loads(card["value"]) for card in flashcards]   
    print(len(cards)) 
    lines = ""
    for card in cards:
        front = card["jp"]
        # Remove .mp3 file
        example = re.sub("{! .* !}", "",card["ex"])
        vi = card["vi"]
        # If it has hatsuon at first
        if first_letter_jpn.match(vi):
            vi = vi.split("\n")
            back = "\n".join(vi[1:])
            hatsuon = vi[0]
        else:
            back = vi
            hatsuon = ""
        line = "\"{front}\",\"{back}\",\"{example}\",\"{hatsuon}\",\"{add_reverse}\"".format(**{
            "front": format(front),
            "back": format(back),
            "example": format(example),
            "hatsuon": format(hatsuon),
            "add_reverse": "y"
        })
        lines += line + "\n"
    with open("import.csv", "w", encoding="utf-8") as w:
        w.write(lines)
