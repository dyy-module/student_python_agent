with open("t.txt", "w", encoding="utf-8") as f:
    f.writelines(["第一行",8, "第二行", "\n第三行\n"])
# 再读回逐行打印
with open("t.txt", "r", encoding="utf-8") as f:
    for line in f:
        print(line)