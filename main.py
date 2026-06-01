from pathlib import Path

from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock

from kivy.lang import Builder
from kivy.resources import resource_add_path
from kivy.properties import StringProperty
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.utils import platform

BASE_DIR = Path(__file__).resolve().parent

from kivy.core.window import Window

# Keep the desktop test window small, but do not force a fixed window on Android.
if platform != "android":
    Config.set("graphics", "resizable", True)

    Window.size = (450, 800)  # 1920, 1080

# Make bundled assets discoverable when the app is packaged.
resource_add_path(str(BASE_DIR))
resource_add_path(str(BASE_DIR / "images"))

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
        app = App.get_running_app()
        app.shared_players = self.nbr_plyrs
        app.table.nbr_of_players(int(self.nbr_plyrs))


class LoadingWindow(Screen):
    def on_enter(self, *args):
        # Defer the first real screen until the window has had a chance to draw.
        Clock.schedule_once(self._show_first_screen, 0.15)

    def _show_first_screen(self, _dt):
        Window.canvas.ask_update()
        if self.manager is not None:
            self.manager.current = "p_number"


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
            if self.chk[i] == True:  # can't be short; without Boolean any object pass as True
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
        app = App.get_running_app()
        selected =[]
        src = App.get_running_app()
        if self.chk[1]: selected.append(src.fc[0])
        if self.chk[2]: selected.append(src.fc[1])
        if self.chk[4]: selected.append(src.fc[2])
        if self.chk[5]: selected.append(src.fc[3])
        if self.chk[6]: selected.append(src.fc[4])

        # Setting table
        app.table.set_game(selected)
        # Clean selection list
        selected.clear()

        # neutral deck visibility
        app.neut = self.ids.neut_check.active

    def is_neutral(self):
        # Option hidden for 3 players game
        if int(App.get_running_app().shared_players) == 3:
            self.ids.neut_lab.opacity = 0
            self.ids.neut_check.opacity = 0
        else:
            self.ids.neut_lab.opacity = 1
            self.ids.neut_check.opacity = 1


#thrid screen (page)
class DrawResultsWindow(Screen):

    def result(self):
        # Access shared variables
        app = App.get_running_app()
        # Number of players
        n = int(app.shared_players)

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
                if app.pl[i].first and st:
                    self.ids.f_line1.text = f"{app.pl[i].faction.name}\n commanded by {app.pl[i].name}"
                    st = False
                elif app.pl[i].first and not st:
                    self.ids.f_line2.text = f"{app.pl[i].faction.name}\n led by {app.pl[i].name}"
                elif not app.pl[i].first and frc:
                    self.ids.f_line3.text = f"{app.pl[i].faction.name}\n commanded by {app.pl[i].name}"
                    frc = False
                else:
                    self.ids.f_line4.text = f"and {app.pl[i].faction.name}\n led by {app.pl[i].name}"
            # Connecting lines
            self.ids.con_line1.text = "in alliance with"
            self.ids.con_line2.text = "starting their war effort against"

            # Neutral decks
            if app.neut:
                self.ids.n_line.text = (f"Neutral deck for\n"
                                        f" Region 1: {app.table.neut[0]}, Region 2: {app.table.neut[1]}")

        # 2 and 3 players game
        else:
            # 1st player
            if app.pl[0].first: st1 = " (starts)"
            self.ids.f_line1.text = f"{app.pl[0].faction.name}\n commanded by {app.pl[0].name}{st1} "

            #2nd player
            if app.pl[1].first: st2 = " (starts)"
            self.ids.f_line2.text = f"{app.pl[1].faction.name}\n leaded by {app.pl[1].name}{st2} "

            # 3rd player
            if n == 3:
                if app.pl[2].first: st3 = " (starts)"
                self.ids.f_line3.text = f"{app.pl[2].faction.name}\n commanded by {app.pl[2].name}{st3} "
                self.ids.con_line2.text = "and against"

            # Neutral deck
            if app.neut: self.ids.n_line.text = f"Neutral deck: {app.table.neut[0]}"


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
        self.ids.n_line.text = ""

class WindowManager(ScreenManager):
    pass



class SelectorApp(App):
    """ Main app """
    # Shared data accessible by all screens
    shared_players = StringProperty("Waiting for players...")
    #fc = factions
    #pl = players
    table = None
    fc = None
    pl = None

    # Should neutral deck be drawn
    neut = True


    def build(self):
        """ Build app """
        from elements import factions, players
        from table import Table

        # Initialize shared data before KV rules are evaluated.
        # faction_window.kv references app.fc during load, so it must exist here.
        self.table = Table()
        self.pl = players
        self.fc = factions

        resource_add_path(str(BASE_DIR))
        resource_add_path(str(BASE_DIR / "images"))
        return Builder.load_file(str(BASE_DIR / "main.kv"))

    def on_start(self):
        """ Initialize app """
        Clock.schedule_once(self._force_initial_redraw, 0)

    def on_resume(self):
        """ Refresh the window after Android returns from background. """
        Clock.schedule_once(self._force_initial_redraw, 0)

    def _force_initial_redraw(self, _dt):
        """ Nudge the first frame onto the screen on drivers that miss it. """
        if self.root is not None and self.root.canvas is not None:
            self.root.canvas.ask_update()
        Window.canvas.ask_update()


if __name__ == "__main__":
    # Run app
    SelectorApp().run()
