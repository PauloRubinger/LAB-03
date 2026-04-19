# LAB-03 – Caracterizando a Atividade de Code Review no GitHub

## Descrição

Este laboratório analisa a atividade de **code review** em repositórios populares do GitHub, identificando variáveis que influenciam no merge de Pull Requests (PRs). O estudo coleta dados dos **200 repositórios mais populares** (com pelo menos 100 PRs) e avalia PRs com status MERGED ou CLOSED que passaram por pelo menos uma revisão humana (tempo de análise ≥ 1 hora).

## Questões de Pesquisa

### A. Feedback Final das Revisões (Status do PR)

| # | Questão |
|---|---------|
| RQ01 | Qual a relação entre o **tamanho** dos PRs e o feedback final das revisões? |
| RQ02 | Qual a relação entre o **tempo de análise** dos PRs e o feedback final das revisões? |
| RQ03 | Qual a relação entre a **descrição** dos PRs e o feedback final das revisões? |
| RQ04 | Qual a relação entre as **interações** nos PRs e o feedback final das revisões? |

### B. Número de Revisões

| # | Questão |
|---|---------|
| RQ05 | Qual a relação entre o **tamanho** dos PRs e o número de revisões realizadas? |
| RQ06 | Qual a relação entre o **tempo de análise** dos PRs e o número de revisões realizadas? |
| RQ07 | Qual a relação entre a **descrição** dos PRs e o número de revisões realizadas? |
| RQ08 | Qual a relação entre as **interações** nos PRs e o número de revisões realizadas? |

## Métricas

| Dimensão | Métricas |
|----------|----------|
| Tamanho | Número de arquivos alterados; total de linhas adicionadas e removidas |
| Tempo de Análise | Intervalo entre criação do PR e última atividade (merge/close) |
| Descrição | Número de caracteres do body do PR (markdown) |
| Interações | Número de participantes; número de comentários |

## Estrutura do Projeto

```
LAB-03/
├── scripts/
├── data/
│   ├── repos.json            # Lista de repositórios selecionados (gerado)
│   └── pull_requests.csv     # Dataset de PRs com métricas (gerado)
├── reports/
│   ├── figures/              # Gráficos gerados pela análise
│   └── summary_stats.csv     # Tabela resumo de estatísticas (gerado)
├── .env.example              # Exemplo de configuração do token GitHub
├── .gitignore
├── requirements.tx
└── README.md
```

## Pré-requisitos

- Python 3.8+
- Token de acesso pessoal do GitHub (com escopo `public_repo`)

## Instalação e Configuração

```bash
# 1. Clonar o repositório e entrar na pasta
cd LAB-03

# 2. Criar ambiente virtual (recomendado)
python -m venv .venv
# Windows:
.venv\Scripts\activate
# Linux/macOS:
source .venv/bin/activate

# 3. Instalar dependências
pip install -r requirements.txt

# 4. Configurar token do GitHub
cp .env.example .env
# Edite o arquivo .env e insira seu token
```

### Criando o Token do GitHub

1. Acesse [GitHub Settings → Tokens](https://github.com/settings/tokens)
2. Clique em **"Generate new token (classic)"**
3. Selecione o escopo `public_repo`
4. Copie o token gerado e cole no arquivo `.env`


## Processo de Desenvolvimento

| Sprint | Entrega | Pontos |
|--------|---------|--------|
| Lab03S01 | Lista de repositórios + Script de coleta de PRs e métricas | 5 |
| Lab03S02 | Dataset completo + Primeira versão do relatório com hipóteses | 5 |
| Lab03S03 | Análise/visualização de dados + Relatório final | 10 |