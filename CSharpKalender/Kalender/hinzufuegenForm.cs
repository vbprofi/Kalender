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

namespace Kalender
{
    public partial class hinzufuegenForm : Form
    {
        private SQLiteConnection sqliteConnection;

        public hinzufuegenForm()
        {
            InitializeComponent();
            initSQLite();
        }

        // Öffentliche Eigenschaft zum Setzen und Anzeigen des TextBox-Texts
        public string TextBoxText
        {
            get { return textBox1.Text; }
            set { textBox1.Text = value; }
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

        private void hinzufuegenForm_Load(object sender, EventArgs e)
        {
            textBox2.ReadOnly = true;
            getDayOfWeek();
            textBox3.Text = "00:00";
        }

        private void button1_Click(object sender, EventArgs e)
        {
            // Daten aus den Textboxen auslesen
            string date = textBox1.Text;
            string dayOfWeek = textBox2.Text;
            string time = textBox3.Text;
            string additionalInfo = textBox4.Text;

            // SQL-Insert-Befehl zum Einfügen der Daten
            string insertQuery = "INSERT INTO Entries (Date, DayOfWeek, time, AdditionalInfo) VALUES (@date, @dayOfWeek, @time, @additionalInfo)";
            SQLiteCommand insertCommand = new SQLiteCommand(insertQuery, sqliteConnection);
            insertCommand.Parameters.AddWithValue("@date", date);
            insertCommand.Parameters.AddWithValue("@dayOfWeek", dayOfWeek);
            insertCommand.Parameters.AddWithValue("@time", time);
            insertCommand.Parameters.AddWithValue("@additionalInfo", additionalInfo);

            try
            {
                // Daten in die SQLite-Datenbank einfügen
                insertCommand.ExecuteNonQuery();
                MessageBox.Show("Daten erfolgreich gespeichert.", "Erfolg", MessageBoxButtons.OK, MessageBoxIcon.Information);
                this.Close();
            }
            catch (Exception ex)
            {
                MessageBox.Show("Fehler beim Speichern der Daten: " + ex.Message, "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
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


    }//end class
}//end namespace
