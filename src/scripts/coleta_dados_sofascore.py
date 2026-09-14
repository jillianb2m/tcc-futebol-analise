# -*- coding: utf-8 -*-
"""
Pipeline de Extração de Dados do Brasileirão - SofaScore
Extrai dados completos dos jogadores com identificação de posição via coordenadas Opta
Anos: 2023, 2024, 2025
"""

import requests
import pandas as pd
import time
import urllib3

# Desabilitar avisos SSL
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Configurações da API do SofaScore
TOURNAMENT_ID = 325  # ID do Brasileirão Série A
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
    "Referer": "https://www.sofascore.com/"
}

# Mapeamento de IDs de temporada do Brasileirão Série A
SEASONS_INFO = [
    {'ano': '2025', 'id': 72034},
    {'ano': '2024', 'id': 58766},
    {'ano': '2023', 'id': 48982}
]

# Mapeamento de siglas táticas para posições em português
MAPEAMENTO_TATICO = {
    'ST': 'Centroavante', 'LW': 'Ponta Esquerda', 'RW': 'Ponta Direita',
    'AM': 'Meia Atacante', 'ML': 'Meia Esquerda', 'MC': 'Meia Central',
    'MR': 'Meia Direita', 'DM': 'Volante',
    'DL': 'Lateral Esquerdo', 'DC': 'Zagueiro', 'DR': 'Lateral Direito',
    'GK': 'Goleiro'
}


def identificar_posicao_opta(x, y):
    """
    Identifica posição tática baseada em coordenadas médias Opta.
    
    Args:
        x: Coordenada X (profundidade, 0-100)
        y: Coordenada Y (largura, 0-100)
    
    Returns:
        Sigla da posição tática (GK, DC, DM, MC, ST, etc.)
    """
    if x is None or y is None:
        return "N/A"
    
    # Eixo X: Profundidade (0-100) | Eixo Y: Largura (0-100)
    if x < 15:
        return "GK"
    if 15 <= x < 38:
        if 30 <= y <= 70:
            return "DC"
        return "DL" if y < 30 else "DR"
    if 38 <= x < 65:
        if 30 <= y <= 70:
            return "DM" if x < 52 else "MC"
        return "ML" if y < 30 else "MR"
    if 65 <= x < 82:
        if 30 <= y <= 70:
            return "AM"
        return "LW" if y < 30 else "RW"
    if x >= 82:
        if 30 <= y <= 70:
            return "ST"
        return "LW" if y < 30 else "RW"
    return "MC"


def get_average_positions(match_id):
    """
    Busca coordenadas médias dos jogadores em uma partida.
    
    Args:
        match_id: ID da partida
    
    Returns:
        Dicionário com coordenadas {player_id: {'x': avg_x, 'y': avg_y}}
    """
    url = f"https://api.sofascore.com/api/v1/event/{match_id}/average-positions"
    try:
        r = requests.get(url, headers=HEADERS, verify=False, timeout=10)
        if r.status_code == 200:
            data = r.json()
            coords = {}
            for side in ['home', 'away']:
                players_list = data.get(side, [])
                for p in players_list:
                    # Converter ID para string para consistência
                    p_id = str(p.get('player', {}).get('id'))
                    if p_id:
                        coords[p_id] = {
                            'x': p.get('averageX'),
                            'y': p.get('averageY')
                        }
            return coords
    except Exception as e:
        print(f"Erro ao buscar coordenadas: {e}")
    return {}


