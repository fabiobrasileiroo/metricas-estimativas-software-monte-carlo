/**
 * Estudo completo: cenários do artigo + conferência analítica + projeto real (nestjs/nest).
 * Uso: bun run simular   (grava resultados/resultados.json e resultados/resultados.js)
 */
import { mkdirSync, readFileSync, writeFileSync } from "node:fs";
import {
  aproximacaoNormal,
  erroPadraoMonteCarlo,
  iteracoesParaMargem,
  margemDKW,
  media,
  momentosDiscretos,
  percentil,
  probabilidadeAte,
  probabilidadeCadeia,
  resumir,
  simularQuando,
  simularQuantos,
  simularTrajetorias,
  throughputSemanal,
  varianciaPopulacional,
  desvioPadrao,
  type ScopeCreep,
} from "./monte-carlo";

const raiz = new URL("..", import.meta.url).pathname;

// --- 1. Cenários do artigo (equipe com 26 semanas de histórico) -------------
export const HISTORICO = [4, 3, 5, 2, 4, 6, 3, 1, 5, 4, 3, 6, 2, 5, 4, 3, 7, 4, 2, 5, 3, 4, 6, 2, 4, 5];
export const BACKLOG = 60;
export const CREEP: ScopeCreep = { valores: [0, 1, 2], probabilidades: [0.5, 0.35, 0.15] };
const N = 10_000;

const cenarioA = simularQuando(HISTORICO, { backlog: BACKLOG, iteracoes: N });
const cenarioB = simularQuando(HISTORICO, { backlog: BACKLOG, iteracoes: N, scopeCreep: CREEP });
const resumoA = resumir(cenarioA);
const resumoB = resumir(cenarioB);

// Curva S (CDF) semana a semana para os dois cenários
const semanasCurva = Array.from({ length: 21 }, (_, i) => i + 10);
const curvaS = semanasCurva.map((s) => ({ semana: s, a: probabilidadeAte(cenarioA, s), b: probabilidadeAte(cenarioB, s) }));

// Histograma do cenário A
const histograma: Record<number, number> = {};
for (const s of cenarioA) histograma[s] = (histograma[s] ?? 0) + 1;

// --- 2. Conferência analítica (TCL de renovação) ---------------------------
const mu = media(HISTORICO);
const sigma2 = varianciaPopulacional(HISTORICO);
const creep = momentosDiscretos(CREEP);
const analiticoA = aproximacaoNormal(BACKLOG, mu, sigma2);
const analiticoB = aproximacaoNormal(BACKLOG, mu - creep.media, sigma2 + creep.variancia);

// --- 3. Pergunta inversa: quantos itens em 12 semanas? ---------------------
const quantos12 = simularQuantos(HISTORICO, 12, N);
const quantos = {
  semanas: 12,
  // Para escopo, o compromisso é o percentil BAIXO: 85% de chance de entregar pelo menos isso
  p85: Math.floor(percentil(quantos12, 15)),
  p50: Math.floor(percentil(quantos12, 50)),
  p95: Math.floor(percentil(quantos12, 5)),
};

// --- 4. Projeto real: nestjs/nest, PRs humanos mergeados -------------------
const linhas = readFileSync(`${raiz}dados/nest_prs_humanos.csv`, "utf8").trim().split("\n");
const datas = linhas.map((l) => new Date(l.split(",")[1]!.replaceAll('"', "")));
const INICIO = new Date("2025-11-17T00:00:00Z"); // segunda-feira
const SEMANAS_REAIS = 52;
const nest = throughputSemanal(datas, INICIO, SEMANAS_REAIS);

// Backtest rolante: treina com 26 semanas, prevê as 6 seguintes, compara com o real
const TREINO = 26;
const HORIZONTE = 6;
const janelas: { semana: number; real: number; compromisso85: number; mediana: number; ingenuo: number }[] = [];
for (let inicio = 0; inicio + TREINO + HORIZONTE <= SEMANAS_REAIS; inicio++) {
  const treino = nest.slice(inicio, inicio + TREINO);
  const real = nest.slice(inicio + TREINO, inicio + TREINO + HORIZONTE).reduce((a, b) => a + b, 0);
  const simulado = simularQuantos(treino, HORIZONTE, N, 100 + inicio);
  const compromisso85 = Math.floor(percentil(simulado, 15));
  const mediana = Math.floor(percentil(simulado, 50));
  const ingenuo = Math.round(media(treino) * HORIZONTE); // "velocity média × semanas"
  janelas.push({ semana: inicio + TREINO + 1, real, compromisso85, mediana, ingenuo });
}
const acertos85 = janelas.filter((j) => j.real >= j.compromisso85).length / janelas.length;
const acertosMediana = janelas.filter((j) => j.real >= j.mediana).length / janelas.length;
const acertosIngenuo = janelas.filter((j) => j.real >= j.ingenuo).length / janelas.length;

