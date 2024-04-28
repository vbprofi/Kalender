# eintragbearbeiten.py
import wx
import sqlite3

class BearbeitungsDialog(wx.Dialog):
    """
    Ein benutzerdefinierter Dialog zum Bearbeiten von Einträgen.

    Attributes:
        parent (wx.Window): Das übergeordnete Fenster, zu dem dieser Dialog gehört.
        db_conn (sqlite3.Connection): Die SQLite-Datenbankverbindung.
        date (str): Das Datum des Eintrags.
        day_of_week (str): Der Wochentag des Eintrags.
        time (str): Die Uhrzeit des Eintrags.
        additional_info (str): Zusätzliche Informationen des Eintrags.
    """

    def __init__(self, parent, db_conn, date, day_of_week, time, additional_info):
        """
        Initialisiert den Bearbeitungsdialog für den ausgewählten Eintrag.

        Args:
            parent (wx.Window): Das übergeordnete Fenster, zu dem dieser Dialog gehört.
            db_conn (sqlite3.Connection): Die SQLite-Datenbankverbindung.
            date (str): Das Datum des Eintrags.
            day_of_week (str): Der Wochentag des Eintrags.
            time (str): Die Uhrzeit des Eintrags.
            additional_info (str): Zusätzliche Informationen des Eintrags.
        """
        super().__init__(parent, title="Eintrag bearbeiten")

        self.db_conn = db_conn
        self.date = date
        self.day_of_week = day_of_week
        self.time = time
        self.additional_info = additional_info

        self.add_autoincrement_id_column()
        # Ermittle die ID des Eintrags in der Datenbank
        self.entry_id = self.get_entry_id()

        self.initialize_ui()

    def initialize_ui(self):
        """Initialisiert die Benutzeroberfläche des Bearbeitungsdialogs."""

        sizer = wx.BoxSizer(wx.VERTICAL)

        # Label und TextCtrl für das Datum (schreibgeschützt)
        date_label = wx.StaticText(self, label="Datum:")
        self.date_text = wx.TextCtrl(self, value=self.date, style=wx.TE_PROCESS_ENTER) #, style=wx.TE_READONLY)

        # Label und TextCtrl für den Wochentag (schreibgeschützt)
        day_of_week_label = wx.StaticText(self, label="Wochentag:")
        self.day_of_week_text = wx.TextCtrl(self, value=self.day_of_week) #, style=wx.TE_READONLY)

        # Label und TextCtrl für die Uhrzeit
        time_label = wx.StaticText(self, label="Uhrzeit:")
        self.time_text = wx.TextCtrl(self, value=self.time)

        # Label und Multiline-TextCtrl für zusätzliche Informationen
        additional_info_label = wx.StaticText(self, label="Zusätzliche Informationen:")
        self.additional_info_text = wx.TextCtrl(self, value=self.additional_info, style=wx.TE_MULTILINE)

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

        # Event-Handler für OK und Abbrechen hinzufügen
        self.Bind(wx.EVT_BUTTON, self.on_ok_button, id=wx.ID_OK)
        self.Bind(wx.EVT_BUTTON, self.on_cancel_button, id=wx.ID_CANCEL)

        # Event-Handler für das Verlassen des Datum-Textfeldes hinzufügen
        self.date_text.Bind(wx.EVT_TEXT_ENTER, self.on_date_text_leave)

        # Festlegen des Sizers für den Dialog
        self.SetSizerAndFit(sizer)

    def get_entry_id(self):
        """
        Ermittelt die ID des Eintrags in der Datenbank basierend auf Datum, Uhrzeit und zusätzlichen Informationen.
        """
        try:
            cursor = self.db_conn.cursor()
            select_query = "SELECT ID FROM Entries WHERE Date = ? AND Time = ? AND AdditionalInfo = ?"
            cursor.execute(select_query, (self.date, self.time, self.additional_info))
            result = cursor.fetchone()
            if result:
                return result[0]  # ID des Eintrags
            return None
        except sqlite3.Error as e:
            wx.MessageBox(f"Fehler beim Abrufen der Eintrags-ID: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)

    def update_entry(self):
        """Aktualisiert den Eintrag in der Datenbank mit den bearbeiteten Informationen."""

        new_date = self.date_text.GetValue()
        new_day_of_week = self.day_of_week_text.GetValue()
        new_time = self.time_text.GetValue()
        new_additional_info = self.additional_info_text.GetValue()

        if self.entry_id is not None:
            print("id")
            try:
                cursor = self.db_conn.cursor()
                update_query = "UPDATE Entries SET Date = ?, DayOfWeek = ?, Time = ?, AdditionalInfo = ? WHERE ID = ?"
                cursor.execute(update_query, (new_date, new_day_of_week, new_time, new_additional_info, self.entry_id))
                
                # Commit der Änderungen
                self.db_conn.commit()
                
                wx.MessageBox("Eintrag erfolgreich aktualisiert.", "Erfolg", wx.OK | wx.ICON_INFORMATION)
            except sqlite3.Error as e:
                wx.MessageBox(f"Fehler beim Aktualisieren des Eintrags: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)
        else:
            print("not id")

    def add_autoincrement_id_column(self):
        cursor = self.db_conn.cursor()
        table_name = 'Entries'

        try:
            # Überprüfen, ob die Spalte 'ID' bereits existiert
            cursor.execute(f"PRAGMA table_info({table_name})")
            columns = cursor.fetchall()

            id_column_exists = any(column[1] == 'ID' for column in columns)

            if not id_column_exists:
                self._add_autoincrement_id_column()
                wx.MessageBox(f"Spalte 'ID' erfolgreich hinzugefügt.", "Erfolg", wx.OK | wx.ICON_INFORMATION)
            else:
                #wx.MessageBox(f"Spalte 'ID' existiert bereits.", "Error", wx.OK | wx.ICON_ERROR)
                pass

        except sqlite3.Error as e:
            wx.MessageBox(f"Fehler beim Hinzufügen der Spalte 'ID': {e}", "Error", wx.OK | wx.ICON_ERROR)

        finally:
            # Verbindung schließen
            pass


    def _add_autoincrement_id_column(self):
        cursor = self.db_conn.cursor()
        table_name = 'Entries'

        try:
            # Erstellen einer neuen temporären Tabelle mit AUTOINCREMENT-ID
            temp_table_name = f"temp_{table_name}"
            create_query = f"CREATE TABLE {temp_table_name} (ID INTEGER PRIMARY KEY AUTOINCREMENT, Date TEXT, DayOfWeek TEXT, Time TEXT, AdditionalInfo TEXT)"
            cursor.execute(create_query)

            # Kopieren von Daten aus der alten Tabelle in die neue Tabelle
            copy_query = f"INSERT INTO {temp_table_name} (Date, DayOfWeek, Time, AdditionalInfo) SELECT Date, DayOfWeek, Time, AdditionalInfo FROM {table_name}"
            cursor.execute(copy_query)

            # Löschen der alten Tabelle
            drop_query = f"DROP TABLE {table_name}"
            cursor.execute(drop_query)

            # Umbenennen der neuen Tabelle in den ursprünglichen Tabellennamen
            rename_query = f"ALTER TABLE {temp_table_name} RENAME TO {table_name}"
            cursor.execute(rename_query)

            # Commit der Änderungen
            self.db_conn.commit()
            print("Spalte 'ID' erfolgreich hinzugefügt.")

        except sqlite3.Error as e:
            print(f"Fehler beim Hinzufügen der Spalte 'ID': {e}")

        finally:
            # Verbindung schließen
            pass

    def on_ok_button(self, event):
        """Event-Handler für den OK-Button"""

        # Führe die Aktualisierung des Eintrags aus
        self.update_entry()

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
            import datetime
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
