using System;
using System.Collections.Generic;
using System.ComponentModel;
using System.Data;
using System.Drawing;
using System.Linq;
using System.Text;
using System.Threading.Tasks;
using System.Windows.Forms;

namespace Kalender
{
    public partial class DetailsForm : Form
    {
        public DetailsForm(string date, string dayOfWeek, string time, string additionalInfo)
        {
            InitializeComponent();
            textBox1.Text = $"{date}\r\n" +
                                  $"{dayOfWeek}, " +
                                  $"{time}\r\n" +
                                  $"\r\n{additionalInfo}";

            textBox1.Focus();
            textBox1.SelectionStart = 0;
        }

        private void DetailsForm_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
                this.Close();
        }

        private void textBox1_KeyDown(object sender, KeyEventArgs e)
        {
            if (e.KeyCode == Keys.Escape)
                this.Close();
        }
    }
}
