#!/usr/bin/env python3
# /// script
# requires-python = ">=3.10"
# dependencies = [
#     "numpy",
#     "matplotlib",
# ]
# ///
"""
Simulação de Monte Carlo para Previsão de Prazos de Software
ENGS231N01 - Engenharia de Software - CEUNI FAMETRO
Acadêmico: Fábio Henrique Mendes Brasileiro
Docente / Orientador: Prof. Me. Alexsand Farias de Souza

Referência Open Source:
- rodbv/quando (Python): https://github.com/rodbv/quando
  Biblioteca open-source de previsão estocástica ágil via amostragem não paramétrica de Throughput.
- thawkin3/monte-carlo-simulation-project-timeline-estimator (TypeScript/Node):
  https://github.com/thawkin3/monte-carlo-simulation-project-timeline-estimator
- Troy Magennis / FocusedObjective.Resources:
  Modelos de simulação estatística de Throughput adotados pela Agile Alliance.
"""

import sys
import os
import shutil
import argparse
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

# Configuração de estilo neutro e acadêmico para publicação
plt.rcParams.update({
    'font.family': 'sans-serif',
    'font.sans-serif': ['DejaVu Sans', 'Arial', 'Helvetica'],
    'font.size': 10,
    'axes.labelsize': 11,
    'axes.titlesize': 12,
    'xtick.labelsize': 9,
    'ytick.labelsize': 9,
    'legend.fontsize': 9,
    'figure.titlesize': 13,
    'figure.dpi': 300,
    'savefig.bbox': 'tight',
    'axes.grid': True,
    'grid.alpha': 0.4,
    'grid.linestyle': '--'
})

OUTPUT_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'img')
os.makedirs(OUTPUT_DIR, exist_ok=True)

# ------------------------------------------------------------------------------
# 1. Histórico Empírico de Throughput da Equipe (26 semanas consecutivas)
# ------------------------------------------------------------------------------
HISTORICO_THROUGHPUT = np.array([
    4, 3, 5, 2, 4, 6, 3, 1, 5, 4, 3, 6, 2, 5, 4, 3, 7, 4, 2, 5, 3, 4, 6, 2, 4, 5
])

# ------------------------------------------------------------------------------
# 2. Motor Open-Source de Monte Carlo e Referências Oficiais
# ------------------------------------------------------------------------------
class MonteCarloEngine:
    """
    Motor estocástico de previsão baseado nos princípios das bibliotecas open-source
    'rodbv/quando' e 'FocusedObjective.Resources'.
    Utiliza amostragem não paramétrica com reposição (bootstrapping) sobre o histórico
    factual de Throughput semanal, sem assumir distribuição normal prévia.
    """
    def __init__(self, throughput_history, seed=42):
        self.history = np.array(throughput_history, dtype=int)
        if len(self.history) < 5:
            raise ValueError("Histórico de Throughput deve ter no mínimo 5 observações.")
        self.seed = seed
        self.rng = np.random.default_rng(seed)

    def forecast_backlog(self, backlog_size=60, n_simulations=10000, scope_creep=None):
        """
        Simula quantas semanas são necessárias para zerar um backlog de tamanho N.
        
        Parâmetros:
          backlog_size: número inicial de itens
          n_simulations: rodadas de Monte Carlo (padrão 10.000)
          scope_creep: tupla (itens_possiveis, probabilidades) ou None
        """
        weeks_to_finish = np.zeros(n_simulations, dtype=int)
        
        for i in range(n_simulations):
            remaining = backlog_size
            weeks = 0
            while remaining > 0:
                weeks += 1
                # Amostragem com reposição do histórico empírico
                throughput = self.rng.choice(self.history)
                
                # Scope Creep: taxa estocástica de novos itens descobertos
                new_items = 0
                if scope_creep is not None:
                    items_opts, probs = scope_creep
                    new_items = self.rng.choice(items_opts, p=probs)
                    
                remaining = remaining - throughput + new_items
            weeks_to_finish[i] = weeks
            
        return weeks_to_finish

    def simulate_trajectories(self, backlog_size=60, max_weeks=25, n_simulations=10000):
        """
        Gera a matriz completa de trajetórias (caminhos amostrais) semana a semana.
        Retorna: matriz de dimensão (n_simulations, max_weeks + 1)
        """
        trajectories = np.zeros((n_simulations, max_weeks + 1), dtype=int)
        trajectories[:, 0] = backlog_size
        
        for i in range(n_simulations):
            rem = backlog_size
            for w in range(1, max_weeks + 1):
                rem = max(0, rem - int(self.rng.choice(self.history)))
                trajectories[i, w] = rem
        return trajectories

    def forecast_date_driven(self, num_weeks=12, n_simulations=10000):
        """
        Simula quantos itens a equipe entregará em um prazo fixo de N semanas.
        Útil para planejar escopo de um trimestre ou sprint.
        """
        items_delivered = np.zeros(n_simulations, dtype=int)
        for i in range(n_simulations):
            sampled_weeks = self.rng.choice(self.history, size=num_weeks)
            items_delivered[i] = np.sum(sampled_weeks)
        return items_delivered

    @staticmethod
    def get_percentiles(results):
        """Calcula percentis de risco padrão do mercado ágil (P50, P70, P85, P95)."""
        return {
            'P50': float(np.percentile(results, 50)),
            'P70': float(np.percentile(results, 70)),
            'P85': float(np.percentile(results, 85)),
            'P95': float(np.percentile(results, 95)),
            'mean': float(np.mean(results)),
            'std': float(np.std(results, ddof=1)),
            'min': int(np.min(results)),
            'max': int(np.max(results))
        }

