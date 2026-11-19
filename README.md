# Simulação de Monte Carlo para Previsão de Prazos de Software

> **Governança da Medição, Modelo GQM e Análise Estocástica na Engenharia de Software**  
> Centro Universitário FAMETRO (CEUNI FAMETRO) • Turma ENGS231N01  
> Disciplina: Engenharia de Software • Docente: Prof. Me. Alexsand Farias de Souza  
> Autor: Fábio Henrique Mendes Brasileiro ([@fabiobrasileiroo](https://github.com/fabiobrasileiroo))

---

## 🎯 Visão Geral & Tema Central (Tema 7)

Este repositório consolida o projeto acadêmico e prático de **Simulação de Monte Carlo para Previsão de Prazos de Software**, desenvolvido no âmbito da Unidade VI (Governança da Medição, Modelo GQM e Análise de Dados) em conformidade com a norma **ISO/IEC/IEEE 15939**.

Enquanto métodos tradicionais recorrem a estimativas determinísticas (como soma de horas ou pontuações subjetivas de *Story Points* no *Planning Poker*), este trabalho adota a **previsão probabilística não paramétrica** baseada na vazão histórica real entregue (*Throughput*).

```
Histórico Factual de Throughput (26 semanas, 102 itens)
                           │
                           ▼
          Algoritmo de Bootstrapping Não Paramétrico
                (10.000 iterações estocásticas)
                           │
             ┌─────────────┴─────────────┐
             ▼                           ▼
    Histograma de Densidade       Curva S Cumulativa (CDF)
   P50: 16 sem | P85: 17 sem      Impacto do Scope Creep
   P95: 18 sem (SLA rigoroso)     P85: 17 sem ➔ 21 sem (+4 sem)
```

---

## 📦 Estrutura do Repositório

```
.
├── documento.md                                 # Artigo acadêmico ABNT em Markdown
├── metricas-estimativas-software.pdf            # Artigo final compilado (18 páginas ABNT completas)
├── apresentacao_simulacao_monte_carlo.html      # Slides interativos (Design Lauren Tan / Fábio Brasileiro)
├── apresentacao_simulacao_monte_carlo.pdf       # Slides compilados em PDF 16:9 (11 páginas)
├── simulacao_monte_carlo.py                     # Motor de simulação e suíte de 7 testes unitários
├── img/                                         # Gráficos em alta resolução (300 DPI)
│   ├── fig1_fisica_area_monte_carlo.png         # Amostragem por rejeição e convergência O(1/√N)
│   ├── fig2_throughput_historico.png            # Distribuição semanal de 26 semanas (102 itens)
│   ├── fig3_monte_carlo_prazos_histograma.png   # Histograma de 10.000 iterações com P50, P85 e P95
│   ├── fig4_curva_s_cdf_risco.png               # Curva S comparativa (Escopo Fixo vs Scope Creep)
│   └── fig5_monte_carlo_trajetorias_convergencia.png # Trajetórias estocásticas e cone de incerteza
├── assets/                                      # Avatares chibi em giz de cera (Design System Fábio)
│   ├── avatar-giz-acai.jpg                      # Pose açaí (deboche de Story Points / humor)
│   ├── avatar-giz-codando.jpg                   # Pose codando (código open-source e matemática)
│   ├── avatar-giz-joinha.jpg                    # Pose joinha (resultados P85 / SLAs)
│   └── avatar-giz-oi.jpg                        # Pose oi (abertura e encerramento)
├── fonts/                                       # Fontes tipográficas locais
│   ├── Gaegu-Bold.ttf                           # Primária para títulos e ressalvas sem acento
│   └── Itim-Regular.ttf                         # Secundária com suporte a acentos e assinatura
└── design_system/                               # Tokens CSS/JSON e especificações da identidade
    ├── DESIGN_SYSTEM_FABIO.md
    ├── tokens.css
    └── tokens.json
```

---

## 🧪 Referência Open-Source e Validação Cruzada

A lógica computacional foi validada contra duas das principais implementações de código aberto disponíveis no ecossistema de engenharia ágil:

1. **[rodbv/quando](https://github.com/rodbv/quando)** (Python): Biblioteca open-source para cálculo de *Service Level Expectations* (SLE) e previsibilidade com dados de Throughput.
2. **[thawkin3/monte-carlo-simulation-project-timeline-estimator](https://github.com/thawkin3/monte-carlo-simulation-project-timeline-estimator)** (TypeScript): Estimador estocástico web/CLI baseado em fluxo empírico.
3. **[FocusedObjective.Resources](https://github.com/FocusedObjective)** (Troy Magennis): Modelos quantitativos de referência adotados pela *Agile Alliance*.

### Comparativo de Validação Cruzada (10.000 Rodadas)

| Métrica / SLE | Motor Próprio (`simulacao_monte_carlo.py`) | Biblioteca `rodbv/quando` | Algoritmo `thawkin3` | Convergência |
| :--- | :---: | :---: | :---: | :---: |
| **Percentil 50 (P50)** | 16 semanas | 16 semanas | 16 semanas | **100% (exato)** |
| **Percentil 85 (P85)** | 17 semanas | 17 semanas | 17 semanas | **100% (exato)** |
| **Percentil 95 (P95)** | 18 semanas | 18 semanas | 18 semanas | **100% (exato)** |
| **Tipo de Amostragem** | Bootstrapping c/ reposição | Bootstrapping c/ reposição | Amostragem iterativa | **Equivalente** |

### O Algoritmo de Bootstrapping Não Paramétrico

```python
def forecast_backlog(throughput_history, backlog_size=60, runs=10000, scope_creep=None):
    weeks_to_finish = np.zeros(runs, dtype=int)
    for i in range(runs):
        remaining, weeks = backlog_size, 0
        while remaining > 0:
            weeks += 1
            remaining -= random.choice(throughput_history) # Amostragem com reposição
            if scope_creep:
                remaining += random.choice(scope_creep[0], p=scope_creep[1])
        weeks_to_finish[i] = weeks
    return weeks_to_finish
```

### Suíte de Testes Automatizados

O script [`simulacao_monte_carlo.py`](simulacao_monte_carlo.py) inclui uma bateria de **7 testes unitários** validando a integridade estatística e compatibilidade open-source:

```bash
uv run simulacao_monte_carlo.py --test
```

- **Teste 1:** Monotonicidade dos percentis ($P_{50} \le P_{70} \le P_{85} \le P_{95}$).
- **Teste 2:** Expansão estocástica de prazo sob *Scope Creep* ($P_{85}(\text{creep}) > P_{85}(\text{fixo})$).
- **Teste 3:** Compatibilidade com o piso teórico da Lei de Little ($W_{\text{Little}} = L / \lambda = 15,29$ semanas).
- **Teste 4:** Previsão orientada a data (*Date-driven forecasting* para 12 semanas).
- **Teste 5:** Reprodutibilidade estrita através de sementes pseudoaleatórias controladas.
- **Teste 6:** Compatibilidade estocástica com a biblioteca open-source `rodbv/quando` (Python).
- **Teste 7:** Compatibilidade de percentis com o projeto open-source `thawkin3` (TypeScript).

---

## 🎨 Apresentação Visual no Estilo Lauren Tan / Fábio Brasileiro

Os slides foram desenvolvidos adotando a estética consagrada pela palestrante internacional **Lauren Tan** (*poteto*), combinada à identidade visual pessoal **Fábio Brasileiro**:

- **Fórmula de Título:** Afirmação forte em minúsculas com cor de tinta `ink` (`#1c1917`) + ressalva irônica em ciano `cyan` (`#12a7c4`) entre parênteses.
- **Tipografia:** Fonte primária **Gaegu Bold** para frases puramente ASCII (sem acentos) e **Itim** para frases com acentuação e assinatura do autor.
- **Minimalismo & Respiração:** Fundo branco puro, bordas suaves de 1px e ampla respiração visual.
- **Personagem Chibi em Giz de Cera:** Quatro poses recortadas com `mix-blend-mode: multiply` que se fundem perfeitamente ao fundo branco.
- **Atalhos da Apresentação Interativa:**
  - `←` / `→` ou `Espaço`: Navegação entre slides
  - `F`: Alternar tela cheia (*Fullscreen*)
  - `O`: Visão geral em grade (*Overview grid*)
  - `P`: Imprimir ou salvar diretamente em PDF 16:9

---

## 📊 Síntese dos Resultados Experimentais

| Métrica / Parâmetro | Cenário A (Escopo Fixo = 60 itens) | Cenário B (Scope Creep = +0,65 itens/sem) | Variação Absoluta |
| :--- | :---: | :---: | :---: |
| **Amostra Histórica** | 26 semanas (102 itens) | 26 semanas (102 itens) | — |
| **Média Semanal Real** | 3,92 itens/sem (DP: 1,49) | 3,92 itens/sem (DP: 1,49) | — |
| **Média Simulada de Prazo** | 15,73 semanas | 18,76 semanas | +3,03 semanas |
| **P50 (Mediana / Cara ou Coroa)** | 16 semanas | 19 semanas | +3 semanas |
| **P70** | 16 semanas | 20 semanas | +4 semanas |
| **P85 (Compromisso Ágil)** | **17 semanas** | **21 semanas** | **+4 semanas** |
| **P95 (Conservador / SLA)** | **18 semanas** | **22 semanas** | **+4 semanas** |
| **Mínimo / Máximo** | 11 a 22 semanas | 13 a 32 semanas | +2 a +10 semanas |

> **Decisão Gerencial:** Assumir o P50 (16 semanas) impõe um risco de atraso de 50%. A governança da medição recomenda pactuar compromissos de entrega no **percentil P85 (17 semanas)**, reservando apenas 15% de incerteza residual.

---

## 🔄 Contraste com os Outros Temas da Disciplina

| Tema da Disciplina | Abordagem Convencional | Por que Quebra? | Resposta com Monte Carlo (Tema 7) |
| :--- | :--- | :--- | :--- |
| **Story Points & Planning Poker** | Pontuação relativa por consenso | Sujeito à Lei de Goodhart e especulação subjetiva | **Throughput factual:** Contagem de itens entregues na *Definition of Done*. |
| **Velocity** | Média aritmética de pontos por sprint | *Flaw of Averages*: a média esconde a variância | **Curva Cumulativa:** Distribuição com percentis de risco auditáveis. |
| **CFD (Cumulative Flow Diagram)** | Visualização gráfica de WIP acumulado | Ferramenta estritamente diagnóstica do passado | **Projeção Futura:** Alimenta o bootstrapping com a taxa de vazão extraída do CFD. |
| **Lei de Little ($L = \lambda W$)** | Fórmula analítica de equilíbrio | Assume fluxo perfeitamente contínuo e estável | **Modelo Estocástico:** Simula a turbulência e filas quando o sistema oscila. |
| **Lead Time / Cycle Time** | Duração temporal de um item individual | Foco no micro-nível de uma tarefa | **Macro-nível:** Responde à pergunta central de negócio: *"Quando a release inteira estará pronta?"* |

---

## 🟦 Motor TypeScript e Teste com Projeto Real (NestJS)

O motor principal agora está em TypeScript (`src/monte-carlo.ts`, executado com Bun). Ele reproduz os percentis do Python (16/17/18 e 19/21/23 semanas) e acrescenta:

- **Conferência analítica:** aproximação normal do Teorema Central do Limite para processos de renovação, `D ≈ N(B/μ + 1/2, Bσ²/μ³)`, que bate com a simulação em menos de 0,1 semana.
- **Precisão da simulação:** desigualdade DKW, que limita o erro da Curva S a ±1,36 ponto percentual com 10.000 iterações.
- **Pergunta inversa:** quantos itens cabem em 12 semanas (P85 ≥ 42 itens).
- **Backtest com dados reais:** 572 PRs humanos mergeados do `nestjs/nest` em 52 semanas. No período estável, o compromisso P85 foi cumprido em 83,3% das janelas, a mediana em 50,0% e "média × semanas" em 41,7%.

```bash
bun install
bun run simular   # grava resultados/resultados.json e .js (usado pelos slides)
bun test          # 15 testes
```

📖 **Roteiro e guia de estudo de cada slide** (incluindo o passo a passo do painel de debug): [GUIA_APRESENTACAO.md](GUIA_APRESENTACAO.md)

## 🚀 Como Executar Localmente

### 1. Pré-requisitos

- Python 3.10+ com gerenciador [`uv`](https://docs.astral.sh/uv/) instalado.
- Sistema Linux/macOS/Windows.

### 2. Rodar a Simulação e Gerar Gráficos

```bash
# Executa a simulação estocástica completa de 10.000 iterações e regenera os 5 gráficos PNG
uv run simulacao_monte_carlo.py

# Executa os 7 testes unitários de conformidade estatística e benchmark open-source
uv run simulacao_monte_carlo.py --test
```

### 3. Visualizar os Slides

Basta abrir o arquivo [`apresentacao_simulacao_monte_carlo.html`](apresentacao_simulacao_monte_carlo.html) em qualquer navegador moderno. Para salvar em PDF, pressione `P` ou utilize o Chromium em modo headless:

```bash
chromium --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=apresentacao_simulacao_monte_carlo.pdf file://$(pwd)/apresentacao_simulacao_monte_carlo.html
```

---

## 📜 Licença e Direitos

Trabalho acadêmico submetido para avaliação curricular no curso de Bacharelado em Engenharia de Software do **Centro Universitário FAMETRO**.  
Código e dados disponibilizados sob licença MIT.
