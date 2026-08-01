# Stepfordle-Solver
kmb_Route934's flagship game has been an icon for Cdex's SG Academy. With this little program, you can solve the daily station with ease (but also cheating)... use under your own discretion and do not abuse it. [for research purposes only]

## Overview

For _v0.1.0-pre_

An **unfinished** software where you can analyse Stepfordle gameplay and get data from different points. UI is still not available and the [main.py](main.py) function is empty, features will be implemented in future updates.

---

## Features

- A console interface to run calculations for Stepforlde game analysis.
- Fully functional module managers.
- CSV based data storage for easier changes in the future.
- Modular architecture for easier maintenence and extension.

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
├── main.py                   # Application entry point
├── README.md
└── requirements.txt          # Python dependencies
```

---

## Requirements

The project depends on:

- NetworkX
- Pillow
- Pandas

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

Launch the program with:

```bash
python main.py
```

or by double clicking the `main.py` file.

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
