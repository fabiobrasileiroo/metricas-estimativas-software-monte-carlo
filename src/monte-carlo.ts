/**
 * Motor de Simulação de Monte Carlo para previsão de prazos (Tema 7).
 *
 * Bootstrapping não paramétrico: cada semana futura recebe um throughput
 * sorteado com reposição do histórico real da equipe. Nenhuma distribuição
 * (normal, Poisson...) é assumida: o próprio histórico é a distribuição.
 *
 * Mesma lógica de rodbv/quando, thawkin3/monte-carlo-simulation-project-timeline-estimator
 * e jabopiti/kanban-monte-carlo-simulation, reescrita em TypeScript puro.
 */

/** Gerador pseudoaleatório com semente (Mulberry32): resultados reprodutíveis. */
export type Rng = () => number;

export function criarRng(semente = 42): Rng {
  let a = semente >>> 0;
  return () => {
    a = (a + 0x6d2b79f5) >>> 0;
    let t = a;
    t = Math.imul(t ^ (t >>> 15), t | 1);
    t ^= t + Math.imul(t ^ (t >>> 7), t | 61);
    return ((t ^ (t >>> 14)) >>> 0) / 4294967296;
  };
}

/** Sorteio uniforme com reposição: probabilidade 1/n para cada semana do histórico. */
export function sortear<T>(amostra: readonly T[], rng: Rng): T {
  return amostra[Math.floor(rng() * amostra.length)]!;
}

/** Distribuição discreta de itens novos por semana (scope creep). */
export interface ScopeCreep {
  valores: readonly number[];
  probabilidades: readonly number[];
}

export function sortearDiscreto({ valores, probabilidades }: ScopeCreep, rng: Rng): number {
  const u = rng();
  let acumulado = 0;
  for (let i = 0; i < valores.length; i++) {
    acumulado += probabilidades[i]!;
    if (u < acumulado) return valores[i]!;
  }
  return valores[valores.length - 1]!;
}

export interface OpcoesQuando {
  backlog: number;
  iteracoes?: number;
  semente?: number;
  scopeCreep?: ScopeCreep;
  /** Trava de segurança contra backlog que nunca zera (creep maior que vazão). */
  limiteSemanas?: number;
}

/** "Quando fica pronto?": semanas necessárias para zerar o backlog, uma por iteração. */
export function simularQuando(historico: readonly number[], opcoes: OpcoesQuando): number[] {
  const { backlog, iteracoes = 10_000, semente = 42, scopeCreep, limiteSemanas = 1_000 } = opcoes;
  if (historico.length < 5) throw new Error("Histórico de throughput precisa de pelo menos 5 semanas.");
  if (historico.every((t) => t === 0)) throw new Error("Histórico só com zeros: a equipe nunca entrega.");

  const rng = criarRng(semente);
  const resultados = new Array<number>(iteracoes);

  for (let r = 0; r < iteracoes; r++) {
    let restante = backlog;
    let semanas = 0;
    while (restante > 0 && semanas < limiteSemanas) {
      semanas++;
      restante -= sortear(historico, rng);
      if (scopeCreep) restante += sortearDiscreto(scopeCreep, rng);
    }
    resultados[r] = semanas;
  }
  return resultados;
}

/** "Quantos itens cabem até a data?": soma de N semanas sorteadas (pergunta inversa). */
export function simularQuantos(
  historico: readonly number[],
  semanas: number,
  iteracoes = 10_000,
  semente = 42,
): number[] {
  const rng = criarRng(semente);
  return Array.from({ length: iteracoes }, () => {
    let soma = 0;
    for (let s = 0; s < semanas; s++) soma += sortear(historico, rng);
    return soma;
  });
}

/** Caminhos amostrais (burn-down) semana a semana, usados no gráfico animado. */
export function simularTrajetorias(
  historico: readonly number[],
  backlog: number,
  quantidade: number,
  semente = 7,
): number[][] {
  const rng = criarRng(semente);
  return Array.from({ length: quantidade }, () => {
    const caminho = [backlog];
    let restante = backlog;
    while (restante > 0) {
      restante = Math.max(0, restante - sortear(historico, rng));
      caminho.push(restante);
    }
    return caminho;
  });
}

// ---------------------------------------------------------------------------
// Estatística descritiva
// ---------------------------------------------------------------------------

export const media = (xs: readonly number[]) => xs.reduce((a, b) => a + b, 0) / xs.length;

/** Desvio padrão amostral (n - 1), igual ao np.std(ddof=1). */
export function desvioPadrao(xs: readonly number[]): number {
  const m = media(xs);
  return Math.sqrt(xs.reduce((acc, x) => acc + (x - m) ** 2, 0) / (xs.length - 1));
}

/** Percentil com interpolação linear, igual ao np.percentile padrão. */
export function percentil(xs: readonly number[], p: number): number {
  const ordenado = [...xs].sort((a, b) => a - b);
  const pos = (p / 100) * (ordenado.length - 1);
  const baixo = Math.floor(pos);
  const alto = Math.ceil(pos);
  return ordenado[baixo]! + (ordenado[alto]! - ordenado[baixo]!) * (pos - baixo);
}

/** Prazo comprometível: semanas inteiras, sempre arredondando para cima. */
export const semanasNoPercentil = (xs: readonly number[], p: number) => Math.ceil(percentil(xs, p));

