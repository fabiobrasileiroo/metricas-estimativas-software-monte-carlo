# Fábio Brasileiro

Identidade visual pessoal do Fábio Brasileiro: um personagem chibi em giz de cera, letra de mão arredondada, fundo branco e frases de efeito com uma ressalva irônica em ciano. Serve para slides de palestra, capas, posts, banners, figurinhas e avatares "no estilo do Fábio".

## A fórmula

Toda peça é **uma afirmação grande + uma ressalva entre parênteses**.

- A afirmação vai em `ink` (`#1c1917`), minúscula, em **Gaegu Bold** (`gaegu`) se a frase não tem acento ou **Itim** (`hand`) se tem — veja Tipografia.
- A ressalva vai **sempre** em `cyan` (`#12a7c4`), nunca rosa, logo abaixo, entre parênteses.
- O tom preferido é **engenheiro raiz** (terminal, produção, log, infraestrutura); o tom fofo fica para posts leves.

| Engenheiro raiz (preferidas) | Fofas |
|---|---|
| a culpa é do DNS **(sempre é)** | todo código é slop **(exceto o meu)** |
| leia o código-fonte **(a documentação mente)** | funciona na minha máquina **(e só nela)** |
| compilou de primeira **(desconfie)** | não é bug **(é feature sem documentação)** |
| o log não mente **(o dev sim)** | o agente errou de novo **(ainda bem que não fui eu)** |
| não é lento **(é O(n²) com estilo)** | só mais uma regra no AGENTS.md **(a 147ª)** |
| git push --force **(com fé)** | testei tudo **(no olho)** |
| cache resolve tudo **(até invalidar)** | meu prompt é perfeito **(o modelo que não entende)** |
| otimizei 2 ms **(levei 2 semanas)** | todo legado é lixo **(até ser o meu)** |
| monólito bem feito **(microsserviço é carência)** | commit pequeno **(só 3 mil linhas)** |
| Kubernetes pra um CRUD **(porque sim)** | deploy na sexta **(o que pode dar errado?)** |
| sem teste não tem merge **(nem o meu)** | código limpo **(até eu abrir de novo)** |
| segfault é feedback **(o compilador é meu mentor)** | café vira código **(e açaí vira refactor)** |
| o problema é de rede **(até provarem o contrário)** | eu reviso todo PR **(dos outros)** |
| SQL na unha **(ORM é muleta)** | a IA escreveu **(eu só levei o crédito)** |

Pose sugerida: frases técnicas → *codando*; vitórias e ironias → *joinha*; recados ao público → *oi*; "todo código é slop", legado e café → *açaí*.

## O personagem

- Chibi desenhado em **giz de cera / lápis de cor**: contorno preto grosso e tremido, cabelo de rabiscos soltos, hachuras visíveis com falhas, bochecha com risquinhos rosados (`blush`), fundo branco.
- Traços fixos: homem brasileiro de ~20 anos, pele morena média (`pele`), cabelo preto ondulado e volumoso com franja bagunçada, sobrancelhas grossas, bigode fino, cavanhaque pontudo só no queixo, **óculos retangulares sem aro com hastes douradas finas (nunca redondos)**, camiseta azul-marinho (`camiseta`).
- Assinatura: tigela de **açaí** (`acai`) com fumacinha rabiscada.
- Quatro poses prontas em 2048×2048 no grupo **Avatares**: açaí, oi, joinha, codando. Cópias leves (~200 KB) em **Avatares web** para páginas.
- Ao usar o desenho num slide, clareie o papel texturizado até branco puro (cada canal `v * 255 / 228`) ou use `mix-blend-mode: multiply` sobre `branco`; senão aparece um quadrado cinza.
- A versão antiga de traço liso (óculos redondos) não deve ser usada e não foi trazida para cá.

## Tipografia

**Regra das frases:** a fonte **primária é Gaegu Bold** (`gaegu`), a mais parecida com a dos slides da poteto, usada quando a frase **não tem acento**. A **secundária é Itim** (`hand`), usada quando a frase tem acento, porque a Gaegu não tem ó, é, ã, ç (as letras somem). Decida pela frase inteira (afirmação + ressalva) e nunca misture as duas na mesma frase. O nome "Fábio Brasileiro" usa sempre Itim.