def extrair_dados_temporada(season_info):
    """
    Extrai dados completos de uma temporada específica.
    
    Args:
        season_info: Dicionário com 'ano' e 'id' da temporada
    
    Returns:
        DataFrame com dados extraídos ou None se falhar
    """
    ano = season_info['ano']
    s_id = season_info['id']
    
    print(f"\n--- Extraindo Temporada {ano} (ID Sofa: {s_id}) ---")
    
    all_players_data = []
    
    # Percorre as 38 rodadas do Brasileirão
    for round_num in range(1, 39):
        print(f"Processando Rodada {round_num}/38", end="\r")
        url_round = f"https://api.sofascore.com/api/v1/unique-tournament/{TOURNAMENT_ID}/season/{s_id}/events/round/{round_num}"
        
        try:
            res_round = requests.get(url_round, headers=HEADERS, verify=False, timeout=10)
            events = res_round.json().get('events', [])
            
            for match in events:
                m_id = match['id']
                
                # Buscar coordenadas médias e escalações
                coords = get_average_positions(m_id)
                res_lineup = requests.get(
                    f"https://api.sofascore.com/api/v1/event/{m_id}/lineups",
                    headers=HEADERS,
                    verify=False,
                    timeout=10
                )
                
                if res_lineup.status_code == 200:
                    lineup_json = res_lineup.json()
                    
                    for side in ['home', 'away']:
                        for p in lineup_json.get(side, {}).get('players', []):
                            stats = p.get('statistics', {})
                            
                            if stats:
                                p_obj = p.get('player', {})
                                p_id_raw = p_obj.get('id')
                                
                                if p_id_raw:
                                    p_id_str = str(p_id_raw)
                                    c = coords.get(p_id_str, {'x': None, 'y': None})
                                    
                                    avg_x = c.get('x')
                                    avg_y = c.get('y')
                                    
                                    # Identificar posição tática
                                    if avg_x is not None:
                                        sigla = identificar_posicao_opta(avg_x, avg_y)
                                    else:
                                        sigla = "N/A"
                                    
                                    # Montar registro do jogador
                                    player_row = {
                                        "Temporada": ano,
                                        "Rodada": round_num,
                                        "Jogador": p_obj.get('name'),
                                        "Time": match[f'{side}Team']['name'],
                                        "Avg_X": avg_x,
                                        "Avg_Y": avg_y,
                                        "Sigla_Opta": sigla,
                                        "Posicao_Real": MAPEAMENTO_TATICO.get(sigla, "Outro"),
                                        **stats
                                    }
                                    
                                    all_players_data.append(player_row)
                
                # Delay para evitar bloqueio da API
                time.sleep(0.1)
                
        except Exception as e:
            print(f"\nErro na rodada {round_num}: {e}")
            continue
    
    if all_players_data:
        df = pd.DataFrame(all_players_data)
        
        # Reorganizar colunas para facilitar leitura
        cols_principais = ["Temporada", "Rodada", "Jogador", "Time", "Avg_X", "Avg_Y", "Sigla_Opta", "Posicao_Real"]
        cols_estatisticas = [c for c in df.columns if c not in cols_principais]
        df = df[cols_principais + cols_estatisticas]
        
        return df
    
    return None


def main():
    """
    Função principal que executa a extração para todas as temporadas.
    """
    print("=" * 60)
    print("PIPELINE DE EXTRAÇÃO DE DADOS - BRASILEIRÃO")
    print("=" * 60)
    print(f"Anos: {', '.join([s['ano'] for s in SEASONS_INFO])}")
    print(f"Campeonato: Brasileirão Série A (ID: {TOURNAMENT_ID})")
    print("=" * 60)
    
    for season in SEASONS_INFO:
        ano = season['ano']
        
        try:
            df = extrair_dados_temporada(season)
            
            if df is not None:
                filename = f"brasileirao_{ano}_opta_final.csv"
                df.to_csv(filename, index=False, encoding='utf-8-sig')
                print(f"\n✓ Sucesso: {filename} gerado com {len(df)} linhas.")
                print(f"  Colunas: {len(df.columns)}")
                print(f"  Jogadores únicos: {df['Jogador'].nunique()}")
                print(f"  Times: {df['Time'].nunique()}")
            else:
                print(f"\n✗ Falha: Não foi possível extrair dados da temporada {ano}")
                
        except Exception as e:
            print(f"\n✗ Erro ao processar temporada {ano}: {e}")
            continue
    
    print("\n" + "=" * 60)
    print("EXTRAÇÃO FINALIZADA COM SUCESSO!")
    print("=" * 60)


if __name__ == "__main__":
    main()