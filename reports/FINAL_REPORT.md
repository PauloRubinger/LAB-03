# Caracterizando a Atividade de Code Review no GitHub

**Autor:** Paulo Victor Pimenta Rubinger  
**Data:** 06 de Maio de 2026  
**Versão do Relatório:** 2.0.0  
**Repositório:** https://github.com/PauloRubinger/LAB-03  
**Disciplina:** Laboratório de Experimentação de Software (6º período — Engenharia de Software)  

---

## Resumo

Este experimento analisa a atividade de code review em repositórios populares do GitHub, investigando variáveis que influenciam no merge de Pull Requests (PRs). O dataset é composto por **17.107 PRs** coletados de **199 repositórios**, com status MERGED ou CLOSED, pelo menos uma revisão humana registrada e tempo de análise superior a uma hora. O estudo busca identificar relações entre características dos PRs — tamanho, tempo de análise, descrição e interações — e dois desfechos: o feedback final da revisão (MERGED vs. CLOSED) e o número de revisões realizadas.

**Principais Resultados:**
- PRs **MERGED** são resolvidos significativamente mais rápido (mediana 25,8h vs. 126,0h para CLOSED).
- PRs **CLOSED** apresentam mais interações (mais participantes e comentários), sugerindo que controvérsia leva à rejeição.
- **Tamanho** (arquivos e linhas) correlaciona positivamente com o número de revisões.
- A **descrição** do PR não influencia significativamente o status final, mas correlaciona fracamente com mais revisões.

---

## 1. Introdução

### 1.1 Contextualização

A prática de code review tornou-se um pilar central nos processos de desenvolvimento ágeis. Em projetos open source hospedados no GitHub, essa atividade se materializa por meio de Pull Requests (PRs): um desenvolvedor propõe uma alteração ao repositório e um ou mais revisores avaliam, discutem e, ao final, aprovam ou rejeitam a integração.

Esse processo apresenta múltiplos fatores que podem influenciar seu desfecho. Do ponto de vista do código submetido, PRs maiores e mais complexos exigem maior esforço de revisão, o que pode impactar tanto a probabilidade de merge quanto o número de rodadas de revisão necessárias. Do ponto de vista da comunicação, uma descrição detalhada pode facilitar o entendimento do revisor e acelerar o processo. Por fim, o volume de interações — participantes e comentários — pode refletir tanto o engajamento da comunidade quanto a controvérsia em torno da mudança proposta.

### 1.2 Problema Foco do Experimento

Quais características de um Pull Request influenciam no resultado do processo de code review? Existe correlação mensurável entre o tamanho, a descrição, o tempo de análise e as interações de um PR e (a) a probabilidade de ser aceito (MERGED) ou rejeitado (CLOSED) e (b) o número de revisões que ele recebe?

### 1.3 Questões de Pesquisa

#### A. Feedback Final das Revisões (Status do PR)

| ID | Questão de Pesquisa | Variável Independente | Variável Dependente |
|----|--------------------|-----------------------|---------------------|
| RQ01 | Qual a relação entre o **tamanho** dos PRs e o feedback final das revisões? | Arquivos alterados; linhas adicionadas e removidas | Status (MERGED / CLOSED) |
| RQ02 | Qual a relação entre o **tempo de análise** dos PRs e o feedback final das revisões? | Intervalo criação → fechamento/merge (horas) | Status (MERGED / CLOSED) |
| RQ03 | Qual a relação entre a **descrição** dos PRs e o feedback final das revisões? | Número de caracteres do body (markdown) | Status (MERGED / CLOSED) |
| RQ04 | Qual a relação entre as **interações** nos PRs e o feedback final das revisões? | Número de participantes; número de comentários | Status (MERGED / CLOSED) |

#### B. Número de Revisões

| ID | Questão de Pesquisa | Variável Independente | Variável Dependente |
|----|--------------------|-----------------------|---------------------|
| RQ05 | Qual a relação entre o **tamanho** dos PRs e o número de revisões realizadas? | Arquivos alterados; linhas adicionadas e removidas | Total de revisões |
| RQ06 | Qual a relação entre o **tempo de análise** dos PRs e o número de revisões realizadas? | Intervalo criação → fechamento/merge (horas) | Total de revisões |
| RQ07 | Qual a relação entre a **descrição** dos PRs e o número de revisões realizadas? | Número de caracteres do body (markdown) | Total de revisões |
| RQ08 | Qual a relação entre as **interações** nos PRs e o número de revisões realizadas? | Número de participantes; número de comentários | Total de revisões |

### 1.4 Hipóteses Informais

Com base em conhecimento prévio sobre práticas de desenvolvimento de software, formulam-se as seguintes hipóteses:

**H1 — Tamanho impacta negativamente o feedback e aumenta o número de revisões (RQ01 e RQ05):**  
PRs maiores (mais arquivos alterados, mais linhas adicionadas e removidas) tendem a ser mais difíceis de revisar. Espera-se que PRs maiores apresentem menor taxa de merge (maior proporção de CLOSED) e exijam mais rodadas de revisão antes de uma decisão final. A hipótese é que revisores resistem a integrar mudanças extensas por razão de risco e esforço de compreensão.

