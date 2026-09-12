r"""
Klippen-Grafik: Fragen pro Monat auf Stack Overflow ab 2021.

Aufruf:  python klippe.py QueryResults.csv
Ausgabe: klippe.svg und klippe.png

CSV stammt aus dem Stack Exchange Data Explorer und hat zwei Spalten:
Month (Zeitstempel) und Questions (Anzahl).

Benoetigt: pandas, matplotlib

C:\Users\sulta\AppData\Local\Python\bin\pip install pandas matplotlib
"""

import sys
from datetime import date
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import pandas as pd

CSV = sys.argv[1] if len(sys.argv) > 1 else r"C:/Users/sulta/git/unlogic.ai/paradoxes/efficiency/stackexchange/QueryResults.csv"
ZIEL = Path(__file__).resolve().parent   # .../paradoxes/efficiency/stackexchange
ZIEL.mkdir(parents=True, exist_ok=True)

AB_JAHR = 2021
FARBE = "#D85A30"
TEXT = "#2C2C2A"
GRAU = "#888780"

MONATE = ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
          "August", "September", "Oktober", "November", "Dezember"]

# --- Daten ---------------------------------------------------------------

df = pd.read_csv(CSV, parse_dates=["Month"])
df["Questions"] = pd.to_numeric(df["Questions"])
df = df.sort_values("Month")

# Laufender Monat ist unvollstaendig und wuerde einen Absturz zeigen,
# den es nicht gibt.
heute = date.today()
df = df[~((df.Month.dt.year == heute.year) & (df.Month.dt.month == heute.month))]

df = df[df.Month >= pd.Timestamp(f"{AB_JAHR}-01-01")].reset_index(drop=True)
start, ende = df.iloc[0], df.iloc[-1]

label = lambda z: f"Fragen im {MONATE[z.Month.month - 1]} {z.Month.year}"
punkt = lambda n: f"{int(n):,}".replace(",", ".")

# --- Grafik --------------------------------------------------------------

fig, ax = plt.subplots(figsize=(12, 6.2))

ax.fill_between(df.Month, df.Questions, color=FARBE, alpha=0.13)
ax.plot(df.Month, df.Questions, color=FARBE, linewidth=2.2)
ax.plot([start.Month, ende.Month], [start.Questions, ende.Questions],
        "o", color=FARBE, markersize=7, linestyle="none")

hoch = df.Questions.max() * 1.05
ax.set_ylim(0, hoch)
ax.set_xlim(df.Month.min(), df.Month.max())

# ChatGPT-Marker
marker = pd.Timestamp("2022-11")
ax.axvline(marker, color=GRAU, linewidth=0.8, linestyle=(0, (4, 4)))
ax.annotate("ChatGPT erscheint\nNovember 2022", xy=(marker, hoch * 0.96),
            xytext=(8, 0), textcoords="offset points",
            fontsize=11, color=GRAU, va="top")

# Die beiden grossen Zahlen ueber der Grafik
for x, ha, zeile in ((0.0, "left", start), (1.0, "right", ende)):
    ax.text(x, 1.14, punkt(zeile.Questions), transform=ax.transAxes,
            fontsize=40, color=TEXT, ha=ha, va="top")
    ax.text(x, 1.02, label(zeile), transform=ax.transAxes,
            fontsize=12, color=GRAU, ha=ha, va="top")

# Achsen entschlacken
for kante in ("top", "right", "left"):
    ax.spines[kante].set_visible(False)
ax.spines["bottom"].set_color(GRAU)
ax.spines["bottom"].set_linewidth(0.5)
ax.tick_params(length=0, labelsize=11, colors=GRAU)
ax.set_yticks([])

ax.text(0.0, -0.14,
        f"Neue Fragen pro Monat, {AB_JAHR} bis {ende.Month.year}. "
        f"Quelle: Stack Exchange Data Explorer, abgerufen am "
        f"{heute.strftime('%d.%m.%Y')}",
        transform=ax.transAxes, fontsize=10, color=GRAU, va="top")

plt.subplots_adjust(top=0.78, bottom=0.16, left=0.04, right=0.97)

for endung in ("svg", "png"):
    pfad = ZIEL / f"klippe.{endung}"
    fig.savefig(pfad, dpi=200, transparent=True)
    print("geschrieben:", pfad)