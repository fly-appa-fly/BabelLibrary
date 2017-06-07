import re
import codecs

text = "I'm \n 123, 33 ssf, "

print(re.findall(r"\w+|[^\w\s]", text, re.UNICODE))

f = codecs.open('Mereźi_komputerovi.txt', 'r', "utf_8_sig")
text = f.read()

word = ''
prev_alpha = False
start = True
symbols = ''
words = []


for i in text:
    if (i.isalpha() or i.isdigit()) and prev_alpha:
        word += i
    elif (i.isalpha() or i.isdigit()) and not prev_alpha:
        if not start:
            words.append([word, symbols])
        else:
            start = False
        prev_alpha = True
        word = '' + i
        symbols = ''
    elif not (i.isalpha() or i.isdigit()) and prev_alpha:
        symbols += i
        prev_alpha = False
    else:
        symbols += i
else:
    words.append([word, symbols])

print(words)