**H2 — Tempo de análise mais longo está associado a merge e a mais revisões (RQ02 e RQ06):**  
PRs que ficam abertos por mais tempo provavelmente passam por discussões mais aprofundadas, sugerindo que os revisores os consideram suficientemente relevantes para investir esforço. Espera-se, portanto, que PRs com maior tempo de análise tenham maior probabilidade de serem MERGED e recebam mais revisões.

**H3 — Descrições mais longas favorecem o merge e aumentam o número de revisões (RQ03 e RQ07):**  
Uma descrição bem elaborada comunica melhor a motivação e o impacto da mudança, facilitando a compreensão do revisor. A hipótese é que PRs com body mais longo (em caracteres) sejam mais frequentemente aceitos (MERGED) e que esse engajamento descritivo estimule revisores a interagir mais, elevando o número de revisões.

**H4 — Mais interações estão associadas a maior probabilidade de merge e a mais revisões (RQ04 e RQ08):**  
PRs com mais participantes e comentários indicam engajamento ativo da comunidade. Embora mais comentários possam também refletir controvérsia, a hipótese inicial é que o envolvimento de múltiplos atores tende a convergir para uma resolução positiva (merge). Além disso, mais participantes naturalmente correspondem a mais revisões formais registradas.

### 1.5 Objetivo

**Objetivo Principal:** Investigar a correlação entre características do processo de submissão de PRs (tamanho, tempo de análise, descrição e interações) e os desfechos do processo de code review (status final e número de revisões) em repositórios populares do GitHub.

**Objetivos Específicos:**
1. Coletar PRs dos 200 repositórios mais populares do GitHub com pelo menos 100 PRs (MERGED + CLOSED).
2. Filtrar PRs com pelo menos uma revisão e tempo de análise superior a uma hora.
3. Calcular as métricas definidas para cada PR coletado.
4. Analisar correlações estatísticas entre as variáveis independentes e dependentes.
5. Validar ou refutar as hipóteses por meio de testes estatísticos apropriados.

---

## 2. Metodologia

### 2.1 Tipo de Estudo

- **Tipo:** Estudo observacional / correlacional
- **Unidade de análise:** Pull Request
- **Abordagem:** Análise quantitativa com técnicas estatísticas

### 2.2 Fluxo do Experimento

O experimento seguiu um pipeline automatizado de três fases:

```
┌─────────────────────────────────────────┐
│ Fase 1 — Seleção de Repositórios        │
│ GitHub GraphQL API                      │
│ Top-200 repos por stars                 │
│ Filtro: ≥ 100 PRs (MERGED + CLOSED)     │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│ Fase 2 — Coleta de PRs e Métricas       │
│ Status: MERGED ou CLOSED                │
│ Filtro: ≥ 1 revisão                     │
│ Filtro: tempo de análise > 1h           │
│ Extração de todas as métricas definidas │
└────────────────────┬────────────────────┘
                     ▼
┌─────────────────────────────────────────┐
│ Fase 3 — Análise Estatística            │
│ Estatísticas descritivas                │
│ Mann-Whitney U (status MERGED/CLOSED)   │
│ Correlação de Spearman (nº revisões)    │
│ Geração de gráficos                     │
└─────────────────────────────────────────┘
```

### 2.3 Amostra

| Parâmetro | Valor |
|-----------|-------|
| Repositórios coletados | 200 |
| Repositórios com PRs no dataset | 199 |
| Total de PRs coletados | 17.107 |
| PRs MERGED | 12.469 (72,9%) |
| PRs CLOSED | 4.638 (27,1%) |
| Critério de seleção | Top-200 repos por stars no GitHub |
| Período | Snapshot em 01/05/2026 |
| Inclusão | PRs com ≥ 1 revisão e tempo de análise > 1h |
| Exclusão | PRs abertos; revisões automatizadas (bots/CI/CD) |

### 2.4 Ferramentas e Materiais

| Ferramenta | Versão | Propósito |
|------------|--------|-----------|
| Python | 3.12 | Orquestração do pipeline e análise estatística |
| GitHub GraphQL API | v4 | Coleta de repositórios e PRs |
| pandas | ≥2.0.0 | Manipulação e consolidação de dados |
| scipy | ≥1.10.0 | Testes estatísticos e correlações |
| matplotlib / seaborn | ≥3.7.0 / ≥0.12.0 | Geração de gráficos e visualizações |

### 2.5 Métricas Coletadas

#### 2.5.1 Métricas de PR (Variáveis Independentes)

| Dimensão | Métrica | Campo / Fórmula | Interpretação |
|----------|---------|-----------------|---------------|
| Tamanho | Número de arquivos alterados | `changedFiles` | Quantidade de arquivos modificados no PR |
| Tamanho | Total de linhas adicionadas | `additions` | Linhas de código inseridas |
| Tamanho | Total de linhas removidas | `deletions` | Linhas de código removidas |
| Tempo de Análise | Intervalo criação → fechamento/merge | `(closedAt − createdAt)` em horas | Duração total do processo de revisão |
| Descrição | Caracteres do body do PR | `len(body)` | Tamanho da descrição em markdown |
| Interações | Número de participantes | `participants.totalCount` | Pessoas envolvidas no PR |
| Interações | Número de comentários | `comments.totalCount` | Volume de discussão gerada |

