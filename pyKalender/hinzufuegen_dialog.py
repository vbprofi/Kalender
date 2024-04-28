# hinzufuegen_dialog.py
import wx
import sqlite3
import datetime

class HinzufuegenDialog(wx.Dialog):
    """
    Ein benutzerdefinierter Dialog zum Hinzufügen neuer Einträge in die Datenbank.

    Attributes:
        parent (wx.Window): Das übergeordnete Fenster, zu dem dieser Dialog gehört.
        db_conn (sqlite3.Connection): Die SQLite-Datenbankverbindung.
        date (str): Das Datum des Eintrags im Format "TT.MM.JJJJ".
    """

    def __init__(self, parent, db_conn, date):
        """
        Initialisiert den Dialog zum Hinzufügen neuer Einträge in die Datenbank.

        Args:
            parent (wx.Window): Das übergeordnete Fenster, zu dem dieser Dialog gehört.
            db_conn (sqlite3.Connection): Die SQLite-Datenbankverbindung.
            date (str): Das Datum des Eintrags im Format "TT.MM.JJJJ".
        """
        super().__init__(parent, title="Neuen Eintrag hinzufügen")

        self.db_conn = db_conn
        self.date = date

        self.initialize_ui()

    def initialize_ui(self):
        """Initialisiert die Benutzeroberfläche des Dialogs zum Hinzufügen neuer Einträge."""

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Label und TextCtrl für das Datum
        date_label = wx.StaticText(self, label="Datum:")
        self.date_text = wx.TextCtrl(self, value=self.date, style=wx.TE_PROCESS_ENTER) #, style=wx.TE_READONLY)

        # Ermittle den Wochentag
        try:
            dt = datetime.datetime.strptime(self.date, "%d.%m.%Y")
            weekday_index = dt.weekday()  # Index des Wochentags (0 = Montag, 1 = Dienstag, ...)

            # Liste mit deutschen Wochentagen
            german_weekdays = [
                "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"
            ]

            # Wähle den entsprechenden deutschen Wochentag aus der Liste
            german_weekday = german_weekdays[weekday_index]
        except ValueError:
            german_weekday = ""

        # Label und TextCtrl für den Wochentag
        day_of_week_label = wx.StaticText(self, label="Wochentag:")
        self.day_of_week_text = wx.TextCtrl(self, value=german_weekday) #, style=wx.TE_READONLY)

        # Label und TextCtrl für die Uhrzeit (standardmäßig auf "00:00" gesetzt)
        time_label = wx.StaticText(self, label="Uhrzeit:")
        self.time_text = wx.TextCtrl(self, value="00:00")

        # Label und Multiline-TextCtrl für zusätzliche Informationen
        additional_info_label = wx.StaticText(self, label="Zusätzliche Informationen:")
        self.additional_info_text = wx.TextCtrl(self, style=wx.TE_MULTILINE)

        # Hinzufügen der Labels und Textfelder zum Sizer
        sizer.Add(date_label, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.date_text, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(day_of_week_label, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.day_of_week_text, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(time_label, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.time_text, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(additional_info_label, 0, wx.ALL | wx.EXPAND, 10)
        sizer.Add(self.additional_info_text, 1, wx.ALL | wx.EXPAND, 10)

        # Button-Sizer für OK und Abbrechen
        btn_sizer = self.CreateButtonSizer(wx.OK | wx.CANCEL)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER | wx.ALL, 10)

        # Event-Handler für das Verlassen des Datum-Textfeldes hinzufügen
        self.date_text.Bind(wx.EVT_TEXT_ENTER, self.on_date_text_leave)

        # Event-Handler für OK und Abbrechen hinzufügen
        self.Bind(wx.EVT_BUTTON, self.on_ok_button, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.on_cancel_button, id=wx.ID_CANCEL)

        # Festlegen des Sizers für den Dialog
        self.SetSizerAndFit(sizer)

    def add_entry_to_database(self):
        """Fügt den neuen Eintrag in die Datenbank ein."""

        new_date = self.date_text.GetValue()
        new_day_of_week = self.day_of_week_text.GetValue()
        new_time = self.time_text.GetValue()
        new_additional_info = self.additional_info_text.GetValue()

        try:
            cursor = self.db_conn.cursor()
            insert_query = "INSERT INTO Entries (Date, DayOfWeek, Time, AdditionalInfo) VALUES (?, ?, ?, ?)"
            cursor.execute(insert_query, (new_date, new_day_of_week, new_time, new_additional_info))
            
            # Commit der Änderungen
            self.db_conn.commit()
            
            wx.MessageBox("Neuer Eintrag erfolgreich hinzugefügt.", "Erfolg", wx.OK | wx.ICON_INFORMATION)
        except sqlite3.Error as e:
            wx.MessageBox(f"Fehler beim Hinzufügen des Eintrags: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)

    def on_ok_button(self, event):
        """Event-Handler für den OK-Button"""

        # Füge den neuen Eintrag in die Datenbank ein
        self.add_entry_to_database()

        # Schließe den Dialog
        self.EndModal(wx.ID_OK)

    def on_cancel_button(self, event):
        """Event-Handler für den Abbrechen-Button"""

        # Schließe den Dialog
        self.EndModal(wx.ID_CANCEL)

    def on_date_text_leave(self, event):
        """Event-Handler für das Verlassen des Datum-Textfeldes"""

        # Ermittle das Datum aus dem Textfeld
        entered_date = self.date_text.GetValue()

        # Versuche, den Wochentag zu ermitteln
        try:
            dt = datetime.datetime.strptime(entered_date, "%d.%m.%Y")
            weekday_index = dt.weekday()  # Index des Wochentags (0 = Montag, 1 = Dienstag, ...)

            # Liste mit deutschen Wochentagen
            german_weekdays = [
                "Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"
            ]

            # Wähle den entsprechenden deutschen Wochentag aus der Liste
            german_weekday = german_weekdays[weekday_index]

            self.day_of_week_text.SetValue(german_weekday)
        except ValueError:
            # Fehler beim Parsen des Datums
            wx.MessageBox("Ungültiges Datumsformat.", "Fehler", wx.OK | wx.ICON_ERROR)

