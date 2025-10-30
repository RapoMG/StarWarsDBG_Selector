from kivy.app import App
from kivy.core.window import Window
from kivy.lang import Builder
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.checkbox import CheckBox

from table import Table
from elements import factions, players

ch = CheckBox()

# Window size
Window.size = (450,800) # (1080,1920)

### Multiple Screens
#First screen (page)
class PlayersWindow(Screen):
    nbr_plyrs = StringProperty("2")

    def incr(self):
        #increases number up to 4
        number = int(self.nbr_plyrs)
        if number < 4: number += 1
        self.nbr_plyrs = str(number)

    def decr(self):
        #decreases value down to 2
        number = int(self.nbr_plyrs)
        if number > 2: number -= 1
        self.nbr_plyrs = str(number)

    def players(self):
        # Save value in the 'shared app' property
        App.get_running_app().shared_players = self.nbr_plyrs
        tbl.nbr_of_players(int(self.nbr_plyrs))


#second screen (page)
class FactionsWindow(Screen):
    # Checkers status
    chk = [None, None, None, None, None, None, None]
    # set1, set1_f1 set1_f2, set2, set2_f1,set2_f2,exp1

    def updt_stat(self):
        # Update values of checkers
        self.chk[1] = self.ids.set1_f1.active
        self.chk[2] =  self.ids.set1_f2.active

        self.chk[4] =  self.ids.set2_f1.active
        self.chk[5] = self.ids.set2_f2.active

        self.chk[6] =  self.ids.exp1.active

        # Sets checkers instance to test against flipper
        self.chk[0] = self.ids.set1
        self.chk[3] =  self.ids.set2

        self.hidden()


    def hidden(self):
        # show hidden button if selected factions equals number of players
        decks = 0
        plrs = App.get_running_app().shared_players
        self.ids.hidden_next.opacity = 0
        for i in range(len(self.chk)):
            if self.chk[i] == True:  # cant be short; without Boolean object pass as True
                decks += 1
                if decks >= int(plrs):
                    self.ids.hidden_next.opacity = 1


    def set_flipper(self, instance, value):
        # Change status for whole set1
        if instance == self.chk[0]:
            if value:
                self.ids.set1_f1.active = True
                self.ids.set1_f2.active = True
            else:
                self.ids.set1_f1.state = "normal"
                self.ids.set1_f2.state = "normal"

        # Change status for whole set1
        if instance == self.chk[3]:
            if value:
                self.ids.set2_f1.state = "down"
                self.ids.set2_f2.state = "down"
            else:
                self.ids.set2_f1.state = "normal"
                self.ids.set2_f2.state = "normal"

    def set_splitter(self):
        # Unchecked faction unchecks set1
        if self.ids.set1_f1.active and self.ids.set1_f2.active:
            self.ids.set1.active = True
        else:
            self.ids.set1.active = False

        ## Unchecked faction unchecks set 2
        if self.ids.set2_f1.active and self.ids.set2_f2.active:
            self.ids.set2.active = True
        else:
            self.ids.set2.active = False

    def draw(self):
        # Number of players and factions compared in hidden() method
        # Prepare selected factions
        selected =[]
        for i in range(len(self.chk)):
            if self.chk[1]: selected.append(self.app.fc[0])
            if self.chk[2]: selected.append(self.app.fc[1])
            if self.chk[4]: selected.append(self.app.fc[2])
            if self.chk[5]: selected.append(self.app.fc[3])
            if self.chk[6]: selected.append(self.app.fc[4])

        # Setting table
        tbl.set_game(selected)
        # Clean selection list?
        selected.clear()


#thrid screen (page)
class DrawResultsWindow(Screen):
    pass

class WindowManager(ScreenManager):
    pass



class SelectorApp(App):
    # Shared data accessible by all screens
    shared_players = StringProperty("Waiting for players...")
    fc = factions
    pl = players


    def build(self):

        return Builder.load_file("plrs_number.kv")

if __name__ == "__main__":
    # Create game table
    tbl = Table()
    # Run app
    SelectorApp().run()
