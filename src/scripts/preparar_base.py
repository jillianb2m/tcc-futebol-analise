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

def main():
  try:
    dataframes = carregar_dados();

    if dataframes is None:
      return None

    for i, df in enumerate(dataframes):
      print(f"\n--- Resumo da Base {i+1} ---")
      print(df.shape)

    return dataframes

  except Exception as e:
    print(f"\nErro no processamento: {e}")
    traceback.print_exc()
    return None

if __name__ == "__main__":
  dataset_base = main()

