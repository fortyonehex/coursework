import json

with open("qn.txt") as a:
    k = a.read().split("\n")

s = 0
j = 0
entries = []
entry = {}
passage = []
questions = []
for l in k:
    print(l)
    if s == 0:
        if l != "": passage.append("\t"+l)
        else: s+= 1
    elif s == 1:
        if l != "":
            if j%5 == 0:
                questions.append([l])
            else:
                questions[-1].append(l)
            j += 1
        else: s+= 1
    elif s == 2:
        if l != "":
            for i in range(len(l)):
                questions[i].append(ord(l[i])-0x41)
        else:
            entry = {"passage": "\n".join(passage), "questions": [
                {"question": i[0], "options": i[1:5], "answer": i[5]} for i in questions
            ]}
            entries.append(entry)
            entry = {}
            passage = []
            questions = []
            s = 0

print(entries)
json.dump(entries, open("targeted.json", "w"))