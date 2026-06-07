import pandas as pd
import traceback
import unicodedata
import numpy as np

# Esconde o aviso de SettingWithCopy de uma vez por todas
pd.options.mode.chained_assignment = None

def carregar_dados():
  arquivos = [
    '/content/tcc-futebol-analise/datasets/sofascore/brasileirao_2023_opta_final.csv',
    '/content/tcc-futebol-analise/datasets/sofascore/brasileirao_2024_opta_final.csv', 
    '/content/tcc-futebol-analise/datasets/sofascore/brasileirao_2025_opta_final.csv'
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

def resolver_valores_ausentes(df):
    
    ausentes_antes = df.isnull().sum()
    total_ausentes_antes = ausentes_antes.sum()
    print(f"Total de valores ausentes: {total_ausentes_antes:,}")
    
    colunas_criticas = ['Jogador', 'Time', 'Posicao_Real', 'minutesPlayed', 'rating']
    
    df_limpo = df.dropna(subset=colunas_criticas)
    
    print(f"Linhas removidas (colunas críticas): {len(df) - len(df_limpo)}")
    
    colunas_numericas = df_limpo.select_dtypes(include=[np.number]).columns.tolist()
    
    for col in colunas_criticas:
        if col in colunas_numericas:
            colunas_numericas.remove(col)
    
    acoes_jogo = ['totalPass', 'accuratePass', 'totalLongBalls', 'accurateLongBalls',
                  'totalCross', 'accurateCross', 'totalShots', 'goals', 'totalTackle',
                  'interceptionWon', 'ballRecovery', 'totalClearance', 'keyPass',
                  'goalAssist', 'aerialWon', 'duelWon', 'touches', 'saves',
                  'blockedScoringAttempt', 'shotOffTarget', 'onTargetScoringAttempt']
    
    acoes_jogo_existentes = [col for col in acoes_jogo if col in colunas_numericas]
    
    if acoes_jogo_existentes:
      df_limpo.loc[:, acoes_jogo_existentes] = df_limpo[acoes_jogo_existentes].fillna(0)
      print(f"Ações de jogo ({len(acoes_jogo_existentes)} colunas): preenchidas com 0")
    
    coordenadas = ['Avg_X', 'Avg_Y']
    coordenadas_existentes = [col for col in coordenadas if col in colunas_numericas]
    
    if coordenadas_existentes:
        for coord in coordenadas_existentes:
            media_por_posicao = df_limpo.groupby('Posicao_Real')[coord].median()
            df_limpo[coord] = df_limpo.apply(
                lambda row: row[coord] if pd.notna(row[coord]) else media_por_posicao.get(row['Posicao_Real'], df_limpo[coord].median()),
                axis=1
            )
        print(f"Coordenadas espaciais ({len(coordenadas_existentes)} colunas): preenchidas com média por posição")
    
    ratings = ['rating']
    ratings_existentes = [col for col in ratings if col in colunas_numericas]
    
    if ratings_existentes:
        for rating_col in ratings_existentes:
            mediana_rating = df_limpo[rating_col].median()
            df_limpo[rating_col] = df_limpo[rating_col].fillna(mediana_rating)
        print(f"Ratings ({len(ratings_existentes)} colunas): preenchidos com mediana")
    
    colunas_restantes = [col for col in colunas_numericas 
                        if col not in acoes_jogo_existentes + coordenadas_existentes + ratings_existentes]
    
    if colunas_restantes:
        df_limpo[colunas_restantes] = df_limpo[colunas_restantes].fillna(0)
        print(f"Demais colunas ({len(colunas_restantes)}): preenchidas com 0")
    
    ausentes_depois = df_limpo.isnull().sum()
    total_ausentes_depois = ausentes_depois.sum()
    print(f"Valores ausentes após tratamento: {total_ausentes_depois}")
    
    return df_limpo

def resumo_estrutura_final(df):
    print(f"Total de registros: {len(df):,}")
    print(f"Total de colunas: {len(df.columns)}")
    print(f"Período: {df['Temporada'].min()} - {df['Temporada'].max()}")
    
    times_unicos = df['Time'].nunique()
    print(f"Times únicos: {times_unicos}")
    
    jogadores_unicos = df['Jogador'].nunique()
    print(f"Jogadores únicos: {jogadores_unicos}")
    
    posicoes_unicas = df['Posicao_Real'].nunique()
    print(f"Posições únicas: {posicoes_unicas}")
    
    print(f"\nDistribuição por posição:")
    dist_posicao = df['Posicao_Real'].value_counts()
    for posicao, count in dist_posicao.items():
        print(f"  {posicao}: {count:,} ({count/len(df)*100:.1f}%)")
    
    print(f"\nEstatística dos jogadores (min):")
    print(f"Média: {df['minutesPlayed'].mean():.1f}")
    print(f"Mediana: {df['minutesPlayed'].median():.1f}")
    print(f"Mínimo: {df['minutesPlayed'].min():.1f}")
    print(f"Máximo: {df['minutesPlayed'].max():.1f}")

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

    # 5º Remover Posição Real 'Outros'
    df_base_tratada = remover_posicao_outros(dataframes_agrupados)

    # 6º Resolver valores ausentes
    df_final = resolver_valores_ausentes(df_base_tratada)

    # 7º Resumo da estrutura final do dataset
    resumo_estrutura_final(df_final);

    # 8º Criar arquivo tratado e processado
    caminho_exportacao = '/content/tcc-futebol-analise/datasets/processed/brasileirao_opta_final.csv'
    
    df_final.to_csv(caminho_exportacao, index=False)
    print(f"\nBase final exportada com sucesso para: {caminho_exportacao}")

    return df_final

  except Exception as e:
    print(f"\nErro no processamento: {e}")
    traceback.print_exc()
    return None

if __name__ == "__main__":
  dataset_base = main()