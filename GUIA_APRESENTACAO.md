# Guia de estudo e roteiro da apresentação

Material de apoio para apresentar o Tema 7 (Simulação de Monte Carlo para previsão de prazos). Para cada slide: o que aparece na tela, o que falar e as perguntas que o professor pode fazer. Tempo total sugerido: 15 a 18 minutos.

Atalhos durante a apresentação: setas ou clique avançam, `R` repete a animação do slide, `F` entra em tela cheia (só o slide fica visível), `#7` no fim do endereço abre direto o slide 7.

Todos os números vêm de `bun run simular` (arquivo `resultados/resultados.json`) e do artigo.

---

## Slide 1 · previsão de prazos com monte carlo

**Na tela:** contadores 10.000 (futuros simulados), 26 (semanas de histórico), 572 (PRs reais do NestJS).

**Fala:** "Em vez de perguntar à equipe quanto tempo cada tarefa vai levar, eu uso o que ela já entregou para simular dez mil futuros possíveis. A resposta deixa de ser uma data e passa a ser uma data com probabilidade. E eu testei isso num projeto real, o NestJS."

## Slide 2 · quando fica pronto?

**Na tela:** três respostas para a mesma pergunta; a última, destacada, é "17 semanas, com 85% de chance".

**Fala:** "As duas primeiras respostas são as que a gente dá no dia a dia. A terceira é o que o Monte Carlo entrega: prazo mais o risco declarado."

## Slide 3 · a média é uma ilusão

**Na tela:** dez blocos de 75% que vão escurecendo; o contador cai de 75% até 5,6%.

**A conta:** se cada tarefa tem 75% de chance de sair no prazo e as dez estão em sequência, a chance de todas saírem é 0,75 multiplicado por ele mesmo dez vezes: 0,75¹⁰ ≈ 0,0563, ou seja, 5,63%.

**Fala:** "Cada estimativa parece segura sozinha, mas a cadeia inteira tem quase 95% de chance de atrasar. Isso é o *Flaw of Averages* do Sam Savage: planejar com médias atrasa por construção."

**Pergunta provável:** "E se as tarefas não forem dependentes?" Resposta: aí a conta muda, mas o prazo total continua sendo uma soma de variáveis incertas, e a média sozinha continua escondendo o risco. O Monte Carlo trata os dois casos sem precisar escolher uma fórmula.

## Slide 4 · do cassino ao software

**Na tela:** pontos caindo num quadrado; os que caem dentro do quarto de círculo ficam ciano. A estimativa de π vai se aproximando de 3,14.

**A ideia:** a área do quarto de círculo de raio 1 é π/4. Se eu sorteio pontos uniformes no quadrado 1×1, a fração que cai dentro do círculo tende a π/4. Multiplicando por 4, tenho π. O erro diminui na proporção de 1/√N: para errar 10 vezes menos, preciso de 100 vezes mais pontos.

**Fala:** "É o mesmo raciocínio que Ulam, von Neumann e Metropolis usaram em Los Alamos em 1946: quando a conta exata é difícil demais, sorteie muitas vezes e conte. O nome vem do cassino de Mônaco."

## Slide 5 · meça com propósito

**Na tela:** a árvore GQM: uma meta, três perguntas, três métricas.

**Fala:** "Antes de medir, defini para que serve a medição. Meta: prever o prazo da release com 85% de confiança. Perguntas: quanto a equipe entrega, qual a chance de entregar até cada semana, quanto o escopo novo atrasa. Isso conversa com o Tema 8 e com a ISO/IEC/IEEE 15939."

## Slide 6 · conte itens concluídos

**Na tela:** barras das 26 semanas (102 itens), com a linha da média em 3,92.

**Fala:** "A entrada da simulação é só isto: quantos itens ficaram prontos em cada semana. Não tem estimativa, não tem ponto. Variou de 1 a 7. Essa variação é justamente o que a simulação aproveita."

## Slide 7 · leia o código-fonte (o painel de debug)