#### 2.5.2 Métricas de Desfecho (Variáveis Dependentes)

| Métrica | Unidade | Range | Interpretação |
|---------|---------|-------|---------------|
| Status do PR (`state`) | Categórico | MERGED / CLOSED | Desfecho final do processo de revisão. **MERGED** = aceito; **CLOSED** = rejeitado sem merge. |
| Número de revisões (`review_count`) | Contagem | 1–∞ | Quantidade de rodadas de revisão formais registradas pela API. Maior = mais ciclos de inspeção. |

### 2.6 Método Estatístico

1. **Estatísticas Descritivas:** Média, mediana, desvio padrão, min e max para todas as métricas, tanto globalmente quanto por grupo (MERGED vs. CLOSED).

2. **Teste de Mann-Whitney U (RQ01–RQ04):** Para comparar as distribuições das métricas entre PRs MERGED e CLOSED. Adequado para dados não normais e com outliers, como é o caso de métricas de PR. Alternativa bilateral (two-sided).

3. **Correlação de Spearman (RQ05–RQ08):** Para medir a associação entre cada métrica de PR e o número de revisões (variável dependente contínua). Escolhido em detrimento do Pearson por ser robusto a distribuições assimétricas e outliers, características marcantes nas métricas coletadas.

4. **Nível de significância:** p < 0,05. Resultados reportados com indicadores: `***` (p < 0,001), `**` (p < 0,01), `*` (p < 0,05), `ns` (não significativo).

A justificativa para o uso do Mann-Whitney em vez do teste t é a forte assimetria observada nas distribuições (medianas muito inferiores às médias em todas as métricas), tornando os testes paramétricos inapropriados.

### 2.7 Tratamento de Dados Ausentes e Exceções

| Situação | Tratamento |
|----------|------------|
| PR sem revisão (`review_count = 0`) | Excluído do dataset |
| PR com tempo de análise ≤ 1h | Excluído do dataset (revisão automática) |
| Body nulo ou ausente | `body_length = 0` |
| Repositório com < 100 PRs | Excluído da seleção inicial |

---

## 3. Resultados

### 3.1 Estatísticas Descritivas

**Métricas globais (n = 17.107):**

| Métrica | Média | Mediana | Desvio Padrão | Min | Max |
|---------|-------|---------|---------------|-----|-----|
| Arquivos alterados | 25,87 | 2,00 | 422,95 | 0 | 28.662 |
| Linhas adicionadas | 1.284,65 | 17,00 | 38.894,61 | 0 | 2.901.110 |
| Linhas removidas | 1.043,43 | 3,00 | 23.586,24 | 0 | 1.451.918 |
| Tempo de análise (h) | 900,43 | 37,31 | 3.944,15 | 1,00 | 92.293,59 |
| Caracteres do body | 1.032,77 | 497,00 | 1.809,17 | 0 | 32.402 |
| Nº de revisões | 2,67 | 1,00 | 4,33 | 1 | 108 |
| Nº de participantes | 2,96 | 2,00 | 4,41 | 0 | 277 |
| Nº de comentários | 2,62 | 1,00 | 8,34 | 0 | 589 |

As métricas de tamanho e tempo apresentam alta variabilidade: a mediana de linhas adicionadas (17) é drasticamente inferior à média (1.284), indicando distribuições fortemente assimétricas à direita com poucos PRs muito grandes dominando a média. O mesmo padrão se observa no tempo de análise, com mediana de 37,31h frente a uma média de 900h, evidenciando que a maioria dos PRs é resolvida rapidamente, mas outliers com semanas ou meses de análise inflam a média.

**Métricas por grupo (mediana):**

| Métrica | MERGED (n=12.469) | CLOSED (n=4.638) |
|---------|-------------------|-----------------|
| Arquivos alterados | 2,00 | 1,00 |
| Linhas adicionadas | 18,00 | 16,00 |
| Linhas removidas | 4,00 | 1,00 |
| Tempo de análise (h) | 25,84 | 126,03 |
| Caracteres do body | 487,00 | 514,00 |
| Nº de revisões | 1,00 | 1,00 |
| Nº de participantes | 2,00 | 3,00 |
| Nº de comentários | 1,00 | 2,00 |

A comparação das medianas já revela padrões notáveis: PRs CLOSED levam quase **5× mais tempo** para serem fechados (126,0h vs. 25,8h) e acumulam mais interações, enquanto PRs MERGED são ligeiramente maiores em tamanho. Esses padrões serão confirmados estatisticamente nas seções seguintes.

### 3.2 Distribuição das Métricas

**Insights sobre as distribuições:**

- Todas as métricas de tamanho e tempo apresentam distribuições fortemente assimétricas à direita, com longas caudas superiores — confirmando a inadequação de testes paramétricos para este dataset.
- A mediana é consistentemente muito inferior à média em todas as métricas, indicando que poucos PRs muito grandes ou muito demorados dominam a média mas não representam o comportamento típico.
- As métricas de interações (participantes, comentários) seguem o mesmo padrão assimétrico: a maioria dos PRs envolve apenas 2 participantes e 1 comentário, com raros casos de discussões extensas.

