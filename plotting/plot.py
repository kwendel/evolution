import seaborn as sns
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

import glob

experiments = '../experiments/'


def read_last_line(file):
    try:
        with open(file) as f:
            lines = f.readlines()
            return lines[-1]
    except FileNotFoundError as e:
        print(e)


def read_file(name):
    ct = -1
    if 'OnePoint' in name:
        ct = 0
    elif 'Uniform' in name:
        ct = 1

    data = read_last_line(name).replace("\n", "").split(sep=" ")
    result = {
        'gen': int(data[0]),
        'evals': int(data[1]),
        'time': int(data[2]),
        'best_fitness': float(data[3]),
        'ct': ct
    }

    return result


def read_popsize(settings):
    result = {}

    for p in settings['p']:
        result[p] = []
        runs = glob.glob(f"{experiments}log_p{p}_m{settings['m']}_k{settings['k']}_d{settings['d']}_c*_run*.txt")

        for r in runs:
            result[p].append(read_file(r))
        result[p] = pd.DataFrame(result[p])

    return result


def plot_popsize(runs=10, settings={}, y='gen', yname='Number of generations', title='Title'):
    dfs = read_popsize(settings)
    ps = settings['p']

    plt.style.use('seaborn-darkgrid')
    fig = plt.figure()  # figsize=(13,10), dpi=100)
    pallete = plt.get_cmap('tab10')

    avg_one = []
    avg_uni = []
    for p, df in dfs.items():
        onepoint = df[df['ct'] == 0]
        uniform = df[df['ct'] == 1]
        avg_one.append(onepoint[y].mean())
        avg_uni.append(uniform[y].mean())

        plt.scatter(np.full(runs, fill_value=p), onepoint[y], color=pallete(0))
        plt.scatter(np.full(runs, fill_value=p), uniform[y], color=pallete(1))

    if y == 'best_fitness':
        ms = np.full(len(ps), fill_value=settings['m'])
        plt.plot(ps, ms, color=pallete(2), linestyle='--')

    plt.plot(ps, avg_one, color=pallete(0))
    plt.plot(ps, avg_uni, color=pallete(1))

    plt.legend(['Optimum', 'Onepoint', 'Uniform'], loc='lower right')
    plt.title(title)
    plt.xlim(left=2)
    plt.ylabel(yname)
    plt.xlabel("Population size")
    plt.show()


if __name__ == '__main__':
    pops = [2]
    pops.extend(range(10, 120, 10))
    settings = {
        'p': pops,
        'm': 16,
        'k': 5,
        'd': 0.2
    }

    plot_popsize(runs=10, settings=settings, y='gen', yname='Number of generations',
                 title='Influence of population size')
    plot_popsize(runs=10, settings=settings, y='best_fitness', yname='Best fitness',
                 title='Influence of population size')
