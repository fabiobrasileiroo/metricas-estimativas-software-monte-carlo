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

### 0. Motor principal em TypeScript (Bun)
```bash
bun install            # dependências (motion, typescript, @types/bun)
bun run simular        # cenários A/B, conferência TCL, DKW e backtest NestJS -> resultados/resultados.{json,js}
bun test               # 15 testes (percentis 16/17/18 e 19/21/23, TCL, DKW, equivalência quando/thawkin3)
bun run typecheck      # tsc --noEmit
bun run vendor         # copia node_modules/motion/dist/motion.js -> vendor/ (slides offline)
uv run scripts/fig6_nestjs.py "$PWD"   # regenera img/fig6_nestjs_backtest.png a partir do JSON
```
Os slides leem `resultados/resultados.js` (window.RESULTADOS); rode `bun run simular` antes de regerar o PDF dos slides.
Dados reais: `dados/nest_prs_humanos.csv` (PRs mergeados de nestjs/nest, 07/11/2025 a 17/11/2026, sem Renovate/Dependabot), coletados com `gh pr list --repo nestjs/nest --state merged`.

### 1. Rodar a Simulação e os Testes em Python (gera as Figuras 1 a 5)
O script possui cabeçalho PEP 723 (gerencia automaticamente `numpy` e `matplotlib`):
```bash
# Executa a simulação de 10.000 iterações e regenera os 4 gráficos PNG em img/
uv run simulacao_monte_carlo.py

# Roda a suíte completa de 7 testes unitários (incluindo testes de equivalência com rodbv/quando e thawkin3)
uv run python simulacao_monte_carlo.py --test
```

### 2. Recompilar o Artigo Acadêmico em LaTeX / ABNT (26 páginas)
O artigo está escrito em `documento.md` (Markdown com frontmatter e fórmulas LaTeX) e é processado pelo motor `doc.py` com Tectonic:
```bash
# Compilar documento.md para metricas-estimativas-software.pdf
python3 /home/fabionote/latex-academico/doc.py gerar /home/fabionote/atividades_academicas/metricas_estimativas_software/documento.md

# O PDF de saída será gerado em:
# metricas-estimativas-software.pdf (26 páginas, ABNT NBR 14724/6023/6028)
```

### 3. Visualizar e Recompilar os Slides de Apresentação
Os slides foram construídos em HTML/CSS autônomo e depois renderizados em PDF 16:9 (1440×810):
```bash
# Para visualizar os slides no navegador:
xdg-open apresentacao_simulacao_monte_carlo.html

# Os slides precisam de HTTP para carregar vendor/motion.js e resultados/resultados.js no preview do app;
# abrindo direto do disco (xdg-open) também funcionam, pois são <script> clássicos.
python3 -m http.server 5179
# PDF (17 slides, estado final das animações):
google-chrome-stable --headless=new --disable-gpu --no-pdf-header-footer \
  --run-all-compositor-stages-before-draw --virtual-time-budget=15000 \
  --print-to-pdf=apresentacao_simulacao_monte_carlo.pdf \
  http://localhost:5179/apresentacao_simulacao_monte_carlo.html
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

### Slides (versão atual, 17 slides)
- Fonte decidida por JS frase a frase (título + ressalva): sem acento -> Gaegu Bold; com acento -> Itim. Corpo em Nunito, código em JetBrains Mono. Nunca tirar acento de palavra para forçar Gaegu: reescreva a frase.
- Animações com Motion 14 (build UMD em `vendor/motion.js`, global `Motion`): entrada de título/ressalva, `[data-anim]` em cascata, avatar com mola, contadores `[data-count]`, gráficos SVG/canvas desenhados a partir de `resultados.js`. Tecla R repete; `#N` na URL abre o slide N. No `@media print` tudo fica no estado final.

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

4. **Resultados Matemáticos Factualmente Obtidos (motor TS, semente 42; médias diferem do Python na 2ª casa, percentis idênticos):**
   - Cenário A TS: média 15,72 ± 1,48 | Cenário B TS: média 18,77 ± 2,16.
   - TCL de renovação: D ≈ N(B/μ + 1/2, Bσ²/μ³) com σ² populacional. A: 15,79 ± 1,46 (P85 17,31). B (μ-λ=3,27; σ²+σλ²=2,75): 18,83 ± 2,14.
   - DKW: N=10.000 -> ±1,36 pp; N=1.000 -> ±4,29 pp; ±1 pp exige 18.445 iterações.
   - Quantos em 12 semanas: P85 >= 42 itens, P50 47, P95 >= 39.
   - NestJS: 572 PRs humanos em 52 semanas (μ=11,00, σ=15,02, 0–58). Mudança de regime na semana 44 (4,98 -> 39,78 PRs/sem). Backtest rolante (treino 26, horizonte 6): período estável (12 janelas) P85 cumprido 83,3%, mediana 50,0%, média×6 41,7%; todas as 21 janelas: 90,5% / 71,4% / 66,7% (inflado pela mudança de regime).
   - Valores do Python (abaixo) seguem válidos para as Figuras 1–5:
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
├── simulacao_monte_carlo.py                     # Motor Python original (gera Figuras 1–5)
├── src/monte-carlo.ts                           # Motor TypeScript (principal) + TCL, DKW, throughput semanal
├── src/estudo.ts                                # Cenários, conferência analítica e backtest NestJS
├── tests/monte-carlo.test.ts                    # 15 testes bun
├── dados/nest_prs_humanos.csv                   # PRs mergeados do nestjs/nest (sem bots)
├── resultados/resultados.{json,js}              # Saída do estudo (o .js alimenta os slides)
├── scripts/fig6_nestjs.py                       # Figura 6 (backtest NestJS)
├── vendor/motion.js                             # Motion 14 UMD para animações offline
├── img/                                         # Gráficos de alta resolução para o PDF e slides
│   ├── fig1_fisica_area_monte_carlo.png         # Método de rejeição (área/pi) e erro O(1/√N)
│   ├── fig2_throughput_historico.png            # Histograma do throughput histórico
│   ├── fig3_monte_carlo_prazos_histograma.png   # Histograma de probabilidades P50/P85/P95
│   ├── fig4_curva_s_cdf_risco.png               # Curva S cumulativa (Escopo Fixo vs Dinâmico)
│   ├── fig5_monte_carlo_trajetorias_convergencia.png # 80 trajetórias de burn-down, cone de incerteza P15-P85 e convergência assintótica
│   └── fig6_nestjs_backtest.png                 # Throughput real do nestjs/nest e backtest rolante
├── assets/                                      # Avatares chibi em giz de cera
├── fonts/                                       # Fontes TTF locais (Itim e Gaegu)
└── design_system/                               # Tokens CSS/JSON do Fábio
```
