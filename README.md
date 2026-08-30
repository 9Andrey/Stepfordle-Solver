# Stepfordle-Solver
kmb_Route934's flagship game has been an icon for Cdex's SG Academy. With this little program, you can solve the daily station with ease (but also cheating)... use under your own discretion and do not abuse it. [for research purposes only]

## Overview

For _v0.3.2-beta_

A software to perfectly play kmb_Route934's Stepfordle game, with it's UI you can input your made guesses and the software will instantly tell you what your next guess should be so you can optimise your game. Use it responsibly.

---

## Features

- A console interface to run calculations for Stepforlde game analysis.
- Fully functional module managers.
- CSV based data storage for easier changes in the future.
- Modular architecture for easier maintenence and extension.
- Full UI implemented.

---

## Project Structure

```
Stepfordle-Solver/
│
├── data/                     # Images and CSV data files
│   ├── connections.csv
│   ├── default_map.png
│   ├── imageRegions.csv
│   ├── stations.csv
│   └── zonesConnections.csv
│ 
├── managers/                 # Core application modules
│   ├── gui_manager.py
│   ├── image_manager.py
│   └── logic_manager.py
│
├── temp/                     # Temporary runtime files
│   └── .gitkeep                   
│
├── .gitignore                  
├── CHANGELOG.md  
├── CREDITS.md
├── LICENSE         
├── main.py                   # Application entry point (still unavailable)
├── README.md
└── requirements.txt          # Python dependencies
```

---

## Requirements

The project depends on:

- NetworkX
- Pillow
- Pandas
- Customtkinter

---

## Instalation

Clone the repository:

```bash
git clone https://github.com/9Andrey/Stepfordle_Solver.git
cd Stepfordle_Solver
```
or download the files from the GitHub repository.

Install the required packages:

```bash
pip install -r requirements.txt
```

---

## Running the Application

> Launch the program with:
> 
> ```bash
> python main.py
> ```
> 
> or by double clicking the `main.py` file.

_Usage of the modules:_

