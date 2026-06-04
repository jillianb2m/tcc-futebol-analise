import pandas as pd
import traceback
import unicodedata

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
    #for i, df in enumerate(dataframes, 1):
        #print(f"Dataset {i} ({2022+i}): {len(df.columns)} colunas")
    
    # Encontrar colunas em comum
    colunas_comuns = set(dataframes[0].columns)
    for df in dataframes[1:]:
        colunas_comuns = colunas_comuns.intersection(set(df.columns))
    
    colunas_comuns = sorted(list(colunas_comuns))
    #print(f"Colunas em comum: {len(colunas_comuns)}")
    
    # Verificar diferenças
    todas_colunas = set()
    for df in dataframes:
        todas_colunas = todas_colunas.union(set(df.columns))
    
    #colunas_diferentes = todas_colunas - set(colunas_comuns)
    #if colunas_diferentes:
        #print(f"Colunas diferentes: {colunas_diferentes}")
    
    # Manter apenas colunas em comum na ordem do primeiro dataset
    ordem_colunas = [col for col in dataframes[0].columns if col in colunas_comuns]
    
    #print(f"Ordem final: {len(ordem_colunas)} colunas")
    
    return ordem_colunas

# Agrupa os dataframes em um dataframe
def agrupar_dataframes(dataframes, ordem_colunas):
    
    # Alinhar
    dataframes_alinhados = []
    for i, df in enumerate(dataframes, 1):
        df_alinhado = df[ordem_colunas].copy()
        dataframes_alinhados.append(df_alinhado)
        #print(f"Dataset {i}: {len(df_alinhado.columns)} colunas após alinhamento")
    
    # Unir
    df_unido = pd.concat(dataframes_alinhados, ignore_index=True)
    
    print(f"\nTotal de registros: {len(df_unido):,}")
    print(f"Total de colunas: {len(df_unido.columns)}")
    
    # Remover duplicatas
    duplicatas = df_unido.duplicated().sum()
    print(f"Linhas duplicadas: {duplicatas:,}")
    
    if duplicatas > 0:
        df_unido = df_unido.drop_duplicates()
        print(f"Duplicatas removidas: {len(df_unido):,} linhas restantes")
    
    return df_unido

def tratar_caracteres_especiais(texto):

    if pd.isna(texto) or texto is None:
        return texto
    
    # Converter para string se não for
    if not isinstance(texto, str):
        texto = str(texto)
    
    # Normalizar caracteres Unicode (remove acentos)
    texto_normalizado = unicodedata.normalize('NFKD', texto)
    
    # Remover caracteres especiais, manter apenas ASCII básico
    texto_limpo = ''.join(
        char for char in texto_normalizado 
        if unicodedata.category(char) != 'Mn' and char.isprintable()
    )
    
    # Substituir caracteres problemáticos por equivalentes simples
    substituicoes = {
        'ç': 'c', 'ñ': 'n', 'ý': 'y', 'ÿ': 'y',
        'â': 'a', 'ã': 'a', 'á': 'a', 'à': 'a', 'ä': 'a', 'å': 'a',
        'ê': 'e', 'é': 'e', 'è': 'e', 'ë': 'e',
        'î': 'i', 'í': 'i', 'ì': 'i', 'ï': 'i',
        'ô': 'o', 'õ': 'o', 'ó': 'o', 'ò': 'o', 'ö': 'o', 'ø': 'o',
        'û': 'u', 'ú': 'u', 'ù': 'u', 'ü': 'u',
        'Â': 'A', 'Ã': 'A', 'Á': 'A', 'À': 'A', 'Ä': 'A', 'Å': 'A',
        'Ê': 'E', 'É': 'E', 'È': 'E', 'Ë': 'E',
        'Î': 'I', 'Í': 'I', 'Ì': 'I', 'Ï': 'I',
        'Ô': 'O', 'Õ': 'O', 'Ó': 'O', 'Ò': 'O', 'Ö': 'O', 'Ø': 'O',
        'Û': 'U', 'Ú': 'U', 'Ù': 'U', 'Ü': 'U'
    }
    
    # Aplicar substituições
    for original, substituto in substituicoes.items():
        texto_limpo = texto_limpo.replace(original, substituto)
    
    # Remover caracteres especiais restantes (exceto espaços e hífens básicos)
    texto_final = ''.join(
        char for char in texto_limpo 
        if char.isalnum() or char in (' ', '-', '_')
    )
    
    # Limpar espaços extras
    texto_final = ' '.join(texto_final.split())
    
    return texto_final


