# meinapp.py
"""
Dieses Modul definiert die `MeinApp`-Klasse, die die gesamte Anwendung steuert.

Die `MeinApp`-Klasse ist eine Unterklasse von `wx.App` und wird verwendet, um die Anwendung zu initialisieren und das Hauptfenster anzuzeigen.
"""

import wx
from hauptfenster import HauptFenster

class MeinApp(wx.App):
    """
    Diese Klasse repräsentiert die Anwendung als Ganzes.

    Sie ist verantwortlich für die Initialisierung und Anzeige des Hauptfensters.

    Args:
        wx.App: Ein Anwendungsobjekt von wxPython.
    """

    def OnInit(self):
        """
        Initialisiert die Anwendung und zeigt das Hauptfenster an.

        Returns:
            bool: True, wenn die Initialisierung erfolgreich war, sonst False.
        """

        self.hauptfenster = HauptFenster(None)
        self.hauptfenster.Show()
        return True