Este é o slide central da parte técnica. O painel à direita **executa de verdade** a primeira iteração do motor, com a mesma semente do arquivo `src/monte-carlo.ts`. Os valores na tela são os mesmos que o programa gera, não uma ilustração.

### O que cada variável do painel significa

| Variável | Significado |
| --- | --- |
| `r` | Número da iteração, ou seja, qual dos 10.000 futuros está sendo simulado. |
| `semanas` | Quantas semanas já se passaram neste futuro. |
| `sorteado` | Quantos itens a equipe "entregou" nesta semana simulada. É uma semana do histórico, escolhida ao acaso. |
| `restante` | Quanto falta do backlog de 60 itens. A barra ciano mostra isso. |
| `historico[26]` | As 26 semanas reais. A que acende é a sorteada. |
| `resultados` | Lista com o total de semanas de cada futuro já simulado. |

### A primeira iteração, semana a semana

| Semana simulada | Semana do histórico sorteada | Itens entregues | Restante |
| --- | --- | --- | --- |
| 1 | 16 | 3 | 57 |
| 2 | 12 | 6 | 51 |
| 3 | 23 | 6 | 45 |
| 4 | 18 | 4 | 41 |
| 5 | 5 | 4 | 37 |
| 6 | 14 | 5 | 32 |
| 7 | 8 | 1 | 31 |
| 8 | 17 | 7 | 24 |
| 9 | 23 | 6 | 18 |
| 10 | 13 | 2 | 16 |
| 11 | 7 | 3 | 13 |
| 12 | 23 | 6 | 7 |
| 13 | 20 | 5 | 2 |
| 14 | 8 | 1 | 1 |
| 15 | 6 | 6 | -5 |

O `restante` ficou negativo na semana 15, então o laço `while (restante > 0)` termina e o programa guarda **15** em `resultados`. Esse futuro terminou em 15 semanas.

Três coisas para apontar na tela:

1. **Sorteio com reposição:** a semana 23 do histórico saiu três vezes (semanas simuladas 3, 9 e 12) e a semana 8 saiu duas. Cada sorteio é independente, como tirar uma carta e devolver ao baralho.
2. **Futuro "sortudo":** nesse futuro a média foi 65 ÷ 15 ≈ 4,3 itens por semana, acima da média histórica de 3,92. Outros futuros saem azarados. É essa variação que gera a distribuição.
3. **Sem distribuição inventada:** o código nunca assume curva normal ou qualquer outra. Ele só reaproveita semanas que aconteceram.

### Depois da primeira iteração

O painel acelera: as próximas iterações dão 17, 15, 17, 18, 17, 16, 15… Depois o `r` dispara até 10.000. No fim, ordenando os 10.000 resultados:

- **P50 = 16 semanas:** pelo menos metade dos futuros terminou até a semana 16 (na verdade 71,7%, porque as semanas são inteiras; veja o slide 9).
- **P85 = 17 semanas:** pelo menos 85% terminaram até a semana 17 (89,0%). É o compromisso recomendado.
- **P95 = 18 semanas:** pelo menos 95% terminaram até a semana 18 (96,5%). Use quando há multa contratual.

**Fala:** "O algoritmo cabe nessas linhas. O painel ao lado está rodando o código de verdade, com a mesma semente do programa. Repara que a semana 23 saiu três vezes: isso é o sorteio com reposição. Esse futuro terminou em 15 semanas. Repetindo isso dez mil vezes, eu ordeno os resultados e leio os percentis."

**Perguntas prováveis:**

- *"Por que semente fixa?"* Para o resultado ser reprodutível e auditável: qualquer pessoa que rodar o código obtém os mesmos números, que é uma exigência da governança da medição.
- *"Mudando a semente muda o resultado?"* As médias mudam na segunda casa decimal, mas os percentis não. O script Python usa outro gerador e chega aos mesmos 16/17/18.
- *"Por que TypeScript?"* É a linguagem que eu domino. A lógica é a mesma do `rodbv/quando` (Python) e do `thawkin3` (TypeScript), e os testes conferem essa equivalência.

