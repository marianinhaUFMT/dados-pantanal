import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.gridspec as gridspec
import numpy as np
from pathlib import Path

# leitura e tratamento de dados
def carregar_dados(caminho: str) -> pd.DataFrame:
    df = pd.read_csv(caminho, parse_dates=["data"])
    df.columns = df.columns.str.strip()           
    df = df.sort_values("data").reset_index(drop=True)
    return df

def tratar_valores_ausentes(df: pd.DataFrame) -> pd.DataFrame:
    colunas_numericas = ["temperatura_c", "nivel_rio_m", "ndvi"]

    ausentes_antes = df[colunas_numericas].isnull().sum()

    for col in colunas_numericas:
        df[col] = df[col].interpolate(method="linear", limit_direction="both")

    ausentes_depois = df[colunas_numericas].isnull().sum()

    print("=" * 55)
    print("  RELATÓRIO DE VALORES AUSENTES")
    print("=" * 55)
    for col in colunas_numericas:
        print(f"  {col:<18}  antes: {ausentes_antes[col]}  →  depois: {ausentes_depois[col]}")
    print("=" * 55)
    return df


# estatisticas basicas
def calcular_estatisticas(df: pd.DataFrame) -> pd.DataFrame:
    colunas = ["temperatura_c", "nivel_rio_m", "ndvi"]
    stats = df[colunas].agg(["mean", "min", "max", "std"]).T
    stats.columns = ["Média", "Mínimo", "Máximo", "Desvio Padrão"]
    stats.index = ["Temperatura (°C)", "Nível do Rio (m)", "NDVI"]

    print("\n  ESTATÍSTICAS DESCRITIVAS")
    print("=" * 55)
    print(stats.round(4).to_string())
    print("=" * 55)
    return stats


# visualizacao
CORES = {
    "temperatura": "#E07A26",
    "rio":         "#2176AE",
    "ndvi":        "#2D6A4F",
    "interpolado": "red",
}

def _configurar_estilo(ax, titulo: str, ylabel: str):
    ax.set_title(titulo, fontsize=13, fontweight="bold", pad=10)
    ax.set_ylabel(ylabel, fontsize=10)
    ax.tick_params(labelsize=9)
    ax.xaxis.set_major_formatter(mdates.DateFormatter("%d/%m"))
    ax.xaxis.set_major_locator(mdates.DayLocator(interval=2))
    ax.grid(linestyle="--", linewidth=0.6, alpha=0.5)
    ax.spines[["top", "right"]].set_visible(False)

