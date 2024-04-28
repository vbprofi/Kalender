# alleanzeigen_dialog.py
"""
Modul zur Definition des benutzerdefinierten Dialogfensters 'AlleAnzeigenDialog'
zur Anzeige und Verwaltung von Einträgen in einer SQLite-Datenbank.

Dieses Modul enthält eine benutzerdefinierte Klasse `AlleAnzeigenDialog`, die ein Dialogfenster
erstellt, das eine Liste von Einträgen aus einer SQLite-Datenbank anzeigt und es dem Benutzer ermöglicht,
Einträge zu bearbeiten oder zu löschen.
"""

import wx
import sqlite3
from datetime import datetime

from eintraganzeigen import EntryContentDialog
from eintragbearbeiten import BearbeitungsDialog

class AlleAnzeigenDialog(wx.Dialog):
    """Ein benutzerdefiniertes Dialogfenster zum Anzeigen und Verwalten von Einträgen."""

    def __init__(self, parent, db_conn, db_datei):
        """
        Initialisiert den Dialog.

        :param parent: Das Elternfenster.
        :param db_conn: Die SQLite-Datenbankverbindung.
        :param db_datei: Der Dateipfad zur SQLite-Datenbank.
        """

        super().__init__(parent, title="Alle anzeigen")

        self.db_conn = db_conn
        self.db_datei = db_datei

        self.initialize_ui()

        # ListView einmalig füllen und sortieren
        self.update_listview()

        # Tastatur-Handler für das Dialogfenster hinzufügen
        self.Bind(wx.EVT_CHAR_HOOK, self.on_key_pressed)


    def initialize_ui(self):
        """Initialisiert die Benutzeroberfläche des Dialogs."""

        sizer = wx.BoxSizer(wx.VERTICAL)

        label = wx.StaticText(self, label="Vorhandene Einträge:")
        sizer.Add(label, 0, wx.ALL | wx.EXPAND, 10)

        self.listview = wx.ListCtrl(self, style=wx.LC_REPORT | wx.LC_SINGLE_SEL)
        self.listview.InsertColumn(0, "Datum", width=150)
        self.listview.InsertColumn(1, "Wochentag", width=150)
        self.listview.InsertColumn(2, "Uhrzeit", width=100)
        self.listview.InsertColumn(3, "Zusätzliche Informationen", width=200)
        sizer.Add(self.listview, 1, wx.ALL | wx.EXPAND, 10)

        self.checkbox = wx.CheckBox(self, label="Alle anzeigen")
        self.checkbox.Bind(wx.EVT_CHECKBOX, self.on_checkbox_toggle)
        sizer.Add(self.checkbox, 0, wx.ALL | wx.EXPAND, 10)

        btn_sizer = wx.BoxSizer(wx.HORIZONTAL)
        bearbeiten_btn = wx.Button(self, label="Bearbeiten")
        bearbeiten_btn.Bind(wx.EVT_BUTTON, self.on_edit_entry)
        btn_sizer.Add(bearbeiten_btn, 0, wx.ALL, 5)
        loeschen_btn = wx.Button(self, label="Löschen")
        loeschen_btn.Bind(wx.EVT_BUTTON, self.on_delete_entry)
        btn_sizer.Add(loeschen_btn, 0, wx.ALL, 5)
        sizer.Add(btn_sizer, 0, wx.ALIGN_CENTER_HORIZONTAL | wx.BOTTOM, 10)

        self.SetSizerAndFit(sizer)

    def update_listview(self):
        """
        Aktualisiert die ListView mit den aktuellen Einträgen aus der Datenbank.

        Wenn die CheckBox aktiviert ist, werden alle Einträge angezeigt.
        Andernfalls werden nur Einträge ab dem aktuellen Datum angezeigt.
        """

        self.listview.DeleteAllItems()

        try:
            cursor = self.db_conn.cursor()
            select_query = "SELECT Date, DayOfWeek, Time, AdditionalInfo FROM Entries"

            if not self.checkbox.GetValue():
                # Nur Einträge ab dem heutigen Datum laden
                today = datetime.today().date()
                cursor.execute(select_query)
                rows = cursor.fetchall()

                for row in rows:
                    str_date, day_of_week, str_time, additional_info = row
                    entry_date = datetime.strptime(str_date, "%d.%m.%Y").date()

                    if entry_date >= today:
                        # Datum mit führenden Nullen anzeigen
                        formatted_date = entry_date.strftime("%d.%m.%Y")
                        index = self.listview.InsertItem(self.listview.GetItemCount(), formatted_date)
                        self.listview.SetItem(index, 1, day_of_week)
                        self.listview.SetItem(index, 2, str_time)
                        self.listview.SetItem(index, 3, additional_info)
            else:
                cursor.execute(select_query)
                rows = cursor.fetchall()

                for row in rows:
                    str_date, day_of_week, str_time, additional_info = row
                    formatted_date = datetime.strptime(str_date, "%d.%m.%Y").strftime("%d.%m.%Y")
                    index = self.listview.InsertItem(self.listview.GetItemCount(), formatted_date)
                    self.listview.SetItem(index, 1, day_of_week)
                    self.listview.SetItem(index, 2, str_time)
                    self.listview.SetItem(index, 3, additional_info)

            cursor.close()
            self.sort_listview_by_datetime()

        except sqlite3.Error as e:
            wx.MessageBox(f"Fehler beim Laden der Einträge aus der Datenbank: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)

    def sort_listview_by_datetime(self):
        """
        Sortiert die Einträge in der ListView nach Datum und Uhrzeit.

        Verwendet die Daten in der ListView und aktualisiert die Anzeige entsprechend.
        """

        try:
            # Erstellen einer Liste von Tupeln (Datum, Uhrzeit, Zeilenindex, Wochentag, Zusätzliche Informationen)
            items_data = [
                (
                    datetime.strptime(self.listview.GetItemText(i, 0), "%d.%m.%Y"),  # Datum
                    datetime.strptime(self.listview.GetItemText(i, 2), "%H:%M"),       # Uhrzeit
                    i,  # Zeilenindex
                    self.listview.GetItemText(i, 1),  # Wochentag
                    self.listview.GetItemText(i, 3)   # Zusätzliche Informationen
                )
                for i in range(self.listview.GetItemCount())
            ]

            # Sortiere die Listeneinträge nach Datum und Uhrzeit
            items_data.sort(key=lambda x: (x[0], x[1]))

            # Lösche alle Einträge in der ListView
            self.listview.DeleteAllItems()

            # Füge die sortierten Einträge wieder hinzu
            for item in items_data:
                formatted_date = item[0].strftime("%d.%m.%Y")
                index = self.listview.InsertItem(self.listview.GetItemCount(), formatted_date)
                self.listview.SetItem(index, 1, item[3])  # Wochentag
                self.listview.SetItem(index, 2, item[1].strftime("%H:%M"))  # Uhrzeit
                self.listview.SetItem(index, 3, item[4])  # Zusätzliche Informationen

        except Exception as e:
            wx.MessageBox(f"Fehler beim Sortieren der Listeneinträge: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)

    def on_checkbox_toggle(self, event):
        """Behandelt das Ereignis, wenn die CheckBox umgeschaltet wird."""

        self.update_listview()

    def on_edit_entry(self, event):
        """
        Behandelt das Ereignis, wenn der Bearbeiten-Button geklickt wird.

        Öffnet ein Bearbeitungsdialogfenster für den ausgewählten Eintrag.
        """

        selected_index = self.listview.GetFirstSelected()
        if selected_index != -1:
            date = self.listview.GetItemText(selected_index)
            day_of_week = self.listview.GetItem(selected_index, 1).GetText()
            time = self.listview.GetItem(selected_index, 2).GetText()
            additional_info = self.listview.GetItem(selected_index, 3).GetText()

            # Öffne Bearbeitungsform mit den ausgewählten Eintragsdetails
            edit_dialog = BearbeitungsDialog(self, self.db_conn, date, day_of_week, time, additional_info)
            edit_dialog.ShowModal()
            edit_dialog.Destroy()
            self.update_listview()
        else:
            wx.MessageBox("Bitte wählen Sie einen Eintrag aus der Liste zum Bearbeiten aus.", "Information", wx.OK | wx.ICON_INFORMATION)

    def on_delete_entry(self, event):
        """
        Behandelt das Ereignis, wenn der Löschen-Button geklickt wird.

        Löscht den ausgewählten Eintrag aus der ListView und der Datenbank.
        """

        selected_index = self.listview.GetFirstSelected()
        if selected_index != -1:
            date = self.listview.GetItemText(selected_index)
            time = self.listview.GetItem(selected_index, 2).GetText()

            try:
                cursor = self.db_conn.cursor()
                delete_query = "DELETE FROM Entries WHERE Date = ? AND Time = ?"
                cursor.execute(delete_query, (date, time))
                self.db_conn.commit()

                if cursor.rowcount > 0:
                    self.listview.DeleteItem(selected_index)
                    wx.MessageBox("Eintrag erfolgreich gelöscht.", "Erfolg", wx.OK | wx.ICON_INFORMATION)
                else:
                    wx.MessageBox("Löschen fehlgeschlagen: Eintrag nicht gefunden.", "Fehler", wx.OK | wx.ICON_ERROR)

                cursor.close()
            except sqlite3.Error as e:
                wx.MessageBox(f"Fehler beim Löschen des Eintrags: {str(e)}", "Fehler", wx.OK | wx.ICON_ERROR)

        else:
            wx.MessageBox("Bitte wählen Sie einen Eintrag aus der Liste zum Löschen aus.", "Information", wx.OK | wx.ICON_INFORMATION)


    def on_key_pressed(self, event):
        """Behandelt das Tastaturereignis für das Dialogfenster."""

        key_code = event.GetKeyCode()

        if key_code == wx.WXK_ESCAPE:
            # ESC-Taste zum Schließen des Dialogfensters
            self.Close()

        elif key_code == wx.WXK_DELETE:
            # Entfernen-Taste zum Löschen des ausgewählten Eintrags
            self.on_delete_entry(event)

        elif key_code == wx.WXK_F2:
            # F2-Taste zum Bearbeiten des ausgewählten Eintrags
            self.on_edit_entry(event)

        elif key_code == wx.WXK_RETURN:
            # Enter-Taste zum Anzeigen der Inhalte des ausgewählten Eintrags
            self.show_entry_contents()

        else:
            event.Skip()  # Weitergabe des Ereignisses an das Standardverhalten

        event.Skip()  # Weitergabe des Ereignisses an das Standardverhalten



    def show_entry_contents(self):
        """Öffnet ein Fenster, das die Inhalte des ausgewählten Eintrags anzeigt."""

        selected_index = self.listview.GetFirstSelected()
        if selected_index != -1:
            date = self.listview.GetItemText(selected_index)
            day_of_week = self.listview.GetItem(selected_index, 1).GetText()
            time = self.listview.GetItem(selected_index, 2).GetText()
            additional_info = self.listview.GetItem(selected_index, 3).GetText()

            content = f"{date}\n{day_of_week}, {time}\n\n{additional_info}"
            dialog = EntryContentDialog(self, title="Eintrag anzeigen", content=content)
            dialog.Show()
        else:
            wx.MessageBox("Bitte wählen Sie einen Eintrag aus der Liste aus.", "Information", wx.OK | wx.ICON_INFORMATION)