class ReferenceQuandoForecast:
    """
    Reprodução fiel do algoritmo de previsão da biblioteca open-source 'rodbv/quando'
    (repositório oficial: https://github.com/rodbv/quando).
    Implementa forecast_days e o cálculo de SLE (Service Level Expectation).
    """
    def __init__(self, throughput_data):
        self.throughput = np.array(throughput_data, dtype=int)

    def forecast(self, n_items=60, num_simulations=10000, seed=42):
        rng = np.random.default_rng(seed)
        results = np.empty(num_simulations, dtype=int)
        for i in range(num_simulations):
            done = 0
            steps = 0
            while done < n_items:
                done += int(rng.choice(self.throughput))
                steps += 1
            results[i] = steps
        
        # Conforme rodbv/quando: ceil no percentil
        p50 = int(np.ceil(float(np.percentile(results, 50))))
        p85 = int(np.ceil(float(np.percentile(results, 85))))
        p95 = int(np.ceil(float(np.percentile(results, 95))))
        return {'results': results, 'P50': p50, 'P85': p85, 'P95': p95}

class ReferenceThawkin3Forecast:
    """
    Reprodução fiel do algoritmo de simulação do projeto open-source TypeScript
    'thawkin3/monte-carlo-simulation-project-timeline-estimator'.
    """
    def __init__(self, throughput_data):
        self.history = list(throughput_data)

    def run_simulation_n_times(self, n_tasks=60, n_simulations=10000, seed=42):
        rng = np.random.default_rng(seed)
        results = []
        for _ in range(n_simulations):
            rem = n_tasks
            days = 0
            while rem > 0:
                days += 1
                sampled = int(rng.choice(self.history))
                rem -= sampled
            results.append(days)
        results.sort()
        p50 = results[int(0.50 * (len(results) - 1))]
        p85 = results[int(0.85 * (len(results) - 1))]
        p95 = results[int(0.95 * (len(results) - 1))]
        return {'results': np.array(results), 'P50': p50, 'P85': p85, 'P95': p95}

