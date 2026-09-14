# Análise de Futebol - TCC

Este repositório contém os scripts desenvolvidos para o Trabalho de Conclusão de Curso (TCC), com foco na análise de dados de futebol utilizando técnicas de ciência de dados e Machine Learning.

## Objetivo

O projeto tem como objetivo explorar dados do Brasileirão para gerar insights táticos, identificar perfis de jogadores através de clustering, e realizar análise de gaps para recomendações de contratação.

## Estrutura do Projeto

- `datasets/`: Dados brutos e processados
- `src/`: Scripts auxiliares e de automação
- `tcc_ml_futebol.ipynb`: Notebook principal para Google Colab

## Funcionalidades Principais

### 1. Coleta de Dados (SofaScore)

Extração de dados do Brasileirão Série A (2023-2025) através da API do SofaScore:
- Coleta de estatísticas detalhadas de jogadores por rodada
- Identificação de posições táticas via coordenadas Opta (Avg_X, Avg_Y)
- Mapeamento de siglas táticas para posições em português
- Geração de arquivos CSV organizados por temporada

### 2. Análise Exploratória de Dados

- Distribuição de jogadores por posição
- Análise descritiva das variáveis de desempenho
- Visualização através de boxplots e gráficos
- Filtragem de jogadores com mínimo de jogos (padrão: 5 jogos)

### 3. Clustering de Jogadores

Implementação de algoritmos de clustering para identificar perfis de jogadores:

**Algoritmos disponíveis:**
- K-Means
- Clustering Hierárquico (Complete e Average Linkage)

**Métodos de determinação de clusters:**
- Método Elbow
- Análise de Silhouette

**Métricas específicas por posição:**
- Goleiro: ballRecovery, aerialWon, totalPass, accuratePass
- Zagueiro: aerialWon, interceptionWon, totalTackle, ballRecovery
- Volante: totalTackle, interceptionWon, ballRecovery, totalPass, accuratePass
- Meia Central: keyPass, goalAssist, goals, totalShots, totalPass, accuratePass, touches

**Análise de resultados:**
- Identificação de perfis de clusters (Criador, Finalizador, Defensivo, etc.)
- Visualização 2D e 3D dos clusters
- Análise de variância (ANOVA) para validar diferenciação entre clusters
- Interpretação de perfis com jogadores representativos

### 4. Gap Analysis (Identificação de Lacunas)

Sistema de análise de desvios para identificar carências do elenco:

**Metodologia:**
- Definição de benchmarks (top 5 times por rating médio)
- Cálculo de desvios por métrica técnica entre time alvo e benchmarks
- Classificação de severidade de gaps (Crítico, Alto, Moderado, Adequado)
- Sistema de pontuação ponderada por posição e métrica

**Funcionalidades:**
- Identificação de posições com maiores carências
- Mapeamento de gaps para perfis de clusters
- Recomendação de perfis de jogadores para contratação
- Priorização de contratações (Alta, Média, Baixa)
- Justificativa tática para cada recomendação

**Visualizações:**
- Heatmap de gaps por posição e métrica
- Gráfico dos maiores gaps (deficiências)
- Distribuição de severidade de gaps
- Gráfico de recomendações de contratação

## Preparação de Dados

O pipeline de dados consolida e trata as informações utilizadas no projeto:

**Etapas principais:**
- Unificação das bases do Brasileirão (2023, 2024 e 2025)
- Padronização de nomes de jogadores e times
- Remoção de duplicidades
- Filtragem de posições irrelevantes (Outros)
- Tratamento de valores ausentes
- Agregação de estatísticas por jogador e posição

**Dataset final:** `datasets/processed/brasileirao_opta_final.csv`

## Execução

### Ambiente Local

```bash
# Executar análise completa
python tcc_ml_futebol.py

# Executar clustering para posição específica
python tcc_ml_futebol.py  # O script pode ser adaptado para posições específicas
```

### Google Colab

```python
# No notebook tcc_ml_futebol.ipynb
main('Meia Central')  # Clustering para posição específica
main()  # Clustering geral
```

## Configurações

Parâmetros configuráveis no script principal:

```python
CONFIG = {
    'MIN_JOGOS': 5,                    # Mínimo de jogos para análise
    'N_CLUSTERS_MAX': 10,              # Máximo de clusters para análise
    'METODO_LINKAGE': 'complete',      # Método de linkage hierárquico
    'METODO_PADRONIZAR': 'sklearn',    # Método de padronização
    'RANDOM_STATE': 100                # Semente para reprodutibilidade
}
```

## Tecnologias Utilizadas

- **Python**: Linguagem principal
- **Pandas**: Manipulação de dados
- **NumPy**: Operações numéricas
- **Scikit-learn**: Algoritmos de clustering e pré-processamento
- **SciPy**: Análise hierárquica e estatística
- **Pingouin**: Análise estatística (ANOVA)
- **Matplotlib/Seaborn**: Visualização de dados
- **Plotly**: Visualizações interativas 3D
- **Requests**: Extração de dados via API (SofaScore)
- **Google Colab**: Ambiente de desenvolvimento

## Metodologia Científica

O projeto segue abordagem baseada em Sumpter (2016) para:
- Identificação de padrões através de modelos matemáticos
- Análise objetiva de desempenho tático
- Comparação sistemática com benchmarks
- Detecção de lacunas táticas específicas

## Estrutura de Saída

Arquivos gerados durante a execução:

**Visualizações:**
- `distribuicao_posicoes.png`: Distribuição de jogadores por posição
- `boxplot_analise_exploratoria.png`: Análise exploratória das variáveis
- `metodo_elbow.png`: Gráfico do método Elbow
- `metodo_silhouette.png`: Gráfico de análise de Silhouette
- `dendrograma_complete.png`: Dendrograma (Complete Linkage)
- `dendrograma_average.png`: Dendrograma (Average Linkage)
- `clusters_kmeans.png`: Visualização 2D dos clusters K-Means
- `clusters_3d.html`: Visualização interativa 3D

**Gap Analysis:**
- `gap_analysis_[time].png`: Relatório visual de gaps
- `recomendacoes_[time].png`: Gráfico de recomendações de contratação

## Observações

- A preparação dos dados deve ser executada antes da análise de clustering
- Os dados foram tratados considerando características específicas do futebol brasileiro
- O projeto pode ser expandido com novas temporadas, ligas ou variáveis
- A análise de gaps requer dados de benchmarks para comparação
- O sistema de recomendação considera pesos específicos por posição e métrica

## Próximos Passos

- Implementação de modelo preditivo para recomendação de jogadores
- Expansão para outras ligas e competições
- Integração com dados de mercado de transferências
- Desenvolvimento de interface para visualização interativa
