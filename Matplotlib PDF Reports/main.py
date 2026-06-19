import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

df = pd.DataFrame({
    'months': ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'],
    'sales': [120, 135, 150, 145, 170, 165, 180, 175, 190, 200, 210, 230],
    'cost': [80, 90, 95, 100, 110, 105, 115, 120, 125, 130, 140, 150]
})

df['profit'] = df['sales'] - df['cost']

with PdfPages('report.pdf') as pdf:
    fig = plt.figure(figsize=(8.27, 11.69))  # A4
    fig.suptitle('Annual Sales Report', fontsize=16, weight='bold')

    gs = fig.add_gridspec(3, 2, height_ratios=[1, 2, 2], hspace=0.4, wspace=0.3)

    ax_table = fig.add_subplot(gs[0, :])
    ax_table.axis('off')

    table = ax_table.table(cellText=df.values, colLabels=df.columns, loc='center')
    table.set_fontsize(8)

    ax1 = fig.add_subplot(gs[1, 0])
    ax1.plot(df.months, df.sales, marker='o', color='red')
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_title('Sales')

    ax2 = fig.add_subplot(gs[1, 1])
    ax2.plot(df.months, df.cost, marker='o', color='blue')
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_title('Cost')

    ax3 = fig.add_subplot(gs[2, 0])
    ax3.bar(df.months, df.profit, color='green')
    ax3.tick_params(axis='x', rotation=45)
    ax3.set_title('Profit')

    ax4 = fig.add_subplot(gs[2, 1])
    ax4.scatter(df.sales, df.cost, color='purple')
    ax4.set_title('Sales vs Cost')
    ax4.set_xlabel('sales')
    ax4.set_ylabel('cost')

    pdf.savefig(fig)
    plt.close(fig)

    fig = plt.figure(figsize=(8.27, 11.69))  # A4
    fig.suptitle('Additional Analysis', fontsize=16, weight='bold')

    gs = fig.add_gridspec(3, 1, height_ratios=[1, 2, 2], hspace=0.4)

    ax_text = fig.add_subplot(gs[0])
    ax_text.axis('off')
    ax_text.text(0.0, 0.9,
        f"Total sales: {df.sales.sum()}\n"
        f"Total cost: {df.cost.sum()}\n"
        f"Total profit: {df.profit.sum()}\n"
        f"Best month: {df.loc[df.profit.idxmax(), 'months']}",
        fontsize=11, va='top')

    ax1 = fig.add_subplot(gs[1])
    ax1.plot(df.months, df.profit.cumsum(), marker='s', color='orange')
    ax1.tick_params(axis='x', rotation=45)
    ax1.set_title('Cumulative Profit')

    ax2 = fig.add_subplot(gs[2])
    ax2.bar(df.months, df.sales, color='cyan', label='sales')
    ax2.bar(df.months, df.cost, color='red', alpha=0.6, label='cost')
    ax2.tick_params(axis='x', rotation=45)
    ax2.set_title('Sales vs Cost')
    ax2.legend()

    pdf.savefig(fig)
    plt.close(fig)


