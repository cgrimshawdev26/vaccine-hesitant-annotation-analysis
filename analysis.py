import pandas as pd
import glob
from sklearn.metrics import cohen_kappa_score
from collections import Counter

csvs = []
for file in glob.glob("*.csv"):
    csvs.append(file)

users = []
for csv in csvs:
    users.append(pd.read_csv(csv))

users3Con = []
for user in users:
    users3Con.append(user[user[user.columns[5]]>3])

users5Con = []
for user in users:
    users5Con.append(user[user[user.columns[5]]==5])

f = open("results.txt", "w")

i=1
f.write("***Statistics***\n\n")
for user in users:
    f.write("User " + str(i) + " " + user.columns[3].split(".")[1] + "\n")
    i += 1

    f.write("Sum: " + str(user.shape[0]) + "\n")

    userPro=user[user[user.columns[3]]==1]
    f.write("Pro-Vaccine: " + str(userPro.shape[0]) + "\n")

    userAnti=user[user[user.columns[3]]==2]
    f.write("Anti-Vaccine: " + str(userAnti.shape[0]) + "\n")

    userHesi=user[user[user.columns[3]]==3]
    f.write("Hesitant: " + str(userHesi.shape[0]) + "\n")

    userIrr=user[user[user.columns[3]]==4]
    f.write("Irrelevant: " + str(userIrr.shape[0]) + "\n")

    f.write("\n")

mergedUsers = []
for i in range(0, len(users)):
    for x in range(i+1, len(users)):
        mergedUsers.append(users[i].merge(users[x], on='text'))

f.write("\n***Cohen Kappa Score***\n\n")

f.write("***ALL***\n\n")
y = 0
for i in range(0, len(users)):
    for x in range(i+1, len(users)):
        labeler1 = mergedUsers[y][users[i].columns[3]]
        labeler2 = mergedUsers[y][users[x].columns[3]]
        y += 1

        f.write(users[i].columns[3].split(".")[1] + " & " + users[x].columns[3].split(".")[1] + ": " + str(cohen_kappa_score(labeler1, labeler2)))
        f.write("\n")
f.write("\n")

mergedUsers3Con = []
for i in range(0, len(users3Con)):
    for x in range(i+1, len(users3Con)):
        mergedUsers3Con.append(users3Con[i].merge(users3Con[x], on='text'))

f.write("***Confidence Score > 3***\n\n")
y = 0
for i in range(0, len(users)):
    for x in range(i+1, len(users)):
        labeler1 = mergedUsers3Con[y][users[i].columns[3]]
        labeler2 = mergedUsers3Con[y][users[x].columns[3]]
        y += 1

        f.write(users[i].columns[3].split(".")[1] + " & " + users[x].columns[3].split(".")[1] + ": " + str(cohen_kappa_score(labeler1, labeler2)))
        f.write("\n")

mergedUsers5Con = []
for i in range(0, len(users5Con)):
    for x in range(i+1, len(users5Con)):
        mergedUsers5Con.append(users5Con[i].merge(users5Con[x], on='text'))
    
f.write("\n")

f.write("***Confidence Score = 5***\n\n")
y = 0
for i in range(0, len(users)):
    for x in range(i+1, len(users)):
        labeler1 = mergedUsers5Con[y][users[i].columns[3]]
        labeler2 = mergedUsers5Con[y][users[x].columns[3]]
        y += 1

        f.write(users[i].columns[3].split(".")[1] + " & " + users[x].columns[3].split(".")[1] + ": " + str(cohen_kappa_score(labeler1, labeler2)))
        f.write("\n")

f.write("\n\n")

f.write("***How the users agreed***\n")
y = 0
for i in range(0, len(users)):
    for x in range(i+1, len(users)):
        agree = []

        a1 = mergedUsers[y][users[i].columns[3]]
        a2 = mergedUsers[y][users[i].columns[7]]

        b1 = mergedUsers[y][users[x].columns[3]]
        b2 = mergedUsers[y][users[x].columns[7]]

        for z in range(0,mergedUsers[y].shape[0]):
            if a1[z] == b1[z] or a1[z] == b2[z] or a2[z] == b1[z] or a2[z] == b2[z]:
                agree.append(1)        
            else:
                agree.append(0)

        f.write(users[i].columns[3].split(".")[1] + " & " + users[x].columns[3].split(".")[1] + "\n")
        f.write("Sum: " + str(len(agree)) + "\n")
        f.write("Agree: " + str(Counter(agree)[1])+ "\n")
        f.write("Disagree: " + str(Counter(agree)[0])+ "\n\n")
        y+=1
    