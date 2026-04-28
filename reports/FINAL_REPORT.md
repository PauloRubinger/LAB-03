# Caracterizando a Atividade de Code Review no GitHub

**Autor:** Paulo Victor Pimenta Rubinger  
**Data:** 28 de Abril de 2026  
**Versão do Relatório:** 1.0.0  
**Repositório:** https://github.com/PauloRubinger/LAB-03  
**Disciplina:** Laboratório de Experimentação de Software (6º período — Engenharia de Software)  
**Professor:** João Paulo Carneiro Aramuni  

---

## Resumo

Este experimento analisa a atividade de code review em repositórios populares do GitHub, investigando variáveis que influenciam no merge de Pull Requests (PRs). O dataset é composto por PRs submetidos aos 200 repositórios mais populares da plataforma, com status MERGED ou CLOSED, pelo menos uma revisão humana registrada e tempo de análise superior a uma hora. O estudo busca identificar relações entre características dos PRs — tamanho, tempo de análise, descrição e interações — e dois desfechos: o feedback final da revisão (MERGED vs. CLOSED) e o número de revisões realizadas.

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

> **Nota:** Esta seção será completamente preenchida na versão final do relatório (Lab03S03), após a coleta e análise completa dos dados.

### 2.1 Tipo de Estudo

- **Tipo:** Estudo observacional / correlacional
- **Unidade de análise:** Pull Request
- **Abordagem:** Análise quantitativa com técnicas estatísticas

### 2.2 Criação do Dataset

O dataset será composto por PRs coletados dos **200 repositórios mais populares** do GitHub, aplicando os seguintes critérios de filtragem:

- Status **MERGED** ou **CLOSED** (excluindo PRs abertos);
- Pelo menos **uma revisão** registrada (campo `reviews.totalCount > 0`);
- Tempo de análise **maior que uma hora** (diferença entre `createdAt` e `closedAt`/`mergedAt` > 1h), para excluir revisões automatizadas por bots ou CI/CD;
- Repositório com pelo menos **100 PRs** (MERGED + CLOSED).

### 2.3 Métricas Coletadas

| Dimensão | Métrica | Campo / Fórmula |
|----------|---------|-----------------|
| **Tamanho** | Número de arquivos alterados | `changedFiles` |
| **Tamanho** | Total de linhas adicionadas | `additions` |
| **Tamanho** | Total de linhas removidas | `deletions` |
| **Tempo de Análise** | Intervalo criação → fechamento/merge | `(closedAt - createdAt)` em horas |
| **Descrição** | Caracteres do body do PR | `len(body)` |
| **Interações** | Número de participantes | `participants.totalCount` |
| **Interações** | Número de comentários | `comments.totalCount` |
| **Desfecho** | Status do PR | `state` ∈ {MERGED, CLOSED} |
| **Desfecho** | Número de revisões | `reviews.totalCount` |

### 2.4 Método Estatístico

Para as correlações entre variáveis independentes numéricas e o número de revisões (variável dependente contínua), será utilizada a **correlação de Spearman** como teste primário, por ser adequada a distribuições não normais e relações monotônicas não necessariamente lineares — característica esperada em métricas de PR.

Para a relação entre variáveis numéricas e o status do PR (variável dependente binária: MERGED vs. CLOSED), serão comparadas as **medianas** dos grupos via teste de **Mann-Whitney U**, complementado por visualizações com boxplots.

A justificativa para a escolha do Spearman em detrimento do Pearson é que as métricas de PR (número de arquivos, linhas, comentários) tendem a apresentar distribuições fortemente assimétricas com outliers, tornando o Pearson menos robusto.

---

## 3. Resultados

> **Nota:** Esta seção será preenchida após a coleta e análise dos dados (Lab03S03).

---

## 4. Discussão

> **Nota:** Esta seção será preenchida após a análise dos resultados (Lab03S03).

---

## 5. Ameaças à Validade

> **Nota:** Esta seção será preenchida na versão final do relatório (Lab03S03).

---

## 6. Conclusão

> **Nota:** Esta seção será preenchida na versão final do relatório (Lab03S03).

---

**Versão:** 1.0.0 | **Data:** 28/04/2026 | **Status:** Em elaboração (Lab03S02 — Hipóteses iniciais)
