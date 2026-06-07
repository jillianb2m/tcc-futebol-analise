# Análise de Futebol - TCC

  Este repositório contém os scripts desenvolvidos para o Trabalho de Conclusão de Curso (TCC), com foco na análise de dados de futebol utilizando técnicas de ciência de dados e Machine Learning.

## Objetivo

  O projeto tem como objetivo explorar dados do Brasileirão para gerar insights e construir bases preparadas para modelos de análise e predição de desempenho de jogadores.

## Estrutura do Projeto

  - datasets: Dados brutos e processados  
  - scripts: Scripts auxiliares e de automação  
  - preparar_base.py: Pipeline de preparação de dados  

### Preparação de Dados

  O script preparar_base.py é responsável por consolidar e tratar os dados utilizados no projeto.

Principais etapas:
  - Unificação das bases do Brasileirão (2023, 2024 e 2025)
  - Padronização de nomes de jogadores e times
  - Remoção duplicidades
  - Filtragem de posições irrelevantes (Outros)
  - Tratamento de valores ausentes

Ao final do processamento, é gerado um dataset pronto para modelagem que pode ser encontrato no caminho: datasets/processed/brasileirao_opta_final.csv

### Execução

  python preparar_base.py

## Script Auxiliar (Colab)

### tcc-commit-github.py

  Script criado para automatizar commits e pushes diretamente do Google Colab.

### Funcionalidades:
  - Autenticação segura via Secrets do Colab
  - Configuração automática do GitHub
  - Sincronização com repositório remoto (git pull --rebase)
  - Criação de commits com mensagem dinâmica
  - Envio automático para a branch main

### Como usar:

  python %run "/content/drive/MyDrive/Colab Notebooks/tcc-commit-github.py"

### Configuração necessária

Certifique-se de configurar os seguintes Secrets no Google Colab:
  - GITHUB_REPO
  - GITHUB_USER
  - GITHUB_EMAIL
  - GITHUB_TOKEN

## Tecnologias utilizadas

  - Python
  - Pandas
  - NumPy
  - Google Colab
  - GitHub

## Observações

  - A preparação dos dados deve ser executada antes dos notebooks de modelagem  
  - Os dados foram tratados considerando características específicas do futebol  
  - O projeto pode ser expandido com novas temporadas ou variáveis