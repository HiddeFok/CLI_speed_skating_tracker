# CLI speed skating race tracker

SkateTracker is an CLI that allows you to track and visualise the progress of an ongoing speed skating competition. 

![Welcome screen](https://github.com/HiddeFok/CLI_speed_skating_tracker/blob/main/img/welcome_screen.png?raw=true)

## Requirements
The package was tested only on a Mac system. So it should at least work for OSX. It will then most likely also worked 
for Linux based systems. 

## Installation

Install with `pip` or any other PyPi package manager:
```bash
pip install SkateTracker
```
Or you can clone this repository and install the CLI directly. It is also possible to install just the requirements and
call the `main.py` script directly.
```bash
git clone git@github.com:HiddeFok/CLI_speed_skating_tracker.git
```
First option:
```bazaar
cd CLI_speed_skating_tracker
pip install . 
```
You can check if it is installed correctly by typing:
```bash
SkateTracker -h
```
This should show a help screen with all variables that can be used.  

Second option:
```bazaar
cd CLI_speed_skating_tracker
pip install -r requirements.txt 
```

## Usage
SkateTracker has several options you can configure before you start:

* `--tournament`, `-t`, Which is the name of the tournament where the race is taking place. For example, the Winter
    Olympics, a World Cup, or a national championship.

* `--gender`, `-g`, if the race is for the Men or the Women. The options are `M` or `F`.
* `--length`, `-l`, the length of the race, for example 1000, 3000, etc. 
* `--save`, `-s`, if the results of each race should be saved to a csv. This will allow you to quit the SkateTracker 
    in between races. The options are `y` or `n`. WARNING: Right now the results will be saved in a folder `skate_data` that
    will be located in the directory your terminal is currently in. 

Two more options are in the making. The first will allow you to set a prediction method. SkateTracker will then predict 
the final time of the race, depending on all the lap times so far of that athlete. The second option allows you
to show all the previous results in the plots as well. 

An example initialisation is
```bash
SkateTracker -t Winter_Olympics -g F -l 1500
```

## Example screen
![Example](https://github.com/HiddeFok/CLI_speed_skating_tracker/blob/main/img/example_final_screen.png?raw=true)

## Acknowledgements

This tool relies heavily on the packages [Rich](https://github.com/Textualize/rich) and [plotext](https://github.com/piccolomo/plotext)
So, please check them out as well!

Have fun using this tool and if there are any issues/improvements, let me know!