Teste de acento (o mesmo do repositório): qualquer caractere fora do ASCII, ignorando ² ³ ª º e travessões, conta como acento. Ex.: "compilou de primeira (desconfie)" → Gaegu; "a culpa é do DNS (sempre é)" → Itim.

| Uso | Família (token) | Observação |
|---|---|---|
| Frase sem acento | `gaegu` — Gaegu Bold | Primária; só peso 700 |
| Frase com acento, nome, títulos de página | `hand` — Itim | Secundária; arredondada e com todo o português |
| Alternativas | `patrick` — Patrick Hand, `gochi` — Gochi Hand | Patrick é mais estreita e legível de longe (auditório); Gochi é um marcador mais solto |
| Destaque, figurinha | `sniglet` — Sniglet ExtraBold | Gorda e fofa, só palavras curtas |
| Memes | `shortstack` — Short Stack | Estilo Comic |
| Texto corrido | `text` — Nunito | Carregada do Google Fonts (400, 600, 800) |

Títulos são escritos em minúsculas. No slide, o título começa em `slide-titulo-sem-acento` ou `slide-titulo` (176px) e encolhe de 4 em 4px até caber em 88% da largura.

## Cores

- `branco` é o fundo de toda peça (slide, banner, cartão); `paper` só no fundo da página de referência.
- `ink` para todo texto principal; `muted` para lede, subtítulos e metadados.
- `cyan` **só em texto grande** (≥24px): sobre branco dá 2,9:1, abaixo do mínimo de acessibilidade, e é assim na fonte original. Nunca em corpo de texto.
- `camiseta`, `acai`, `pele` e `blush` são as cores do desenho; use como acento gráfico, não como texto.
- Bordas: 1px `line`; nada de sombras pesadas — só `shadow-slide` sob o slide e `shadow-ring` no cartão selecionado.

## Layout

- **Slide 16:9 (1920×1080)**: fundo branco, título no alto à esquerda (`slide-inset` 110px), ressalva ciano logo abaixo, nome embaixo à esquerda, avatar cortado no peito no canto inferior direito (~43% da largura). Não coloque instituição (FAMETRO) no slide.
- **Banner 3:1** (X, LinkedIn): nome + linha ciano "código, café e açaí" à esquerda, avatar *codando* saindo pela borda à direita.
- **Foto de perfil**: pose *oi*, recorte circular (`radius-round`).
- Cantos `radius-card` (14px) em cartões e slides; botões e etiquetas em pílula (`radius-pill`).

## Gerar novas poses

Melhor resultado: Gemini (Nano Banana) na **mesma conversa** onde o personagem já existe, anexando `avatar-giz-acai.jpeg` como referência:

> Keep exactly the same character, the same rectangular rimless glasses with thin gold temples, and the same crayon / colored-pencil doodle style on a plain white background. Change only the pose: [POSE]. Chest up, square 1:1, no text.

Gerador de slide no repositório: `tools/build_slide.py AVATAR SAIDA.png FONTE.ttf "título" "(ressalva)" "nome"`.

## Créditos

Inspirado no avatar e nos slides de Lauren Tan (poteto) na palestra *All Code Is Slop (Except Mine)*. O personagem é original; a arte dela não faz parte deste sistema.

## Não sincronizado

- Novidades de `d8aa60e` ainda não trazidas: banner do LinkedIn (`banner/`, 1584×396, com ícones de stack) e a fonte JetBrains Mono para código/handles (instalada no sistema, não está no repositório).
- Avatares antigos de traço liso (`gerados/avatar-*.png`, `gerados/web/avatar-*.jpg` sem "giz") e os slides intermediários (`slide-capa.png`, `slide-capa-corrigido.png`): fora, por estarem marcados como "não usar".
- Variáveis CSS e valores avulsos de `index.html` sem papel de marca (gaps de 6px, 10px, 18px, 22px) não viraram tokens.
- Não há logo nem ícones no repositório: a marca é o personagem + o nome em Itim.
- Componentes: o repositório não tem biblioteca de componentes. Os cinco cartões aqui (SlideCapa, Frase, Botao, AvatarCard, Banner) são **reproduções estáticas escritas à mão a partir de `index.html`**, sem bundle JavaScript.
- Fonte: `fabiobrasileiroo/fabio-estilo` @ `d8aa60e` (main); fora a regra Gaegu/Itim, o resto veio de `ee6e777`.