def grafico_series_temporais(df: pd.DataFrame, saida: Path):
    fig = plt.figure(figsize=(12, 9))
    fig.suptitle("Monitoramento Ambiental · Pantanal  |  Jan 2025", fontsize=16, fontweight="bold", y=0.99)

    gs = gridspec.GridSpec(3, 1, hspace=0.6, top=0.93, bottom=0.08, left=0.09, right=0.97)

    # temperatura
    ax1 = fig.add_subplot(gs[0])
    ax1.fill_between(df["data"], df["temperatura_c"],
                     alpha=0.15, color=CORES["temperatura"])
    ax1.plot(df["data"], df["temperatura_c"],
             color=CORES["temperatura"], linewidth=2.2,
             marker="o", markersize=5, label="Temperatura (°C)")
    mask_interp_t = [3, 6]
    ax1.scatter(df["data"].iloc[mask_interp_t],
                df["temperatura_c"].iloc[mask_interp_t],
                color=CORES["interpolado"], s=50, zorder=5, label="Interpolado",
                edgecolors="white", linewidths=1.0)
    _configurar_estilo(ax1, "Temperatura do Ar", "°C")
    ax1.legend(fontsize=8, loc="upper right")

    # nivel do rio
    ax2 = fig.add_subplot(gs[1])
    ax2.fill_between(df["data"], df["nivel_rio_m"],
                     alpha=0.15, color=CORES["rio"])
    ax2.plot(df["data"], df["nivel_rio_m"],
             color=CORES["rio"], linewidth=2.2,
             marker="s", markersize=5, label="Nível do Rio (m)")
    mask_interp_r = [2, 6]
    ax2.scatter(df["data"].iloc[mask_interp_r],
                df["nivel_rio_m"].iloc[mask_interp_r],
                color=CORES["interpolado"], s=50, zorder=5, label="Interpolado",
                edgecolors="white", linewidths=1.0)
    _configurar_estilo(ax2, "Nível do Rio", "metros")
    ax2.legend(fontsize=8, loc="upper right")

    # ndvi
    ax3 = fig.add_subplot(gs[2])
    ax3.fill_between(df["data"], df["ndvi"],
                     alpha=0.15, color=CORES["ndvi"])
    ax3.plot(df["data"], df["ndvi"],
             color=CORES["ndvi"], linewidth=2.2,
             marker="D", markersize=5, label="NDVI")
    mask_interp_n = [3, 8]
    ax3.scatter(df["data"].iloc[mask_interp_n],
                df["ndvi"].iloc[mask_interp_n],
                color=CORES["interpolado"], s=50, zorder=5, label="Interpolado",
                edgecolors="white", linewidths=1.0)
    _configurar_estilo(ax3, "Índice de Vegetação (NDVI)", "NDVI (0–1)")
    ax3.legend(fontsize=8, loc="upper right")

    fig.savefig(saida / "grafico1_series_temporais.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"\n  Gráfico 1 salvo: {saida / 'grafico1_series_temporais.png'}")


def grafico_correlacao_e_barras(df: pd.DataFrame, stats: pd.DataFrame, saida: Path):
    fig, (ax_sc, ax_bar) = plt.subplots(1, 2, figsize=(12, 5), gridspec_kw={"width_ratios": [1.3, 1], "wspace": 0.35})

    fig.suptitle("Análise Estatística · Pantanal  |  Jan 2025", fontsize=15, fontweight="bold", y=1.02)

    # dispersão temperatura × ndvi
    sc = ax_sc.scatter(
        df["temperatura_c"], df["ndvi"],
        c=df["nivel_rio_m"], cmap="YlGnBu",
        s=90, edgecolors="grey", linewidths=0.8, zorder=3
    )
    cbar = fig.colorbar(sc, ax=ax_sc, pad=0.03)
    cbar.set_label("Nível do Rio (m)", fontsize=9)

    # linha de tendência
    z = np.polyfit(df["temperatura_c"], df["ndvi"], 1)
    p = np.poly1d(z)
    xs = np.linspace(df["temperatura_c"].min(), df["temperatura_c"].max(), 100)
    ax_sc.plot(xs, p(xs), "--", color="tomato", linewidth=1.4,
               label=f"Tendência (r²={np.corrcoef(df['temperatura_c'], df['ndvi'])[0,1]**2:.2f})")
    ax_sc.set_xlabel("Temperatura (°C)", fontsize=10)
    ax_sc.set_ylabel("NDVI", fontsize=10)
    ax_sc.set_title("Temperatura × NDVI\n(cor = nível do rio)", fontsize=12, fontweight="bold")
    ax_sc.grid(linestyle="--", linewidth=0.6, alpha=0.5)
    ax_sc.spines[["top", "right"]].set_visible(False)
    ax_sc.legend(fontsize=8)

    # barras de médias
    variaveis = ["Temperatura\n(°C)", "Nível do Rio\n(m)", "NDVI"]
    valores   = [
        df["temperatura_c"].mean(),
        df["nivel_rio_m"].mean(),
        df["ndvi"].mean(),
    ]
    cores = [CORES["temperatura"], CORES["rio"], CORES["ndvi"]]

    bars = ax_bar.bar(variaveis, valores, color=cores, width=0.5,
                      edgecolor="white", linewidth=1.2)

    for bar, val in zip(bars, valores):
        ax_bar.text(
            bar.get_x() + bar.get_width() / 2,
            bar.get_height() + max(valores) * 0.02,
            f"{val:.3f}",
            ha="center", va="bottom", fontsize=10, fontweight="bold"
        )

    ax_bar.set_title("Médias do Período", fontsize=12, fontweight="bold")
    ax_bar.set_ylabel("Valor médio", fontsize=10)
    ax_bar.grid(axis="y", linestyle="--", linewidth=0.6, alpha=0.5)
    ax_bar.spines[["top", "right"]].set_visible(False)

    fig.savefig(saida / "grafico2_correlacao_medias.png", dpi=150, bbox_inches="tight")
    plt.close(fig)
    print(f"  Gráfico 2 salvo: {saida / 'grafico2_correlacao_medias.png'}")

def main():
    base = Path(__file__).parent
    dados_path = base / "dados_pantanal.csv"
    saida_path = base / "outputs"
    saida_path.mkdir(exist_ok=True)

    print("\n" + "═" * 55)
    print("  Análise de Dados Ambientais – Pantanal (Jan/2025)")
    print("═" * 55)

    df = carregar_dados(dados_path)
    print(f"\n  Dados carregados: {len(df)} registros, {df.shape[1]} variáveis")

    df = tratar_valores_ausentes(df)

    stats = calcular_estatisticas(df)

    print("\n  Gerando visualizações...")
    grafico_series_temporais(df, saida_path)
    grafico_correlacao_e_barras(df, stats, saida_path)

    df.to_csv(saida_path / "dados_pantanal_tratados.csv", index=False)
    print(f"  ✔  Dados tratados salvos: {saida_path / 'dados_pantanal_tratados.csv'}")

    print("\n  Análise concluída com sucesso!\n")

if __name__ == "__main__":
    main()