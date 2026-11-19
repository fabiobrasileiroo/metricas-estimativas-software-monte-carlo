import { describe, expect, test } from "bun:test";
import {
  aproximacaoNormal,
  criarRng,
  margemDKW,
  media,
  momentosDiscretos,
  percentil,
  probabilidadeCadeia,
  quantilNormal,
  resumir,
  simularQuando,
  simularQuantos,
  throughputSemanal,
  varianciaPopulacional,
} from "../src/monte-carlo";

const HISTORICO = [4, 3, 5, 2, 4, 6, 3, 1, 5, 4, 3, 6, 2, 5, 4, 3, 7, 4, 2, 5, 3, 4, 6, 2, 4, 5];
const CREEP = { valores: [0, 1, 2], probabilidades: [0.5, 0.35, 0.15] };

describe("gerador e estatística", () => {
  test("mesma semente gera a mesma sequência (reprodutibilidade)", () => {
    const a = criarRng(42);
    const b = criarRng(42);
    expect(Array.from({ length: 5 }, a)).toEqual(Array.from({ length: 5 }, b));
  });

  test("percentil interpola igual ao np.percentile", () => {
    expect(percentil([1, 2, 3, 4], 50)).toBe(2.5);
    expect(percentil([10, 20, 30, 40, 50], 85)).toBeCloseTo(44);
  });

  test("histórico tem 102 itens e média 3,92", () => {
    expect(HISTORICO.reduce((a, b) => a + b, 0)).toBe(102);
    expect(media(HISTORICO)).toBeCloseTo(3.923, 3);
  });

  test("quantil da normal: z(0,85) = 1,036 e z(0,95) = 1,645", () => {
    expect(quantilNormal(0.85)).toBeCloseTo(1.0364, 3);
    expect(quantilNormal(0.95)).toBeCloseTo(1.6449, 3);
  });
});

describe("cenários do artigo (10.000 iterações)", () => {
  const a = resumir(simularQuando(HISTORICO, { backlog: 60 }));
  const b = resumir(simularQuando(HISTORICO, { backlog: 60, scopeCreep: CREEP }));

  test("cenário A: P50 16, P85 17, P95 18 (mesmo resultado do Python)", () => {
    expect([a.p50, a.p85, a.p95]).toEqual([16, 17, 18]);
  });

  test("cenário B: scope creep empurra o P85 para 21 semanas", () => {
    expect([b.p50, b.p85, b.p95]).toEqual([19, 21, 23]);
  });

  test("percentis são monótonos e P50 nunca é compromisso seguro", () => {
    expect(a.p50).toBeLessThanOrEqual(a.p85);
    expect(a.p85).toBeLessThanOrEqual(a.p95);
    expect(a.min).toBeGreaterThanOrEqual(Math.ceil(60 / Math.max(...HISTORICO)));
  });

  test("Teorema Central do Limite confere a simulação (erro < 0,2 semana)", () => {
    const tcl = aproximacaoNormal(60, media(HISTORICO), varianciaPopulacional(HISTORICO));
    expect(Math.abs(tcl.media - a.media)).toBeLessThan(0.2);
    expect(Math.abs(tcl.desvio - a.desvio)).toBeLessThan(0.2);

    const c = momentosDiscretos(CREEP);
    expect(c.media).toBeCloseTo(0.65);
    const tclB = aproximacaoNormal(60, media(HISTORICO) - c.media, varianciaPopulacional(HISTORICO) + c.variancia);
    expect(Math.abs(tclB.desvio - b.desvio)).toBeLessThan(0.2);
  });
});

describe("equivalência com algoritmos open-source", () => {
  // rodbv/quando: acumula entregas até alcançar o backlog e arredonda o percentil para cima
  function quando(historico: number[], itens: number, iteracoes: number, semente: number) {
    const rng = criarRng(semente);
    return Array.from({ length: iteracoes }, () => {
      let feito = 0;
      let passos = 0;
      while (feito < itens) {
        feito += historico[Math.floor(rng() * historico.length)]!;
        passos++;
      }
      return passos;
    });
  }

  test("rodbv/quando (acumular até B) ≡ motor próprio (descontar até 0)", () => {
    const nosso = simularQuando(HISTORICO, { backlog: 60, semente: 9 });
    const deles = quando(HISTORICO, 60, 10_000, 9);
    expect(deles).toEqual(nosso);
  });

  test("thawkin3: índice inteiro do vetor ordenado dá os mesmos P50/P85/P95", () => {
    const ordenado = simularQuando(HISTORICO, { backlog: 60 }).sort((x, y) => x - y);
    const p = (q: number) => ordenado[Math.floor(q * (ordenado.length - 1))];
    expect([p(0.5), p(0.85), p(0.95)]).toEqual([16, 17, 18]);
  });
});

describe("garantias matemáticas", () => {
  test("cadeia de 10 tarefas com 75% cada: só 5,63% de chance", () => {
    expect(probabilidadeCadeia(0.75, 10)).toBeCloseTo(0.0563, 4);
  });

  test("DKW: 10.000 iterações garantem Curva S a ±1,36 pp", () => {
    expect(margemDKW(10_000)).toBeCloseTo(0.0136, 4);
  });

  test("quantos itens: média de 12 semanas ≈ 12 × μ", () => {
    expect(media(simularQuantos(HISTORICO, 12))).toBeCloseTo(12 * media(HISTORICO), 0);
  });

  test("throughput semanal agrupa datas na semana certa", () => {
    const inicio = new Date("2026-01-05T00:00:00Z");
    const datas = ["2026-01-05", "2026-01-11", "2026-01-12", "2026-01-30"].map((d) => new Date(`${d}T12:00:00Z`));
    expect(throughputSemanal(datas, inicio, 4)).toEqual([2, 1, 0, 1]);
  });

  test("histórico curto ou só com zeros é rejeitado", () => {
    expect(() => simularQuando([1, 2], { backlog: 10 })).toThrow();
    expect(() => simularQuando([0, 0, 0, 0, 0], { backlog: 10 })).toThrow();
  });
});
