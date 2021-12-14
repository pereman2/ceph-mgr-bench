import json
import matplotlib.pyplot as plt
import sys


if len(sys.argv) < 3:
    raise Error("Missing arguments, python plot.py num_labels data_length data_path")
num_labels = int(sys.argv[1])
data_length = int(sys.argv[2])
path = sys.argv[3]

from typing import List, Dict

def get_data(path) -> Dict[str, List[dict]]:
    res = {}
    with open(path, 'r') as f:
        lines = f.read().split("\n")
    p = 0
    for i in range(num_labels):
        label = lines[p]
        p += 1
        data = []
        for j in range(data_length):
            splitted_line = lines[p].split(";")
            print(splitted_line[1])
            data.append({
                    "num_osds": int(splitted_line[0]),
                    "stats": json.loads(splitted_line[1])
                    })
            p += 1
        res[label] = data
    return res

style = {
        "PyFormatter current implementation": {
            "color": "black",
            "linestyle": "solid"
            },
        "PyFormatter with pickle copy": {
            "color": "red",
            "linestyle": "solid"
            },
        "PyFormatter with pickle copy cached": {
            "color": "red",
            "linestyle": "dashed"
            },
        "JSONFormatter with json deserialization": {
            "color": "blue",
            "linestyle": "solid"
            },
        "JSONFormatter with json deserialization cached": {
            "color": "blue",
            "linestyle": "dashed"
            },
        "MsgpackFormatter": {
            "color": "yellow",
            "linestyle": "solid"
            },
        "MsgpackFormatter cached": {
            "color": "yellow",
            "linestyle": "dashed"
            },

}
def plot_simple(path: str, data_dict: Dict[str, List[dict]]) -> None:
    fig = plt.figure()
    ax = plt.axes()
    # ax.set_title("Time te retrieve pg_stats from the mgr module")
    # ax.set_ylabel("Seconds")
    # ax.set_xlabel("Pgs")
    ax.set_title("Time to retrieve osdmap")
    ax.set_ylabel("Seconds")
    ax.set_xlabel("Number of osds")
    legend = []
    for label, data in data_dict.items():
        x = []
        y = []
        legend.append(label)
        for line in data:
            x.append(line["num_osds"])
            y.append(line["stats"]["avg"] )
        print(label.split())
        ax.plot(x, y, marker='o', linestyle=style[label]["linestyle"], color=style[label]["color"])
    x1, x2, y1, y2 = plt.axis()
    # set max y
    # plt.axis((x1, x2, 0, 10))
    ax.legend(legend)
    fig.savefig(path)

# data format
# label
# data_length lines of csv

data: Dict[str, List[dict]] = get_data(path)
plot_simple("simple.png", data)
