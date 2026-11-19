# /// script
# requires-python = ">=3.10"
# dependencies = ["matplotlib"]
# ///
"""Figura 6: throughput real do nestjs/nest e backtest do compromisso P85 (lê resultados/resultados.json)."""
import json
import sys
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

raiz = Path(sys.argv[1]) if len(sys.argv) > 1 else Path.cwd()
r = json.loads((raiz / "resultados" / "resultados.json").read_text())["nest"]
bt = r["backtest"]

plt.rcParams.update({"font.family": "sans-serif", "font.sans-serif": ["DejaVu Sans"], "font.size": 10,
                     "axes.spines.top": False, "axes.spines.right": False})
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(13, 4.6), dpi=180)

semanas = list(range(1, len(r["semanal"]) + 1))
cores = ["#B83A3A" if s >= bt["semanaRegime"] else "#3B6978" for s in semanas]
ax1.bar(semanas, r["semanal"], color=cores, edgecolor="#161D26", linewidth=0.4)
ax1.axvline(bt["semanaRegime"] - 0.5, color="#161D26", linestyle="--", linewidth=1.2)
ax1.text(bt["semanaRegime"] - 1, max(r["semanal"]) * 0.92, "mudança de regime\n(salto de vazão ~8×)", ha="right", fontsize=9)
ax1.set_title(f"nestjs/nest: PRs humanos mergeados por semana ({r['totalPRs']} PRs, 52 semanas)")
ax1.set_xlabel("Semana (a partir de 17/11/2025)")
ax1.set_ylabel("Throughput (PRs/semana)")

j = bt["janelas"]
x = [w["semana"] for w in j]
ax2.plot(x, [w["real"] for w in j], "o-", color="#161D26", label="Real entregue em 6 semanas")
ax2.plot(x, [w["compromisso85"] for w in j], "s--", color="#E67E22", label="Compromisso P85 (Monte Carlo)")
ax2.plot(x, [w["ingenuo"] for w in j], "^:", color="#B83A3A", label="Média × semanas (velocity)")
ax2.axvspan(bt["semanaRegime"] - bt["horizonte"] + 0.5, max(x) + 0.5, color="#B83A3A", alpha=0.08)
ax2.set_yscale("log")
ax2.set_title("Backtest rolante: treino de 26 semanas, previsão das 6 seguintes")
ax2.set_xlabel("Primeira semana prevista")
ax2.set_ylabel("PRs no horizonte (escala log)")
est = bt["estavel"]
ax2.text(0.02, 0.97, f"Período estável ({est['janelas']} janelas)\nP85 cumprido: {est['acertos85']*100:.1f}%\n"
         f"Mediana cumprida: {est['acertosMediana']*100:.1f}%\nMédia × semanas: {est['acertosIngenuo']*100:.1f}%",
         transform=ax2.transAxes, va="top", fontsize=9,
         bbox=dict(boxstyle="round,pad=0.5", facecolor="#F4F4F6", edgecolor="#C9CCD3"))
ax2.legend(loc="center left", fontsize=8.5)

fig.tight_layout()
fig.savefig(raiz / "img" / "fig6_nestjs_backtest.png", bbox_inches="tight")
print("img/fig6_nestjs_backtest.png")
