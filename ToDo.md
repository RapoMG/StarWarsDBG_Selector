# To Do Order

1. ~~Faction names pics~~
2. ~~Missing Neutral~~
3. ~~Switch factions buttons~~
4. New first window
5. ~~Bubble speech pics for existing buttons~~
6. Setting players names
7. Start campaign after 2 players draw
8. Campaign list window
9. Campaign details

---

# Display Factions

## ~~Replace Names and Sets~~
Replace text with pictures:
- Core (purple and black)
  - Rebels (red)
  - Empire (blue)
- Clone Wars (purple and black)
  - Republic (red)
  - Separatists (blue)
- Mandalorian (green)
- Random neutral deck

## ~~Switch Pictures Dim/Normal~~
- Add pictures switching function to main.py
- Add checkbox-like function for names

```kv
<TeamSwitch@ToggleButton>:
    background_normal: (
        "assets/light_side.png"
        if self.state == "normal"
        else "assets/dark_side.png"
    )
    background_down: self.background_normal
    border: 0, 0, 0, 0
```

```kv
TeamSwitch:
    size_hint: 0.5, 0.2
```

## ~~Missing Neutral on 3 Players~~

---

# Additional Info

## Button Opening Pop-up Window
- Settings - input 4 players names / restore default Player 1 etc.
- Project info with ko-fi link/button
- Contact info (job recruitment purposes, but subtle)

---

# Campaign Tracker

- Removed cards - Base
- Starter deck cards removed
- Starter deck cards added
- Galaxy deck cards removed
- Galaxy deck cards added
- Force level (games 1 to 4)

---

# New First Screen

- Options
- Draw factions
- Campaign

---

# Campaign Window

## Campaign List
- Factions and game number

## Campaign Tracker (Details)



