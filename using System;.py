using System;
using System.Numerics;
using System.Threading;
using System.Windows.Forms;

namespace PrimeFibApp
{
    public partial class MainForm : Form
    {
        private NumberWorker _primeWorker;
        private NumberWorker _fibWorker;

        public MainForm()
        {
            InitializeComponent();
        }

        // ---------- Запуск / управление простыми числами ----------
        private void btnStartPrimes_Click(object sender, EventArgs e)
        {
            long? from = ParseNullableLong(txtPrimeFrom.Text);
            long? to   = ParseNullableLong(txtPrimeTo.Text);

            _primeWorker?.Stop();
            lstPrimes.Items.Clear();

            _primeWorker = new NumberWorker(
                kind: WorkerKind.Primes,
                from: from,
                to: to,
                onNumber: n => lstPrimes.Items.Add(n.ToString()),
                onFinished: () => SetPrimesButtons(false));

            _primeWorker.Start();
            SetPrimesButtons(true);
        }

        private void btnPausePrimes_Click(object sender, EventArgs e) => _primeWorker?.Pause();
        private void btnResumePrimes_Click(object sender, EventArgs e) => _primeWorker?.Resume();
        private void btnStopPrimes_Click(object sender, EventArgs e)
        {
            _primeWorker?.Stop();
            SetPrimesButtons(false);
        }

        private void btnRestartPrimes_Click(object sender, EventArgs e)
        {
            btnStartPrimes_Click(sender, e); // Stop + новый Start = рестарт с новыми границами
        }

        // ---------- Запуск / управление Фибоначчи ----------
        private void btnStartFib_Click(object sender, EventArgs e)
        {
            long? from = ParseNullableLong(txtFibFrom.Text);
            long? to   = ParseNullableLong(txtFibTo.Text);

            _fibWorker?.Stop();
            lstFib.Items.Clear();

            _fibWorker = new NumberWorker(
                kind: WorkerKind.Fibonacci,
                from: from,
                to: to,
                onNumber: n => lstFib.Items.Add(n.ToString()),
                onFinished: () => SetFibButtons(false));

            _fibWorker.Start();
            SetFibButtons(true);
        }

        private void btnPauseFib_Click(object sender, EventArgs e) => _fibWorker?.Pause();
        private void btnResumeFib_Click(object sender, EventArgs e) => _fibWorker?.Resume();
        private void btnStopFib_Click(object sender, EventArgs e)
        {
            _fibWorker?.Stop();
            SetFibButtons(false);
        }

        private void btnRestartFib_Click(object sender, EventArgs e)
        {
            btnStartFib_Click(sender, e);
        }

        // ---------- Вспомогательное ----------
        private static long? ParseNullableLong(string s)
        {
            if (string.IsNullOrWhiteSpace(s)) return null;
            return long.TryParse(s, out var v) ? v : (long?)null;
        }

        private void SetPrimesButtons(bool running)
        {
            btnPausePrimes.Enabled  = running;
            btnResumePrimes.Enabled = running;
            btnStopPrimes.Enabled   = running;
        }

        private void SetFibButtons(bool running)
        {
            btnPauseFib.Enabled  = running;
            btnResumeFib.Enabled = running;
            btnStopFib.Enabled   = running;
        }

        protected override void OnFormClosing(FormClosingEventArgs e)
        {
            _primeWorker?.Stop();
            _fibWorker?.Stop();
            base.OnFormClosing(e);
        }
    }
}