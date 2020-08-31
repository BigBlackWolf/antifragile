from collections import Counter
import plotly.express as ps
import pandas as pd
import csv
import re

with open("/home/buch/keylogger_storage.txt", "r") as f:
    data = f.read()

res = re.split(r"\d+\-\d+\-\d+", data)[1:]
dates = re.findall(r"\d+\-\d+\-\d+", data)
c = dict(zip(dates, res))

counter = Counter()
for i in c.items():
    d = i[1].split(",")
    counter += Counter(d)

counter = [{"letter": k, "counter": v} for k, v in counter.items()]

with open("/home/buch/keylogger_storage.csv", 'w') as f:
    header = ["letter", "counter"]
    writer = csv.DictWriter(f, header)
    writer.writeheader()
    writer.writerows(counter)

dataset = pd.read_csv("/home/buch/keylogger_storage.csv")
dataset = dataset.sort_values("counter", ascending=True)

fig = ps.bar(dataset, x="letter", y="counter")
fig.show()
