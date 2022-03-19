import csv
import glob
import sys
import traceback

import matplotlib.pyplot as plt
import numpy as np
from scipy.optimize import curve_fit


def motor_model(arg, J, B, C):
    p, t = arg
    return (p-C)/B*(t+J/B*(np.exp(-B/J*t)-1))


def main():
    if len(sys.argv) > 1:
        dirname = sys.argv[1]
    else:
        dirname = input("ディレクトリ名を指定してください")
    print(dirname+'/*.csv')

    all_filepass = glob.glob(dirname+'/*.csv', recursive=True)
    if not len(all_filepass):
        print(dirname+"にCSVファイルがありません。ディレクトリを確かめてください。")
        exit()
    for file_path in all_filepass:
        print(file_path)
    print(len(all_filepass), "個のファイルを確認")

    fig = plt.figure(figsize=(8, 8))
    ax = fig.add_subplot(111, projection='3d')

    fitting_data = [[], [], []]  # fitting用。すべてのデータ点の情報をまとめる。

    # ファイルオープン
    for file_path in all_filepass:
        try:
            with open(file_path) as f:
                data = np.array([[float(value) for value in row]
                                for row in csv.reader(f)]).T
                for i in range(3):
                    fitting_data[i].extend(data[i])  # すべての点を1つの配列にまとめる
                ax.scatter(data[0], data[1], data[2], s=5)  # Plot登録
        except Exception:
            traceback.print_exc()
            print(file_path, "でエラーが発生しました")
            exit()
    '''
        Scipyのフィッティング関数。
        第一引数：関数
        第二引数：関数の引数（二つ以上はタプルで渡す）
        第三引数：実際の値。関数によって出た値をこれに近づける。
        bounds=各パラメーターの下限上限
    '''
    popt, pcov = curve_fit(
        motor_model, (fitting_data[0], fitting_data[1]), fitting_data[2], bounds=(0, np.inf))
    print("パラメーターは[J,B,C]=", popt)

    # 解曲面のPlot
    P, T = np.meshgrid(
        np.linspace(min(fitting_data[0]), max(fitting_data[0]), 20),
        np.linspace(min(fitting_data[1]), max(fitting_data[1]), 20)
    )
    Omega = motor_model((P, T), *popt)
    ax.plot_surface(P, T, Omega, cmap="summer", alpha=0.5)
    plt.show()


if __name__ == '__main__':
    main()
