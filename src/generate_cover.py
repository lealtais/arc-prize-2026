"""
Gera a imagem de capa (Cover Image) obrigatória para a Media Gallery do Kaggle Writeup
mostrando um exemplo visual de transformação no ARC-AGI-2 (Input -> Program Synthesis -> Output).
"""

from pathlib import Path
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

# Paleta oficial de 10 cores do ARC
ARC_COLORS = [
    "#000000",  # 0: black
    "#0074D9",  # 1: blue
    "#FF4136",  # 2: red
    "#2ECC40",  # 3: green
    "#FFDC00",  # 4: yellow
    "#AAAAAA",  # 5: grey
    "#F012BE",  # 6: magenta
    "#FF851B",  # 7: orange
    "#7FDBFF",  # 8: teal
    "#870C25",  # 9: maroon
]
ARC_CMAP = ListedColormap(ARC_COLORS)


def plot_grid(ax, grid: np.ndarray, title: str):
    ax.imshow(grid, cmap=ARC_CMAP, vmin=0, vmax=9)
    h, w = grid.shape
    ax.set_xticks(np.arange(-0.5, w, 1), minor=True)
    ax.set_yticks(np.arange(-0.5, h, 1), minor=True)
    ax.grid(which="minor", color="#333333", linestyle="-", linewidth=1.5)
    ax.tick_params(which="both", bottom=False, left=False, labelbottom=False, labelleft=False)
    ax.set_title(title, fontsize=11, fontweight="bold", color="#FFFFFF", pad=8)


def generate_cover():
    out_dir = Path(__file__).resolve().parent.parent / "paper" / "media"
    out_dir.mkdir(parents=True, exist_ok=True)
    out_path = out_dir / "cover_image.png"

    fig, axes = plt.subplots(1, 3, figsize=(12, 4.2), facecolor="#0F172A")
    fig.suptitle(
        "ARC Prize 2026 — Compositional Test-Time Program Synthesis",
        fontsize=15,
        fontweight="bold",
        color="#38BDF8",
        y=0.96,
    )

    inp = np.array(
        [
            [0, 1, 0, 0, 0],
            [1, 1, 1, 0, 0],
            [0, 1, 0, 0, 0],
            [0, 0, 0, 2, 2],
            [0, 0, 0, 2, 0],
        ]
    )
    mid = np.rot90(inp, 1)
    out = mid.copy()
    out[mid == 1] = 3
    out[mid == 2] = 4

    plot_grid(axes[0], inp, "1. Unseen Input Grid X")
    plot_grid(axes[1], mid, "2. Geometric Induction: rot90(X)")
    plot_grid(axes[2], out, "3. Late Color Binding: f(X) -> Y")

    plt.tight_layout(rect=[0, 0.03, 1, 0.88])
    plt.savefig(out_path, dpi=180, facecolor=fig.get_facecolor())
    plt.close(fig)
    print(f"Cover image gerada com sucesso em: {out_path}")


if __name__ == "__main__":
    generate_cover()
