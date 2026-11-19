# Contexto do Projeto para Claude Code: Simulação de Monte Carlo (Engenharia de Software)

> **Arquivo de Onboarding Rápido (`CLAUDE.md`)**  
> Este repositório contém a atividade acadêmica da **Unidade VI (Métricas e Estimativas de Software / Modelo GQM)** do curso de **Bacharelado em Engenharia de Software** do **CEUNI FAMETRO**.
>
> - **Tema Principal Escolhido (Tema 7):** Simulação de Monte Carlo para Previsão de Prazos de Projetos de Software.
> - **Docente:** Prof. Me. Alexsand Farias de Souza
> - **Autor / Acadêmico:** Fábio Henrique Mendes Brasileiro ([@fabiobrasileiroo](https://github.com/fabiobrasileiroo))
> - **Repositório Privado GitHub:** `https://github.com/fabiobrasileiroo/metricas-estimativas-software-monte-carlo`

---

## 🚀 Como Executar e Compilar Tudo Rapidamente

### 1. Rodar a Simulação e os Testes em Python
O script possui cabeçalho PEP 723 (gerencia automaticamente `numpy` e `matplotlib`):
```bash
# Executa a simulação de 10.000 iterações e regenera os 4 gráficos PNG em img/
uv run simulacao_monte_carlo.py

# Roda a suíte completa de 7 testes unitários (incluindo testes de equivalência com rodbv/quando e thawkin3)
uv run python simulacao_monte_carlo.py --test
```

### 2. Recompilar o Artigo Acadêmico em LaTeX / ABNT (17 páginas)
O artigo está escrito em `documento.md` (Markdown com frontmatter e fórmulas LaTeX) e é processado pelo motor `doc.py` com Tectonic:
```bash
# Compilar documento.md para metricas-estimativas-software.pdf
python3 /home/fabionote/latex-academico/doc.py gerar /home/fabionote/atividades_academicas/metricas_estimativas_software/documento.md

# O PDF de saída será gerado em:
# metricas-estimativas-software.pdf (17 páginas estritamente em normas ABNT NBR 14724/6023/6028)
```

### 3. Visualizar e Recompilar os Slides de Apresentação
Os slides foram construídos em HTML/CSS autônomo e depois renderizados em PDF 16:9 (1440×810):
```bash
# Para visualizar os slides no navegador:
xdg-open apresentacao_simulacao_monte_carlo.html

# Para recompilar o PDF dos slides a partir do HTML via Chromium:
chromium --headless --disable-gpu --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=5000 \
  --print-to-pdf=apresentacao_simulacao_monte_carlo.pdf \
  apresentacao_simulacao_monte_carlo.html
```

### 4. Atualizar o Repositório Privado no GitHub
```bash
git add .
git commit -m "refactor: refinos no artigo e design system dos slides"
git push origin main
```

---

## 🎨 Guia de Design System dos Slides ("Fábio Brasileiro" / Estilo Lauren Tan)

Os slides foram desenvolvidos inspirando-se nas palestras da **Lauren Tan** adaptadas à **identidade visual pessoal "Fábio Brasileiro"** (extraída de `Fábio_Brasileiro.zip`):

### A Fórmula Visual
1. **Afirmativa em minúsculas:** Texto em cor de tinta escura (`--ink: #1c1917`), fonte de mão arredondada (`Itim` ou `Gaegu-Bold`).
2. **Ressalva irônica entre parênteses:** **SEMPRE em ciano** (`--cyan: #12a7c4`), nunca rosa, posicionada logo abaixo da afirmativa.
3. **Fundo branco puro:** (`#ffffff`), sem poluição visual.
4. **Chibi em giz de cera:** O personagem Fábio posicionado no canto inferior/lateral em 4 poses conceituais:
   - `assets/avatar-giz-codando.jpg`: Para slides de código, algoritmos, simulação e fórmulas.
   - `assets/avatar-giz-joinha.jpg`: Para conclusões de sucesso, compromisso P85 e alinhamento com stakeholders.
   - `assets/avatar-giz-acai.jpg`: Para deboche amigável de Story Points, analogias do mundo real e relaxamento.
   - `assets/avatar-giz-oi.jpg`: Para abertura e agradecimentos.

### Paleta de Tokens (`design_system/tokens.css`):
```css
--ink: #1c1917;        /* Texto principal */
--cyan: #12a7c4;       /* Ressalva irônica entre parênteses e destaques */
--branco: #ffffff;     /* Fundo dos slides */
--paper: #fbfaf7;      /* Fundo suave de cards */
--line: #e7e2da;       /* Bordas finas de tabelas e métricas */
--muted: #78716c;      /* Textos explicativos e notas */
--acai: #4a1d5c;       /* Roxo de contraste da tigela de açaí */
--camiseta: #1f2b47;   /* Azul marinho */
```

---

## 🧠 Núcleo Teórico e Técnico (O que não pode faltar)

Se for refinar o texto ou os slides, mantenha a coerência técnica:

1. **Protagonismo Absoluto do Tema 7 (Simulação de Monte Carlo):**
   - **Origem Física:** Criado por Stanislaw Ulam, John von Neumann e Nicholas Metropolis no Projeto Manhattan (Los Alamos, 1946–1949). Batizado em homenagem ao Cassino de Monte Carlo (tio de Ulam que jogava na roleta).
   - **Analogias Didáticas Clássicas:**
     - *Cálculo da área de um lago irregular:* sorteio aleatório de coordenadas em um retângulo envolvente; razão entre acertos dentro da água e total converge para a área pela Lei Forte dos Grandes Números ($O(1/\sqrt{N})$).
     - *Cassino e House Edge:* cada aposta individual é caótica/imprevisível, mas a agregação de milhares de jogadas converge inevitavelmente para a expectativa estocástica matemática.
   - **Aplicação no Software:** Drenagem de backlog estocástica através de *bootstrapping* não paramétrico sobre o histórico de *Throughput* semanal real (amostragem com reposição).

2. **Crítica e Contraste com os Outros Temas (Sem roubar os temas dos colegas):**
   - **Story Points e Velocity (Temas 1 e 2):** Não têm base física/estatística. Sofrem do *The Flaw of Averages* de Sam Savage ($E[f(X)] \neq f(E[X])$). Vulneráveis à **Lei de Goodhart** (quando a métrica vira meta, a equipe inflaciona os pontos sem entregar mais valor). Cadeia de 10 dependências com 75% de confiança individual resulta em apenas $0,75^{10} \approx 5,63\%$ de chance de entrega conjunta.
   - **Throughput, WIP, Cycle Time e Lead Time (Temas 3 e 4):** São as variáveis de entrada do Monte Carlo, regidas pela **Lei de Little** ($WIP = Throughput \times CycleTime$).
   - **Cumulative Flow Diagram - CFD (Tema 5):** Ferramenta visual que evidencia gargalos e variabilidade de WIP.
   - **Governança e Modelo GQM (Tema 8):** O trabalho estrutura a medição em **Meta Conceitual** (Prever prazos com 85% de confiança), **Questões Operacionais** (Qual a vazão? Qual o risco de atraso?) e **Métricas Quantitativas** (Throughput histórico, percentis P50/P85/P95, taxa de *Scope Creep*).

3. **Projetos Open Source de Referência (Auditados e Comparados):**
   - [`rodbv/quando`](https://github.com/rodbv/quando) (Python): Cálculo de Service Level Expectations (SLE) e Monte Carlo a partir de CSV com datas de início e fim.
   - [`thawkin3/monte-carlo-simulation-project-timeline-estimator`](https://github.com/thawkin3/monte-carlo-simulation-project-timeline-estimator) (TypeScript): Simulador interativo via web que desconta entregas aleatórias do backlog restante.

4. **Resultados Matemáticos Factualmente Obtidos:**
   - Amostra histórica: 26 semanas, 102 itens entregues ($\mu = 3,92$ itens/semana, $\sigma = 1,49$).
   - Backlog alvo: 60 itens.
   - **Cenário A (Escopo Fixo — 10.000 iterações):**
     - Média: 15,73 semanas | Desvio: 1,50 semanas | Mínimo: 11 | Máximo: 22
     - P50 (Mediana): 16 semanas (cara ou coroa — 50% de risco)
     - P85 (Compromisso Ágil Recomendado): 17 semanas (85% de certeza)
     - P95 (Conservador / SLA): 18 semanas (95% de certeza)
   - **Cenário B (Escopo Dinâmico com Scope Creep de +0,65 itens/semana):**
     - Média: 18,85 semanas | Desvio: 2,17 semanas | Mínimo: 12 | Máximo: 28
     - P50: 19 semanas | P85: 21 semanas (+4 semanas de impacto) | P95: 23 semanas

---

## 📁 Mapa Completo de Arquivos

```
/home/fabionote/atividades_academicas/metricas_estimativas_software/
├── CLAUDE.md                                    # ESTE ARQUIVO (leitura rápida para o Claude Code)
├── README.md                                    # README detalhado do repositório
├── documento.md                                 # Artigo acadêmico ABNT (fonte editável)
├── metricas-estimativas-software.pdf            # PDF do artigo pronto para o Google Classroom
├── apresentacao_simulacao_monte_carlo.html      # Slides interativos (Lauren Tan / Fábio Brasileiro)
├── apresentacao_simulacao_monte_carlo.pdf       # PDF dos slides pronto para o Google Classroom
├── simulacao_monte_carlo.py                     # Algoritmo de bootstrapping e testes pytest
├── img/                                         # Gráficos de alta resolução para o PDF e slides
│   ├── fig1_fisica_area_monte_carlo.png         # Método de rejeição (área/pi) e erro O(1/√N)
│   ├── fig2_throughput_historico.png            # Histograma do throughput histórico
│   ├── fig3_monte_carlo_prazos_histograma.png   # Histograma de probabilidades P50/P85/P95
│   ├── fig4_curva_s_cdf_risco.png               # Curva S cumulativa (Escopo Fixo vs Dinâmico)
│   └── fig5_monte_carlo_trajetorias_convergencia.png # 80 trajetórias de burn-down, cone de incerteza P15-P85 e convergência assintótica
├── assets/                                      # Avatares chibi em giz de cera
├── fonts/                                       # Fontes TTF locais (Itim e Gaegu)
└── design_system/                               # Tokens CSS/JSON do Fábio
```
