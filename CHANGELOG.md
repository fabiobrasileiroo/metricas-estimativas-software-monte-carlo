# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.1.0/).

## [Não lançado]

### Adicionado
- Motor de Monte Carlo em TypeScript (`src/monte-carlo.ts`, Bun) com semente fixa, pergunta inversa ("quantos itens até a data?"), aproximação analítica pelo TCL de renovação, erro padrão e margem DKW.
- Estudo `src/estudo.ts` que grava `resultados/resultados.json` e `resultados.js`, usado pelos slides.
- 15 testes `bun test`, incluindo equivalência com a lógica de `rodbv/quando` e `thawkin3`.
- Estudo de caso 2 com dados reais do `nestjs/nest` (572 PRs humanos, 52 semanas) e backtest rolante; Figura 6.
- Artigo: seções de aproximação analítica (TCL), precisão da simulação (DKW), curadoria de oito repositórios open-source e estudo NestJS; 8 novas referências.
- Slides refeitos (17) com animações Motion, gráficos vivos em SVG/canvas e regra automática de fonte Gaegu/Itim.

### Alterado
- Tabela de resultados do artigo passa a citar os valores do motor TypeScript (percentis idênticos ao Python).
- Seção de validação reescrita: os testes reimplementam a lógica das bibliotecas de referência, em vez de afirmar que as importam.

### Decisões
- Build UMD do Motion em `vendor/` em vez de ESM via CDN: módulos ES não carregam via `file://` e a apresentação precisa funcionar offline.
- PRs de Renovate e Dependabot excluídos do throughput (56% dos merges), pois não medem a capacidade da equipe.
- Backtest reportado separando o período estável da mudança de regime da semana 44, para não inflar a taxa de acerto.
