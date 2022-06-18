from easygui import diropenbox


class DataHandler:
    def __init__(self):
        self.directory = ""

    def choose_directory(self):
        """
           This functions uses easygui's directory chooser and sets the given path into the program.
        """
        try:
            directory = diropenbox()
            if directory != "":
                self.directory = directory

        except Exception as e:
            print(e)

    def save_data(self):
        pass