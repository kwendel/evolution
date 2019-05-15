import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt


import glob



def read_last_line(file):
    try:
        with open(file) as f:
            lines = f.readlines()
            return lines[-1]
    except FileNotFoundError as e:
        print(e)


def compare_popsize(settings):
    experiments = '../experiments/'

    ps = [2, 10, 100]
    result = {}

    for p in ps:
        result[p] = []
        runs = glob.glob(f"{experiments}log_p{p}{settings}_run*.txt")

        for r in runs:
            ct = ''
            if 'OnePoint' in r:
                ct = 0
            elif 'Uniform' in r:
                ct = 1

            data = read_last_line(r).split(sep=" ")
            result[p].append({
                'gen': data[0],
                'evals': data[1],
                'time': data[2],
                'best_fitness': data[3],
                'ct': ct
            })
        result[p] = pd.DataFrame(result[p])

    return result


def plot_popsize(dfs, y='gen',yname='Number of generations', runs=1):
    plt.style.use('seaborn-darkgrid')
    fig = plt.figure() #figsize=(13,10), dpi=100)
    pallete = plt.get_cmap('tab10')

    ps = []
    avg_one = []
    avg_uni = []
    for p, df in dfs.items():
        ps.append(p)
        avg_one.append(df[df['ct'] == 0][y].mean())
        avg_uni.append(df[df['ct'] == 1][y].mean())
        plt.scatter(np.full(runs,fill_value=p), df[y], color=pallete(df['ct']) )

    # plt.plot(ps, avg_one, color=pallete(0))
    # plt.plot(ps, avg_uni, color=pallete(1))

    plt.title("Plot")
    plt.xlim(left=2)
    plt.ylabel(yname)
    plt.xlabel("Population size")
    plt.show()




if __name__ == '__main__':
    res = compare_popsize("_m8_k10_d0.0_cOnePoint")
    plot_popsize(res, y='gen')
