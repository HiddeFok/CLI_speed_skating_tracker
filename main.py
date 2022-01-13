"""
CLI tool (python module) that helps you track lap times during a speed skating race.
It will also predict the final time, as well as visualise some useful satistics
"""

import argparse
import time

import plotext as plt
import numpy as np

from typing import List
from math import ceil
# TODO: add a Table next to the plots using
# https://github.com/piccolomo/plotext/issues/26
from rich.console import Console
from rich.table import Table


def ordinal(n: int):
    return "%d%s" % (n, "tsnrhtdd"[(n // 10 % 10 != 1) * (n % 10 < 4) * n % 10::4])


def welcome_print(gender: str, length: int, prediction_method: str, accumulate: str, save: str):
    """
    :param gender:
    :param length:
    :param prediction_method:
    :param accumulate:
    :param save:
    :return:
    """
    gender_name = "Men" if gender == "M" else "Women"
    accumulated = "be accumulated" if accumulate == "y" else "not be accumulated"
    save_text = "be saved" if save == "y" else "not be saved"
    print("\033[F")
    print(
        f"Welcome to this CLI speed skate race tracker!"
        f"I will start tracking the race with the following parameters:\n\n"
        f"\t-- {gender_name}'s {length}m race,\n"
        f"\t-- Predictions will be made with {prediction_method},\n"
        f"\t-- The results will {accumulated},\n"
        f"\t-- The results will {save_text}.\n\n"
        f"During every race, you will be able to track one athlete or both athletes. Indicate which one you want by "
        f"typing the name(s) of the athlete(s) in a comma separated fashion\n")


def track_race(names: List[str], nr_laps: int):
    """

    :param names:
    :param nr_laps:
    :return:
    """
    n_athletes = len(names)

    times = np.zeros((len(names), nr_laps))
    for i in range(nr_laps):
        correct = False
        while not correct:
            lap_time = np.array([float(t) for t in input(f"Lap times of {ordinal(i+1)} lap:").replace(" ", "").split(",")])
            if lap_time.shape[0] != n_athletes:
                print("ERROR: you need to enter the correct amount of times!")
            else:
                correct = True
                times[:, i] = lap_time
    print(times)
    return times


def plot_race(gender: str, length: int, names: List[str], lap_times: np.array):
    """
    :param gender:
    :param length:
    :param names:
    :param lap_times:
    :return:
    """
    gender_name = "Men" if gender == "M" else "Women"
    title_names = " vs ".join(names)
    nr_athletes = len(names)
    nr_laps = lap_times.shape[1]
    plt.subplots(1, 2)

    total_times = np.cumsum(lap_times, axis=1)
    # TODO: layouting (colors, markers, etc)
    # Plot of the total
    plt.subplot(1, 1)
    for i in range(nr_athletes):
        plt.plot(total_times[i, :])
    plt.title(f"{gender_name}'s {length}m race total times: {title_names}")
    plt.xticks(list(range(nr_laps)))

    # Plot of the lap times
    plt.subplot(1, 2)
    for i in range(nr_athletes):
        plt.plot(lap_times[i, :])
    plt.title(f"{gender_name}'s {length}m race lap times: {title_names}")
    plt.xticks(list(range(nr_laps)))
    plt.show()

    time.sleep(2)
    plt.clear_terminal()
    time.sleep(2)


def main(gender: str, length: int, prediction_method: str, accumulate: str, save: str):
    """
    :param gender:
    :param length:
    :param prediction_method:
    :param accumulate:
    :param save:
    :return:
    """

    # verify if all the arguments are correct (some combinations are not possible)
    if gender == "M" and length == 3000:
        raise ValueError("This combination is not a valid race!")
    if gender == "F" and length == 10000:
        raise ValueError("This combination is not a valid race!")

    welcome_print(gender, length, prediction_method, accumulate, save)

    nr_laps = ceil(length / 400)
    tracking = True

    while tracking:
        names = input("The names are:").replace(" ", "").split(",")
        print(names)
        lap_times = track_race(names, nr_laps)
        plot_race(gender, length, names, lap_times)
        tracking = False
    return 0


# Press the green button in the gutter to run the script.
if __name__ == '__main__':

    parser = argparse.ArgumentParser(
        description="CLI tool to track and predict Speed Skating races"
    )

    # Arguments to add:
    # TODO: gender, length, prediction_methods, accumulate, save

    parser.add_argument('--gender', '-g', type=str, choices=["M", "F"], required=True,
                        help="Indicate if the race is for the Men (M) or the Women (W).")
    parser.add_argument('--length', '-l', type=int, choices=[500, 1000, 1500, 3000, 5000, 10000], required=True,
                        help="Indicate the length of the race.")
    parser.add_argument('--prediction_method', '-pm', nargs="+", type=str,
                        choices=["mean", "latest", "lr", "LSTM", "online"], required=True,
                        help="Indicate which method to use to predict the ending time.")
    parser.add_argument("--accumulate", "-a", choices=["y", "n"], type=str, default="y",
                        help="Indicate if previous results should be accumulated in the visualisations.")
    parser.add_argument("--save", "-s", choices=["y", "n"], type=str, default="y",
                        help="Indicate if all the results should be saved.")
    # For now this will be a simple csv, might change into an sqlite db

    args = parser.parse_args()
    kwargs = vars(args)

    main(**kwargs)
