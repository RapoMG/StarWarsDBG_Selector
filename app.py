from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.screenmanager import Screen, ScreenManager


# Window size
Window.size = (450,800) # (1080,1920)

### Multiple Screens
#First screen (page)
class PlayersWindow(Screen):

    def incr(self):
        #increases number up to 4
        number = int(self.ids.n_players.text)
        if number < 4:
            number += 1
        self.ids.n_players.text = str(number)

    def decr(self):
        #decreases value down to 2
        number = int(self.ids.n_players.text)
        if number > 2:
            number -= 1
        self.ids.n_players.text = str(number)

#second screen (page)
class FactionsWindow(Screen):
    pass

#thrid screen (page)
class DrawResultsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass


class SelectorApp(App):
    def build(self):
        return Builder.load_file("plrs_number.kv")

if __name__ == "__main__":
    SelectorApp().run()