### 3.3 RQ01 — Tamanho vs. Feedback Final das Revisões

**Pergunta:** Qual a relação entre o tamanho dos PRs e o feedback final das revisões?

| Métrica | Mediana MERGED | Mediana CLOSED | p-valor | Significância |
|---------|---------------|----------------|---------|---------------|
| Arquivos alterados | 2,00 | 1,00 | 2,26e-33 | *** |
| Linhas adicionadas | 18,00 | 16,00 | 1,87e-03 | ** |
| Linhas removidas | 4,00 | 1,00 | 6,23e-70 | *** |

![](figures/rq01_tamanho_vs_status.png)

**Figura 1 —** Box plots das métricas de tamanho por status (MERGED vs. CLOSED). Eixos em escala logarítmica. PRs MERGED apresentam medianas superiores em arquivos alterados e linhas removidas.

**Hipótese H1:** PRs maiores apresentam menor taxa de merge (maior proporção de CLOSED).

**Resultado: H1 rejeitada.** Contrariando a hipótese, PRs MERGED apresentam medianas maiores em todas as métricas de tamanho — especialmente em arquivos alterados (2 vs. 1) e linhas removidas (4 vs. 1). As diferenças são altamente significativas (p < 0,001 para arquivos e deleções; p < 0,01 para adições).

**Insights:**
- PRs que removem mais código têm maior chance de serem aceitos, possivelmente porque deleções frequentemente indicam limpeza e refatoração — contribuições bem-vindas pelos revisores.
- PRs CLOSED com poucos arquivos alterados podem representar contribuições incompletas, divergentes do escopo do projeto ou submetidas ao repositório errado.
- A diferença em linhas adicionadas é pequena (18 vs. 16), sugerindo que o volume bruto de adições é menos determinante que a natureza das mudanças.

### 3.4 RQ02 — Tempo de Análise vs. Feedback Final das Revisões

**Pergunta:** Qual a relação entre o tempo de análise dos PRs e o feedback final das revisões?

| Métrica | Mediana MERGED | Mediana CLOSED | p-valor | Significância |
|---------|---------------|----------------|---------|---------------|
| Tempo de análise (h) | 25,84 | 126,03 | 1,25e-224 | *** |

![](figures/rq02_tempo_vs_status.png)

**Figura 2 —** Box plot do tempo de análise por status. Mediana MERGED: 25,8h; mediana CLOSED: 126,0h (~5× maior).

**Hipótese H2:** PRs com maior tempo de análise têm maior probabilidade de serem MERGED.

**Resultado: H2 rejeitada.** O resultado é diametralmente oposto à hipótese: PRs CLOSED ficam abertos por um tempo mediano de 126,0h (≈5 dias), enquanto PRs MERGED são resolvidos em apenas 25,8h (≈1 dia). A diferença é extremamente significativa (p < 1,25e-224).

**Insights:**
- PRs que são MERGED tendem a ser resolvidos rapidamente, possivelmente porque representam contribuições alinhadas com os objetivos do projeto e de fácil avaliação pelos revisores.
- PRs CLOSED frequentemente acumulam tempo de análise por ficarem em estado de abandono — o autor para de responder ao feedback ou a mudança se torna obsoleta com o tempo.
- Um longo tempo de análise pode ser um sinal de que o PR está em disputa ou que não há consenso entre os revisores, levando eventualmente à rejeição.

### 3.5 RQ03 — Descrição vs. Feedback Final das Revisões

**Pergunta:** Qual a relação entre a descrição dos PRs e o feedback final das revisões?

| Métrica | Mediana MERGED | Mediana CLOSED | p-valor | Significância |
|---------|---------------|----------------|---------|---------------|
| Caracteres do body | 487,00 | 514,00 | 0,200 | ns |

A **Figura 3** apresenta os box plots comparativos de tamanho de descrição.

![](figures/rq03_descricao_vs_status.png)

**Figura 3 —** Box plot dos caracteres do *body* por status. Medianas praticamente idênticas (MERGED: 487; CLOSED: 514), p = 0,200 (ns).

**Hipótese H3:** PRs com descrições mais longas têm maior probabilidade de serem MERGED.

**Resultado: H3 rejeitada.** Não foi encontrada diferença estatisticamente significativa entre a descrição de PRs MERGED e CLOSED (p = 0,200). As medianas são praticamente idênticas (487 vs. 514 caracteres).

**Insights:**
- A descrição do PR, isoladamente, não é um preditor do seu desfecho. O conteúdo e a qualidade da mudança proposta parecem ser mais determinantes que a elaboração textual da justificativa.
- PRs CLOSED podem ter descrições ligeiramente mais longas porque os autores de PRs rejeitados eventualmente detalham mais a proposta na esperança de convencer os revisores — sem sucesso.
- Este resultado sugere que revisores em repositórios populares avaliam primariamente o código, não a justificativa escrita.

### 3.6 RQ04 — Interações vs. Feedback Final das Revisões

**Pergunta:** Qual a relação entre as interações nos PRs e o feedback final das revisões?

| Métrica | Mediana MERGED | Mediana CLOSED | p-valor | Significância |
|---------|---------------|----------------|---------|---------------|
| Nº de participantes | 2,00 | 3,00 | 2,39e-31 | *** |
| Nº de comentários | 1,00 | 2,00 | 7,86e-84 | *** |

