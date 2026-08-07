from managers import gui_manager as ui
from managers import image_manager as img
from managers import logic_manager as logic
from pathlib import Path
import pandas as pd


def declarePaths() -> None:
    """Makes variables for the different paths where data can
    and is stored."""
    
    # Project directory
    global BASE_DIR
    BASE_DIR = Path(__file__).resolve().parent

    # Data folder
    global DATA_DIR
    DATA_DIR = BASE_DIR / "data"


def createLookups():
    global stations
    stations = stations = (
        pd.read_csv(DATA_DIR / "stations.csv", skipinitialspace=True)
        .set_index("id")
        .to_dict(orient="index"))
    
    global name_to_id
    name_to_id = {data["station_name"]: id for id, data in stations.items()}
    
    global target_colour
    target_colour = "#69b1ff"
    
    global best_guess_colour
    best_guess_colour = "#57ffb0"


def initialise():
    declarePaths()
    createLookups()


def fromStationNameGetId(station_name: str) -> int:
    return name_to_id.get(station_name)


def whenGuessInserted():
    made_guesses = app.get_values()
    
    guesses_list = []
    
    for guess in made_guesses:
        id = fromStationNameGetId(guess["station"])
        zone_dist = guess["zone_dist"]
        stop_dist = guess["stop_dist"]
        
        guesses_list.append((id, zone_dist, stop_dist))
        
    available_targets = logic.givenGuessesGivePossibleTargets(*guesses_list)
    best_guesses = logic.bestGuessGivenTargets(*guesses_list)
    
    if len(available_targets) == 1: 
        colour_regions = img.fromStationIdsGetRegionsWithData(target_colour, 100, available_targets[0])
        new_image = img.highlightImage(*colour_regions)
        
        app.set_map(new_image)
        app.ui.rows[-1].lock_row()
        
        app.set_status(f"The station you were looking for is: {stations[available_targets[0]]["station_name"]}.")
    
    else:
        targets_regions = img.fromStationIdsGetRegionsWithData(target_colour, 100, *available_targets)
        guesses_regions = img.fromStationIdsGetRegionsWithData(best_guess_colour, 100, *best_guesses)  
        
        colour_regions = [*targets_regions, *guesses_regions]
        new_image = img.highlightImage(*colour_regions)
        
        app.set_map(new_image)
        
        if len(best_guesses) == 1:
            app.set_status(f"Your best guess is: {best_guesses[0]}.")
        else:
            guessses_names = [stations[id]["station_name"] for id in best_guesses]
            
            app.set_status(f"Your best guesses are: {', '.join(guessses_names[:-1])} or {guessses_names[-1]}.")

initialise()

app = ui.App(whenGuessInserted)
app.mainloop()