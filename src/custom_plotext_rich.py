from rich.layout import Layout
from rich.live import Live
from rich.ansi import AnsiDecoder
from rich.console import Group as RenderGroup
from rich.jupyter import JupyterMixin
from rich.panel import Panel
from rich.table import Table
from rich.prompt import Prompt
from rich import print
import os
from time import sleep
import plotext as plt


def make_plot(*size):
    plt.clf()
    plt.subplots(2, 1)
    plt.subplot(1, 1)
    plt.scatter(plt.sin(1000, 3))
    plt.plotsize(*size)
    plt.title("Plotext Integration in Rich - Test")
    plt.subplot(2, 1)
    plt.scatter(plt.sin(1000, 4))
    plt.plotsize(*size)
    plt.title("Plotext Integration in Rich - Test")
    return plt.build()


class plotextMixin(JupyterMixin):
    def __init__(self):
        self.decoder = AnsiDecoder()

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height / 2)
        self.rich_canvas = RenderGroup(*self.decoder.decode(canvas))
        yield self.rich_canvas


def make_layout():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3,),
        Layout(name="main", ratio=1),
        Layout(name="progress", size=3)
    )
    layout["main"].split_row(
        Layout(name="plotext", size=60),
        Layout(name="main_right"),
    )
    layout["progress"].split_row(
        Layout(name="prompt", size=60),
        Layout(name="bar")
    )
    return layout


layout = make_layout()
plotext_layout = layout["plotext"]
table_layout = layout["main"]["main_right"]
prompt_layout = layout["progress"]["bar"]

mix = plotextMixin()
mix = Panel(mix)
plotext_layout.update(mix)

table = Table(title="Lap times progression")

table.add_column("Released", justify="right", style="cyan", no_wrap=True)
table.add_column("Title", style="magenta")
table.add_column("Box Office", justify="right", style="green")

table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
table.add_row("May 25, 2018", "Solo: A Star Wars Story", "$393,151,347")
table.add_row("Dec 15, 2017", "Star Wars Ep. V111: The Last Jedi", "$1,332,539,889")
table.add_row("Dec 16, 2016", "Rogue One: A Star Wars Story", "$1,332,439,889")

table_layout.update(table)
while True:
    os.system("clear")

    print(layout)
    input("Type your input: ")
# with Live(layout, refresh_per_second=2) as live:
#     while True:
#         table.add_row("Dec 20, 2019", "Star Wars: The Rise of Skywalker", "$952,110,690")
#         prompt_layout.update(Panel(input("hallo")))