## Slide 8 · um futuro por linha

**Na tela:** 60 trajetórias de burn-down se desenhando; os pontos ciano empilham na semana em que cada uma zerou.

**Fala:** "Cada linha é um futuro como o do slide anterior. Nenhuma termina exatamente na mesma semana. Os pontos empilhados já formam o histograma do próximo slide. E isso conversa com o Tema 6: cada trajetória é um burndown possível."

## Slide 9 · p50 é cara ou coroa

**Na tela:** histograma dos 10.000 resultados com as marcas P50, P85 e P95.

**Fala:** "Prometer a mediana é, em geral, cara ou coroa: metade dos futuros passa dela. O compromisso responsável é o P85, aqui 17 semanas."

**Cuidado com um detalhe (pode cair em pergunta):** como o prazo é contado em semanas inteiras, a probabilidade de terminar **até** cada semana dá saltos. Pela Curva S deste exemplo:

| Prazo | Chance de terminar até ele |
| --- | --- |
| 15 semanas | 45,6% |
| 16 semanas (P50) | 71,7% |
| 17 semanas (P85) | 89,0% |
| 18 semanas (P95) | 96,5% |

Ou seja, a mediana é 16, mas prometer 16 semanas tem 71,7% de chance de sucesso, não exatamente 50%; prometer 15 é que fica abaixo de 50%. O percentil diz o **menor prazo inteiro** que atinge aquele nível de confiança, e a chance real é igual ou maior. Se perguntarem, essa é a resposta correta; a ideia de "cara ou coroa" é sobre a mediana em geral, e o backtest do NestJS (slide 13) mostra os 50% acontecendo de fato.

## Slide 10 · o escopo sempre cresce

**Na tela:** duas curvas S. A azul é o escopo fixo; a roxa, com scope creep (0, 1 ou 2 itens novos por semana, média de 0,65).

**Como ler a curva S:** escolha uma semana no eixo horizontal e leia no vertical a chance de terminar até ela. A linha tracejada marca 85%.

**Fala:** "Com 0,65 item novo por semana, o P85 vai de 17 para 21 semanas. Agora o cliente sabe o preço de pedir mais coisa: 4 semanas, e não uma opinião."

## Slide 11 · a conta de padaria

**Na tela:** a fórmula e a substituição dos números.

**A fórmula:** P85 ≈ B/μ + ½ + 1,036 · √(B·σ²/μ³)

- B = 60 itens (backlog); μ = 3,92 (média semanal); σ² = 2,22 (variância das semanas).
- B/μ = 15,29 é o prazo "pela média".
- ½ corrige a contagem em semanas inteiras.
- 1,036 é o valor da curva normal que deixa 85% abaixo.
- √(B·σ²/μ³) = 1,46 é o desvio padrão do prazo.
- Resultado: 15,29 + 0,5 + 1,036 × 1,46 ≈ **17,3 semanas**. A simulação deu 17.

**Fala:** "Essa fórmula vem do Teorema Central do Limite para processos de renovação. Ela não substitui a simulação, mas confere que o código está certo. A média e o desvio batem com diferença menor que 0,1 semana."

**Detalhe bom para citar:** a folga cresce com a raiz do backlog. Dobrar o backlog dobra o prazo médio, mas a folga de segurança cresce só cerca de 41%, porque √2 ≈ 1,41.

## Slide 12 · dez mil não é número mágico

**Na tela:** barras do erro máximo da Curva S para 100, 1.000, 10.000 e 100.000 iterações.

**A ideia:** a desigualdade de Dvoretzky–Kiefer–Wolfowitz (DKW) garante que, com N iterações, a Curva S simulada fica a no máximo ε = √(ln(2/α) / 2N) da verdadeira, com confiança de 1 − α (aqui, 95%).

- N = 1.000 → erro de até ±4,29 pontos percentuais.
- N = 10.000 → erro de até ±1,36 ponto percentual.
- Para ±1 ponto percentual seriam necessárias 18.445 iterações.