![](figures/rq04_interacoes_vs_status.png)

**Figura 4 —** Box plots de participantes e comentários por status. PRs CLOSED apresentam mais interações que os MERGED.

**Hipótese H4:** PRs com mais interações têm maior probabilidade de serem MERGED.

**Resultado: H4 rejeitada.** PRs CLOSED apresentam mais participantes (mediana 3 vs. 2) e mais comentários (mediana 2 vs. 1). Ambas as diferenças são altamente significativas (p < 0,001).

**Insights:**
- Mais interações em um PR estão associadas à sua **rejeição**, não à aceitação. Isso sugere que interações refletem controvérsia e resistência, não apenas engajamento positivo.
- PRs MERGED com poucas interações provavelmente representam contribuições de colaboradores confiáveis e frequentes, que já têm credibilidade no projeto e cujo código é aprovado com menor discussão.
- O padrão de mais comentários em PRs CLOSED pode refletir um ciclo de revisão-correção que eventualmente é abandonado ou encerrado sem merge.

### 3.7 RQ05 — Tamanho vs. Número de Revisões

**Pergunta:** Qual a relação entre o tamanho dos PRs e o número de revisões realizadas?

| Métrica | Spearman ρ | p-valor | Significância |
|---------|-----------|---------|---------------|
| Arquivos alterados vs. nº revisões | 0,2412 | 5,18e-225 | *** |
| Linhas adicionadas vs. nº revisões | 0,2817 | 1,34e-309 | *** |
| Linhas removidas vs. nº revisões | 0,1623 | 2,74e-101 | *** |

A **Figura 5** apresenta os scatter plots de tamanho vs. número de revisões.

![](figures/rq05_tamanho_vs_revisoes.png)

**Figura 5 —** Scatter plots de arquivos alterados e linhas modificadas vs. número de revisões. Spearman ρ = 0,24 (arquivos) e ρ = 0,27 (linhas), p < 0,001.

**Hipótese H1 (RQ05):** PRs maiores exigem mais revisões.

**Resultado: H1 confirmada.** Todas as métricas de tamanho apresentam correlação positiva e altamente significativa com o número de revisões. A correlação mais forte é com linhas adicionadas (ρ = 0,28), seguida por arquivos alterados (ρ = 0,24) e linhas removidas (ρ = 0,16).

**Insights:**
- PRs com mais linhas adicionadas naturalmente exigem mais ciclos de revisão, pois há mais código a ser inspecionado e potencialmente corrigido.
- A correlação mais fraca com deleções (ρ = 0,16) é coerente com o resultado de RQ01: remoções de código são bem-vindas e requerem menos ciclos de discussão.
- As correlações são moderadas (0,16–0,28), indicando que o tamanho explica parte, mas não a totalidade, da variação no número de revisões.

### 3.8 RQ06 — Tempo de Análise vs. Número de Revisões

**Pergunta:** Qual a relação entre o tempo de análise dos PRs e o número de revisões realizadas?

| Métrica | Spearman ρ | p-valor | Significância |
|---------|-----------|---------|---------------|
| Tempo de análise (h) vs. nº revisões | 0,0714 | 8,70e-21 | *** |

A **Figura 6** apresenta o scatter plot de tempo de análise vs. número de revisões.

![](figures/rq06_tempo_vs_revisoes.png)

**Figura 6 —** Scatter plot do tempo de análise vs. número de revisões. Spearman ρ = 0,071, p < 0,001 (correlação fraca).

**Hipótese H2 (RQ06):** PRs com maior tempo de análise recebem mais revisões.

**Resultado: H2 confirmada (fraca).** A correlação é positiva e significativa, mas fraca (ρ = 0,071). PRs que ficam abertos por mais tempo tendem a acumular mais revisões.

**Insights:**
- A correlação fraca sugere que o tempo por si só não é um bom preditor do número de revisões. Um PR pode ficar aberto por semanas sem receber nenhuma revisão adicional (abandono) ou receber várias revisões em poucas horas (PR controverso).
- O resultado é consistente com a ideia de que revisões adicionais geram mais tempo de análise — a causalidade pode ser inversa: mais revisões → mais tempo, e não mais tempo → mais revisões.

### 3.9 RQ07 — Descrição vs. Número de Revisões

**Pergunta:** Qual a relação entre a descrição dos PRs e o número de revisões realizadas?

| Métrica | Spearman ρ | p-valor | Significância |
|---------|-----------|---------|---------------|
| Caracteres do body vs. nº revisões | 0,1692 | 4,55e-110 | *** |

A **Figura 7** apresenta o scatter plot de descrição vs. número de revisões.

![](figures/rq07_descricao_vs_revisoes.png)

**Figura 7 —** Scatter plot do comprimento da descrição vs. número de revisões. Spearman ρ = 0,17, p < 0,001.

**Hipótese H3 (RQ07):** PRs com descrições mais longas recebem mais revisões.

**Resultado: H3 confirmada.** A correlação é positiva e significativa (ρ = 0,17, p < 0,001). Embora fraca, o resultado indica que PRs com descrições mais elaboradas tendem a receber mais rodadas de revisão.

