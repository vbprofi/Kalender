using System;
using System.Globalization;
using System.Reflection;
using System.Windows.Forms;

namespace Kalender
{
    public partial class Form1 : Form
    {
        private MenuStrip menuStrip1;
        private ToolStripMenuItem dateiToolStripMenuItem, aktionToolStripMenuItem, hilfeToolStripMenuItem;
        private ToolStripMenuItem beendenToolStripMenuItem, alleEintraegeToolStripMenuItem, hinzufuegenToolStripMenuItem, infoToolStripMenuItem;

        public Form1()
        {
            InitializeComponent();
            InitializeMenu();
            InitializeCalendar();
        }

        private void InitializeCalendar()
        {
            DateTime currentDate = DateTime.Today;
            DisplayDate(currentDate);
            DisplayMonths(currentDate.Month);
            DisplayDaysOfMonth(currentDate.Year, currentDate.Month);
            SelectCurrentDay(currentDate.Day);
        }

        private void DisplayDate(DateTime date)
        {
            textBox1.Text = date.ToString("dd.MM.yyyy");
            numericUpDown1.Value = date.Year;
        }

        private void DisplayMonths(int selectedMonth)
        {
            listBox1.Items.Clear();
            DateTimeFormatInfo dateFormat = CultureInfo.CurrentCulture.DateTimeFormat;

            for (int month = 1; month <= 12; month++)
            {
                string monthName = $"{month:00} {dateFormat.GetMonthName(month)}";
                listBox1.Items.Add(monthName);

                if (month == selectedMonth)
                    listBox1.SelectedIndex = month - 1; // Index beginnt bei 0
            }
        }

        private void DisplayDaysOfMonth(int year, int month)
        {
            listView1.Items.Clear();

            DateTime firstDayOfMonth = new DateTime(year, month, 1);
            int daysInMonth = DateTime.DaysInMonth(year, month);

            for (int day = 1; day <= daysInMonth; day++)
            {
                DateTime date = new DateTime(year, month, day);
                string dayOfWeek = date.ToString("ddd");
                string dayOfMonth = $"{day:00} {dayOfWeek}";

                listView1.Items.Add(dayOfMonth);
            }
        }

        private void SelectCurrentDay(int day)
        {
            foreach (ListViewItem item in listView1.Items)
            {
                if (item.Text.Contains($"{day:00}"))
                {
                    item.Selected = true;
                    item.EnsureVisible();
                    listView1.FocusedItem = item;
                    break;
                }
            }
        }

        private void UpdateCalendarFromListBox()
        {
            if (listBox1.SelectedItem != null)
            {
                int selectedMonth = int.Parse(listBox1.SelectedItem.ToString().Substring(0, 2));
                DisplayDaysOfMonth((int)numericUpDown1.Value, selectedMonth);
                UpdateDateFromCalendar();
            }
        }

        private void UpdateDateFromCalendar()
        {
            DateTime currentDate;
            if (DateTime.TryParseExact(textBox1.Text, "dd.MM.yyyy", CultureInfo.InvariantCulture, DateTimeStyles.None, out currentDate))
            {
                int selectedMonth = listBox1.SelectedIndex + 1;
                DateTime updatedDate = new DateTime(currentDate.Year, selectedMonth, currentDate.Day);
                DisplayDate(updatedDate);
                SelectCurrentDay(updatedDate.Day);
            }
        }

        private void UpdateDateFromListView()
        {
            if (listView1.SelectedItems.Count > 0)
            {
                string selectedDayText = listView1.SelectedItems[0].Text;
                string selectedDay = selectedDayText.Substring(0, 2);
                DateTime currentDate;
                if (DateTime.TryParseExact(textBox1.Text, "dd.MM.yyyy", CultureInfo.InvariantCulture, DateTimeStyles.None, out currentDate))
                {
                    DateTime updatedDate = new DateTime(currentDate.Year, currentDate.Month, int.Parse(selectedDay));
                    DisplayDate(updatedDate);
                }
            }
        }

        private void textBox1_KeyPress(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Enter)
            {
                e.SuppressKeyPress = true;
                UpdateDateFromTextBox();
            }
        }

        private void UpdateDateFromTextBox()
        {
            DateTime newDate;
            if (DateTime.TryParseExact(textBox1.Text, "dd.MM.yyyy", CultureInfo.InvariantCulture, DateTimeStyles.None, out newDate))
            {
                DisplayDate(newDate);
                DisplayMonths(newDate.Month);
                DisplayDaysOfMonth(newDate.Year, newDate.Month);
                SelectCurrentDay(newDate.Day);
            }
            else
            {
                MessageBox.Show("Ungültiges Datumsformat.", "Fehler", MessageBoxButtons.OK, MessageBoxIcon.Error);
            }
        }

        private void numericUpDown1_ValueChanged(object sender, EventArgs e)
        {
            UpdateDateFromYearUpDown();
        }

        private void UpdateDateFromYearUpDown()
        {
            DateTime currentDate;
            if (DateTime.TryParseExact(textBox1.Text, "dd.MM.yyyy", CultureInfo.InvariantCulture, DateTimeStyles.None, out currentDate))
            {
                DateTime updatedDate = new DateTime((int)numericUpDown1.Value, currentDate.Month, currentDate.Day);
                DisplayDate(updatedDate);
                DisplayDaysOfMonth(updatedDate.Year, updatedDate.Month);
                SelectCurrentDay(updatedDate.Day);
            }
        }

        private void listBox1_SelectedIndexChanged(object sender, EventArgs e)
        {
            UpdateCalendarFromListBox();
        }

