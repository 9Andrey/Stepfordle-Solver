"""Work in progress"""

import customtkinter
from PIL import Image
from pathlib import Path

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
    
    
def initialise():
    declarePaths()


class GuessGraphics(customtkinter.CTk):
    def __init__(self, id, values):
        ...


class App(customtkinter.CTk):
    def __init__(self):
        super().__init__()
        # Setup default theme
        customtkinter.set_default_color_theme("dark-blue")
        customtkinter.set_appearance_mode("system")

        # Basic app information        
        self.title("Stepfordle Solver")
        self.geometry("1080x600")
        
        # Set grid
        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure((0), weight=1)
        
        # Create parts for the app
        best_guess_text = customtkinter.CTkLabel(self, 
                                                 text="Make a guess to begin!", 
                                                 font=("Sans-serif", 30))
        best_guess_text.grid(row=1, column=0, padx=20, pady=20)

        # Add image
        picture = Image.open(DATA_DIR / "default_map.png")
        network_image = customtkinter.CTkImage(size=(500, 312), 
                                               dark_image=picture)        
        image_label = customtkinter.CTkLabel(self, image=network_image, text="")
        image_label.grid(row=2, column=0, padx=20, pady=20)

        # Add legend
        legend_text = customtkinter.CTkLabel(self, 
                                             text="(Blue) Possible stations | (Green) Best guess",
                                              font=("sans-serif", 20))
        legend_text.grid(row=3, column=0, padx=20, pady=20)


initialise()

if __name__ == "__main__":
    app = App()
    app.mainloop()