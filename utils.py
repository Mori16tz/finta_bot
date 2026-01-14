from database import get_fach, Vorlesung
import pandas as pd
import matplotlib.pyplot as plt

BG_COLOR = "#070709"
GRID_COLOR = "#4F545C"
TEXT_COLOR = "#FFFFFF"

def generate_picture(vorlesung):
    rows = []
    for entry in get_fach(vorlesung):
        rows.append({
            "Vorlesung": entry.nummer,
            "Datum": entry.date.strftime("%d.%m.%Y"),
            "Gesamt": entry.gesamt,
            "FINTA": entry.finta,
            "Prozentual": f"{entry.quote} %"
        })

    df = pd.DataFrame(rows)
    df.sort_values(["Datum", "Vorlesung"], inplace=True)

    fig, ax = plt.subplots(figsize=(8, len(df)*0.5 + 1))
    fig.patch.set_facecolor(BG_COLOR)
    ax.axis('off')

    title = vorlesung.value
    plt.title(title, fontsize=16, fontweight='bold', pad=20, color=TEXT_COLOR)

    table = ax.table(
        cellText=df.values,
        colLabels=df.columns,
        cellLoc='center',
        loc='center',
        colColours=[BG_COLOR]*len(df.columns),
    )

    table.auto_set_font_size(False)
    table.set_fontsize(12)
    table.scale(1, 1.5)

    for (i, j), cell in table.get_celld().items():
        cell.set_edgecolor(GRID_COLOR)
        cell.set_text_props(color=TEXT_COLOR)
        if i == 0:
            cell.set_facecolor(GRID_COLOR)
            cell.set_text_props(weight='bold')
        else:
            cell.set_facecolor(BG_COLOR)

    plt.tight_layout()
    plt.savefig("table.png", dpi=200, facecolor=fig.get_facecolor())
    plt.show()
    
if __name__ == "__main__":
    generate_picture(Vorlesung.RSN)