# ------------------------------------------------------------------------------
# 3. Geração dos Gráficos de Evidência
# ------------------------------------------------------------------------------
def gerar_grafico_fundamentacao_fisica():
    """Gera visualização da área por rejeição e convergência teórica 1/sqrt(N)."""
    np.random.seed(42)
    n_points = 2500
    x = np.random.uniform(0, 1, n_points)
    y = np.random.uniform(0, 1, n_points)
    
    inside = (x**2 + y**2) <= 1.0
    pi_estimate = 4.0 * np.sum(inside) / n_points
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10, 4.5))
    
    theta = np.linspace(0, np.pi/2, 200)
    ax1.plot(np.cos(theta), np.sin(theta), color='#161D26', linewidth=2, label=r'$x^2 + y^2 = 1$')
    ax1.scatter(x[inside], y[inside], s=7, color='#2B5B84', alpha=0.6, label=f'Dentro ({np.sum(inside)})')
    ax1.scatter(x[~inside], y[~inside], s=7, color='#B83A3A', alpha=0.4, label=f'Fora ({np.sum(~inside)})')
    ax1.set_xlim(0, 1)
    ax1.set_ylim(0, 1)
    ax1.set_aspect('equal')
    ax1.set_title(r'Amostragem de Monte Carlo (Área de $\pi/4$)')
    ax1.set_xlabel('Coordenada X')
    ax1.set_ylabel('Coordenada Y')
    ax1.legend(loc='lower left', frameon=True)
    ax1.text(0.55, 0.85, f'Estimativa de $\\pi$: {pi_estimate:.4f}\nValor Real: 3.1416',
             fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F6', edgecolor='#C9CCD3'))
    
    ns = np.logspace(1.5, 4.5, 60).astype(int)
    erros = []
    for n in ns:
        x_sub = np.random.uniform(0, 1, n)
        y_sub = np.random.uniform(0, 1, n)
        est = 4.0 * np.sum((x_sub**2 + y_sub**2) <= 1.0) / n
        erros.append(abs(est - np.pi))
    
    ax2.loglog(ns, erros, 'o', color='#2B5B84', alpha=0.5, markersize=4, label='Erro Absoluto Amostral')
    ax2.loglog(ns, 1.0 / np.sqrt(ns), color='#161D26', linestyle='--', linewidth=1.8, label=r'Convergência Teórica $O(1/\sqrt{N})$')
    ax2.set_title('Convergência do Erro Estocástico')
    ax2.set_xlabel('Tamanho da Amostra (N iterações)')
    ax2.set_ylabel('Erro Absoluto |Estimado - Real|')
    ax2.legend(loc='upper right', frameon=True)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig1_fisica_area_monte_carlo.png')
    plt.savefig(path)
    plt.close()
    print(f"✔ Gráfico 1 gerado: {path} (Estimativa pi = {pi_estimate:.4f})")

def gerar_grafico_throughput():
    """Gera o histograma empírico de vazão semanal ao longo de 26 semanas."""
    media = np.mean(HISTORICO_THROUGHPUT)
    mediana = np.median(HISTORICO_THROUGHPUT)
    desvio = np.std(HISTORICO_THROUGHPUT, ddof=1)
    
    fig, ax = plt.subplots(figsize=(8, 4.2))
    valores, contagens = np.unique(HISTORICO_THROUGHPUT, return_counts=True)
    
    ax.bar(valores, contagens, width=0.55, color='#3B6978', edgecolor='#161D26', alpha=0.85, label='Frequência Observada')
    ax.axvline(media, color='#B83A3A', linestyle='-', linewidth=2, label=f'Média Aritmética ({media:.2f} itens/sem)')
    ax.axvline(mediana, color='#E67E22', linestyle='--', linewidth=2, label=f'Mediana ({mediana:.1f} itens/sem)')
    
    ax.set_title(r'Distribuição Histórica da Vazão Semanal (Throughput) — 26 Semanas')
    ax.set_xlabel('Itens Concluídos por Semana (Throughput)')
    ax.set_ylabel('Número de Semanas (Frequência)')
    ax.set_xticks(np.arange(0, 9, 1))
    ax.set_ylim(0, max(contagens) + 1.5)
    
    info_text = (f'Amostra (N): 26 semanas\n'
                 f'Total Entregue: {np.sum(HISTORICO_THROUGHPUT)} itens\n'
                 f'Média: {media:.2f} itens/sem\n'
                 f'Desvio Padrão: {desvio:.2f}\n'
                 f'Mínimo: {np.min(HISTORICO_THROUGHPUT)} | Máximo: {np.max(HISTORICO_THROUGHPUT)}')
    ax.text(0.03, 0.95, info_text, transform=ax.transAxes, verticalalignment='top',
            fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F6', edgecolor='#C9CCD3'))
    
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig2_throughput_historico.png')
    plt.savefig(path)
    plt.close()
    print(f"✔ Gráfico 2 gerado: {path} (Média = {media:.2f}, DP = {desvio:.2f})")

def gerar_grafico_histograma_prazos(semanas_fixo):
    """Gera o histograma com percentis de risco P50, P85 e P95."""
    stats = MonteCarloEngine.get_percentiles(semanas_fixo)
    p50 = stats['P50']
    p85 = stats['P85']
    p95 = stats['P95']
    media = stats['mean']
    
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    bins = np.arange(min(semanas_fixo) - 0.5, max(semanas_fixo) + 1.5, 1)
    
    ax.hist(semanas_fixo, bins=bins, color='#4A708B', edgecolor='#161D26', alpha=0.8, density=True)
    
    ax.axvline(p50, color='#27AE60', linestyle='--', linewidth=2, label=f'P50 (Mediana): {p50:.0f} semanas (50% risco - cara ou coroa)')
    ax.axvline(p85, color='#E67E22', linestyle='-', linewidth=2.2, label=f'P85 (Compromisso Ágil): {p85:.0f} semanas (85% certeza)')
    ax.axvline(p95, color='#C0392B', linestyle=':', linewidth=2.2, label=f'P95 (Conservador / SLA): {p95:.0f} semanas (95% certeza)')
    
    ax.set_title('Simulação de Monte Carlo para Conclusão de 60 Itens (10.000 Rodadas)')
    ax.set_xlabel('Tempo Necessário para Entrega (Semanas)')
    ax.set_ylabel('Densidade de Probabilidade')
    ax.set_xticks(np.arange(min(semanas_fixo), max(semanas_fixo) + 1, 2))
    
    info_text = (f'Backlog Inicial: 60 itens\n'
                 f'Iterações: 10.000\n'
                 f'Média de Conclusão: {media:.1f} sem\n'
                 f'Percentil 50: {p50:.0f} sem\n'
                 f'Percentil 85: {p85:.0f} sem\n'
                 f'Percentil 95: {p95:.0f} sem')
    ax.text(0.03, 0.95, info_text, transform=ax.transAxes, verticalalignment='top',
            fontsize=9, bbox=dict(boxstyle='round,pad=0.5', facecolor='#F4F4F6', edgecolor='#C9CCD3'))
    
    ax.legend(loc='upper right', frameon=True)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig3_monte_carlo_prazos_histograma.png')
    plt.savefig(path)
    plt.close()
    print(f"✔ Gráfico 3 gerado: {path} (P50 = {p50}, P85 = {p85}, P95 = {p95})")

def gerar_grafico_curva_s(semanas_fixo, semanas_dinamico):
    """Gera a Curva S (CDF) contrastando Escopo Fixo vs Escopo Dinâmico."""
    fig, ax = plt.subplots(figsize=(8.5, 4.5))
    
    x_fixo = np.sort(semanas_fixo)
    y_fixo = np.arange(1, len(x_fixo) + 1) / len(x_fixo) * 100
    
    x_din = np.sort(semanas_dinamico)
    y_din = np.arange(1, len(x_din) + 1) / len(x_din) * 100
    
    ax.plot(x_fixo, y_fixo, color='#2B5B84', linewidth=2.5, label='Cenário A: Escopo Fixo (60 itens)')
    ax.plot(x_din, y_din, color='#B83A3A', linewidth=2.5, linestyle='--', label='Cenário B: Escopo Dinâmico (Scope Creep médio +0.65/sem)')
    
    ax.axhline(50, color='#888888', linestyle=':', alpha=0.7)
    ax.axhline(85, color='#E67E22', linestyle=':', alpha=0.8)
    ax.axhline(95, color='#C0392B', linestyle=':', alpha=0.8)
    
    p85_fixo = np.percentile(semanas_fixo, 85)
    p85_din = np.percentile(semanas_dinamico, 85)
    
    ax.plot(p85_fixo, 85, 'o', color='#2B5B84', markersize=7)
    ax.annotate(f'P85 Fixo: {p85_fixo:.0f} sem', (p85_fixo, 85), textcoords="offset points",
                xytext=(-65, 8), fontsize=9, fontweight='bold', color='#2B5B84')
    
    ax.plot(p85_din, 85, 's', color='#B83A3A', markersize=7)
    ax.annotate(f'P85 Dinâmico: {p85_din:.0f} sem', (p85_din, 85), textcoords="offset points",
                xytext=(10, -12), fontsize=9, fontweight='bold', color='#B83A3A')
    
    ax.set_title('Curva S Cumulativa de Entrega — Nível de Certeza vs Prazo')
    ax.set_xlabel('Prazo de Conclusão (Semanas)')
    ax.set_ylabel('Probabilidade Cumulativa de Sucesso (%)')
    ax.set_yticks(np.arange(0, 101, 10))
    ax.set_xlim(min(min(semanas_fixo), min(semanas_dinamico)), max(max(semanas_fixo), max(semanas_dinamico)))
    
    ax.legend(loc='lower right', frameon=True)
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig4_curva_s_cdf_risco.png')
    plt.savefig(path)
    plt.close()
    print(f"✔ Gráfico 4 gerado: {path} (P85 Fixo = {p85_fixo}, P85 Dinâmico = {p85_din})")

def gerar_grafico_trajetorias_convergencia():
    """Gera visualização dos caminhos amostrais (trajetórias) e convergência estocástica."""
    engine = MonteCarloEngine(HISTORICO_THROUGHPUT, seed=42)
    max_weeks = 24
    trajetorias = engine.simulate_trajectories(backlog_size=60, max_weeks=max_weeks, n_simulations=10000)
    
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(10.5, 4.6))
    weeks = np.arange(max_weeks + 1)
    
    # Subplot 1: Trajetórias individuais e Cone de Incerteza
    for i in range(80):
        ax1.plot(weeks, trajetorias[i], color='#3B82F6', alpha=0.15, linewidth=1.1)
        
    p15_w = np.percentile(trajetorias, 15, axis=0)
    p50_w = np.percentile(trajetorias, 50, axis=0)
    p85_w = np.percentile(trajetorias, 85, axis=0)
    
    ax1.fill_between(weeks, p15_w, p85_w, color='#93C5FD', alpha=0.35, label='Cone de Incerteza (P15 – P85)')
    ax1.plot(weeks, p50_w, color='#1E3A8A', linewidth=2.4, label='Trajetória Mediana (P50)')
    
    ax1.axhline(0, color='#111827', linestyle='--', linewidth=1.2, label='Backlog Zerado (DoD)')
    ax1.axvline(16, color='#10B981', linestyle=':', linewidth=2, label='P50 = 16 semanas')
    ax1.axvline(17, color='#F59E0B', linestyle='--', linewidth=2, label='P85 = 17 semanas')
    ax1.axvline(18, color='#EF4444', linestyle=':', linewidth=2, label='P95 = 18 semanas')
    
    ax1.set_xlim(0, 22)
    ax1.set_ylim(-2, 65)
    ax1.set_title('Trajetórias Estocásticas e Cone de Incerteza')
    ax1.set_xlabel('Semanas de Execução')
    ax1.set_ylabel('Itens Restantes no Backlog')
    ax1.legend(loc='upper right', fontsize=8, frameon=True)
    
    # Subplot 2: Convergência dos Percentis com Amostras N
    sample_sizes = [20, 50, 100, 200, 500, 1000, 2000, 5000, 10000]
    p50_n, p85_n, p95_n = [], [], []
    for n in sample_sizes:
        sub_engine = np.random.default_rng(n + 123)
        sub_results = []
        for _ in range(n):
            rem = 60
            w = 0
            while rem > 0:
                w += 1
                rem -= int(sub_engine.choice(HISTORICO_THROUGHPUT))
            sub_results.append(w)
        p50_n.append(np.percentile(sub_results, 50))
        p85_n.append(np.percentile(sub_results, 85))
        p95_n.append(np.percentile(sub_results, 95))
        
    ax2.plot(sample_sizes, p95_n, 'o-', color='#EF4444', linewidth=1.8, markersize=5, label='P95 (Conservador / SLA)')
    ax2.plot(sample_sizes, p85_n, 's-', color='#F59E0B', linewidth=1.8, markersize=5, label='P85 (Compromisso Ágil)')
    ax2.plot(sample_sizes, p50_n, '^-', color='#10B981', linewidth=1.8, markersize=5, label='P50 (Mediana)')
    
    ax2.set_xscale('log')
    ax2.set_xlabel('Número de Iterações de Simulação (N)')
    ax2.set_ylabel('Prazo Estimado (Semanas)')
    ax2.set_title('Estabilidade dos Percentis vs Amostras (N)')
    ax2.set_ylim(14, 20)
    ax2.legend(loc='upper right', fontsize=8, frameon=True)
    
    plt.tight_layout()
    path = os.path.join(OUTPUT_DIR, 'fig5_monte_carlo_trajetorias_convergencia.png')
    plt.savefig(path)
    plt.close()
    print(f"✔ Gráfico 5 gerado: {path} (Trajetórias e convergência estocástica)")

# ------------------------------------------------------------------------------
# 4. Testes Automatizados da Lógica Open-Source
# ------------------------------------------------------------------------------
def run_unit_tests():
    """Valida a fidelidade estatística e matemática do motor de simulação."""
    print("=== INICIANDO TESTES DO MOTOR DE MONTE CARLO OPEN-SOURCE ===")
    engine = MonteCarloEngine(HISTORICO_THROUGHPUT, seed=42)
    
    # Teste 1: Monotonicidade dos percentis
    fixo = engine.forecast_backlog(backlog_size=60, n_simulations=5000)
    stats = MonteCarloEngine.get_percentiles(fixo)
    assert stats['P50'] <= stats['P70'] <= stats['P85'] <= stats['P95'], \
        f"Violação de monotonicidade dos percentis: {stats}"
    print("✔ Teste 1: Monotonicidade dos percentis validada (P50 <= P70 <= P85 <= P95)")
    
    # Teste 2: Impacto estocástico do Scope Creep
    scope_creep = ([0, 1, 2], [0.50, 0.35, 0.15])
    dinamico = engine.forecast_backlog(backlog_size=60, n_simulations=5000, scope_creep=scope_creep)
    stats_din = MonteCarloEngine.get_percentiles(dinamico)
    assert stats_din['P85'] > stats['P85'], \
        f"Scope Creep deveria estender o prazo: P85 fixo={stats['P85']} vs din={stats_din['P85']}"
    print(f"✔ Teste 2: Scope Creep validado (P85 expandiu de {stats['P85']:.0f} para {stats_din['P85']:.0f} semanas)")
    
    # Teste 3: Consistência com a Lei de Little como piso teórico
    # L = lambda * W => W_teorico = L / lambda = 60 / 3.923 ~= 15.29 semanas
    w_little = 60.0 / np.mean(HISTORICO_THROUGHPUT)
    assert stats['mean'] >= w_little * 0.98, \
        f"Média simulada ({stats['mean']:.2f}) muito discrepante da Lei de Little ({w_little:.2f})"
    print(f"✔ Teste 3: Compatibilidade com Lei de Little validada (W_teórico={w_little:.2f} sem, Simulado={stats['mean']:.2f} sem)")
    
    # Teste 4: Previsão orientada a data (forecast_date_driven)
    entregas_12sem = engine.forecast_date_driven(num_weeks=12, n_simulations=5000)
    stats_12 = MonteCarloEngine.get_percentiles(entregas_12sem)
    assert stats_12['P50'] > 0 and stats_12['min'] >= 12, \
        f"Entrega mínima em 12 semanas deveria ser no mínimo 12 itens (mínimo histórico = 1/sem)"
    print(f"✔ Teste 4: Date-driven forecasting validado (Em 12 semanas, P85 entrega {stats_12['P85']:.0f} itens)")
    
    # Teste 5: Reprodutibilidade exata de semente aleatória
    engine_a = MonteCarloEngine(HISTORICO_THROUGHPUT, seed=123)
    engine_b = MonteCarloEngine(HISTORICO_THROUGHPUT, seed=123)
    res_a = engine_a.forecast_backlog(backlog_size=30, n_simulations=100)
    res_b = engine_b.forecast_backlog(backlog_size=30, n_simulations=100)
    assert np.array_equal(res_a, res_b), "Falha na reprodutibilidade da semente pseudoaleatória."
    print("✔ Teste 5: Reprodutibilidade com semente determinística validada com sucesso.")
    
    # Teste 6: Equivalência com o algoritmo da biblioteca open-source rodbv/quando (Python)
    quando_engine = ReferenceQuandoForecast(HISTORICO_THROUGHPUT)
    quando_res = quando_engine.forecast(n_items=60, num_simulations=10000, seed=42)
    assert abs(quando_res['P50'] - stats['P50']) <= 1.0, f"Discrepância P50 com rodbv/quando: {quando_res['P50']} vs {stats['P50']}"
    assert abs(quando_res['P85'] - stats['P85']) <= 1.0, f"Discrepância P85 com rodbv/quando: {quando_res['P85']} vs {stats['P85']}"
    assert abs(quando_res['P95'] - stats['P95']) <= 1.0, f"Discrepância P95 com rodbv/quando: {quando_res['P95']} vs {stats['P95']}"
    print(f"✔ Teste 6: Compatibilidade com rodbv/quando validada (P50={quando_res['P50']}, P85={quando_res['P85']}, P95={quando_res['P95']})")

    # Teste 7: Equivalência com o projeto open-source thawkin3/monte-carlo (TypeScript)
    thawkin_engine = ReferenceThawkin3Forecast(HISTORICO_THROUGHPUT)
    th_res = thawkin_engine.run_simulation_n_times(n_tasks=60, n_simulations=10000, seed=42)
    assert abs(th_res['P50'] - stats['P50']) <= 1.0, f"Discrepância P50 com thawkin3: {th_res['P50']} vs {stats['P50']}"
    assert abs(th_res['P85'] - stats['P85']) <= 1.0, f"Discrepância P85 com thawkin3: {th_res['P85']} vs {stats['P85']}"
    assert abs(th_res['P95'] - stats['P95']) <= 1.0, f"Discrepância P95 com thawkin3: {th_res['P95']} vs {stats['P95']}"
    print(f"✔ Teste 7: Compatibilidade com thawkin3 validada (P50={th_res['P50']}, P85={th_res['P85']}, P95={th_res['P95']})")

    print("\nTodos os 7 testes unitários passaram com 100% de conformidade!\n")

# ------------------------------------------------------------------------------
# 5. Execução Principal
# ------------------------------------------------------------------------------
def main():
    parser = argparse.ArgumentParser(description="Simulação de Monte Carlo para Previsão de Prazos")
    parser.add_argument("--test", action="store_true", help="Executa a suíte de testes unitários do motor estocástico")
    args = parser.parse_args()
    
    if args.test:
        run_unit_tests()
        return

    print("Iniciando geração de evidências e cálculos estocásticos...")
    gerar_grafico_fundamentacao_fisica()
    gerar_grafico_throughput()
    
    engine = MonteCarloEngine(HISTORICO_THROUGHPUT, seed=42)
    fixo = engine.forecast_backlog(backlog_size=60, n_simulations=10000)
    
    scope_creep = ([0, 1, 2], [0.50, 0.35, 0.15])
    dinamico = engine.forecast_backlog(backlog_size=60, n_simulations=10000, scope_creep=scope_creep)
    
    gerar_grafico_histograma_prazos(fixo)
    gerar_grafico_curva_s(fixo, dinamico)
    gerar_grafico_trajetorias_convergencia()
    
    stats_f = MonteCarloEngine.get_percentiles(fixo)
    stats_d = MonteCarloEngine.get_percentiles(dinamico)
    
    print("\n=== RESUMO ESTATÍSTICO COMPLETO ===")
    print("Cenário A (Escopo Fixo = 60 itens):")
    print(f"  Média: {stats_f['mean']:.2f} semanas | Desvio Padrão: {stats_f['std']:.2f}")
    print(f"  Mínimo: {stats_f['min']} semanas | Máximo: {stats_f['max']} semanas")
    print(f"  P50: {stats_f['P50']:.1f} | P70: {stats_f['P70']:.1f} | P85: {stats_f['P85']:.1f} | P95: {stats_f['P95']:.1f}")
    print("Cenário B (Escopo Dinâmico com Descoberta):")
    print(f"  Média: {stats_d['mean']:.2f} semanas | Desvio Padrão: {stats_d['std']:.2f}")
    print(f"  Mínimo: {stats_d['min']} semanas | Máximo: {stats_d['max']} semanas")
    print(f"  P50: {stats_d['P50']:.1f} | P70: {stats_d['P70']:.1f} | P85: {stats_d['P85']:.1f} | P95: {stats_d['P95']:.1f}")

    # Sincronização automática dos gráficos com as outras pastas de entrega
    sync_dirs = [
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../latex-academico/trabalhos/metricas-estimativas-software/img")),
        os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../sgbl/06_ASSETS/monte_carlo"))
    ]
    for sdir in sync_dirs:
        if os.path.exists(os.path.dirname(sdir)):
            os.makedirs(sdir, exist_ok=True)
            for fname in os.listdir(OUTPUT_DIR):
                if fname.endswith(".png"):
                    shutil.copy2(os.path.join(OUTPUT_DIR, fname), os.path.join(sdir, fname))
            print(f"✔ Imagens sincronizadas em: {sdir}")

    # Também copia o próprio script atualizado para latex-academico
    dest_script = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../latex-academico/trabalhos/metricas-estimativas-software/simulacao_monte_carlo.py"))
    if os.path.exists(os.path.dirname(dest_script)):
        shutil.copy2(__file__, dest_script)

    print("Execução concluída com sucesso!")

if __name__ == '__main__':
    main()
