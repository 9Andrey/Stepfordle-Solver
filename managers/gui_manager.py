import customtkinter as ctk
from PIL import Image
from pathlib import Path
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


def makeDictionaries():
    """Creates useful dictionaries for efficient lookups,
        instead of looking in the CSVs"""
    
    # Get a dictionary with station data
    global stations
    stations = (
        pd.read_csv(DATA_DIR / "stations.csv", skipinitialspace=True)
        .set_index("id")
        .to_dict(orient="index")
    )

    
def initialise():
    declarePaths()
    makeDictionaries()


initialise()


# Integer selection box
class IntSpinbox(ctk.CTkFrame):
    def __init__(
        self,
        master,
        value=0,
        min_value=0,
        max_value=20,
        width=110,
        **kwargs,
    ):
        super().__init__(master, fg_color="transparent", **kwargs)

        self.min_value = min_value
        self.max_value = max_value

        self.minus = ctk.CTkButton(
            self,
            text="-",
            width=28,
            command=self.decrease,
        )
        self.minus.pack(side="left", padx=(0, 2))

        self.entry = ctk.CTkEntry(
            self,
            width=45,
            justify="center",
        )
        self.entry.pack(side="left", padx=2)
        self.entry.insert(0, str(value))

        self.plus = ctk.CTkButton(
            self,
            text="+",
            width=28,
            command=self.increase,
        )
        self.plus.pack(side="left", padx=(2, 0))


    def get(self):
        try:
            value = int(self.entry.get())
        except ValueError:
            value = self.min_value

        value = max(self.min_value, min(self.max_value, value))
        return value


    def set(self, value):
        self.entry.delete(0, "end")
        self.entry.insert(0, str(value))


    def increase(self):
        self.set(self.get() + 1)


    def decrease(self):
        self.set(self.get() - 1)


    def lock(self):
        self.minus.configure(state="disabled")
        self.plus.configure(state="disabled")
        self.entry.configure(state="disabled")


# Guess input row.
class Guess(ctk.CTkFrame):
    station_names = [station["station_name"] for station in stations.values()]
    
    def __init__(self, master, confirm_callback):
        super().__init__(master, fg_color="transparent")

        self.confirm_callback = confirm_callback

        self.station = ctk.CTkComboBox(
            self,
            values=self.station_names,
            width=220,
            state="readonly",
        )
        self.station.pack(side="left", padx=5)

        if self.station_names:
            self.station.set(self.station_names[0])

        self.zone = IntSpinbox(self, value=0)
        self.zone.pack(side="left", padx=5)

        self.stops = IntSpinbox(self, value=0)
        self.stops.pack(side="left", padx=5)

        self.button = ctk.CTkButton(
            self,
            text="✓",
            width=45,
            command=self.confirm,
        )
        self.button.pack(side="left", padx=5)


    def confirm(self):
        self.station.configure(state="disabled")
        self.zone.lock()
        self.stops.lock()
        self.button.configure(state="disabled")

        self.confirm_callback()


    def get_data(self):
        return {
            "station": self.station.get(),
            "zone_distance": self.zone.get(),
            "stops": self.stops.get(),
        }


# List of all guesses
class GuessesUI(ctk.CTkFrame):
    MAX_ROWS = 6
    station_names = [station["station_name"] for station in stations.values()]


    def __init__(
        self,
        master,
        image_size=(850, 415),
        **kwargs,
    ):
        super().__init__(master, **kwargs)
        
        self.image_size = image_size

        self.rows = []

        self.input_frame = ctk.CTkFrame(self)
        self.input_frame.pack(fill="x", padx=10, pady=10)

        self.add_row()

        self.status_label = ctk.CTkLabel(
            self,
            text="Ready",
            anchor="w",
            font=ctk.CTkFont(size=18, weight="bold"),
        )
        self.status_label.pack(fill="x", padx=10, pady=(5, 10))
        
        self.image_label = ctk.CTkLabel(self, text="")
        self.image_label.pack(padx=10)

        self.legend_label = ctk.CTkLabel(
            self,
            text="Map legend",
            font=ctk.CTkFont(size=14),
        )
        self.legend_label.pack(pady=(5, 10))

        self.set_image(DATA_DIR / "default_map.png")


    def add_row(self):
        if len(self.rows) >= self.MAX_ROWS:
            return

        row = Guess(
            self.input_frame,
            self.add_row)

        row.pack(fill="x", pady=4)
        self.rows.append(row)


    def get_all_values(self):
        """Returns all confirmed rows."""

        values = []

        for row in self.rows:
            if row.button.cget("state") == "disabled":
                values.append(row.get_data())

        return values


    def set_status(self, text: str):
        self.status_label.configure(text=text)


    def set_legend(self, text: str):
        self.legend_label.configure(text=text)


    def set_image(self, path: Path):
        image = ctk.CTkImage(
            light_image=Image.open(path),
            dark_image=Image.open(path),
            size=self.image_size,
        )

        self.current_image = image
        self.image_label.configure(image=image)


class App(ctk.CTk):
    def __init__(self):
        super().__init__()

        self.title("Stepfordle Solver")
        self.geometry("1080x605")

        ctk.set_appearance_mode("system")
        
        self.ui = GuessesUI(self)
        self.ui.pack(fill="both", expand=True)

        # Example setup
        self.ui.set_status("Start by setting a guess!")
        self.ui.set_legend("Blue: available guesses | Green: best guess")


    def get_values(self):
        return self.ui.get_all_values()


    def set_status(self, text: str):
        self.ui.set_status(text)


    def set_map(self, path: Path):
        self.ui.set_image(path)


    def set_legend(self, text: str):
        self.ui.set_legend(text)


if __name__ == "__main__":
    app = App()
    app.mainloop()