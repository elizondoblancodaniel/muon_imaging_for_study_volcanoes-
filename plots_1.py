import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import json
import functools
from scipy.stats import mannwhitneyu
from matplotlib.backends.backend_pdf import PdfPages
from matplotlib.patches import Patch
import os

# source .venv/bin/activate

def publication_style(ax, ylabel):
    """Apply a publication-quality style to the plot."""
    ax.set_xlabel("")
    ax.set_ylabel(ylabel, fontsize=11)
    ax.tick_params(axis="both", labelsize=10)
    ax.yaxis.grid(True, linestyle="--", linewidth=0.7, alpha=0.55)
    ax.set_axisbelow(True)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.legend(title="Volcano", bbox_to_anchor=(1.02, 1), loc="upper left", frameon=False, fontsize=9, title_fontsize=10)

output_dir_1 = "/home/daniel-elizondo/Escritorio/ECEN_2026/images"
os.makedirs(output_dir_1, exist_ok=True)

df_data = pd.read_csv("/home/daniel-elizondo/Escritorio/ECEN_2026/Rev_muones_list_hoja1.csv")

# =========================
# 2. Limpiar variables
# =========================
# Limpiar columna de volcán
df_data['VOL'] = df_data['VOL'].astype(str).str.strip()

# Columnas que contienen valores binarios o conteos
cols = ['MON', 'SIM', 'MET', 'INS', 'PC', 'EN', 'DG']

df_data[cols] = (df_data[cols].apply(pd.to_numeric, errors='coerce').fillna(0))
# Columnas para gráficas
cols_estudio = ['SIM', 'MET', 'INS', 'MON']
cols_tecnologia = ['PC', 'EN', 'DG', 'WCD']

# =========================
# 3. Definir colores por volcán
# =========================

colores_volcan = {
    "Chacaltaya & Chimborazo": "#1b9e77",
    "Mt. Unzen": "#d95f02",
    "Vesuvius": "#7570b3",
    "Cerro Machín": "#e7298a",
    "Sakurajima": "#66a61e",
    "La Soufrière": "#e6ab02",
    "Laoheishan": "#a6761d",
    "Omuroyama": "#666666",
    "Mt. Etna": "#1f78b4",
    "Sierra Negra": "#b2df8a",
    "Puy Dome": "#fb9a99",
    "Copahue": "#cab2d6",
    "Mt. Usu": "#ffac80",
}
orden_volcanes = list(colores_volcan.keys())
lista_colores = [colores_volcan[v] for v in orden_volcanes]

# =========================
# 4. Plot 1: Articles by year and volcano
# =========================

tabla_anio_vol = pd.crosstab(df_data["ANO"], df_data["VOL"])
anios = list(range(int(df_data["ANO"].min()), int(df_data["ANO"].max()) + 1))

tabla_anio_vol = tabla_anio_vol.reindex(
    index=anios,
    columns=orden_volcanes,
    fill_value=0
)

fig, ax = plt.subplots(figsize=(9, 5.5))

tabla_anio_vol.plot(
    kind="bar",
    stacked=True,
    color=lista_colores,
    width=0.65,
    ax=ax
)

publication_style(ax, "Number of articles")
ax.set_xticklabels(anios, rotation=0)

fig.tight_layout()
fig.savefig(
    os.path.join(output_dir_1, "02_articles_per_year.png"),
    dpi=600,
    bbox_inches="tight"
)
plt.show()
plt.close(fig)

# =========================
# 5. Plot 2: Study types by volcano
# =========================

tabla_temas_vol = df_data.groupby("VOL")[cols_estudio].sum()
tabla_temas_vol = tabla_temas_vol.reindex(orden_volcanes).fillna(0)

# Esta línea debe aparecer antes de tabla_plot.plot(...)
tabla_plot = tabla_temas_vol.T

fig, ax = plt.subplots(figsize=(9, 5.5))

tabla_plot.plot(
    kind="bar",
    stacked=True,
    color=lista_colores,
    width=0.60,
    ax=ax
)

publication_style(ax, "Number of articles")
ax.set_xticks(range(len(cols_estudio)))
ax.set_xticklabels(
    ["Simulation", "Methodology", "Instrumentation", "Monitoring"],
    rotation=0
)

fig.tight_layout()
fig.savefig(
    os.path.join(output_dir_1, "03_studies.png"),
    dpi=600,
    bbox_inches="tight"
)
plt.show()
plt.close(fig)

# =========================
# 6. Plot 3: Detector technology by volcano
# =========================

# max() cuenta cada volcán una sola vez por tecnología.
tabla_tecnologia_vol = df_data.groupby("VOL")[cols_tecnologia].max()
tabla_tecnologia_vol = tabla_tecnologia_vol.reindex(orden_volcanes).fillna(0)
tabla_tecnologia_plot = tabla_tecnologia_vol.T

fig, ax = plt.subplots(figsize=(9, 5.5))

tabla_tecnologia_plot.plot(
    kind="bar",
    stacked=True,
    color=lista_colores,
    width=0.55,
    ax=ax
)

publication_style(ax, "Number of volcanoes")
ax.set_xticks(range(len(cols_tecnologia)))
ax.set_xticklabels(
    ["Plastic Scintillator", "Nuclear Emulsion", "Gas Detector", "Water Cherenkov"],
    rotation=0
)

fig.tight_layout()
fig.savefig(
    os.path.join(output_dir_1, "04_Detector_type.png"),
    dpi=600,
    bbox_inches="tight"
)
plt.show()
plt.close(fig)
