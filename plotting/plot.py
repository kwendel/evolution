import glob

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd

experiments = '../experiments/'


def read_line(file, idx):
    try:
        with open(file) as f:
            lines = f.readlines()
            return lines[idx]
    except FileNotFoundError as e:
        print(e)


def read_last_eval(file):
    return read_line(file, -1)


def read_genotype(file):
    ct = -1

    if 'OnePoint' in file:
        ct = 0
    elif 'Uniform' in file:
        ct = 1

    data = read_line(file, -1).replace("\n", "").split(sep=" ")
    result = {
        'genotype': data[0],
        'zeros': int(data[1]),
        'ones': int(data[2]),
        'ct': ct
    }
    return result


def read_file(name):
    ct = -1
    if 'OnePoint' in name:
        ct = 0
    elif 'Uniform' in name:
        ct = 1

    data = read_last_eval(name).replace("\n", "").split(sep=" ")
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

    legend = []
    if y == 'best_fitness':
        ms = np.full(len(ps), fill_value=settings['m'])
        plt.plot(ps, ms, color=pallete(2), linestyle='--')

        legend.append('Optimum')

    plt.plot(ps, avg_one, color=pallete(0))
    plt.plot(ps, avg_uni, color=pallete(1))

    legend.append('Onepoint')
    legend.append('Uniform')

    plt.legend(legend, loc='lower right')
    plt.title(title)
    plt.xlim(left=2)
    plt.ylabel(yname)
    plt.xlabel("Population size")
    plt.show()


def print_counts(settings):
    result = []
    runs = glob.glob(
        f"{experiments}log_p{settings['p']}_m{settings['m']}_k{settings['k']}_d{settings['d']}_c*_run*.txt")

    for r in runs:
        result.append(read_genotype(r))

    df = pd.DataFrame(result)
    onepoint = df[df['ct'] == 0]
    uniform = df[df['ct'] == 1]

    def __printer(df, ct):
        print(f"## Counts - d={settings['d']} - {ct}")
        print(f"Zeros: {df['zeros'].mean()}")
        print(f"Ones: {df['ones'].mean()}")

    __printer(onepoint, 'Onepoint')
    __printer(uniform, 'Uniform')


def analyse_d():
    pops = [2]
    pops.extend(range(10, 210, 10))

    runs = 100
    k = 10
    settings = {
        'p': pops,
        'm': 4,
        'k': k,
        'd': 0.0
    }
    # Analyze the best fitness that is founded for different population sizes
    # plot_popsize(runs=runs, settings=settings, y='best_fitness', yname='Best fitness',
    #              title='Best fitness with d = 0')
    #
    # settings['d'] = 1.0 / k
    # plot_popsize(runs=runs, settings=settings, y='best_fitness', yname='Best fitness',
    #              title='Best fitness with d = 1/k')
    # settings['d'] = 1.0 - (1.0 / k)
    # plot_popsize(runs=runs, settings=settings, y='best_fitness', yname='Best fitness',
    #              title='Best fitness with d = 1 - 1/k')

    # Analyze the amount of zeros vs ones for a specific population size
    settings['p'] = 200
    settings['d'] = 0.0
    print_counts(settings)
    settings['d'] = 1.0 / k
    print_counts(settings)
    settings['d'] = 1.0 - (1.0 / k)
    print_counts(settings)
    settings['d'] = 1.0
    print_counts(settings)


def analyse_popsize():
    pops = [2]
    pops.extend(range(10, 210, 10))
    settings = {
        'p': pops,
        'm': 4,
        'k': 5,
    }

    runs = 100
    settings['d'] = 1.0 / 5.0
    plot_popsize(runs, settings, y='best_fitness', yname='Best fitness',
                 title=f"Fitness after termination condition with {settings['d']}")
    plot_popsize(runs, settings, y='evals', yname='Number of evaluation',
                 title=f"Evaluations after termination condition with {settings['d']}")
    plot_popsize(runs, settings, y='gen', yname='Number of generations',
                 title=f"Generations after termination condition with {settings['d']}")
    settings['d'] = 1 - (1.0 / 5.0)
    plot_popsize(runs, settings, y='evals', yname='Number of evaluation',
                 title=f"Evaluations after termination condition with {settings['d']}")
    plot_popsize(runs, settings, y='gen', yname='Number of generations',
                 title=f"Generations after termination condition with {settings['d']}")
    plot_popsize(runs, settings, y='best_fitness', yname='Best fitness',
                 title=f"Fitness after termination condition with {settings['d']}")


if __name__ == '__main__':
    # analyse_d()
    analyse_popsize()
