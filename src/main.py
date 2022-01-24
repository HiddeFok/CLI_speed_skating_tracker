"""
CLI tool (python module) that helps you track lap times during a speed skating race.
It will also predict the final time, as well as visualise some useful satistics
"""
import argparse
from math import ceil

from rich import print

from layout import *
from utils import *
from plot import create_plotext_panel


def welcome_print(gender: str, length: int, prediction_method: str, accumulate: str, save: str) -> Panel:
    """Prints a welcome message showing what parameters have been set and wat will happen next.

    :param str gender: string indicating if the race is for Men or Women. Accepted values are ["M", "F"]
    :param int length: integer indicating the length of the race. Accepted values are [500, 1000, 1500, 3000, 5000,
    10000]
    :param str prediction_method: string indicating which prediction method to use. NOT IMPLEMENTED YET
    :param str accumulate: string which indicates if all previous results should also be shown. Accepted values
    ["y", "n"]. NOT IMPLEMENTED YET
    :param str save: string which indicates if the results after each race should be saved to a csv file. If the user
    exits the tool and restarts it again with the same settings, it will use this file to load the previous results
    :return rich.Panel: returns a rich.Panel with the welcome message
    """
    gender_name = "Men" if gender == "M" else "Women"
    accumulated = "be accumulated" if accumulate == "y" else "not be accumulated"
    save_text = "be saved" if save == "y" else "not be saved"

    # console.print(ascii_art, style="bold white on blue", justify="left", highlight=False)
    panel = Panel(
        f"I will start tracking the race with the following parameters:\n\n"
        f"\t-- {gender_name}'s {length}m race,\n"
        f"\t-- Predictions will be made with {prediction_method},\n"
        f"\t-- The results will {accumulated},\n"
        f"\t-- The results will {save_text}.\n\n",
        title="CLI speed skate race tracker",
        padding=(2, 2),
        border_style="green"
    )

    return panel


def make_instruction_panel() -> Panel:
    """Prints the instruction message showing what the user has to do next

    :return rich.Panel: returns a rich.Panel with the instruction message
    """
    panel = Panel(
        Align.center(
            f"During every race, you will be able to track one athlete or both athletes.\n\n"
            f"Indicate which one you want by typing the name(s) of the athlete(s) in a comma separated fashion",
            vertical="middle"
        ),
        title="Instructions",
        padding=(2, 2),
        border_style="red",
    )
    return panel


def create_race_view(
        gender: str,
        names: List[str],
        times: np.array,
        nr_laps: int,
        best_names: List[str],
        best_times: np.array,
        race_layout: Layout,
        first: bool = False,
        final: bool = False) -> None:
    """Creates the main race view and layout.

    :param gender: string indicating if the race is for Men or Women. Accepted values are ["M", "F"].
    :type gender: str
    :param List[str] names: List of strings with the names of the athletes.
    :param np.array times: Numpy array with the times so far.
    :param int nr_laps: integer indicating how many laps this race is going to take.
    :param List[str] best_names: List of strings with the names of the best athletes so far.
    :param np.array best_times: Numpy array with the best times so far.
    :param rich.Layout race_layout: rich.Layout object with the prescribed layout for all the tables and plots
    :param bool first: Boolean indicating if this is the first time making the view. Otherwise, the progress bar will
    be advanced instead of initiated.
    :param bool final: Boolean indicating if this is the final time the view will be shown. THe progress bar does not
    need to be progressed or initiated then.
    :return None: Nothing
    """

    plotext_layout = race_layout["plotext"]
    current_race_layout = race_layout["main"]["current_race"]
    best_results_layout = race_layout["main"]["best_results"]
    progress_layout = race_layout["progress"]

    if first:
        progress_panel = create_progress_panel(nr_laps)
        progress_layout.update(progress_panel)
    else:
        if not final:
            progress_panel = progress_layout.renderable
            progress_panel.renderable.renderable.advance(progress_panel.renderable.renderable.task_ids[0])
            progress_layout.update(progress_panel)

    _ = create_plotext_panel(
        gender,
        nr_laps,
        names,
        times,
        plotext_layout
    )

    table_progression = create_progress_table(names, times, best_times)
    table_best_results = create_best_table(best_names, best_times)

    current_race_layout.update(table_progression)
    best_results_layout.update(table_best_results)


def track_race(gender: str, names: List[str], nr_laps: int, best_names: List[str], best_times: np.array) -> np.array:
    """
    :param gender:
    :param names:
    :param nr_laps:
    :param best_names:
    :param best_times:
    :return:
    """
    n_athletes = len(names)
    times = np.zeros((len(names), nr_laps))

    race_layout = make_race_layout()
    create_race_view(
        gender,
        names,
        times,
        nr_laps,
        best_names,
        best_times,
        race_layout,
        first=True
    )
    print(race_layout)
    # for i in track(range(nr_laps), description="Lap number"):
    for i in range(nr_laps):
        correct = False
        while not correct:
            try:
                lap_time = np.array([float(t) for t in input(f"Lap times of {ordinal(i+1)} lap:").replace(" ", "").split(",")])
            except ValueError:
                print("ERROR: You need to enter numbers!")
            else:
                if lap_time.shape[0] != n_athletes:
                    print("ERROR: you need to enter the correct amount of times!")
                # elif any(isinstance(t, ))

                else:
                    correct = True
                    times[:, i] = lap_time

                os.system("clear")
                create_race_view(
                    gender,
                    names,
                    times,
                    nr_laps,
                    best_names,
                    best_times,
                    race_layout
                )
                print(race_layout)
    return times, race_layout


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

    use = check_saved(gender, length)

    welcome_panel = welcome_print(gender, length, prediction_method, accumulate, save)
    instruction_panel = make_instruction_panel()

    layout_start = make_start_layout()
    layout_start["header"].update(Header())
    layout_start["main"]["side"].update(instruction_panel)
    layout_start["main"]["body"].update(welcome_panel)
    print(layout_start)
    # welcome_print(gender, length, prediction_method, accumulate, save)

    nr_laps = ceil(length / 400)
    tracking = True

    best_names = ["None", "None", "None"]
    best_times = np.zeros((3, nr_laps))

    if use == "y":
        all_names, all_results = load_results(gender=gender, length=length)
        best_names, best_times = update_best_times(all_names, all_results, best_names, best_times)
    else:
        all_names = []
        all_results = []

    while tracking:
        names = input("The names of the athletes are: ").replace(" ", "").split(",")
        lap_times, race_layout = track_race(gender, names, nr_laps, best_names, best_times)
        best_names, best_times = update_best_times(names, lap_times, best_names, best_times)

        if save == "y":
            if len(all_names) != 0:
                all_results = np.vstack((all_results, lap_times))
                all_names = all_names + names
                save_results(gender, length, all_names, all_results.T)
            else:
                all_results = lap_times
                all_names = names
                save_results(gender, length, all_names, all_results.T)

        correct = False
        while not correct:
            next_race = input("Do you want to start tracking the next race? [y/n]: ")
            if not (next_race == "y" or next_race == "n"):
                print("ERROR: please select a valid response!")
            else:
                correct = True

        if next_race == "n":
            create_race_view(
                gender,
                names,
                lap_times,
                nr_laps,
                best_names,
                best_times,
                race_layout,
                final=True
            )
            print(race_layout)
            input("Input anything to quit the Tracker!")
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
