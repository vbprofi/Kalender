# main.py
"""
Dieses Skript initialisiert und startet die Kalenderanwendung.

Es erstellt eine Instanz der `MeinApp`-Klasse aus dem Modul `meinapp.py`
und startet die Hauptereignisschleife von wxPython, um die Anwendung auszuführen.
"""

import wx
from meinapp import MeinApp

def main():
    """
    Hauptfunktion, die die Anwendung startet.

    Erstellt eine Instanz der `MeinApp`-Klasse und startet die Hauptereignisschleife.

    Returns:
        None
    """
    app = MeinApp()
    app.MainLoop()

if __name__ == "__main__":
    main()