# Trata caracteres especiais dos nomes dos jogadores e times
def tratar_nomes_jogadores_times(dataframes):
    
    dataframes_tratados = []
    
    for i, df in enumerate(dataframes, 1):
        
        df_tratado = df.copy()
        
        # Tratar coluna Jogador
        if 'Jogador' in df_tratado.columns:
            exemplos_antes = df_tratado['Jogador'].dropna().head(3).tolist()
            #print(f"  Jogadores (antes): {exemplos_antes}")
            
            df_tratado['Jogador'] = df_tratado['Jogador'].apply(tratar_caracteres_especiais)
            
            exemplos_depois = df_tratado['Jogador'].dropna().head(3).tolist()
            #print(f"  Jogadores (depois): {exemplos_depois}")
        
        # Tratar coluna Time
        if 'Time' in df_tratado.columns:
            exemplos_antes = df_tratado['Time'].dropna().head(3).tolist()
            #print(f"  Times (antes): {exemplos_antes}")
            
            df_tratado['Time'] = df_tratado['Time'].apply(tratar_caracteres_especiais)
            
            exemplos_depois = df_tratado['Time'].dropna().head(3).tolist()
            #print(f"  Times (depois): {exemplos_depois}")
        
        dataframes_tratados.append(df_tratado)
    
    return dataframes_tratados

# Remover Posição Real 'Outro'
def remover_posicao_outros(df_agrupado):  

    # Verificar valores únicos em Posicao_Real
    if 'Posicao_Real' in df_agrupado.columns:
        valores_unicos = df_agrupado['Posicao_Real'].value_counts()

        for posicao, count in valores_unicos.items():
            print(f"  {posicao}: {count:,} ({count/len(df_agrupado)*100:.1f}%)")
        
        # Remover 'Outro'
        total_antes = len(df_agrupado)
        df_filtrado = df_agrupado[df_agrupado['Posicao_Real'] != 'Outro'].copy()
        total_depois = len(df_filtrado)
        
        print(f"\nRemovidos: {total_antes - total_depois:,} registros")
        print(f"Restantes: {total_depois:,} registros")
        print(f"Redução: {(1 - total_depois/total_antes)*100:.1f}%")
        
        return df_filtrado
    else:
        print("Coluna 'Posicao_Real' não encontrada")
        return df_agrupado

def main():
  try:
    # 1º Carregar os 3 datasets em um mesmo dataframe
    dataframes = carregar_dados();

    if dataframes is None:
      return None

    print(f"\n--- Resumo da Bases ---")

    for i, df in enumerate(dataframes):
      print(f"\nBase {i+1}")
      print(f"Shape: {df.shape}")

    print("----------------------")

    # 2º Tratar caracteres especiais
    dataframes_tratados = tratar_nomes_jogadores_times(dataframes)

    # 3º Analisar estrutura de colunas
    ordem_colunas = analisar_estrutura_colunas(dataframes_tratados)

    # 4º Agrupar dataframes
    dataframes_agrupados = agrupar_dataframes(dataframes_tratados, ordem_colunas)
    #print(dataframes_agrupados.head())

    df_base_tratada = remover_posicao_outros(dataframes_agrupados)

    return dataframes_agrupados

  except Exception as e:
    print(f"\nErro no processamento: {e}")
    traceback.print_exc()
    return None

if __name__ == "__main__":
  dataset_base = main()

