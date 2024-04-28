using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;
using static System.Windows.Forms.VisualStyles.VisualStyleElement;

using System.Data.SQLite;
using static System.Windows.Forms.VisualStyles.VisualStyleElement.TaskbarClock;
using System.Windows.Forms.VisualStyles;

namespace Kalender
{
    public partial class BearbeitungsForm : Form
    {
        private SQLiteConnection sqliteConnection;
        private string originalDate;
        private string originalTime;

        public BearbeitungsForm(string date, string time, string dayOfWeek, string additionalInfo)
        {
            InitializeComponent();
            initSQLite();


            // Anzeigen der Originalwerte
            textBox1.Text = date;
            textBox3.Text = time;
            textBox2.Text = dayOfWeek;
            textBox4.Text = additionalInfo;

            // Speichern der Originalwerte (für die Aktualisierung in der Datenbank)
            originalDate = date;
            originalTime = time;
        }
                
        private void getDayOfWeek()
        {
            // Datum aus textBox1 extrahieren und Wochentag ermitteln
            if (DateTime.TryParseExact(textBox1.Text, "dd.MM.yyyy", null, System.Globalization.DateTimeStyles.None, out DateTime date))
            {
                // Wochentag ermitteln (z.B. Montag, Dienstag usw.)
                string dayOfWeek = date.ToString("dddd", System.Globalization.CultureInfo.CurrentCulture);

                // Den ermittelten Wochentag in textBox2 anzeigen
                textBox2.Clear();
                textBox2.Text = dayOfWeek;
            }
            else
            {
                MessageBox.Show("Ungültiges Datumsformat." + Environment.NewLine + "TT.MM.JJJJ - Format verwenden bitte.", "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void BearbeitungsForm_Load(object sender, EventArgs e)
        {
            textBox2.ReadOnly = true;
            getDayOfWeek();
            if(textBox3.Text.Length <=1)
            textBox3.Text = "00:00";
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Daten aus den Textboxen auslesen
            string date = textBox1.Text;
            string dayOfWeek = textBox2.Text;
            string time = textBox3.Text;
            string additionalInfo = textBox4.Text;

            // Aufrufen der Methode zur Aktualisierung des Eintrags in der Datenbank
            UpdateEntryInDatabase(date, time, dayOfWeek, additionalInfo);

            // Schließen der Bearbeitungsform
            this.Close();
        }

        private void button2_Click(object sender, EventArgs e)
        {
            this.Close();
        }

        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if(e.KeyCode == Keys.Enter)
            getDayOfWeek();
        }

        private void textBox2_Enter(object sender, EventArgs e)
        {
            getDayOfWeek();
        }

        private void initSQLite()
        {
            // SQLite-Verbindung initialisieren
            sqliteConnection = new SQLiteConnection("Data Source=calendar.db;Version=3;");
            sqliteConnection.Open();

            // Tabelle erstellen, falls sie nicht existiert
            string createTableQuery = "CREATE TABLE IF NOT EXISTS Entries (Date TEXT, DayOfWeek TEXT, time TEXT, AdditionalInfo TEXT)";
            SQLiteCommand createTableCommand = new SQLiteCommand(createTableQuery, sqliteConnection);
            createTableCommand.ExecuteNonQuery();
        }

        private void UpdateEntryInDatabase(string newDate, string newTime, string newDayOfWeek, string newAdditionalInfo)
        {
            try
            {
                using (SQLiteConnection connection = new SQLiteConnection("Data Source=calendar.db;Version=3;"))
                {
                    connection.Open();

                    string updateQuery = "UPDATE Entries SET Date = @newDate, Time = @newTime, DayOfWeek = @newDayOfWeek, AdditionalInfo = @newAdditionalInfo WHERE Date = @originalDate AND Time = @originalTime";
                    SQLiteCommand updateCommand = new SQLiteCommand(updateQuery, connection);
                    updateCommand.Parameters.AddWithValue("@newDate", newDate);
                    updateCommand.Parameters.AddWithValue("@newTime", newTime);
                    updateCommand.Parameters.AddWithValue("@newDayOfWeek", newDayOfWeek);
                    updateCommand.Parameters.AddWithValue("@newAdditionalInfo", newAdditionalInfo);
                    updateCommand.Parameters.AddWithValue("@originalDate", originalDate);
                    updateCommand.Parameters.AddWithValue("@originalTime", originalTime);

                    int rowsAffected = updateCommand.ExecuteNonQuery();
                    if (rowsAffected > 0)
                    {
                        MessageBox.Show("Eintrag erfolgreich aktualisiert.", "Erfolg", MessageBoxButtons.OK, MessageBoxIcon.Information);
                    }
                    else
                    {
                        MessageBox.Show("Aktualisierung fehlgeschlagen: Eintrag nicht gefunden.", "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
                    }
                }
            }
            catch (Exception ex)
            {
                MessageBox.Show("Fehler beim Aktualisieren des Eintrags: " + ex.Message, "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void textBox4_TextChanged(object sender, EventArgs e)
        {

        }
    }//end class
}//end namespace