        private void listView1_SelectedIndexChanged(object sender, EventArgs e)
        {
            UpdateDateFromListView();
        }

        private void listView1_Enter(object sender, EventArgs e)
        {
            foreach (ListViewItem item in listView1.Items)
            {
                if (item.Selected)
                {
                    listView1.FocusedItem = item;
                    break;
                }
            }
        }

        private void numericUpDown1_KeyPress(object sender, KeyEventArgs e)
        {
            textBox1_KeyPress(sender, e);
        }

        private void InitializeMenu()
        {
            menuStrip1 = new MenuStrip();
            dateiToolStripMenuItem = new ToolStripMenuItem();
            aktionToolStripMenuItem = new ToolStripMenuItem();
            hilfeToolStripMenuItem = new ToolStripMenuItem();

            beendenToolStripMenuItem = new ToolStripMenuItem();
            alleEintraegeToolStripMenuItem = new ToolStripMenuItem();
            hinzufuegenToolStripMenuItem = new ToolStripMenuItem();
            infoToolStripMenuItem = new ToolStripMenuItem();

            menuStrip1.SuspendLayout();

            dateiToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] {
                beendenToolStripMenuItem
            });
            dateiToolStripMenuItem.Name = "dateiToolStripMenuItem";
            dateiToolStripMenuItem.Size = new System.Drawing.Size(58, 20);
            dateiToolStripMenuItem.Text = "Datei";

            beendenToolStripMenuItem.Name = "beendenToolStripMenuItem";
            beendenToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            beendenToolStripMenuItem.Text = "Beenden";
            beendenToolStripMenuItem.Click += new EventHandler(beendenToolStripMenuItem_Click);

            aktionToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] {
                alleEintraegeToolStripMenuItem,
                hinzufuegenToolStripMenuItem
            });
            aktionToolStripMenuItem.Name = "aktionToolStripMenuItem";
            aktionToolStripMenuItem.Size = new System.Drawing.Size(58, 20);
            aktionToolStripMenuItem.Text = "Aktion";

            alleEintraegeToolStripMenuItem.Name = "alleEintraegeToolStripMenuItem";
            alleEintraegeToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            alleEintraegeToolStripMenuItem.Text = "&Alle Einträge zeigen";
            alleEintraegeToolStripMenuItem.Click += new EventHandler(alleEintraegeToolStripMenuItem_Click);

            hinzufuegenToolStripMenuItem.Name = "hinzufuegenToolStripMenuItem";
            hinzufuegenToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            hinzufuegenToolStripMenuItem.Text = "&Hinzufügen";
            hinzufuegenToolStripMenuItem.Click += new EventHandler(hinzufuegenToolStripMenuItem_Click);


            hilfeToolStripMenuItem.DropDownItems.AddRange(new ToolStripItem[] {
                infoToolStripMenuItem
            });
            hilfeToolStripMenuItem.Name = "hilfeToolStripMenuItem";
            hilfeToolStripMenuItem.Size = new System.Drawing.Size(58, 20);
            hilfeToolStripMenuItem.Text = "?";

            infoToolStripMenuItem.Name = "infoToolStripMenuItem";
            infoToolStripMenuItem.Size = new System.Drawing.Size(180, 22);
            infoToolStripMenuItem.Text = "&Info";
            infoToolStripMenuItem.Click += new EventHandler(infoToolStripMenuItem_Click);

            menuStrip1.Items.AddRange(new ToolStripItem[] {
                dateiToolStripMenuItem,
                aktionToolStripMenuItem,
                hilfeToolStripMenuItem
            });

            menuStrip1.Location = new System.Drawing.Point(0, 0);
            menuStrip1.Name = "menuStrip1";
            menuStrip1.Size = new System.Drawing.Size(800, 24);
            menuStrip1.TabIndex = 8;
            menuStrip1.Text = "menuStrip1";

            Controls.Add(menuStrip1);

            menuStrip1.ResumeLayout(false);
            menuStrip1.PerformLayout();
        }

        private void beendenToolStripMenuItem_Click(object sender, EventArgs e)
        {
            Application.Exit();
        }

        private void alleEintraegeToolStripMenuItem_Click(object sender, EventArgs e)
        {
            AlleEintraegeForm openForm = new AlleEintraegeForm();
            openForm.ShowInTaskbar = false;
            openForm.ShowDialog();
        }

        private void hinzufuegenToolStripMenuItem_Click(object sender, EventArgs e)
        {
            hinzufuegenForm addForm = new hinzufuegenForm();
            addForm.TextBoxText = textBox1.Text;
            addForm.ShowInTaskbar = false;
            addForm.ShowDialog();
        }

        private void infoToolStripMenuItem_Click(object sender, EventArgs e)
        {
            string appName = Assembly.GetEntryAssembly().GetName().Name;
            string appVersion = Assembly.GetEntryAssembly().GetName().Version.ToString();
            string targetFramework = AppDomain.CurrentDomain.SetupInformation.TargetFrameworkName;
            string executeFileName = Application.ExecutablePath;
            string currentFolder = Environment.CurrentDirectory;

            string infoMessage = $"App Name: {appName}\n" +
                                 $"App Version: {appVersion}\n" +
                                 $"Target Framework: {targetFramework}\n" +
                                 $"Execute File Name: {executeFileName}\n" +
                                 $"Current Folder: {currentFolder}";

            MessageBox.Show(infoMessage, $"Info über {appName}", MessageBoxButtons.OK, MessageBoxIcon.Information);
        }

        private void Form1_Load(object sender, EventArgs e)
        {
        }

    }//end class
}//end namespace
