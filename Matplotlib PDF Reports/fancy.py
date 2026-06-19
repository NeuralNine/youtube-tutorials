# AI-generated code

import datetime as dt

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import FancyBboxPatch
from matplotlib.lines import Line2D

INK = "#1b2a4a"
ACCENT = "#e4572e"
TEAL = "#17a2b8"
GREEN = "#2bae66"
GOLD = "#f3a712"
PURPLE = "#7b4 db".replace(" ", "")
PURPLE = "#7b4dbb"
PAPER = "#f7f6f2"
PANEL = "#ffffff"
MUTED = "#8a93a6"

plt.rcParams.update({
    "font.family": "DejaVu Sans",
    "font.size": 10,
    "axes.edgecolor": "#d8dbe2",
    "axes.linewidth": 0.8,
    "axes.grid": True,
    "grid.color": "#e7e9ef",
    "grid.linewidth": 0.8,
    "axes.axisbelow": True,
    "xtick.color": MUTED,
    "ytick.color": MUTED,
    "text.color": INK,
    "axes.labelcolor": INK,
    "axes.titlecolor": INK,
    "figure.facecolor": PAPER,
})

A4 = (8.27, 11.69)

rng = np.random.default_rng(42)
months = ["Jan", "Feb", "Mar", "Apr", "May", "Jun",
          "Jul", "Aug", "Sep", "Oct", "Nov", "Dec"]

df = pd.DataFrame({
    "month": months,
    "sales": [120, 135, 150, 145, 170, 165, 180, 175, 190, 200, 210, 230],
    "cost":  [80, 90, 95, 100, 110, 105, 115, 120, 125, 130, 140, 150],
})

df["profit"] = df["sales"] - df["cost"]
df["margin"] = (df["profit"] / df["sales"] * 100).round(1)

regions = ["North", "South", "East", "West"]
region_sales = pd.DataFrame(rng.integers(40, 120, size=(12, 4)), columns=regions, index=months)

products = ["Widgets", "Gadgets", "Gizmos", "Doohickeys", "Thingamajigs"]
product_share = np.array([34, 25, 18, 13, 10])


def style_axes(ax):
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.tick_params(length=0)


def lift(ax):
    ax.set_zorder(2)
    ax.patch.set_alpha(0)
    return ax


def page_frame(fig, title, subtitle, page_no, total):
    fig.patches.append(plt.Rectangle((0, 0), 1, 1, transform=fig.transFigure, facecolor=PAPER, zorder=-10))
    fig.patches.append(plt.Rectangle((0, 0.93), 1, 0.07, transform=fig.transFigure, facecolor=INK, zorder=5))
    fig.patches.append(plt.Rectangle((0, 0.928), 1, 0.004, transform=fig.transFigure, facecolor=ACCENT, zorder=6))

    fig.text(0.06, 0.957, title, color="white", fontsize=18, fontweight="bold", va="center", zorder=7)
    fig.text(0.06, 0.937, subtitle, color="#aeb7cc", fontsize=9, va="center", zorder=7)
    fig.text(0.94, 0.952, "ACME ANALYTICS", color="white", fontsize=10, fontweight="bold", ha="right", va="center", zorder=7)

    fig.patches.append(plt.Rectangle((0.06, 0.035), 0.88, 0.0015, transform=fig.transFigure, facecolor="#d8dbe2", zorder=5))
    fig.text(0.06, 0.022, f"Generated {dt.date.today():%B %d, %Y}", color=MUTED, fontsize=8)
    fig.text(0.94, 0.022, f"Page {page_no} of {total}", color=MUTED, fontsize=8, ha="right")


def card(fig, x, y, w, h, color=PANEL):
    fig.patches.append(
        FancyBboxPatch(
            (x, y), w, h,
            transform=fig.transFigure,
            boxstyle="round,pad=0.0,rounding_size=0.012",
            linewidth=0, facecolor=color, zorder=0,
            mutation_aspect=A4[0] / A4[1]
        )
    )


def kpi(fig, x, y, w, label, value, delta, color):
    h = 0.085
    card(fig, x, y, w, h, PANEL)

    fig.patches.append(plt.Rectangle((x, y), 0.006, h, transform=fig.transFigure, facecolor=color, zorder=1))

    fig.text(x + 0.025, y + h - 0.032, value, fontsize=19, fontweight="bold", color=INK, va="center")
    fig.text(x + 0.025, y + 0.018, label, fontsize=8.5, color=MUTED, va="center")

    if delta is not None:
        up = delta >= 0
        fig.text(x + w - 0.02, y + 0.018, f"{'▲' if up else '▼'} {abs(delta)}%",
                 fontsize=9, fontweight="bold", ha="right", va="center",
                 color=GREEN if up else ACCENT)


