from pathlib import Path
import shutil
from PIL import Image, ImageDraw, ImageColor
import pandas as pd


def declarePaths() -> None:
    """Makes variables for the different paths where data can
    and is stored."""
    
    # Project directory
    global BASE_DIR
    BASE_DIR = Path(__file__).resolve().parent.parent

    # Data folder (Default image)
    global DATA_DIR
    DATA_DIR = BASE_DIR / "data"
    
    # Temp folder (Store new pictures)
    global TEMP_DIR
    TEMP_DIR = BASE_DIR / "temp"
    
    
def createLabelsRegionLookup() -> None:
    """Get data out from imageRegions.csv and store it in a 
    dictionary"""
    
    global regions
    regions = (
        pd.read_csv(DATA_DIR / "imageRegions.csv", skipinitialspace=True)
        .set_index("id")
        .to_dict(orient="index")
    )


def initialise() -> None:
    global image_index 
    image_index = 0
    
    declarePaths()
    createLabelsRegionLookup()
  
  
def fromStationIdsGetRegionsWithData(colour, alpha, *stations: int) -> list:
    """You input as many station ids as you want, this outputs
    a list composed of (x, y, dx, dy, colour, alpha) for as many 
    stations you inputed."""
    
    output = []
    for id in stations:
        x = regions[id]["x"]
        y = regions[id]["y"]
        dx = regions[id]["dx"]
        dy = regions[id]["dy"]
        output.append((x, y, dx, dy, colour, alpha))
    
    return output


def highlightImage(*regions: tuple[int, int, int, int, str, int], output_name: str = "highlighted") -> Path:
    """Highlight one or more rectangular regions of an image."""

    global image_index
    
    input_path = DATA_DIR / "default_map.png"

    TEMP_DIR.mkdir(exist_ok=True)

    image = Image.open(input_path).convert("RGBA")

    overlay = Image.new("RGBA", image.size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(overlay)

    for x, y, dx, dy, colour_hex, alpha in regions:

        rgb = ImageColor.getrgb(colour_hex)

        draw.rectangle((x, y, x + dx, y + dy), fill=(*rgb, alpha))

    result = Image.alpha_composite(image, overlay)

    output_name += str(image_index) + ".png"
    output_path = TEMP_DIR / output_name
    result.save(output_path)

    image_index += 1
    
    return output_path


def clearTempFolder() -> None:
    """Delete the entire temp folder and all its contents."""

    if TEMP_DIR.exists():
        shutil.rmtree(TEMP_DIR)


# When module is called, setup essential stuff
initialise()
