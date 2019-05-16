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
    return read_line(file, -2)


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
    parameters = name.split("_")

    result = {
        'p': int(parameters[1][1:]),
        'm': int(parameters[2][1:]),
        'k': int(parameters[3][1:]),
        'd': float(parameters[4][1:]),
        'l': int(parameters[2][1:]) * int(parameters[3][1:]),
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


def analyze_d():
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
    plot_popsize(runs=runs, settings=settings, y='best_fitness', yname='Best fitness',
                 title='Best fitness with d = 0')

    settings['d'] = 1.0 / k
    plot_popsize(runs=runs, settings=settings, y='best_fitness', yname='Best fitness',
                 title='Best fitness with d = 1/k')
    settings['d'] = 1.0 - (1.0 / k)
    plot_popsize(runs=runs, settings=settings, y='best_fitness', yname='Best fitness',
                 title='Best fitness with d = 1 - 1/k')

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


def analyze_popsize():
    pops = [2]
    pops.extend(range(10, 210, 10))
    settings = {
        'p': pops,
        'm': 2,
        'k': 5,
    }

    runs = 100
    settings['d'] = 1.0 / settings['k']
    plot_popsize(runs, settings, y='best_fitness', yname='Best fitness',
                 title=f"Fitness after termination condition")
    plot_popsize(runs, settings, y='evals', yname='Number of evaluation',
                 title=f"Evaluations after termination condition")
    plot_popsize(runs, settings, y='gen', yname='Number of generations',
                 title=f"Generations after termination condition")

    settings['m'] = 8
    settings['k'] = 10
    settings['d'] = 1.0 / settings['k']
    plot_popsize(runs, settings, y='evals', yname='Number of evaluation',
                 title=f"Evaluations after termination condition")
    plot_popsize(runs, settings, y='gen', yname='Number of generations',
                 title=f"Generations after termination condition")
    plot_popsize(runs, settings, y='best_fitness', yname='Best fitness',
                 title=f"Fitness after termination condition")


def analyze_popsize_big():
    pops = [2]
    pops.extend(range(100, 2100, 100))
    settings = {'p': pops, 'm': 8, 'k': 10, 'd': 0.1}
    runs = 100

    plot_popsize(runs, settings, y='evals', yname='Number of evaluation',
                 title=f"Evaluations after termination condition")
    plot_popsize(runs, settings, y='gen', yname='Number of generations',
                 title=f"Generations after termination condition")
    plot_popsize(runs, settings, y='best_fitness', yname='Best fitness',
                 title=f"Fitness after termination condition")


def compare(compare='m', ps=[20], ms=[4], ks=[5], ds=[0.2]):
    compare_opts = {
        'p': ps,
        'm': ms,
        'k': ks,
        'd': ds,
        'l': np.multiply(ms, ks),
    }

    result = {}

    for i in range(len(compare_opts[compare])):
        v = compare_opts[compare][i]
        p = v if compare == 'p' else ps[0]
        m = v if compare == 'm' else ms[0]
        k = v if compare == 'k' else ks[0]
        d = v if compare == 'd' else ds[0]
        if compare == 'k':
            d = ds[i]
        if compare == 'l':
            m = ms[i]
            k = ks[i]
            d = ds[i]
            v = f'{v}_{m}x{k}'

        file_glob = f"{experiments}log_p{p}_m{m}_k{k}_d{d}_c*_run*.txt"
        print(file_glob)
        result[v] = []
        runs = glob.glob(file_glob)
        print(runs)

        for r in runs:
            result[v].append(read_file(r))

        result[v] = pd.DataFrame(result[v])

    print(result)

    return result


def plot_m(dfs, vs, compare, y='best_fitness', y_label='Normalized fitness (fitness/m)', title='Plot'):
    x_labels = {
        'p': 'Population size',
        'm': 'm',
        'k': 'k',
        'd': 'd',
    }
    x_label = x_labels[compare]

    plt.style.use('seaborn-darkgrid')
    plt.rcParams.update({'font.size': 13})
    plt.ylim(0.4, 1.01)
    palette = plt.get_cmap('tab10')

    avg_one = []
    avg_uni = []
    for v, df in dfs.items():
        onepoint = df[df['ct'] == 0]
        uniform = df[df['ct'] == 1]
        avg_one.append(onepoint[y].mean() / v)
        avg_uni.append(uniform[y].mean() / v)

        plt.scatter(np.full(len(onepoint), fill_value=v), onepoint[y] / v, color=palette(0))
        plt.scatter(np.full(len(uniform), fill_value=v), uniform[y] / v, color=palette(1))

    legend = []
    if y == 'best_fitness':
        if compare == 'm':
            ms = np.full(len(vs), fill_value=1)
        else:
            ms = np.full(len(vs), fill_value=settings['m'])
        plt.plot(vs, ms, color=palette(2), linestyle='--')

        legend.append('Optimum')

    plt.plot(vs, avg_one, color=palette(0))
    plt.plot(vs, avg_uni, color=palette(1))

    legend.append('Onepoint')
    legend.append('Uniform')

    plt.legend(legend, loc='lower left')
    plt.title(title)
    plt.xlim(left=2)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(f'./plots/m_relative_fitness_k{title.split("=")[1]}.png')
    plt.show()


def plot_l(dfs, compare, y='best_fitness', y_label='y',
           title='Average normalized fitness for different genotype lengths'):
    x_labels = {
        'p': 'Population size',
        'm': 'm',
        'k': 'k',
        'd': 'd',
        'l': 'Genotype length (l)',
    }
    x_label = x_labels[compare]

    plt.style.use('seaborn-darkgrid')
    plt.rcParams.update({'font.size': 13})
    plt.ylim(0.4, 1.01)
    palette = plt.get_cmap('tab20')

    avg_one_m_k = []
    avg_one_k_m = []
    avg_uni_m_k = []
    avg_uni_k_m = []
    vs = []
    for v, df in dfs.items():
        m = df.iloc[0]['m']
        l = df.iloc[0]['l']
        vs.append(l)
        onepoint = df[df['ct'] == 0]
        uniform = df[df['ct'] == 1]
        onepoint_m_k = onepoint[onepoint['m'] < onepoint['k']]
        onepoint_k_m = onepoint[onepoint['m'] > onepoint['k']]
        uniform_m_k = uniform[uniform['m'] < uniform['k']]
        uniform_k_m = uniform[uniform['m'] > uniform['k']]

        avg_one_m_k.append(onepoint_m_k[y].mean() / m)
        avg_one_k_m.append(onepoint_k_m[y].mean() / m)
        avg_uni_m_k.append(uniform_m_k[y].mean() / m)
        avg_uni_k_m.append(uniform_k_m[y].mean() / m)

        # plt.scatter(np.full(len(onepoint_m_k), fill_value=l), onepoint_m_k[y] / m, color=palette(0))
        # plt.scatter(np.full(len(onepoint_k_m), fill_value=l), onepoint_k_m[y] / m, color=palette(1))
        # plt.scatter(np.full(len(uniform_m_k), fill_value=l), uniform_m_k[y] / m, color=palette(2))
        # plt.scatter(np.full(len(uniform_k_m), fill_value=l), uniform_k_m[y] / m, color=palette(3))

    legend = []

    plt.plot(vs, np.full(len(vs), fill_value=1), color=palette(2), linestyle='--')
    legend.append('Optimum')

    avg_one_m_k = [x for x in avg_one_m_k if str(x) != 'nan']
    avg_one_k_m = [x for x in avg_one_k_m if str(x) != 'nan']
    avg_uni_m_k = [x for x in avg_uni_m_k if str(x) != 'nan']
    avg_uni_k_m = [x for x in avg_uni_k_m if str(x) != 'nan']
    plt.plot(np.unique(vs), avg_one_m_k, color=palette(0))
    plt.plot(np.unique(vs), avg_one_k_m, color=palette(1))
    plt.plot(np.unique(vs), avg_uni_m_k, color=palette(2))
    plt.plot(np.unique(vs), avg_uni_k_m, color=palette(3))

    legend.append('Onepoint (m<k)')
    legend.append('Onepoint (k<m)')
    legend.append('Uniform (m<k)')
    legend.append('Uniform (k<m)')

    plt.legend(legend, loc='upper right')
    plt.title(title)
    plt.xlim(left=2)
    plt.ylabel(y_label)
    plt.xlabel(x_label)
    plt.savefig(f'./plots/l_relative_fitness.png')
    plt.show()


def analyze_m_k():
    vs = [1, 2, 4, 8, 16]
    metric = 'm'
    res = compare(compare=metric, ps=[20], ms=vs, ks=[3], ds=[1.0 / 3.0])
    plot_m(res, vs, metric, y_label='Normalized fitness (fitness/m)',
           title='Achieved fitness for different values of m with k=3')
    res = compare(compare=metric, ps=[20], ms=vs, ks=[5], ds=[0.2])
    plot_m(res, vs, metric, y_label='Normalized fitness (fitness/m)',
           title='Achieved fitness for different values of m with k=5')
    res = compare(compare=metric, ps=[20], ms=vs, ks=[10], ds=[0.1])
    plot_m(res, vs, metric, y_label='Normalized fitness (fitness/m)',
           title='Achieved fitness for different values of m with k=10')
    res = compare(compare=metric, ps=[20], ms=vs, ks=[50], ds=[0.02])
    plot_m(res, vs, metric, y_label='Normalized fitness (fitness/m)',
           title='Achieved fitness for different values of m with k=50')


def analyze_m_k_2():
    ms = [2, 10, 2, 30, 2, 50, 10, 15, 15, 30]
    ks = [10, 2, 30, 2, 50, 2, 15, 10, 30, 15]
    ds = np.divide(1, ks)
    res = compare(compare='l', ps=[20], ms=ms, ks=ks, ds=ds)
    plot_l(res, 'l', y_label='Normalized fitness (fitness/m)')


if __name__ == '__main__':
    analyze_d()
    analyze_popsize()
    analyze_popsize_big()
    analyze_m_k()
    analyze_m_k_2()
