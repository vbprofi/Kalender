# hauptfenster.py
"""
Dieses Modul definiert die `HauptFenster`-Klasse, die das Hauptfenster der Kalenderanwendung repräsentiert.
"""

import wx
import sys
import calendar
import sqlite3
import os

from alleanzeigen_dialog import AlleAnzeigenDialog
from hinzufuegen_dialog import HinzufuegenDialog

class HauptFenster(wx.Frame):
    """
    Diese Klasse repräsentiert das Hauptfenster der Kalenderanwendung.

    Args:
        wx.Frame: Ein Fensterobjekt von wxPython.

    Attributes:
        db_datei (str): Der Pfad zur SQLite-Datenbankdatei.
        db_conn (sqlite3.Connection): Die Verbindung zur geöffneten Datenbank.
        datum_textbox (wx.TextCtrl): Das Textfeld zur Eingabe des Datums.
        jahr_numeric (wx.SpinCtrl): Die Steuerung für die Auswahl des Jahres.
        monat_listbox (wx.ListBox): Die ListBox zur Auswahl des Monats.
        wochentag_listbox (wx.ListBox): Die ListBox zur Anzeige der Wochentage.
        wochentag_label (wx.StaticText): Das Label für den ausgewählten Wochentag.
    """

    def __init__(self, *args, **kwargs):
        """
        Initialisiert das Hauptfenster der Kalenderanwendung.

        Args:
            *args: Positionale Argumente für wx.Frame.
            **kwargs: Schlüsselwortargumente für wx.Frame.
        """

        super(HauptFenster, self).__init__(*args, **kwargs)

        self.SetTitle("Kalender")
        self.SetSize((400, 200))

        # Datenbank-Datei-Variable
        self.db_datei = None
        self.db_conn = None

        # Oberflächenelemente erstellen
        self.erstelle_gui()

        # Aktuelles Datum ermitteln
        self.aktualisiere_aktuelles_datum()

        # Menüeinträge initialisieren
        self.update_menu_items()

    def erstelle_gui(self):
        """
        Erstellt die Benutzeroberfläche des Hauptfensters.
        """

        panel = wx.Panel(self)

        # Sizer für das Layout
        sizer = wx.BoxSizer(wx.VERTICAL)

        # Label für das Datum
        datum_label = wx.StaticText(panel, label="Datum (tt.mm.jjjj):")
        sizer.Add(datum_label, 0, wx.ALL | wx.EXPAND, 10)

        # Textbox für das Datum
        self.datum_textbox = wx.TextCtrl(panel, style=wx.TE_PROCESS_ENTER)
        self.Bind(wx.EVT_TEXT_ENTER, self.on_enter_datum, self.datum_textbox)
        sizer.Add(self.datum_textbox, 0, wx.ALL | wx.EXPAND, 10)

        # Label und NumericCtrl für das Jahr
        jahr_label = wx.StaticText(panel, label="Jahr:")
        sizer.Add(jahr_label, 0, wx.ALL | wx.EXPAND, 10)
        self.jahr_numeric = wx.SpinCtrl(panel, min=1900, max=2100)
        self.Bind(wx.EVT_SPINCTRL, self.on_jahr_changed, self.jahr_numeric)
        sizer.Add(self.jahr_numeric, 0, wx.ALL | wx.EXPAND, 10)

        # Label und ListBox für Monate
        monat_label = wx.StaticText(panel, label="Monat:")
        sizer.Add(monat_label, 0, wx.ALL | wx.EXPAND, 10)
        monate = ["01 Januar", "02 Februar", "03 März", "04 April", "05 Mai", "06 Juni",
                  "07 Juli", "08 August", "09 September", "10 Oktober", "11 November", "12 Dezember"]
        self.monat_listbox = wx.ListBox(panel, choices=monate, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.on_monat_auswahl, self.monat_listbox)
        sizer.Add(self.monat_listbox, 0, wx.ALL | wx.EXPAND, 10)

        # Label und ListBox für Wochentage
        self.wochentag_label = wx.StaticText(panel, label="Wochentag:")
        sizer.Add(self.wochentag_label, 0, wx.ALL | wx.EXPAND, 10)
        self.wochentag_listbox = wx.ListBox(panel, style=wx.LB_SINGLE)
        self.Bind(wx.EVT_LISTBOX, self.on_wochentag_auswahl, self.wochentag_listbox)
        sizer.Add(self.wochentag_listbox, 0, wx.ALL | wx.EXPAND, 10)

        # Hauptmenü erstellen
        menubar = wx.MenuBar()
        datei_menu = wx.Menu()
        aktion_menu = wx.Menu()
        info_menu = wx.Menu()

        # Menüeintrag für Öffnen
        self.open_item = datei_menu.Append(wx.ID_ANY, "&Öffnen\tCtrl-O", "Öffne .db Datei")
        self.Bind(wx.EVT_MENU, self.on_open, self.open_item)

        # Menüeintrag für Schließen
        self.close_item = datei_menu.Append(wx.ID_ANY, "&Schließen\tCtrl-S", "Schließe .db Datei")
        self.Bind(wx.EVT_MENU, self.on_close, self.close_item)

        # Menüeintrag für Beenden
        exit_item = datei_menu.Append(wx.ID_ANY, "&Beenden\tCtrl-Q", "Beende die Anwendung")
        self.Bind(wx.EVT_MENU, self.on_exit, exit_item)

        menubar.Append(datei_menu, "&Datei")

        # Menüeintrag für alle anzeigen
        self.alleAnzeigen_item = aktion_menu.Append(wx.ID_ANY, "&Alle anzeigen\tCtrl-W", "Zeige alle Einträge")
        self.Bind(wx.EVT_MENU, self.on_alle_anzeigen, self.alleAnzeigen_item)

        # Menüeintrag für hinzufügen
        self.hinzufuegen_item = aktion_menu.Append(wx.ID_ANY, "&Hinzufügen\tCtrl-H", "Füge neuen Eintrag hinzu")
        self.Bind(wx.EVT_MENU, self.on_hinzufuegen, self.hinzufuegen_item)

        # Menüeintrag für Datenbank-Informationen
        self.datenbank_info_item = aktion_menu.Append(wx.ID_ANY, "&Datenbank-Informationen\tCtrl-d", "Zeige Datenbank-Informationen")
        self.Bind(wx.EVT_MENU, self.on_datenbank_info, self.datenbank_info_item)

        menubar.Append(aktion_menu, "&Aktion")

        # Menüeintrag für Info
        info_item = info_menu.Append(wx.ID_ANY, "&Info\tCtrl-I", "Zeige Python Info")
        self.Bind(wx.EVT_MENU, self.on_info_klick, info_item)

        menubar.Append(info_menu, "&?")

        self.SetMenuBar(menubar)

        # Sizer zum Panel hinzufügen und Layout anwenden
        panel.SetSizer(sizer)
        sizer.Fit(self)

    def on_info_klick(self, event):
        """
        Zeigt eine Info-MessageBox mit Python- und wxPython-Version an.

        Args:
            event: Das auslösende Ereignis.
        """

        python_version = sys.version
        wx_version = wx.version()
        info_text = f"Python Version: {python_version}\nwxPython Version: {wx_version}"
        wx.MessageBox(info_text, "Info", wx.OK | wx.ICON_INFORMATION)

    def on_open(self, event):
        """
        Öffnet eine Dialogbox zum Öffnen einer SQLite-Datenbankdatei.

        Args:
            event: Das auslösende Ereignis.
        """

        wildcard = "DB Dateien (*.db)|*.db"
        dialog = wx.FileDialog(self, message="DB Datei öffnen", wildcard=wildcard, style=wx.FD_OPEN)
        if dialog.ShowModal() == wx.ID_OK:
            self.db_datei = dialog.GetPath()
            self.open_database()
            self.update_menu_items()
        dialog.Destroy()

    def on_close(self, event):
        """
        Schließt die geöffnete SQLite-Datenbankverbindung.

        Args:
            event: Das auslösende Ereignis.
        """

        if self.db_conn:
            self.db_conn.close()
            self.db_conn = None
            wx.MessageBox("Datenbank erfolgreich geschlossen.", "Erfolg", wx.OK | wx.ICON_INFORMATION)
            self.update_menu_items()

    def on_exit(self, event):
        """
        Schließt die Anwendung.

        Args:
            event: Das auslösende Ereignis.
        """

        if self.db_conn:
            self.on_close(event)  # Schließe die geöffnete Datenbank vor dem Beenden
        self.Close()

    def aktualisiere_aktuelles_datum(self):
        """
        Aktualisiert die Anzeige mit dem aktuellen Datum.
        """

        heute = wx.DateTime.Now()
        self.datum_textbox.SetValue(heute.Format("%d.%m.%Y"))
        self.jahr_numeric.SetValue(heute.GetYear())
        monat = heute.GetMonth() + 1
        self.monat_listbox.SetSelection(monat - 1)
        self.aktualisiere_wochentage(monat, heute.GetYear())
        self.on_enter_datum(None)  # Wochentag für aktuelles Datum auswählen

    def aktualisiere_wochentage(self, monat, jahr):
        """
        Aktualisiert die ListBox mit den Wochentagen für den ausgewählten Monat und Jahr.

        Args:
            monat (int): Der ausgewählte Monat.
            jahr (int): Das ausgewählte Jahr.
        """

        self.wochentag_listbox.Clear()
        _, days_in_month = calendar.monthrange(jahr, monat)
        german_weekdays = ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag", "Samstag", "Sonntag"]
        for tag in range(1, days_in_month + 1):
            wochentag_index = calendar.weekday(jahr, monat, tag)
            tag_label = f"{tag:02d}. {german_weekdays[wochentag_index]}"
            self.wochentag_listbox.Append(tag_label)

    def on_enter_datum(self, event):
        """
        Event-Handler für die Eingabe eines Datums.

        Args:
            event: Das auslösende Ereignis.
        """

        datum_string = self.datum_textbox.GetValue()
        try:
            tag, monat, jahr = map(int, datum_string.split('.'))
            if 1 <= tag <= 31 and 1 <= monat <= 12 and 1900 <= jahr <= 2100:
                self.jahr_numeric.SetValue(jahr)
                self.monat_listbox.SetSelection(monat - 1)
                self.aktualisiere_wochentage(monat, jahr)
                self.on_wochentag_auswahl(None)
                self.select_tag_in_listbox()
        except ValueError:
            wx.MessageBox("Ungültiges Datumsformat. Bitte verwenden Sie tt.mm.jjjj.", "Fehler", wx.OK | wx.ICON_ERROR)

    def on_jahr_changed(self, event):
        """
        Event-Handler für die Änderung des Jahres.

        Args:
            event: Das auslösende Ereignis.
        """

        jahr = self.jahr_numeric.GetValue()
        monat_index = self.monat_listbox.GetSelection()
        monat = monat_index + 1
        self.datum_textbox.SetValue(f"{self.datum_textbox.GetValue().split('.')[0]}.{self.monat_listbox.GetSelection() + 1}.{jahr}")
        self.on_enter_datum(None)

    def on_monat_auswahl(self, event):
        """
        Event-Handler für die Auswahl eines Monats.

        Args:
            event: Das auslösende Ereignis.
        """

        monat_index = self.monat_listbox.GetSelection()
        jahr = self.jahr_numeric.GetValue()
        monat = monat_index + 1
        self.datum_textbox.SetValue(f"{self.datum_textbox.GetValue().split('.')[0]}.{self.monat_listbox.GetSelection() + 1}.{jahr}")
        self.on_enter_datum(None)
        self.select_tag_in_listbox()

    def on_wochentag_auswahl(self, event):
        """
        Event-Handler für die Auswahl eines Wochentags.

        Args:
            event: Das auslösende Ereignis.
        """

        try:
            # Extrahiere das aktuelle Datum aus der TextBox
            datum_string = self.datum_textbox.GetValue()
            tag, monat, jahr = map(int, datum_string.split('.'))

            # Extrahiere den ausgewählten Eintrag aus der ListBox
            selected_tag_and_wochentag = self.wochentag_listbox.GetStringSelection()
            selected_tag = int(selected_tag_and_wochentag.split('.')[0])  # Extrahiere den ausgewählten Tag

            # Aktualisiere das Datum in der TextBox mit dem ausgewählten Tag
            self.datum_textbox.SetValue(f"{selected_tag}.{monat}.{jahr}")
        except ValueError:
            pass

    def select_tag_in_listbox(self):
        """
        Selektiert den entsprechenden Tag in der ListBox basierend auf dem aktuellen Datum.
        """

        datum_string = self.datum_textbox.GetValue()
        tag, monat, jahr = map(int, datum_string.split('.'))
        # Durchlaufe die Einträge in der ListBox für Tag/Wochentag
        item_count = self.wochentag_listbox.GetCount()
        for index in range(item_count):
            item = self.wochentag_listbox.GetString(index)
            if item.startswith(f"{tag:02d}."):
                # Wähle den entsprechenden Tag aus
                self.wochentag_listbox.SetSelection(index)
                break

    def update_menu_items(self):
        """
        Aktualisiert die Menüeinträge je nach Status der Datenbankverbindung.
        """

        # Aktualisiere die Menüeinträge basierend auf dem Status der Datenbankverbindung
        if self.db_conn:
            self.open_item.Enable(False)
            self.close_item.Enable(True)
            self.alleAnzeigen_item.Enable(True)
            self.hinzufuegen_item.Enable(True)
            self.datenbank_info_item.Enable(True)
        else:
            self.open_item.Enable(True)
            self.close_item.Enable(False)
            self.alleAnzeigen_item.Enable(False)
            self.hinzufuegen_item.Enable(False)
            self.datenbank_info_item.Enable(False)

    def open_database(self):
        """
        Öffnet die SQLite-Datenbankverbindung.

        Zeigt eine MessageBox mit Erfolgsmeldung oder Fehlermeldung an.
        """

        try:
            self.db_conn = sqlite3.connect(self.db_datei)
            wx.MessageBox("Datenbank erfolgreich geöffnet.", "Erfolg", wx.OK | wx.ICON_INFORMATION)
        except Exception as e:
            wx.MessageBox(f"Fehler beim Öffnen der Datenbank: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)

    def on_alle_anzeigen(self, event):
        dialog = AlleAnzeigenDialog(self, self.db_conn, self.db_datei)
        dialog.ShowModal()
        dialog.Destroy()

    def on_hinzufuegen(self, event):
        dialog = HinzufuegenDialog(self, self.db_conn, self.datum_textbox.GetValue())
        dialog.ShowModal()
        dialog.Destroy()


    def on_datenbank_info(self, event):
        """
        Event-Handler für den Menüeintrag 'Datenbank-Informationen'.

        Args:
            event: Das auslösende Ereignis.
        """
        if self.db_conn:
            # Sammle Datenbank-Informationen und Statistiken
            try:
                cursor = self.db_conn.cursor()

                # Beispiel: Anzahl der Einträge in der Datenbank
                cursor.execute("SELECT COUNT(*) FROM Entries")
                count = cursor.fetchone()[0]

                # Beispiel: Liste der Tabellen in der Datenbank
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = [table[0] for table in cursor.fetchall()]

                # Zusammenstellen der Informationen
                info_text = f"Anzahl der Einträge: {count}\nTabellen: {', '.join(tables)}"

                # MessageBox mit Datenbank-Informationen anzeigen
                wx.MessageBox(info_text, "Datenbank-Informationen", wx.OK | wx.ICON_INFORMATION)
            except sqlite3.Error as e:
                wx.MessageBox(f"Fehler beim Abrufen der Datenbank-Informationen: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Datenbankverbindung nicht geöffnet.", "Fehler", wx.OK | wx.ICON_ERROR)

        self.datenbank_info()


    def datenbank_info(self):
        """
        Event-Handler für den Menüeintrag 'Datenbank-Informationen'.

        Args:
            event: Das auslösende Ereignis.
        """
        if self.db_conn:
            try:
                cursor = self.db_conn.cursor()

                # SQLite-Informationen abrufen
                cursor.execute(f"SELECT sqlite_version()")
                sqlite_version = cursor.fetchone()[0]

                # Datenbank-Dateigröße abrufen
                db_file_size = os.path.getsize(self.db_datei)  # in Bytes
                db_size_mb = db_file_size / (1024 * 1024)  # in Megabytes

                # Anzahl der Tabellen in der Datenbank
                cursor.execute("SELECT COUNT(*) FROM sqlite_master WHERE type='table'")
                table_count = cursor.fetchone()[0]

                # Gesamtanzahl der Datensätze in allen Tabellen
                total_records = 0
                cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
                tables = cursor.fetchall()
                for table in tables:
                    table_name = table[0]
                    cursor.execute(f"SELECT COUNT(*) FROM {table_name}")
                    records_count = cursor.fetchone()[0]
                    total_records += records_count

                # Zusammenstellen der Informationen
                info_text = (
                    f"SQLite Version: {sqlite_version}\n"
                    f"Datenbank-Dateigröße: {db_size_mb:.2f} MB\n"
                    f"Anzahl der Tabellen: {table_count}\n"
                    f"Gesamtanzahl der Datensätze: {total_records}\n"
                )

                # MessageBox mit Datenbank-Informationen anzeigen
                wx.MessageBox(info_text, "Datenbank-Informationen", wx.OK | wx.ICON_INFORMATION)

            except sqlite3.Error as e:
                wx.MessageBox(f"Fehler beim Abrufen der Datenbank-Informationen: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)
        else:
            wx.MessageBox("Datenbankverbindung nicht geöffnet.", "Fehler", wx.OK | wx.ICON_ERROR)