**Insights:**
- Ao contrário do que foi observado em RQ03 (sem efeito no status final), a descrição influencia o *processo* de revisão: PRs bem descritos engajam mais os revisores, que interagem mais com o conteúdo.
- A diferença entre os resultados de RQ03 e RQ07 revela que uma descrição elaborada pode aumentar o número de revisões sem necessariamente aumentar a probabilidade de merge — o engajamento não garante aceitação.

### 3.10 RQ08 — Interações vs. Número de Revisões

**Pergunta:** Qual a relação entre as interações nos PRs e o número de revisões realizadas?

| Métrica | Spearman ρ | p-valor | Significância |
|---------|-----------|---------|---------------|
| Nº de participantes vs. nº revisões | 0,3246 | < 1e-300 | *** |
| Nº de comentários vs. nº revisões | 0,2763 | 2,92e-297 | *** |

A **Figura 8** apresenta os scatter plots de interações vs. número de revisões.

![](figures/rq08_interacoes_vs_revisoes.png)

**Figura 8 —** Scatter plots de participantes e comentários vs. número de revisões. Spearman ρ = 0,32 (participantes) e ρ = 0,28 (comentários), p < 0,001 — correlações mais fortes do estudo.

**Hipótese H4 (RQ08):** PRs com mais interações recebem mais revisões.

**Resultado: H4 confirmada.** As correlações são as mais fortes encontradas no estudo. Participantes apresenta ρ = 0,32 e comentários ρ = 0,28, ambos com significância máxima.

**Insights:**
- O número de participantes é o preditor mais forte do número de revisões entre todas as métricas analisadas. Isso é esperado: cada revisor adicional gera pelo menos uma revisão formal.
- A correlação com comentários (ρ = 0,28) confirma que PRs com mais discussão textual também acumulam mais revisões formais — os dois processos são interdependentes.
- Esses resultados são os mais intuitivos do estudo e confirmam que interações e revisões são dimensões correlacionadas do mesmo processo de code review.

### 3.11 Visão Geral: Sumário dos Resultados

| Hipótese | Expectativa (Status) | Resultado (Status) | Expectativa (Revisões) | Resultado (Revisões) |
|----------|---------------------|-------------------|----------------------|---------------------|
| **H1** (Tamanho) | Maior PR → mais CLOSED | Maior PR → mais **MERGED** | Maior PR → mais revisões | **Confirmada** (ρ 0,16–0,28) |
| **H2** (Tempo) | Mais tempo → mais MERGED | Mais tempo → mais **CLOSED** | Mais tempo → mais revisões | **Confirmada (fraca)** (ρ=0,071) |
| **H3** (Descrição) | Mais chars → mais MERGED | **Sem diferença** (ns) | Mais chars → mais revisões | **Confirmada (fraca)** (ρ=0,17) |
| **H4** (Interações) | Mais interações → mais MERGED | Mais interações → mais **CLOSED** | Mais interações → mais revisões | **Confirmada** (ρ 0,28–0,32) |

---

### 3.12 Visão Geral: Matriz de Correlação

A **Figura 9** apresenta a matriz de correlação de Spearman entre todas as métricas analisadas, resumindo visualmente as relações encontradas.

![Matriz de Correlação de Spearman](figures/spearman_correlation_matrix.png)

**Figura 9 —** Matriz de correlação de Spearman entre todas as métricas. Escala divergente: vermelho (positivo) a azul (negativo). Correlação mais forte entre variáveis distintas: `participants` × `review_count` (ρ = 0,32).

**Insights:**

- O bloco mais intenso está na interseção de `additions` e `total_lines` com `review_count`, confirmando que o tamanho do código é o fator mais associado ao número de revisões.
- `participants` e `comments` apresentam correlações positivas moderadas tanto com `review_count` quanto entre si (ρ = 0,34), sugerindo que interações e revisões são dimensões interdependentes do mesmo processo.
- `analysis_time_hours` apresenta correlação **negativa** com as métricas de tamanho (ρ ≈ −0,07 a −0,12), indicando que PRs maiores tendem a ser resolvidos mais rapidamente — coerente com o resultado de RQ01 (PRs MERGED são ligeiramente maiores).
- `body_length` apresenta correlação fraca com `review_count` (ρ = 0,17) e negativa com `participants` (ρ = −0,08), sugerindo que descrições longas não atraem mais participantes, apenas mais ciclos de revisão.
- As métricas de tamanho (`changed_files`, `additions`, `deletions`, `total_lines`) são positivamente correlacionadas entre si (ρ entre 0,52 e 0,95), indicando multicolinearidade esperada.

---

## 4. Discussão

### 4.1 Comparação entre Hipóteses e Resultados

