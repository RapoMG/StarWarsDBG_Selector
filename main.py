from copy import deepcopy
from pathlib import Path
from typing import List, Optional
from functools import partial

from kivy.app import App
from kivy.config import Config
from kivy.clock import Clock

from kivy.lang import Builder
from kivy.resources import resource_add_path, resource_find
from kivy.properties import StringProperty
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.screenmanager import Screen, ScreenManager
from kivy.uix.popup import Popup
from kivy.utils import platform

from kivy.core.text import LabelBase
from kivy.uix.textinput import TextInput


BASE_DIR = Path(__file__).resolve().parent

from campaign import CampaignsListWindow, CampaignDetailsWindow, NewCampaignWindow


from kivy.core.window import Window

# Keep the desktop test window small, but do not force a fixed window on Android.
if platform != "android":
    Config.set("graphics", "resizable", True)

    Window.size = (450, 800)  # (1080, 1920)

# Make bundled assets discoverable when the app is packaged.
resource_add_path(str(BASE_DIR))
resource_add_path(str(BASE_DIR / "images"))

# Fonts
LabelBase.register(name="Comic",
                   fn_regular="fonts/HeroikanamikusRegular.otf",
                   fn_bold="fonts/HeroikanamikusBold.otf",
                   fn_italic="fonts/HeroikanamikusItalic.otf",
                   fn_bolditalic="fonts/HeroikanamikusBolditalic.otf",
                   )

LabelBase.register(name="Results", fn_regular="fonts/RussoOne-Regular.ttf",)
LabelBase.register(name="SW", fn_regular="fonts/StarJediHollow-A4lL.ttf",
                   fn_bold="fonts/StarJedi-DGRW.ttf")

LabelBase.register(name="Holo",
                   fn_regular="fonts/Firjar-Regular.ttf",
                   fn_bold="fonts/Firjar-Bold.ttf",
                   )
LabelBase.register(name="Holo_Ex",
                   fn_regular="fonts/FirjarExpanded-Regular.ttf",
                   fn_bold="fonts/FirjarExpanded-Bold.ttf",
                   )
class CardRenameBase(TextInput):
    """Base for CardRename and CardRenameRight for a card row for settings popup """
    text = StringProperty()

class CardRename(CardRenameBase):
    """Card row for settings popup """
    # text = StringProperty()
    pass


class CardRenameRight(CardRenameBase):
    """Card row for settings popup with different visual kivy output. """
    # text = StringProperty()
    pass


### Multiple Screens ###

## Main Screen ##
class WelcomeWindow(Screen):
    """
    Main window.
    """
    pass

## Draw Factions Screens ##

# Faction draw first screen (page)
class PlayersWindow(Screen):
    """
    Player selection screen.
    """
    nbr_plyrs = StringProperty("2")

    def incr(self):
        """
        Increases number up to 4.
        """
        #increases number up to 4
        number = int(self.nbr_plyrs)
        if number < 4: number += 1
        self.nbr_plyrs = str(number)

    def decr(self):
        """
        Decreases value down to 2.
        """
        #decreases value down to 2
        number = int(self.nbr_plyrs)
        if number > 2: number -= 1
        self.nbr_plyrs = str(number)

    def players(self):
        """
        Save value in the 'shared app' property.
        """
        # Save value in the 'shared app' property
        app = App.get_running_app()
        app.shared_players = self.nbr_plyrs
        app.table.nbr_of_players(int(self.nbr_plyrs))


class LoadingWindow(Screen):
    """
    Loading screen.
    """
    def on_enter(self, *args):
        # Defer the first real screen until the window has had a chance to draw.
        Clock.schedule_once(self._show_first_screen, 0.15)

    def _show_first_screen(self, _dt):
        Window.canvas.ask_update()
        if self.manager is not None:
            self.manager.current = "welcome"