> ### Logic module: [logic_manager.py](managers/logic_manager.py)
> 
> When calling the module, `initialise()` will automatically be executed.
> 
> 1. `getPossibleZones(*zones_info: tuple) -> list`
> 
> > Given none, one or more tuples `(zone_num, dist)` returns the eligible zones that are `tuple[1]` distance from `tuple[0]`. If no zones are given, all 10 zones will be returned.
> > 
> > **Example:**
> > ```python
> > getPossibleZones((1, 3), (9, 2))
> > ```
> > 
> > Output:
> > ```text
> > [5]
> > ```
>  
> 2. `getAllStationsInZones(zones: tuple) -> tuple`
> 
> > Given a list of zones, it outputs every station inside those zones. One or more inputs are accepted.
> > 
> > **Example:**
> > ```python
> > getAllStationsInZones((4, 5))
> > ```
> > 
> > Output:
> > ```text
> > (38, 39, 40, 41, 42, 29, 37, 43, 44, 45)
> > ```
> 
> 3. `getPossibleStationsFrom(possibilities: tuple, *stop_info: tuple) -> list`
> 
> > From the `possibilities` (a tuple with all station ids), get the possible station given the (in `stop_info`) station id `tuple[0]` is `tuple[1]` distance from target.
> > 
> > **Example:**
> > ```python
> > getPossibleStationsFrom((38, 39, 40, 41, 42, 29, 37, 43, 44, 45), (8, 3))
> > ```
> > 
> > Output:
> > ```text
> > [38, 40, 29, 43]
> > ```
> 
> 4. `givenGuessesGivePossibleTargets(*guesses: tuple) -> list`
> 
> > Given one or more tuples `(id, zone_dist, stop_dist)` get all possible targets.
> > 
> > **Example:**
> > ```python
> > givenGuessesGivePossibleTargets((7, 2, 7))
> > ```
> > 
> > Output:
> > ```text
> > [25, 26]
> > ```
> 
> 5. `getBestGuesses(*already_guessed: tuple) -> list`
> 
> > When you input every guess you did `(id, zone_dist, stop_dist)`, it looks for which stations narrow it down the furthest.
> > 
> > **Example:**
> > ```python
> > getBestGuesses((7, 2, 7))
> > ```
> > 
> > Output:
> > ```text
> > [20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 32, 33, 34, 36, 37, 38, 39, 40, 41, 42, 43, 44, 45, 46, 47, 48, 49, 50, 51, 52, 53, 54, 55, 56, 57, 58, 59, 60, 61, 62, 63, 64, 65, 66, 67, 68, 69, 70, 71, 72, 73, 74, 75]
> > ```
> 
> 6. `reduceGuessesWithTargets(targets: tuple, candidate_guesses: tuple) -> list`
> 
> > Priotitises `tragets` for the best guesses, if one or more of the `targets` is in `candidate_guesses` it outputs a list of every `candidate_guesses` that is in `targets`. If no duplicates exist, it returns `candidate_guesses`.
> > 
> > **Example:**
> > ```python
> > reduceGuessesWithTargets((20, 21), (19, 20, 21, 22))
> > ```
> > 
> > Output:
> > ```text
> > [20, 21]
> > ```
> 
> 7. `bestGuessGivenTargets(*already_guessed: tuple) -> list`
>
> > When inputing the guesses made, it narrows it down the furthest to get the best stations for the next guess
> >
> > **Example:**
> > ```python
> > bestGuessGivenTargets((7, 2, 7))
> > ```
> > 
> > Output:
> > ```text
> > [25, 26]
> > ```
>
> ### Image module: [image_manager.py](managers/image_manager.py) 
> 
> When calling the module, `initialise()` will automatically be executed.
> 
> 1. `fromStationIdsGetRegionsWithData(colour, alpha, *stations: int) -> list`
> 
> > You input as many station ids as you want, this outputs a list composed of `(x, y, dx, dy, colour, alpha)` for as many stations you inputed. For `x`, `y`, `dx` and `dy` it looks with the station ids given in the dictionary created after `imageRegions.csv`. Colour is the RGB value in hex (e.g. `#ff0000`) and Alpha is the transparency (0-255), 0 being fully transparent and 255 being fully opaque.
> > 
> > **Example:**
> > ```python
> > fromStationIdsGetRegionsWithData("#ff0000", 100, 0, 1)
> > ```
> > 
> > Output:
> > ```text
> > [(265, 1018, 234, 50, '#ff0000', 100), (343, 1155, 265, 50, '#ff0000', 100)]
> > ```
> 
> 2. `highlightImage(*regions: tuple[int, int, int, int, str, int], output_name: str = "highlighted") -> Path`
> 
> > Highlight one or more rectangular regions of an image according to the lists given in the `fromStationIdsGetRegionsWithData()`. If `output_name` is inserted, it names it `output_name[index].png` if no `output_name` is set, it wil default to `highlighted[index].png`. Index refers to the generation number, to avoid duplicate names.
> > 
> > **Example:**
> > ```python
> > highlightImage((0, 0, 100, 100, "#ff0000", 100))
> > ```
> >
> > Output: 
> > 
> > An image in `temp/` folder called `highlighted0.png` with a 100x100 region starting from 0, 0 highligthed in red with an alpha value of 100.
> 
> ### UI module: [gui_manager.py](managers/gui_manager.py) 
> 
> When calling the module, `initialise()` will automatically be executed.
> 
> 1. `App()` class (Setup)
>
> > Creates the UI app 
> > 
> > **Usage:**
> > ```python
> > app = App() # Create the app
> > app.mainloop() # Launch the app
> > ```
> 
> 2. `app.get_values() -> list[dict["station":str, "zone_dist":int, "stop_dist":int]]`
>
> > Get every value inserted in the guesses part.
> > 
> > **Example output:**
> > ```text
> > [{"station":"Stepford Victoria", "zone_dist":4, "stop_dist":9},
> >  {"station":"Benton", "zone_dist":1, "stop_dist":4}]
> > ```
> 
> 3. `app.set_status(text: str)`
>
> > Edits the label above the image, used for sending messages.
> > 
> > **Example:**
> > ```python
> > app.set_status("This is a new status.")
> > ```
> > 
> > Output:
> > In the UI, above the picture, the new message will be set.
> 
> 4. `app.set_image(path: Path, image_size: tuple =(650, 406))`
> 
> > Given a path, it changes the picture to the picture stored in the path. Used with the [image_manager.py](managers/image_manager.py) and the `highlightImage(...)` function, as it returns the generated picture's path.
> >
> > **Example:**
> > ```python
> > app.set_image(highlightImage((0, 0, 100, 100, "#ff0000", 100)))
> > ```
> > 
> > Output:
> > The picture in the UI is changed for an image generated in the `temp/` folder called `highlighted0.png` with a 100x100 region starting from 0, 0 highligthed in red with an alpha value of 100. The image is 650 \* 406 px

---

## License

This project is licensed under the MIT License.

See the [LICENSE](LICENSE) file for details.

---

## Credits

This project makes use of several open-source libraries.

Special thanks to kmb_Route934 (@3tw2527 - _Discord_) for creating the inspiration for this software: Stepfordle. You can visit it [here](https://scr-sg.presbc.com/#stepfordle-game).

See [CREDITS.md](CREDITS.md) for acknowledgements and licensing information.

---

## Contributing

Bug reports, feature requests, and pull requests are welcome.

Please open an issue before making major changes to discuss the proposed improvements.

---

## Author

Created by **9Andrey**.

**GitHub:** https://github.com/9Andrey

**Discord:** @fokacivilengineer
