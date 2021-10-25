import csv
import json
import os
import random
import sys

import matplotlib.pyplot as plt
import numpy as np


def create_test_data(T, p, J, B, C):
    return max(0, p-C)/B*(T+J/B*(np.exp(-B/J*T)-1))


def main():
    random.seed()
    if len(sys.argv) > 1:
        filename = sys.argv[1]
    else:
        filename = input("ファイル名を指定してください")

    try:
        file = open(filename, mode='r')
        params = json.load(file)
    except Exception:
        print("ファイルの読み込みに失敗しました。ファイルが正しく指定されているか、指定のJSON形式であるかを確認してください")
        exit()

    lines = []

    try:
        t = np.linspace(params["t"]["start"], params["t"]
                        ["stop"], params["t"]["num"])
        p = np.linspace(params["p"]["start"], params["p"]
                        ["stop"], params["p"]["num"])
        for i in range(params["p"]["num"]*params["num"]):
            J = params["J"]["value"] + \
                np.random.normal(0, params["J"]["variance"])
            B = params["B"]["value"] + \
                np.random.normal(0, params["B"]["variance"])
            C = params["C"]["value"] + \
                np.random.normal(0, params["C"]["variance"])
            omega = create_test_data(t, p[i//params["num"]], J, B, C)
            plt.plot(t, omega)
            lines.append({"t": t, "omega": omega, "p": p[i//params["num"]]})
        plt.show()
    except Exception:
        print("テストデータの作成に失敗しました。JSON形式を確かめてください")
        exit()

    try:
        if not os.path.exists("./test_data"):
            os.mkdir("./test_data")
        for i in range(params["p"]["num"]*params["num"]):
            file_name = "test_data/data"+str(i)+"_p="+str(lines[i]["p"])+".csv"
            with open(file_name, 'w', newline="") as f:
                writer = csv.writer(f)
                writer.writerows(
                    np.array([
                        [lines[i]["p"]]*len(lines[i]["t"]),
                        lines[i]["t"],
                        lines[i]["omega"]
                    ]).T.tolist()
                )
    except Exception:
        print("データの保存に失敗しました")
        exit()


if __name__ == '__main__':
    main()