# Faction draw second screen (page)
class FactionsWindow(Screen):
    """
    Faction selection screen.
    """
    # Checkers status
    chk:List[Optional[bool]] = [None, None, None, None, None, None, None]
    # set1, set1_f1 set1_f2, set2, set2_f1,set2_f2,exp1

    def updt_stat(self):
        """
        Update values of checkers. Calls hidden()
        """
        # Update values of checkers
        self.chk[1] = True if self.ids.set1_f1.state == "down" else False
        self.chk[2] =  True if self.ids.set1_f2.state == "down" else False

        self.chk[4] =  True if self.ids.set2_f1.state == "down" else False
        self.chk[5] = True if self.ids.set2_f2.state == "down" else False

        self.chk[6] =  True if self.ids.exp1.state == "down" else False

        # Sets checkers instance to test against flipper
        self.chk[0] = self.ids.set1
        self.chk[3] =  self.ids.set2

        self.hidden()

    def hidden(self):
        """
        Check if the number of selected factions equals the number of players.
        If so, show the next window button.
        """
        # show hidden button if selected factions equals number of players
        decks = 0
        plrs = App.get_running_app().shared_players
        self.ids.hidden_next.opacity = 0
        self.ids.hidden_next.disabled = True
        for i in range(len(self.chk)):
            if self.chk[i] == True:  # can't be short; without Boolean any object pass as True
                decks += 1
                if decks >= int(plrs):
                    self.ids.hidden_next.opacity = 1
                    self.ids.hidden_next.disabled = False

    def set_flipper(self, instance, value):
        """
        Check or uncheck all factions in a set
        """
        # Change status for whole set1
        if instance == self.chk[0]:
            if value:
                self.ids.set1_f1.state = "down"
                self.ids.set1_f2.state = "down"
            else:
                self.ids.set1_f1.state = "normal"
                self.ids.set1_f2.state = "normal"

        # Change status for whole set2
        if instance == self.chk[3]:
            if value:
                self.ids.set2_f1.state = "down"
                self.ids.set2_f2.state = "down"
            else:
                self.ids.set2_f1.state = "normal"
                self.ids.set2_f2.state = "normal"

    def set_splitter(self):
        """
        Uncheck the set if not all factions are checked
        """
        # Unchecked faction unchecks set1
        if self.ids.set1_f1.state == "down" and self.ids.set1_f2.state == "down":
            self.ids.set1.state = "down"
        else:
            self.ids.set1.state = "normal"

        ## Unchecked faction unchecks set 2
        if self.ids.set2_f1.state == "down" and self.ids.set2_f2.state == "down":
            self.ids.set2.state = "down"
        else:
            self.ids.set2.state = "normal"

    def draw(self):
        """
        Draw the selected factions and prepare the starting player
        """
        # Number of players and factions compared in hidden() method
        # Prepare selected factions
        app = App.get_running_app()
        selected =[]

        if self.chk[1]: selected.append(app.fc[0])
        if self.chk[2]: selected.append(app.fc[1])
        if self.chk[4]: selected.append(app.fc[2])
        if self.chk[5]: selected.append(app.fc[3])
        if self.chk[6]: selected.append(app.fc[4])

        # Setting table
        if not app.table.set_game(selected):
            return False

        # Clean selection list
        selected.clear()

        # neutral deck visibility
        app.neut = True if self.ids.neut_check.state == "down" else False
        app.root.current = "result"
        return True

    def is_neutral(self):
        """
        Hide neutral deck option for 3 players game
        """
        # Option hidden for 3 players game
        if int(App.get_running_app().shared_players) == 3:
            self.ids.neut_check.opacity = 0
        else:
            self.ids.neut_check.opacity = 1


# Faction draw third screen (page)
class DrawResultsWindow(Screen):
    """
    Draw results and starting player
    """

    def result(self):
        """
        Display the draw results and starting player switching lines to display depending on the number of players.
        """
        # Access shared variables
        app = App.get_running_app()
        # Number of players
        n = int(app.shared_players)
        players = app.data.get_players()  # Get players from storage

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
                if players[i].first and st:
                    self.ids.f_line1.text = f"{players[i].faction.name}\n commanded by {players[i].name}"
                    st = False
                elif players[i].first and not st:
                    self.ids.f_line2.text = f"{players[i].faction.name}\n led by {players[i].name}"
                elif not players[i].first and frc:
                    self.ids.f_line3.text = f"{players[i].faction.name}\n commanded by {players[i].name}"
                    frc = False
                else:
                    self.ids.f_line4.text = f"and {players[i].faction.name}\n led by {players[i].name}"
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
            if players[0].first: st1 = "\n (starts)"
            self.ids.f_line1.text = f"{players[0].faction.name}\n commanded by {players[0].name}{st1} "

            #2nd player
            if players[1].first: st2 = " (starts)"
            self.ids.f_line2.text = f"{players[1].faction.name}\n leaded by {players[1].name}{st2} "

            # 3rd player
            if n == 3:
                if players[2].first: st3 = " (starts)"
                self.ids.f_line3.text = f"{players[2].faction.name}\n commanded by {players[2].name}{st3} "
                self.ids.con_line2.text = "and against"
                self.ids.n_line.opacity = 0  # Neutral deck hidden (3 players deck used)

            # Neutral deck
            if app.neut: self.ids.n_line.text = f"Neutral deck: {app.table.neut[0]}"

    def clean(self):
        """
        Reset the draw results and text when going back to the previous screen
        """

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
        self.ids.n_line.opacity = 1  # Neutral deck visible


