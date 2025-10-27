from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.uix.widget import Widget

Window.size = (450,800)
#Window.size = (1080,1920)

class MainLayout(Widget):
    Builder.load_file("plrs_number.kv")

    def incr(self):
        #increas number up to 4
        number = int(self.ids.n_players.text)
        if number < 4:
            number += 1
        self.ids.n_players.text = str(number)

    def decr(self):
        #decreas value down to 2
        number = int(self.ids.n_players.text)
        if number > 2:
            number -= 1
        self.ids.n_players.text = str(number)

class SelectorApp(App):
    def build(self):
        return MainLayout()

if __name__ == "__main__":
    SelectorApp().run()