// Mudança de regime: na semana 44 a vazão salta de ~5 para ~45 PRs/semana (salto de vazão).
// Janelas "estáveis" são as cujo horizonte termina antes do salto (premissa de estacionariedade).
const SEMANA_REGIME = 44;
const estaveis = janelas.filter((j) => j.semana + HORIZONTE - 1 < SEMANA_REGIME);
const taxa = (xs: typeof janelas, k: "compromisso85" | "mediana" | "ingenuo") => xs.filter((j) => j.real >= j[k]).length / xs.length;
const estavel = {
  janelas: estaveis.length,
  acertos85: taxa(estaveis, "compromisso85"),
  acertosMediana: taxa(estaveis, "mediana"),
  acertosIngenuo: taxa(estaveis, "ingenuo"),
  mediaAntes: media(nest.slice(0, SEMANA_REGIME - 1)),
  mediaDepois: media(nest.slice(SEMANA_REGIME - 1)),
};

// Previsão final: backlog de 60 PRs com as últimas 26 semanas
const nestUltimas = nest.slice(-TREINO);
const nestQuando = resumir(simularQuando(nestUltimas, { backlog: 60, iteracoes: N }));

// --- 5. Saída ---------------------------------------------------------------
const resultados = {
  geradoEm: new Date().toISOString().slice(0, 10),
  historico: HISTORICO,
  estatisticas: { total: HISTORICO.reduce((a, b) => a + b, 0), media: mu, desvio: desvioPadrao(HISTORICO), varPop: sigma2 },
  cenarioA: resumoA,
  cenarioB: resumoB,
  curvaS,
  histograma,
  analitico: { a: analiticoA, b: analiticoB, creep },
  erros: {
    erroPadraoA: erroPadraoMonteCarlo(resumoA.desvio, N),
    dkw10k: margemDKW(N),
    dkw1k: margemDKW(1_000),
    iteracoesPara1pp: iteracoesParaMargem(0.01),
  },
  cadeia: { p75n10: probabilidadeCadeia(0.75, 10), p90n10: probabilidadeCadeia(0.9, 10) },
  quantos,
  trajetorias: simularTrajetorias(HISTORICO, BACKLOG, 60),
  nest: {
    repositorio: "nestjs/nest",
    periodo: { inicio: "2025-11-17", fim: "2026-11-15" },
    totalPRs: nest.reduce((a, b) => a + b, 0),
    semanal: nest,
    media: media(nest),
    desvio: desvioPadrao(nest),
    min: Math.min(...nest),
    max: Math.max(...nest),
    backtest: { treino: TREINO, horizonte: HORIZONTE, janelas, acertos85, acertosMediana, acertosIngenuo, semanaRegime: SEMANA_REGIME, estavel },
    previsao60: nestQuando,
  },
};

mkdirSync(`${raiz}resultados`, { recursive: true });
writeFileSync(`${raiz}resultados/resultados.json`, JSON.stringify(resultados, null, 2));
// Versão .js para os slides abrirem via file:// sem fetch (bloqueado por CORS)
writeFileSync(`${raiz}resultados/resultados.js`, `window.RESULTADOS = ${JSON.stringify(resultados)};\n`);

const f = (x: number, c = 2) => x.toFixed(c).replace(".", ",");
console.log(`Histórico: μ=${f(mu)} σ=${f(desvioPadrao(HISTORICO))}`);
console.log(`Cenário A: média ${f(resumoA.media)} ± ${f(resumoA.desvio)} | P50 ${resumoA.p50} P85 ${resumoA.p85} P95 ${resumoA.p95} | ${resumoA.min}–${resumoA.max}`);
console.log(`Cenário B: média ${f(resumoB.media)} ± ${f(resumoB.desvio)} | P50 ${resumoB.p50} P85 ${resumoB.p85} P95 ${resumoB.p95} | ${resumoB.min}–${resumoB.max}`);
console.log(`Analítico A: ${f(analiticoA.media)} ± ${f(analiticoA.desvio)} | P85 ${f(analiticoA.p85)} P95 ${f(analiticoA.p95)}`);
console.log(`Analítico B: ${f(analiticoB.media)} ± ${f(analiticoB.desvio)} | P85 ${f(analiticoB.p85)} P95 ${f(analiticoB.p95)}`);
console.log(`Erro padrão MC (A): ${f(resultados.erros.erroPadraoA, 4)} sem | DKW 10k: ±${f(resultados.erros.dkw10k * 100)} pp | 1k: ±${f(resultados.erros.dkw1k * 100)} pp | N p/ ±1pp: ${resultados.erros.iteracoesPara1pp}`);
console.log(`Quantos em 12 sem: P85 ≥ ${quantos.p85} | P50 ${quantos.p50} | P95 ≥ ${quantos.p95}`);
console.log(`NestJS: ${resultados.nest.totalPRs} PRs, μ=${f(resultados.nest.media)} σ=${f(resultados.nest.desvio)} [${resultados.nest.min}–${resultados.nest.max}]`);
console.log(`Backtest (${janelas.length} janelas): P85 cumprido ${f(acertos85 * 100, 1)}% | mediana ${f(acertosMediana * 100, 1)}% | média×semanas ${f(acertosIngenuo * 100, 1)}%`);
console.log(`Período estável (${estavel.janelas} janelas): P85 ${f(estavel.acertos85 * 100, 1)}% | mediana ${f(estavel.acertosMediana * 100, 1)}% | média×semanas ${f(estavel.acertosIngenuo * 100, 1)}% | μ antes ${f(estavel.mediaAntes)} depois ${f(estavel.mediaDepois)}`);
console.log(`NestJS 60 PRs: P50 ${nestQuando.p50} P85 ${nestQuando.p85} P95 ${nestQuando.p95}`);
