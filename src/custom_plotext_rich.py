from rich.layout import Layout
from rich.live import Live
from rich.ansi import AnsiDecoder
from rich.console import Group as RenderGroup
from rich.jupyter import JupyterMixin
from rich.panel import Panel

from time import sleep
import plotext as plt


def make_plot(*size):
    plt.clf()
    plt.scatter(plt.sin(1000, 3))
    plt.plotsize(*size)
    plt.title("Plotext Integration in Rich - Test")
    return plt.build()


class plotextMixin(JupyterMixin):
    def __init__(self):
        self.decoder = AnsiDecoder()

    def __rich_console__(self, console, options):
        self.width = options.max_width or console.width
        self.height = options.height or console.height
        canvas = make_plot(self.width, self.height)
        self.rich_canvas = RenderGroup(*self.decoder.decode(canvas))
        yield self.rich_canvas


def make_layout():
    layout = Layout(name="root")
    layout.split(
        Layout(name="header", size=3),
        Layout(name="main", ratio=1),
    )
    layout["main"].split_row(
        Layout(name="plotext", size=60),
        Layout(name="main_right"),
    )
    return layout


layout = make_layout()
plotext_layout = layout["plotext"]
mix = plotextMixin()
mix = Panel(mix)
plotext_layout.update(mix)

with Live(layout, refresh_per_second=0.1) as live:
    while True:
        sleep(0.1)