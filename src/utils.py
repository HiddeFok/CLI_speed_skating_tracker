import os
import numpy as np

from typing import List

from art import ascii_art

from rich.table import Table
from rich.panel import Panel
from rich.markdown import Markdown


def ordinal(n: int):
    """

    :param n:
    :return:
    """
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def update_best_times(names: List[str], times: np.array, best_names: List[str], best_times: np.array) -> np.array:
    """

    :param names:
    :param times:
    :param best_names:
    :param best_times:
    :return:
    """
    all_names = np.array(names + best_names, dtype=object)
    all_times = np.vstack((times, best_times))

    total_times = all_times.sum(axis=1)
    total_times[total_times == 0] = np.infty
    total_times_sorted = total_times.argsort()
    return list(all_names[total_times_sorted[:3]]), all_times[total_times_sorted[:3]]


def check_saved(gender: str, length: int):
    gender_name = "Men" if gender == "M" else "Women"

    if os.path.isfile(os.path.join(os.getcwd(), 'skate_data', f"race_{gender_name}_{length}m_data.csv")):
        correct = False
        while not correct:
            use = input("Data for this race was already found. Do you want to use it? [y/n]")
            if not (use == "y" or use == "n"):
                print("ERROR: please input a valid response!")
            else:
                correct = True
    else:
        use = "no file"
    return use


def save_results(gender: str, length: int, names: List[str], times: np.array):

    if not os.path.isdir(os.path.join(os.getcwd(), 'skate_data')):
        os.mkdir(os.path.join(os.getcwd(), 'skate_data'))

    gender_name = "Men" if gender == "M" else "Women"

    np.savetxt(
        os.path.join(os.getcwd(), 'skate_data', f"race_{gender_name}_{length}m_data.csv"),
        times,
        header=",".join(names),
        delimiter=",",
        comments="",
        fmt="%1.2f"
    )


def load_results(fname=None, gender=None, length=None) -> (List[str], np.array):
    if fname is not None:
        with open(fname) as f:
            names = f.readline().rstrip().split(",")
        results = np.loadtxt(fname, delimiter=",", skiprows=1)
    else:
        if gender is not None and length is not None:
            gender_name = "Men" if gender == "M" else "Women"
            fname = os.path.join(os.getcwd(), 'skate_data', f"race_{gender_name}_{length}m_data.csv")
            with open(fname) as f:
                names = f.readline().rstrip().split(",")
            results = np.loadtxt(fname, delimiter=",", skiprows=1)
        else:
            raise ValueError("ERROR: Please insert a valid gender or length")
    return names, results.T


class Header:
    """Display header with clock."""

    def __rich__(self) -> Panel:
        grid = Table.grid(expand=True)
        grid.add_column(justify="right", width=5)
        grid.add_column(justify='right', width=40, vertical="middle")
        grid.add_column(justify="center", ratio=1)
        grid.add_row(
            " ",
            Markdown("# Welcome to this CLI speed skate race tracker!\n"),
            ascii_art
        )
        return Panel(grid, style="bold white on blue")