TOTAL_PAGES = 4

with PdfPages("report_fancy.pdf") as pdf:

    fig = plt.figure(figsize=A4)
    page_frame(fig, "Annual Performance Report",
               "Fiscal Year 2025  ·  Confidential", 1, TOTAL_PAGES)

    fig.text(0.06, 0.80, "Executive", fontsize=46, fontweight="bold",
             color=INK)
    fig.text(0.06, 0.73, "Summary", fontsize=46, fontweight="bold",
             color=ACCENT)
    fig.text(0.06, 0.685,
             "A year of momentum: record revenue, expanding margins,\n"
             "and balanced growth across every region.",
             fontsize=11, color="#566179", linespacing=1.5)

    ky = 0.55
    kpi(fig, 0.06, ky, 0.20, "Total Sales", f"${df['sales'].sum()}k", 14, ACCENT)
    kpi(fig, 0.30, ky, 0.20, "Total Profit", f"${df['profit'].sum()}k", 9, GREEN)
    kpi(fig, 0.54, ky, 0.20, "Avg Margin", f"{df['margin'].mean():.0f}%", 3, TEAL)
    kpi(fig, 0.78, ky, 0.16, "Best Month", "Dec", None, GOLD)

    card(fig, 0.06, 0.10, 0.88, 0.38)
    ax = lift(fig.add_axes([0.12, 0.16, 0.78, 0.27]))
    style_axes(ax)
    ax.plot(df["month"], df["sales"], color=ACCENT, lw=2.5, marker="o",
            mfc="white", mec=ACCENT, mew=2, zorder=3, label="Sales")
    ax.fill_between(range(12), df["sales"], color=ACCENT, alpha=0.12)
    ax.plot(df["month"], df["cost"], color=INK, lw=2, ls="--",
            alpha=0.7, label="Cost")
    ax.set_title("Monthly Sales vs Cost", loc="left", fontweight="bold",
                 fontsize=12, pad=12)
    ax.set_ylabel("Thousands ($)")
    ax.legend(frameon=False, loc="upper left")
    ax.margins(x=0.02)
    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=A4)
    page_frame(fig, "Revenue Breakdown",
               "Where the growth came from", 2, TOTAL_PAGES)
    gs = fig.add_gridspec(2, 2, left=0.09, right=0.93, top=0.86,
                          bottom=0.10, hspace=0.45, wspace=0.30)

    ax1 = fig.add_subplot(gs[0, 0]); style_axes(ax1)
    colors = cm.YlOrRd(np.linspace(0.35, 0.85, 12))
    bars = ax1.bar(df["month"], df["profit"], color=colors)
    ax1.bar_label(bars, fontsize=7, color=INK, padding=2)
    ax1.set_title("Monthly Profit", loc="left", fontweight="bold")
    ax1.tick_params(axis="x", rotation=45)

    ax2 = fig.add_subplot(gs[0, 1]); style_axes(ax2)
    ax2.axhspan(33, 37, color=TEAL, alpha=0.10)
    ax2.axhline(35, color=TEAL, ls="--", lw=1, alpha=0.8)
    ax2.plot(df["month"], df["margin"], color=TEAL, lw=2.5, marker="D",
             mfc="white", mec=TEAL, mew=1.8)
    ax2.set_title("Profit Margin (%)", loc="left", fontweight="bold")
    ax2.tick_params(axis="x", rotation=45)
    ax2.text(0.5, 35.3, "target", color=TEAL, fontsize=7)

    ax3 = fig.add_subplot(gs[1, 0]); style_axes(ax3)
    bottom = np.zeros(12)
    region_colors = [ACCENT, TEAL, GREEN, GOLD]
    for reg, c in zip(regions, region_colors):
        ax3.bar(months, region_sales[reg], bottom=bottom, label=reg, color=c)
        bottom += region_sales[reg].values
    ax3.set_title("Sales by Region (stacked)", loc="left", fontweight="bold")
    ax3.tick_params(axis="x", rotation=45)
    ax3.legend(frameon=False, fontsize=7, ncol=2, loc="upper left")

    ax4 = fig.add_subplot(gs[1, 1])
    wedges, _, autotexts = ax4.pie(
        product_share, labels=None, autopct="%d%%", startangle=90,
        colors=[ACCENT, TEAL, GREEN, GOLD, PURPLE],
        wedgeprops=dict(width=0.42, edgecolor=PANEL, linewidth=2),
        pctdistance=0.78)
    for t in autotexts:
        t.set_color("white"); t.set_fontsize(8); t.set_fontweight("bold")
    ax4.set_title("Product Mix", loc="left", fontweight="bold")
    ax4.legend(wedges, products, frameon=False, fontsize=6.5,
               loc="center left", bbox_to_anchor=(0.82, -0.18), ncol=1)
    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=A4)
    page_frame(fig, "Regional Deep Dive",
               "Heatmap & correlation analysis", 3, TOTAL_PAGES)

    card(fig, 0.06, 0.50, 0.88, 0.36)
    ax = lift(fig.add_axes([0.14, 0.55, 0.74, 0.26]))
    im = ax.imshow(region_sales.T.values, aspect="auto", cmap="YlOrRd")
    ax.set_xticks(range(12)); ax.set_xticklabels(months)
    ax.set_yticks(range(4)); ax.set_yticklabels(regions)
    ax.set_title("Sales Intensity by Region & Month", loc="left",
                 fontweight="bold", pad=10)
    ax.tick_params(length=0)
    for i in range(4):
        for j in range(12):
            ax.text(j, i, region_sales.T.values[i, j], ha="center",
                    va="center", fontsize=6.5, color="#333")
    cbar = fig.colorbar(im, ax=ax, fraction=0.025, pad=0.02)
    cbar.outline.set_visible(False)

    card(fig, 0.06, 0.10, 0.88, 0.34)
    ax = lift(fig.add_axes([0.13, 0.16, 0.78, 0.23]))
    style_axes(ax)
    sizes = (df["profit"] - df["profit"].min() + 10) * 6
    sc = ax.scatter(df["sales"], df["cost"], s=sizes, c=df["margin"],
                    cmap="viridis", alpha=0.85, edgecolors="white", lw=1.2)

    m, b = np.polyfit(df["sales"], df["cost"], 1)
    xs = np.array([df["sales"].min(), df["sales"].max()])
    ax.plot(xs, m * xs + b, color=ACCENT, ls="--", lw=1.5)
    ax.set_xlabel("Sales ($k)"); ax.set_ylabel("Cost ($k)")
    ax.set_title("Sales vs Cost  (size = profit, color = margin)",
                 loc="left", fontweight="bold", pad=10)
    cbar = fig.colorbar(sc, ax=ax, fraction=0.03, pad=0.02)
    cbar.set_label("Margin %", color=MUTED); cbar.outline.set_visible(False)
    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=A4)
    page_frame(fig, "Appendix",
               "Full data & key takeaways", 4, TOTAL_PAGES)

    card(fig, 0.06, 0.40, 0.88, 0.46)
    ax = lift(fig.add_axes([0.09, 0.43, 0.82, 0.40])); ax.axis("off")
    cols = ["Month", "Sales", "Cost", "Profit", "Margin %"]
    table = ax.table(cellText=df.values, colLabels=cols, loc="upper center",
                     cellLoc="center")
    table.auto_set_font_size(False)
    table.set_fontsize(8.5)
    table.scale(1, 1.45)
    for (r, c), cell in table.get_celld().items():
        cell.set_edgecolor("#e7e9ef")
        if r == 0:
            cell.set_facecolor(INK)
            cell.set_text_props(color="white", fontweight="bold")
            cell.set_height(0.075)
        elif r % 2 == 0:
            cell.set_facecolor("#f2f3f7")
        if c == 4 and r > 0:
            cell.set_text_props(color=GREEN, fontweight="bold")

    fig.text(0.06, 0.34, "Key Takeaways", fontsize=14, fontweight="bold",
             color=INK)
    bullets = [
        ("Revenue up 14% YoY", "Driven by a strong Q4 and the West region."),
        ("Margins held near 35%", "Cost growth stayed below sales growth all year."),
        ("Widgets lead the mix", "34% of revenue — consider doubling down."),
        ("December was the peak", "$230k in sales, the best month on record."),
    ]
    y = 0.30
    for head, body in bullets:
        fig.patches.append(plt.Circle(
            (0.075, y + 0.006), 0.006, transform=fig.transFigure,
            facecolor=ACCENT, zorder=3))
        fig.text(0.10, y, head, fontsize=10.5, fontweight="bold", color=INK)
        fig.text(0.10, y - 0.018, body, fontsize=9, color="#566179")
        y -= 0.055

    pdf.savefig(fig)
    plt.close(fig)

    d = pdf.infodict()
    d["Title"] = "Annual Performance Report — FY2025"
    d["Author"] = "ACME Analytics"

print("Wrote report_fancy.pdf")