**Fala:** "Dez mil não é número mágico: com dez mil, quando eu digo 85%, o valor real está entre 83,6% e 86,4%. Mas atenção: isso mede só o erro do sorteio. Se o histórico não representar o futuro, mais iterações não resolvem."

## Slide 13 · testei no mundo real

**Na tela:** o backtest no `nestjs/nest` (período estável, 12 janelas) e três porcentagens.

**O que é backtest:** voltar no tempo e fazer a previsão que eu teria feito naquele momento, usando só os dados de antes, e depois comparar com o que aconteceu. Em cada janela: 26 semanas de histórico, previsão das 6 seguintes.

**Fonte dos dados:** 572 PRs mergeados por pessoas em 52 semanas, coletados com `gh pr list`. Os PRs de robôs (Renovate e Dependabot) foram excluídos, porque eram 56% dos merges e não medem a capacidade da equipe.

**Resultado:**

- Compromisso P85: cumprido em **83,3%** das janelas (a meta era 85%).
- Mediana: cumprida em **50,0%** (o cara ou coroa, agora com dados reais).
- Média × 6 semanas (o jeito velocity): cumprida em só **41,7%**.

**Fala:** "Por que a média se saiu pior até que a mediana? Porque algumas semanas excepcionais, com 16 e 25 PRs, puxam a média para cima, e a maioria das semanas fica abaixo dela."

## Slide 14 · o passado tem validade

**Na tela:** as 52 semanas do NestJS; a partir da semana 44, as barras roxas saltam de cerca de 5 para cerca de 40 PRs por semana.

**Fala:** "Quando incluo as semanas depois do salto, o P85 acerta 90,5%, mas isso não é mérito do modelo: a equipe passou a entregar muito acima de qualquer previsão. É a premissa de estacionariedade: o futuro precisa se parecer com o passado. Quando o fluxo muda, o histórico tem que recomeçar." Completar com as outras duas premissas: itens de tamanho parecido e WIP limitado (Lei de Little).

## Slide 15 · não reinvente a roda

**Na tela:** curadoria em duas colunas: projetos para estudar (CSV e notebook) e plataformas para usar.

**Fala:** "Pesquisei implementações abertas. Para entender o algoritmo, os mais parecidos com o meu são o Kanban Monte Carlo Simulation, o Kanban Metrics e o quando. Para usar no dia a dia, o Lighthouse é o mais completo, e o template de Power BI do Nick Brown atende quem já usa Jira ou Azure DevOps. Não achei forks entre eles: são implementações independentes que chegaram à mesma ideia."

## Slide 16 · monte carlo junta as peças

**Na tela:** tabela relacionando os outros temas com a previsão.

**Fala:** "Não quero roubar o tema dos colegas. Os temas deles são a matéria-prima: throughput e WIP são a entrada, o CFD mostra o gargalo, cada trajetória é um burndown, e o GQM organiza tudo. Story points e velocity aparecem como o contraste."

## Slide 17 · previsibilidade sem chute

**Na tela:** os quatro passos e o endereço do repositório.

**Fala:** "Resumindo em quatro passos: limite o WIP, conte o throughput por semana, simule dez mil futuros e prometa o P85, ou o P95 se houver multa. O artigo, o código, os testes e os dados estão no repositório público. Obrigado!"

---

## Glossário rápido

| Termo | Explicação curta |
| --- | --- |
| Throughput | Itens concluídos por semana. |
| Backlog | Itens que faltam fazer (aqui, 60). |
| Bootstrapping | Sortear com reposição a partir dos próprios dados, sem supor uma distribuição. |
| Percentil (P85) | Valor abaixo do qual estão 85% dos resultados simulados. |
| Curva S | Probabilidade acumulada de terminar até cada semana. |
| Scope creep | Itens novos que entram no backlog durante o projeto. |
| Semente | Número inicial do gerador aleatório; a mesma semente produz os mesmos sorteios. |
| Backtest | Testar uma previsão com dados do passado, como se fosse feita naquela época. |
| Estacionariedade | O processo se comporta no futuro como no passado. |
