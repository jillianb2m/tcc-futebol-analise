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
- Meia Central: keyPass, goalAssist, goals, totalShots, ballRecovery, interceptionWon, wonTackle, possessionLostCtrl (combinação "sem_volume" - 8 variáveis)

**Análise de resultados:**
- Identificação de perfis de clusters com nomenclatura em português (Meia de Apoio, Meia atacante, Meia contenção)
- Visualização 2D e 3D dos clusters
- Análise de variância (ANOVA) para validar diferenciação entre clusters
- Interpretação de perfis com jogadores representativos
- **Tabela de centróides** - Comportamento médio dos jogadores por cluster
- **Tabela de distribuição** - Quantidade de jogadores alocados por cluster
- **Tabela estatística detalhada** - Média, mediana e desvio padrão das variáveis por cluster
- **Análise detalhada do Cluster 0** - Top 10 jogadores e características específicas

**Metodologia de escolha de k e métricas:**
- Validação através de métodos Elbow e Silhouette
- Análise de sensibilidade de diferentes combinações de métricas
- Combinação "sem_volume" para Meia Central (remoção de totalPass, accuratePass, touches)
- Justificativa: Foco em métricas qualitativas que diferenciam melhor os perfis de meias

### 4. Gap Analysis (Análise de Lacunas)

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

## Nomenclatura e Tradução

Todas as variáveis e métricas foram traduzidas para português para facilitar a interpretação:

**Variáveis principais:**
- keyPass → Passes-chave
- goalAssist → Assistências
- goals → Gols
- totalShots → Finalizações
- totalPass → Total de passes
- accuratePass → Passes certos
- touches → Toques na bola
- ballRecovery → Recuperações de bola
- interceptionWon → Interceptações
- wonTackle → Desarmes Ganhos
- possessionLostCtrl → Perdas de posse

**Nomes dos clusters:**
- Cluster 0 → Meia de Apoio
- Cluster 1 → Meia atacante
- Cluster 2 → Meia contenção

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

## Caso de Estudo: Meia Central

**Objetivo:** Identificar perfis de meias centrais para análise tática e recomendações de contratação

**Metodologia aplicada:**
1. **Seleção de métricas:** Combinação "sem_volume" (8 variáveis qualitativas)
2. **Determinação de k:** Métodos Elbow e Silhouette (ambos sugeriram k=3)
3. **Validação estatística:** ANOVA para confirmar diferenciação significativa entre clusters
4. **Nomenclatura:** Termos de futebol em português (Meia de Apoio, Meia atacante, Meia contenção)

**Resultados obtidos:**
- **Cluster 0 (41.2%):** Meia de Apoio - jogadores com participação limitada
- **Cluster 1 (17.3%):** Meia atacante - jogadores ofensivos com alta produção
- **Cluster 2 (41.5%):** Meia contenção - jogadores defensivos com alto recuperação

**Justificativa para k=3:**
- Consistência entre métodos Elbow e Silhouette
- Separação clara entre perfis ofensivos e defensivos
- Interpretação tática válida para contexto do futebol brasileiro

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

**Tabelas de Análise:**
- `tabela_centroides_kmeans.csv`: Comportamento médio dos jogadores por cluster (centróides)
- `tabela_distribuicao_clusters_kmeans.csv`: Quantidade de jogadores alocados por cluster
- `tabela_estatistica_clusters_formatada.csv`: Tabela estatística detalhada (média, mediana, desvio padrão) por cluster
- `tabela_estatistica_clusters_completa.csv`: Tabela estatística completa com todas as métricas

**Gap Analysis:**
- `gap_analysis_[time].png`: Relatório visual de gaps
- `recomendacoes_[time].png`: Gráfico de recomendações de contratação

## Observações

- A preparação dos dados deve ser executada antes da análise de clustering
- Os dados foram tratados considerando características específicas do futebol brasileiro
- O projeto pode ser expandido com novas temporadas, ligas ou variáveis
- A análise de gaps requer dados de benchmarks para comparação
- O sistema de recomendação considera pesos específicos por posição e métrica
- Para Meia Central, a combinação "sem_volume" (8 variáveis) foi validada estatisticamente