| Hipótese | Expectativa | Resultado | Veredito |
|----------|-------------|-----------|----------|
| **H1** (Tamanho → Status) | Maior PR = mais CLOSED | Maior PR = mais MERGED | **Rejeitada** |
| **H1** (Tamanho → Revisões) | Maior PR = mais revisões | Maior PR = mais revisões | **Confirmada** |
| **H2** (Tempo → Status) | Mais tempo = mais MERGED | Mais tempo = mais CLOSED | **Rejeitada** |
| **H2** (Tempo → Revisões) | Mais tempo = mais revisões | Correlação fraca positiva | **Confirmada (fraca)** |
| **H3** (Descrição → Status) | Mais chars = mais MERGED | Sem diferença significativa | **Rejeitada** |
| **H3** (Descrição → Revisões) | Mais chars = mais revisões | Correlação fraca positiva | **Confirmada (fraca)** |
| **H4** (Interações → Status) | Mais interações = mais MERGED | Mais interações = mais CLOSED | **Rejeitada** |
| **H4** (Interações → Revisões) | Mais interações = mais revisões | Correlação moderada positiva | **Confirmada** |

### 4.2 Interpretação dos Resultados

**Tamanho não reduz a chance de merge (RQ01).** Ao contrário do esperado, PRs MERGED são ligeiramente maiores. Uma explicação plausível é o viés de seleção: contribuidores experientes, que têm mais PRs aceitos, tendem a submeter mudanças mais substanciais e bem estruturadas. PRs muito pequenos CLOSED podem representar submissões de baixa qualidade ou fora do escopo. Já em relação às revisões (RQ05), a hipótese se confirma: mais código significa mais inspeção.

**Tempo longo é sinal de rejeição, não de rigor (RQ02).** O resultado mais surpreendente do estudo: PRs CLOSED ficam abertos por tempo mediano de 126,0h, quase 5× mais que os MERGED (25,8h). Isso inverte completamente a hipótese de que mais tempo refletiria maior cuidado do revisor. A interpretação mais provável é que PRs CLOSED ficam em estado de limbo — aguardando correções que nunca chegam, ou aguardando decisão de mantenedores que não priorizam aquela mudança — até serem encerrados. PRs MERGED, por sua vez, são resolvidos rapidamente porque o código é aprovado nas primeiras rodadas.

**Descrição não influencia o desfecho, mas influencia o processo (RQ03 e RQ07).** A ausência de correlação com o status (RQ03) e a presença de correlação fraca com revisões (RQ07) revelam uma dissociação interessante: escrever mais sobre o PR não aumenta a chance de ser aceito, mas atrai mais atenção dos revisores. Em repositórios populares, os mantenedores parecem avaliar o código diretamente, sem que a elaboração textual seja um fator decisivo na aprovação.

**Interações refletem controvérsia, não aceitação (RQ04 e RQ08).** PRs CLOSED têm mais participantes e comentários que PRs MERGED. Isso sugere que interações frequentemente representam negociação malsucedida: o autor tenta convencer os revisores por meio de discussão, mas sem sucesso. Em contraste, PRs MERGED tendem a ser aprovados com poucas interações — contribuições de qualidade de contribuidores reconhecidos não precisam de muita discussão. A confirmação da hipótese em RQ08 (mais interações = mais revisões) é trivialmente esperada, pois participantes adicionais geram revisões formais.

### 4.3 Síntese dos Insights

1. **Velocidade de resolução é o maior diferenciador.** PRs MERGED são resolvidos ~5× mais rápido que os CLOSED (25,8h vs. 126,0h), sendo o tempo de análise a variável mais discriminante entre os dois grupos.
2. **Interações indicam atrito, não aprovação.** Mais participantes e comentários estão associados à rejeição do PR, não à sua aceitação.
3. **Tamanho favorece levemente o merge.** Ao contrário da hipótese, PRs maiores têm mais chance de serem aceitos — possivelmente porque vêm de contribuidores experientes.
4. **Descrição não decide o desfecho.** O comprimento do body do PR não tem relação estatisticamente significativa com o status final.
5. **O número de participantes é o melhor preditor do número de revisões** (ρ = 0,32), seguido pelo número de linhas adicionadas (ρ = 0,28).

---

## 5. Ameaças à Validade

### 5.1 Ameaças Internas

- **Viés de seleção:** Apenas os top-200 repositórios por stars foram analisados. Repositórios de nicho ou organizacionais privados podem apresentar padrões diferentes de code review.
- **Fatores de confusão:** A experiência do autor do PR, sua reputação no projeto, e a política específica de cada repositório não foram controladas. Contribuidores recorrentes têm maior probabilidade de merge independentemente das métricas.
- **Filtro de 1 hora:** O corte de 1h para excluir revisões automáticas pode ter removido PRs legítimos resolvidos rapidamente por revisores humanos.

### 5.2 Ameaças Externas

- **Generalização:** Os resultados valem especificamente para repositórios muito populares no GitHub. Projetos menores ou de outras plataformas podem apresentar comportamentos distintos.
- **Temporalidade:** Trata-se de um snapshot único (maio de 2026), sem análise da evolução temporal das práticas de code review.
- **Heterogeneidade:** Os 199 repositórios abrangem domínios e culturas organizacionais muito diferentes, o que aumenta a variância e pode diluir correlações específicas de contexto.

### 5.3 Ameaças de Construto

- **`body_length` como indicador de qualidade:** O número de caracteres não captura a relevância ou clareza da descrição — um body longo pode ser vago, e um curto pode ser preciso.
- **`review_count` como indicador de rigor:** O número de revisões registradas na API inclui revisões formais (APPROVED, CHANGES_REQUESTED) mas pode não capturar toda a discussão qualitativa.
- **Causalidade:** Correlações não implicam causalidade. PRs CLOSED terem mais comentários não significa que comentários causam rejeição — ambos podem ser consequência de um terceiro fator (qualidade do código).

