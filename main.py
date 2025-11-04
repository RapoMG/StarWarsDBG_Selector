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
        src = App.get_running_app()
        if self.chk[1]: selected.append(src.fc[0])
        if self.chk[2]: selected.append(src.fc[1])
        if self.chk[4]: selected.append(src.fc[2])
        if self.chk[5]: selected.append(src.fc[3])
        if self.chk[6]: selected.append(src.fc[4])

        # Setting table
        tbl.set_game(selected)
        # Clean selection list
        selected.clear()


#thrid screen (page)
class DrawResultsWindow(Screen):

    def result(self):
        # Access shared variables
        a = App.get_running_app()
        # Number of players
        n = int(App.get_running_app().shared_players)

        # Starting player txt
        st1=""
        st2=""
        st3=""

        # 4 players (team play)
        if n==4:
            # Factions lines
            st = True
            frc = True
            for i in range (4):
                if a.pl[i].first and st:
                    self.ids.f_line1.text = f"{a.pl[i].faction.name}\n commanded by {a.pl[i].name}"
                    st = False
                elif a.pl[i].first and not st:
                    self.ids.f_line2.text = f"{a.pl[i].faction.name}\n led by {a.pl[i].name}"
                elif not a.pl[i].first and frc:
                    self.ids.f_line3.text = f"{a.pl[i].faction.name}\n commanded by {a.pl[i].name}"
                    frc = False
                else:
                    self.ids.f_line4.text = f"and {a.pl[i].faction.name}\n led by {a.pl[i].name}"
            # Connecting lines
            self.ids.con_line1.text = "in alliance with"
            self.ids.con_line2.text = "starting their war effort against"

        # 2 and 3 players game
        else:
            # 1st player
            if a.pl[0].first: st1 = " (starts)"
            self.ids.f_line1.text = f"{a.pl[0].faction.name}\n commanded by {a.pl[0].name}{st1} "

            #2nd player
            if a.pl[1].first: st2 = " (starts)"
            self.ids.f_line2.text = f"{a.pl[1].faction.name}\n leaded by {a.pl[1].name}{st2} "

            # 3rd player
            if n == 3:
                if a.pl[2].first: st3 = " (starts)"
                self.ids.f_line3.text = f"{a.pl[2].faction.name}\n commanded by {a.pl[2].name}{st3} "
                self.ids.con_line2.text = "and against"


    def clean(self):
        # Reset draws
        for i in range(4):
            App.get_running_app().pl[i].add_faction(None)
            App.get_running_app().pl[i].first = False

        # Reset text
        self.ids.con_line1.text = "versus"
        self.ids.con_line2.text = ""
        self.ids.f_line3.text = ""
        self.ids.f_line4.text = ""

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