/** Probabilidade empírica de terminar em até `prazo` semanas (ponto da Curva S). */
export const probabilidadeAte = (xs: readonly number[], prazo: number) =>
  xs.filter((x) => x <= prazo).length / xs.length;

export interface Resumo {
  media: number;
  desvio: number;
  min: number;
  max: number;
  p50: number;
  p70: number;
  p85: number;
  p95: number;
}

export function resumir(xs: readonly number[]): Resumo {
  return {
    media: media(xs),
    desvio: desvioPadrao(xs),
    min: Math.min(...xs),
    max: Math.max(...xs),
    p50: semanasNoPercentil(xs, 50),
    p70: semanasNoPercentil(xs, 70),
    p85: semanasNoPercentil(xs, 85),
    p95: semanasNoPercentil(xs, 95),
  };
}

// ---------------------------------------------------------------------------
// Conferência analítica (Teorema Central do Limite para processos de renovação)
// ---------------------------------------------------------------------------

/** Quantil da normal padrão (aproximação de Acklam, erro < 1e-9). */
export function quantilNormal(p: number): number {
  const a = [-39.69683028665376, 220.9460984245205, -275.9285104469687, 138.357751867269, -30.66479806614716, 2.506628277459239];
  const b = [-54.47609879822406, 161.5858368580409, -155.6989798598866, 66.80131188771972, -13.28068155288572];
  const c = [-0.007784894002430293, -0.3223964580411365, -2.400758277161838, -2.549732539343734, 4.374664141464968, 2.938163982698783];
  const d = [0.007784695709041462, 0.3224671290700398, 2.445134137142996, 3.754408661907416];
  const q = p < 0.5 ? Math.sqrt(-2 * Math.log(p)) : Math.sqrt(-2 * Math.log(1 - p));
  if (p < 0.02425 || p > 1 - 0.02425) {
    const x = (((((c[0]! * q + c[1]!) * q + c[2]!) * q + c[3]!) * q + c[4]!) * q + c[5]!) /
      ((((d[0]! * q + d[1]!) * q + d[2]!) * q + d[3]!) * q + 1);
    return p < 0.5 ? x : -x;
  }
  const r = p - 0.5;
  const s = r * r;
  return ((((((a[0]! * s + a[1]!) * s + a[2]!) * s + a[3]!) * s + a[4]!) * s + a[5]!) * r) /
    (((((b[0]! * s + b[1]!) * s + b[2]!) * s + b[3]!) * s + b[4]!) * s + 1);
}

/**
 * Aproximação normal do prazo T para zerar B itens com vazão líquida de média μ
 * e variância σ² por semana:  T ≈ N( B/μ ,  B·σ²/μ³ ).
 * O termo +1/2 corrige a discretização (o prazo é contado em semanas inteiras).
 */
export function aproximacaoNormal(backlog: number, mu: number, sigma2: number) {
  const mediaT = backlog / mu + 0.5;
  const desvioT = Math.sqrt((backlog * sigma2) / mu ** 3);
  const prazo = (p: number) => mediaT + quantilNormal(p) * desvioT;
  return { media: mediaT, desvio: desvioT, p50: prazo(0.5), p85: prazo(0.85), p95: prazo(0.95) };
}

/** Variância populacional (o bootstrap sorteia da amostra como se fosse a população). */
export function varianciaPopulacional(xs: readonly number[]): number {
  const m = media(xs);
  return xs.reduce((acc, x) => acc + (x - m) ** 2, 0) / xs.length;
}

export function momentosDiscretos({ valores, probabilidades }: ScopeCreep) {
  const m = valores.reduce((acc, v, i) => acc + v * probabilidades[i]!, 0);
  const m2 = valores.reduce((acc, v, i) => acc + v * v * probabilidades[i]!, 0);
  return { media: m, variancia: m2 - m * m };
}

/** Erro padrão de Monte Carlo da média: σ/√N (cai pela metade a cada 4× iterações). */
export const erroPadraoMonteCarlo = (desvio: number, iteracoes: number) => desvio / Math.sqrt(iteracoes);

/**
 * Desigualdade de Dvoretzky–Kiefer–Wolfowitz: com N iterações, a Curva S empírica
 * fica a no máximo ε da curva verdadeira com confiança 1 - α, em todos os pontos.
 */
export const margemDKW = (iteracoes: number, alfa = 0.05) => Math.sqrt(Math.log(2 / alfa) / (2 * iteracoes));

/** Iterações necessárias para a Curva S ter margem máxima ε (inversa da DKW). */
export const iteracoesParaMargem = (epsilon: number, alfa = 0.05) => Math.ceil(Math.log(2 / alfa) / (2 * epsilon ** 2));

/** Probabilidade de uma cadeia de n tarefas independentes acertarem juntas o prazo. */
export const probabilidadeCadeia = (confiancaIndividual: number, n: number) => confiancaIndividual ** n;

// ---------------------------------------------------------------------------
// Dados reais: agrupar merges por semana
// ---------------------------------------------------------------------------

/** Conta eventos (ex.: PRs mergeados) por semana ISO a partir de `inicio`. */
export function throughputSemanal(datas: readonly Date[], inicio: Date, semanas: number): number[] {
  const contagem = new Array<number>(semanas).fill(0);
  const umaSemana = 7 * 24 * 60 * 60 * 1000;
  for (const d of datas) {
    const indice = Math.floor((d.getTime() - inicio.getTime()) / umaSemana);
    if (indice >= 0 && indice < semanas) contagem[indice]!++;
  }
  return contagem;
}