---

## 6. Conclusão

Este estudo analisou **17.107 PRs** de **199 dos 200 repositórios mais populares** do GitHub, investigando a relação entre características dos PRs (tamanho, tempo de análise, descrição e interações) e os desfechos do processo de code review (status final e número de revisões).

O **tempo de análise** revelou-se o fator mais discriminante entre PRs aceitos e rejeitados: PRs MERGED são resolvidos em mediana de 25,8h, enquanto PRs CLOSED ficam abertos por 126,0h — quase 5× mais. Contrariando as hipóteses iniciais, PRs maiores têm ligeiramente mais chance de serem aceitos, e mais interações (participantes e comentários) estão associadas à **rejeição**, não à aceitação, sugerindo que discussão prolongada frequentemente reflete controvérsia irresolvida. A descrição do PR não influencia o desfecho final, mas PRs mais bem descritos atraem mais revisões. O número de participantes é o preditor mais forte do número de revisões (ρ = 0,32), seguido pelo volume de linhas adicionadas (ρ = 0,28).

Esses resultados desafiam a intuição de que engajamento ativo leva necessariamente à aceitação de uma contribuição e reforçam que PRs resolvidos rapidamente — focados, bem estruturados e submetidos por contribuidores com credibilidade no projeto — têm maior probabilidade de serem integrados.

**Recomendações para pesquisa futura:**
1. Analisar o conteúdo qualitativo dos comentários (positivos vs. negativos) para entender melhor o papel das interações.
2. Controlar pelo histórico do autor do PR (contribuidor frequente vs. novo) para isolar o efeito das métricas objetivas.
3. Estender a análise a plataformas alternativas (GitLab, Bitbucket) para verificar generalização.
4. Coletar dados longitudinais para analisar a evolução das práticas de code review ao longo do tempo.

---

## 7. Reprodutibilidade

### 7.1 Como Repetir o Experimento

```bash
# 1. Clone o repositório
git clone https://github.com/PauloRubinger/LAB-03.git
cd LAB-03

# 2. Crie ambiente virtual e instale dependências
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
pip install -r requirements.txt

# 3. Configure o token GitHub
cp .env.example .env
# Edite .env e adicione seu GITHUB_TOKEN

# 4. Colete a lista de repositórios
python scripts/collect_repos.py

# 5. Colete os PRs e métricas
python scripts/collect_prs.py

# 6. Analise os PRs
python scripts/analyze_data.py
```

### 7.2 Dados e Código

| Artefato | Localização |
|----------|-------------|
| Repositório | https://github.com/PauloRubinger/LAB-03 |
| Lista de repositórios | `data/raw/repos.json` |
| Dataset de PRs | `data/processed/pull_requests.csv` |
| Scripts de coleta | `scripts/` |
| Relatório final | `reports/FINAL_REPORT.md` |

---

## Referências

1. **GitHub GraphQL API v4.** Disponível em: https://docs.github.com/en/graphql

---

## Apêndices

### Apêndice A — Configurações e Parâmetros

```python
# Coleta de repositórios
query: "sort:stars"
max_repos: 200
min_prs: 100  # PRs MERGED + CLOSED

# Filtros de PRs
states: ["MERGED", "CLOSED"]
min_reviews: 1
min_analysis_hours: 1.0

# Paginação
batch_size: 50
```

### Apêndice B — Logs de Execução

**Resumo da execução:**

| Etapa | Resultado |
|-------|-----------|
| Repositórios consultados (top-200 por stars) | 200 |
| Repositórios com ≥ 100 PRs (MERGED + CLOSED) | 199 |
| Repositórios excluídos (< 100 PRs) | 1 (`ruanyf/weekly` — repositório de newsletter, sem PRs válidos) |
| PRs candidatos coletados (MERGED ou CLOSED) | ~25.000+ |
| PRs filtrados: sem revisão (`review_count = 0`) | excluídos |
| PRs filtrados: tempo de análise ≤ 1h | excluídos |
| **PRs no dataset final** | **17.107** |
| PRs MERGED no dataset final | 12.469 (72,9%) |
| PRs CLOSED no dataset final | 4.638 (27,1%) |

### Apêndice C — Ambiente de Execução

| Componente | Versão |
|------------|--------|
| Sistema Operacional | macOS / Windows |
| Python | 3.12 |
| GitHub GraphQL API | v4 |
| pandas | ≥2.0.0 |
| scipy | ≥1.10.0 |
| matplotlib | ≥3.7.0 |
| seaborn | ≥0.12.0 |
| requests | ≥2.28.0 |
| python-dotenv | ≥1.0.0 |

**Dependências Python:**

```
pandas>=2.0.0
numpy>=1.24.0
scipy>=1.10.0
matplotlib>=3.7.0
seaborn>=0.12.0
requests>=2.28.0
python-dotenv>=1.0.0
```

---

**Versão:** 2.0.0 | **Data:** 08/05/2026 | **Status:** Completo

