# eintraganzeigen.py
import wx

class EntryContentDialog(wx.Frame):
    """Ein benutzerdefiniertes Fenster zum Anzeigen der Inhalte eines ausgewählten Eintrags."""

    def __init__(self, parent, title, content):
        """
        Initialisiert das EntryContentDialog-Objekt.

        Args:
            parent (wx.Window): Das Elternfenster, zu dem dieses Fenster gehört.
            title (str): Der Titel des Fensters.
            content (str): Der Inhalt, der im Fenster angezeigt werden soll.
        """

        super().__init__(parent, title=title, size=(800, 800))

        panel = wx.Panel(self)
        sizer = wx.BoxSizer(wx.VERTICAL)

        text_ctrl = wx.TextCtrl(panel, style=wx.TE_MULTILINE | wx.TE_READONLY)
        text_ctrl.SetValue(content)
        sizer.Add(text_ctrl, 1, wx.EXPAND | wx.ALL, 10)

        panel.SetSizerAndFit(sizer)

        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_pressed)

    def on_key_pressed(self, event):
        """Behandelt das Tastaturereignis für das Fenster."""

        key_code = event.GetKeyCode()

        if key_code == wx.WXK_ESCAPE:
            # ESC-Taste zum Schließen des Fensters
            self.Close()
        else:
            event.Skip()  # Weitergabe des Ereignisses an das Standardverhalten
