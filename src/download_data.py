"""
Script para baixar os dados oficiais do ARC Prize 2026 via kagglehub.
Certifique-se de estar autenticado no Kaggle (variáveis KAGGLE_USERNAME / KAGGLE_KEY
ou arquivo ~/.kaggle/kaggle.json) e de ter aceitado as regras da competição na página do Kaggle.
"""

import kagglehub


def download_all():
    competitions = [
        "arc-prize-2026-paper-track",
        "arc-prize-2026-arc-agi-2",
    ]
    for comp in competitions:
        try:
            print(f"Baixando arquivos de '{comp}'...")
            path = kagglehub.competition_download(comp)
            print(f"[OK] Caminho dos arquivos de {comp}: {path}")
        except Exception as exc:
            print(f"[AVISO] Não foi possível baixar '{comp}': {exc}")
            print(
                f" -> Verifique se você aceitou as regras em: https://www.kaggle.com/competitions/{comp}/rules"
            )


if __name__ == "__main__":
    download_all()
