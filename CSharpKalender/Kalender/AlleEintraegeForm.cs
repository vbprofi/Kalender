using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

using System.Data.SQLite;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;
using System.Globalization;

namespace Kalender
{
    public partial class AlleEintraegeForm : Form
    {
        private SQLiteConnection sqliteConnection;

        public AlleEintraegeForm()
        {
            InitializeComponent();
            InitializeListView();
            LoadEntriesFromDatabase();
        }

        private void InitializeListView()
        {
            listView1.View = View.Details;
            listView1.Columns.Add("Datum", 150);
            listView1.Columns.Add("Wochentag", 150);
            listView1.Columns.Add("Uhrzeit", 100);
            listView1.Columns.Add("Zusätzliche Informationen", 200);
        }

        private void LoadEntriesFromDatabase()
        {
            listView1.Items.Clear(); // ListView vor dem Neuladen leeren
            InitializeListView();

            try
            {
                sqliteConnection = new SQLiteConnection("Data Source=calendar.db;Version=3;");
                sqliteConnection.Open();

                string selectQuery = "SELECT Date, DayOfWeek, Time, AdditionalInfo FROM Entries";
                if (!checkBox1.Checked)
                {
                    // Nur Einträge ab dem heutigen Datum laden
                    selectQuery += " WHERE Date >= @today";
                }

                SQLiteCommand selectCommand = new SQLiteCommand(selectQuery, sqliteConnection);

                if (!checkBox1.Checked)
                {
                    // Parameter für das heutige Datum setzen (ohne führende Nullen im Datum)
                    selectCommand.Parameters.AddWithValue("@today", DateTime.Today.ToString("d", CultureInfo.InvariantCulture));
                }

                SQLiteDataReader dataReader = selectCommand.ExecuteReader();

                List<ListViewItem> itemsToAdd = new List<ListViewItem>();

                while (dataReader.Read())
                {
                    string date = dataReader["Date"].ToString();
                    string dayOfWeek = dataReader["DayOfWeek"].ToString();
                    string time = dataReader["Time"].ToString();
                    string additionalInfo = dataReader["AdditionalInfo"].ToString();

                    // Datum aus der Datenbank im Format "TT.MM.JJJJ" in ein DateTime-Objekt konvertieren
                    if (DateTime.TryParseExact(date, "dd.MM.yyyy", CultureInfo.InvariantCulture, DateTimeStyles.None, out DateTime parsedDate))
                    {
                        // Nur hinzufügen, wenn das Datum später oder gleich dem heutigen Datum ist (wenn nicht anders angezeigt)
                        if (checkBox1.Checked || parsedDate.Date >= DateTime.Today)
                        {
                            ListViewItem item = new ListViewItem(date);
                            item.SubItems.Add(dayOfWeek);
                            item.SubItems.Add(time);
                            item.SubItems.Add(additionalInfo);
                            itemsToAdd.Add(item);
                        }
                    }
                }

                dataReader.Close();

                // Einträge zur ListView hinzufügen und nach Datum und Uhrzeit sortieren
                listView1.Items.AddRange(itemsToAdd.OrderBy(item =>
                {
                    // Extrahiere Datum und Uhrzeit für die Sortierung
                    string date = item.SubItems[0].Text;
                    string time = item.SubItems[2].Text;

                    // Erzeuge ein kombiniertes Sortierformat (Datum + Uhrzeit)
                    DateTime combinedDateTime = DateTime.ParseExact($"{date} {time}", "dd.MM.yyyy HH:mm", CultureInfo.InvariantCulture);
                    return combinedDateTime;
                }).ToArray());

                // Einträge zur ListView hinzufügen und nach Datum sortieren
                //listView1.Items.AddRange(itemsToAdd.OrderBy(item => DateTime.ParseExact(item.SubItems[0].Text, "dd.MM.yyyy", CultureInfo.InvariantCulture)).ToArray());
            }
            catch (Exception ex)
            {
                MessageBox.Show("Fehler beim Laden der Daten aus der Datenbank: " + ex.Message, "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
            finally
            {
                if (sqliteConnection != null && sqliteConnection.State != ConnectionState.Closed)
                {
                    sqliteConnection.Close();
                    sqliteConnection.Dispose();
                }
            }
        }


        private void AlleEintraegeForm_FormClosing(object sender, FormClosingEventArgs e)
        {
            try
            {
            if (sqliteConnection != null && sqliteConnection.State != ConnectionState.Closed)
            {
                sqliteConnection.Close();
                sqliteConnection.Dispose();
            }
            } catch
            {

            }
        }

        private void ShowSelectedEntryDetails()
        {
            if (listView1.SelectedItems.Count > 0)
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                string date = selectedItem.SubItems[0].Text;
                string dayOfWeek = selectedItem.SubItems[1].Text;
                string time = selectedItem.SubItems[2].Text;
                string additionalInfo = selectedItem.SubItems[3].Text;

                DetailsForm detailsForm = new DetailsForm(date, dayOfWeek, time, additionalInfo);
                detailsForm.ShowDialog();
            }
            else
            {
                MessageBox.Show("Bitte wählen Sie einen Eintrag aus der Liste aus.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void listView1_DoubleClick(object sender, EventArgs e)
        {
            ShowSelectedEntryDetails();

        }

        private void listView1_ItemActivate(object sender, EventArgs e)
        {
            ShowSelectedEntryDetails();
        }

        private void listView1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
                this.Close();

            if (e.KeyCode == Keys.Delete)
            {
                loeschenEintrag();
            }
        }

        private void AlleEintraegeForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
                this.Close();
        }

        private void checkBox1_CheckedChanged(object sender, EventArgs e)
        {
            listView1.Clear();
            LoadEntriesFromDatabase();
        }

        private void AlleEintraegeForm_FormClosing_1(object sender, FormClosingEventArgs e)
        {
            AlleEintraegeForm_FormClosing(sender, e);
        }

        private void button1_Click(object sender, EventArgs e)
        {
            loeschenEintrag();
        }

        private void loeschenEintrag()
        {
            if (listView1.SelectedItems.Count > 0)
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                string date = selectedItem.SubItems[0].Text;
                string time = selectedItem.SubItems[2].Text;

                try
                {
                    sqliteConnection = new SQLiteConnection("Data Source=calendar.db;Version=3;");
                    sqliteConnection.Open();

                    string deleteQuery = $"DELETE FROM Entries WHERE Date = @date and time = @time";
                    SQLiteCommand deleteCommand = new SQLiteCommand(deleteQuery, sqliteConnection);
                    deleteCommand.Parameters.AddWithValue("@date", date);
                    deleteCommand.Parameters.AddWithValue("@time", time);
                    int rowsAffected = deleteCommand.ExecuteNonQuery();

                    if (rowsAffected > 0)
                    {
                        // Erfolgreich gelöscht, entferne auch aus der ListView
                        listView1.Items.Remove(selectedItem);
                        MessageBox.Show("Eintrag erfolgreich gelöscht.", "Erfolg", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    else
                    {
                        MessageBox.Show("Löschen fehlgeschlagen: Eintrag nicht gefunden.", "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
                catch (Exception ex)
                {
                    MessageBox.Show("Fehler beim Löschen des Eintrags: " + ex.Message, "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
                }
                finally
                {
                    if (sqliteConnection != null && sqliteConnection.State != ConnectionState.Closed)
                    {
                        sqliteConnection.Close();
                        sqliteConnection.Dispose();
                    }
                }
            }
            else
            {
                MessageBox.Show("Bitte wählen Sie einen Eintrag aus der Liste zum Löschen aus.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void button2_Click(object sender, EventArgs e)
        {
            if (listView1.SelectedItems.Count > 0)
            {
                ListViewItem selectedItem = listView1.SelectedItems[0];
                string date = selectedItem.SubItems[0].Text;
                string dayOfWeek = selectedItem.SubItems[1].Text;
                string time = selectedItem.SubItems[2].Text;
                string additionalInfo = selectedItem.SubItems[3].Text;

                // Bearbeitungsform mit den Informationen des ausgewählten Eintrags anzeigen
                BearbeitungsForm editForm = new BearbeitungsForm(date, time, dayOfWeek, additionalInfo);
                editForm.ShowDialog();

                // Nachdem die Bearbeitungsform geschlossen wurde, ListView neu laden (um Änderungen zu reflektieren)
                LoadEntriesFromDatabase();
            }
            else
            {
                MessageBox.Show("Bitte wählen Sie einen Eintrag aus der Liste zum Bearbeiten aus.", "Information", MessageBoxButtons.OK, MessageBoxIcon.Information);
            }
        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {

        }
    }//end class
}//end namespace
