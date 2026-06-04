import pandas as pd
import traceback

def carregar_dados():
  arquivos = [
    'datasets/sofascore/brasileirao_2023_opta_final.csv',
    'datasets/sofascore/brasileirao_2024_opta_final.csv', 
    'datasets/sofascore/brasileirao_2025_opta_final.csv'
  ]

  dataframes = []

  for arquivo in arquivos:
    try:
      df = pd.read_csv(arquivo)      
      dataframes.append(df)
    except Exception as e:
      print(f"Erro ao carregar {arquivo}: {e}")
      return None
  return dataframes

## Verifica ordem das colunas dos datasets
## Define ordem das colunas para o dataset principal
def analisar_estrutura_colunas(dataframes):
    
    # Verificar colunas de cada arquivo
    for i, df in enumerate(dataframes, 1):
        print(f"Dataset {i} ({2022+i}): {len(df.columns)} colunas")
    
    # Encontrar colunas em comum
    colunas_comuns = set(dataframes[0].columns)
    for df in dataframes[1:]:
        colunas_comuns = colunas_comuns.intersection(set(df.columns))
    
    colunas_comuns = sorted(list(colunas_comuns))
    print(f"Colunas em comum: {len(colunas_comuns)}")
    
    # Verificar diferenças
    todas_colunas = set()
    for df in dataframes:
        todas_colunas = todas_colunas.union(set(df.columns))
    
    colunas_diferentes = todas_colunas - set(colunas_comuns)
    if colunas_diferentes:
        print(f"Colunas diferentes: {colunas_diferentes}")
    
    # Manter apenas colunas em comum na ordem do primeiro dataset
    ordem_colunas = [col for col in dataframes[0].columns if col in colunas_comuns]
    
    print(f"Ordem final: {len(ordem_colunas)} colunas")
    
    return ordem_colunas

# Agrupa os dataframes em um dataframe
def agrupar_dataframes(dataframes, ordem_colunas):
    
    # Alinhar
    dataframes_alinhados = []
    for i, df in enumerate(dataframes, 1):
        df_alinhado = df[ordem_colunas].copy()
        dataframes_alinhados.append(df_alinhado)
        print(f"Dataset {i}: {len(df_alinhado.columns)} colunas após alinhamento")
    
    # Unir
    df_unido = pd.concat(dataframes_alinhados, ignore_index=True)
    
    print(f"\nTotal de registros unidos: {len(df_unido):,}")
    print(f"Total de colunas: {len(df_unido.columns)}")
    
    # Remover duplicatas
    duplicatas = df_unido.duplicated().sum()
    print(f"Linhas duplicadas: {duplicatas:,}")
    
    if duplicatas > 0:
        df_unido = df_unido.drop_duplicates()
        print(f"Duplicatas removidas: {len(df_unido):,} linhas restantes")
    
    return df_unido

# Trata caracteres especiais dos nomes dos jogadores e times
def tratar_caracteres_especiais(dataframes):
    
    dataframes_tratados = []
    
    for i, df in enumerate(dataframes, 1):
        print(f"Tratando Dataset {i}...")
        
        df_tratado = df.copy()
        
        # Tratar coluna Jogador
        if 'Jogador' in df_tratado.columns:
            exemplos_antes = df_tratado['Jogador'].dropna().head(3).tolist()
            print(f"  Jogadores (antes): {exemplos_antes}")
            
            df_tratado['Jogador'] = df_tratado['Jogador'].apply(tratar_caracteres_especiais)
            
            exemplos_depois = df_tratado['Jogador'].dropna().head(3).tolist()
            print(f"  Jogadores (depois): {exemplos_depois}")
        
        # Tratar coluna Time
        if 'Time' in df_tratado.columns:
            exemplos_antes = df_tratado['Time'].dropna().head(3).tolist()
            print(f"  Times (antes): {exemplos_antes}")
            
            df_tratado['Time'] = df_tratado['Time'].apply(tratar_caracteres_especiais)
            
            exemplos_depois = df_tratado['Time'].dropna().head(3).tolist()
            print(f"  Times (depois): {exemplos_depois}")
        
        dataframes_tratados.append(df_tratado)
        print(f"  ✅ Dataset {i} tratado")
    
    return dataframes_tratados

def main():
  try:
    # 1º Carregar os 3 datasets em um mesmo dataframe
    dataframes = carregar_dados();

    if dataframes is None:
      return None

    for i, df in enumerate(dataframes):
      print(f"\n--- Resumo da Base {i+1} ---")
      print(df.shape)

    # 2º Analisar estrutura de colunas
    ordem_colunas = analisar_estrutura_colunas(dataframes)

    # 3º Agrupar dataframes
    dataframes_agrupados = agrupar_dataframes(dataframes, ordem_colunas)

    # 4º Tratar caracteres especiais
    # dataframes_tratados = tratar_caracteres_especiais(dataframes_agrupados)

    return dataframes_agrupados

  except Exception as e:
    print(f"\nErro no processamento: {e}")
    traceback.print_exc()
    return None

if __name__ == "__main__":
  dataset_base = main()