## Utilities ##
class InfoPopup(Popup):
    """
    Popup window with setting players names and information about the app.
    Values are passed from SelectorApp.open_settings().
    """

    # Properties for players names
    player1_name = StringProperty("")
    player2_name = StringProperty("")
    player3_name = StringProperty("")
    player4_name = StringProperty("")

    # Property for information about the app
    about = StringProperty("")

    def on_open(self):

        app = App.get_running_app()

        reb_cards = app.fc[0]
        imp_cards = app.fc[1]

        reb_rein = app.rein[0]
        imp_rein = app.rein[1]

        pub_cards = app.fc[2]
        sep_cards = app.fc[3]

        mando_cards = app.fc[4]


        self.populate_cards_list(
            self.ids.reb_layout,
            reb_cards
        )

        self.populate_cards_list(
            self.ids.reb_re_layout,
            reb_rein,
            True
        )

        self.populate_cards_list(
            self.ids.imp_layout,
            imp_cards
        )

        self.populate_cards_list(
            self.ids.imp_re_layout,
            imp_rein,
            True
        )

        self.populate_cards_list(
            self.ids.pub_layout,
            pub_cards
        )

        self.populate_cards_list(
            self.ids.sep_layout,
            sep_cards
        )

        self.populate_cards_list(
            self.ids.mando_layout,
            mando_cards
        )

    def populate_cards_list(self, container, deck, right_side: bool = False):
        """
        Populate a container with TextInput widgets for each card in the list.

        :param container: The container to populate
        :param deck: List of cards to populate the container with
        :param right_side: If True uses class with different look to populate container
        """

        container.clear_widgets()

        widget_class = CardRenameRight if right_side else CardRename

        for i, card_name in enumerate(deck.cards):
            ti = widget_class(
                text=card_name,
                multiline=False,
                size_hint_y=None,
                height=25,
            )

            ti.bind(text=partial(self.update_card_name, deck, i))
            container.add_widget(ti)

    @staticmethod
    def update_card_name( deck, index, widget, text):
        """
        Update the name of a card in the list.

        :param deck: Class Faction or Reinforcements
        :param index: Index of the card to update
        :param widget: TextInput widget
        :param text: New text for the card
        """
        deck.rename_card(index, text)

    def update(self):
        """
        Save players names to storage
        """
        # Get players names from text fields
        players = [
            self.ids.pl1_name.text,
            self.ids.pl2_name.text,
            self.ids.pl3_name.text,
            self.ids.pl4_name.text
        ]

        app = App.get_running_app()
        # Update players names in storage
        app.data.update_players(players)
        # Save changes to file
        app.data.save_file()

    @staticmethod
    def link_to_github(ref):
        """
        Open the app's GitHub page with the project page in the default web browser.
        """
        import webbrowser
        if ref == "homepage":
            webbrowser.open("https://github.com/RapoMG/StarWarsDBG_Selector")


class WindowManager(ScreenManager):
    pass


class SelectorApp(App):
    """ Main app """

    # Shared data accessible by all screens
    shared_players = StringProperty("Waiting for players...")
    selected_campaign = None
    working_campaign = None

    table = None
    data = None

    # base lists
    pl = None  # players
    fc = None  # factions
    rein = None  # reinforcements

    # working instances
    pl_working = None  # players
    fc_working = None  # factions
    rein_working = None  # reinforcements

    neut_deck = None  # neutral decks

    # Should neutral deck be drawn
    neut = True

    # Temporary variables
    selected_cards = None

    def build(self):
        """ Build app """
        #from elements import factions
        from table import Table
        from storage import Data

        # Load saved data
        self.data = Data()
        self.data.load_file()

        # Initialize shared data before KV rules are evaluated.
        # faction_window.kv references app.fc during load, so it must exist here.
        self.pl = self.data.get_players()
        self.fc = self.data.factions
        self.neut_deck = self.data.neutral
        self.rein = self.data.reinforcements

        self.table = Table(self.pl)

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

    def prepare_working_campaign(self, campaign=None):
        """
        Prepare working campaign for editing or clean current if param is empty.
        :param campaign: Campaign to work on or *None* to clean current campaign
        """
        self.selected_campaign = campaign
        self.working_campaign = deepcopy(self.selected_campaign)

    def prepare_working_elements(self):
        """
        Prepares working elements for editing.
        pl_working - Players
        fc_working - Factions
        rein_working - Reinforcements
        """

        self.pl_working = deepcopy(self.pl)
        self.fc_working = deepcopy(self.fc)
        self.rein_working = deepcopy(self.rein)

    def clear_working_elements(self):
        """Removes all working instances"""

        if self.pl_working is not None:
            self.pl_working.clear()

        if self.fc_working is not None:
            self.fc_working.clear()

        if self.rein_working is not None:
            self.rein_working.clear()

        self.selected_campaign = None
        self.working_campaign = None

    def open_settings(self):
        """ Open settings and info popup """
        app = App.get_running_app()
        # Prepare values
        players = app.data.get_players()
        about_path = resource_find("about.md")
        if about_path is None:
            about_path = BASE_DIR / "about.md"
        try:
            about = Path(about_path).read_text(encoding="utf-8")
        except FileNotFoundError:
            about = "Missing file"

        popup = InfoPopup(
            # Pass players names
            player1_name=players[0].name,
            player2_name=players[1].name,
            player3_name=players[2].name,
            player4_name=players[3].name,
            # Pass factions and reinforcements cards


            # Pass about text
            about=about,
        )
        # Open popup with prepared values
        popup.open()


if __name__ == "__main__":
    # Run app
    SelectorApp().run()
