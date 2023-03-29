import requests
from secrets_smm import get_secret_param

API_KEY = get_secret_param("riot_api_key")
REGION = 'EUN1'


def get_champion_data():
    version_url = "https://ddragon.leagueoflegends.com/api/versions.json"
    versions = requests.get(version_url).json()
    latest_version = versions[0]

    champions_url = f"https://ddragon.leagueoflegends.com/cdn/{latest_version}/data/en_US/champion.json"
    champions_data = requests.get(champions_url).json()["data"]

    champion_id_name_map = {int(champion["key"]): champion["name"] for champion in champions_data.values()}
    return champion_id_name_map


def get_summoner_id(summoner_name):
    base_url = f'https://{REGION}.api.riotgames.com/lol/summoner/v4/summoners/by-name/'
    url = f'{base_url}{summoner_name}?api_key={API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Given {summoner_name} cannot be found for {REGION} region')

    return response.json()['id']


def get_active_match_data(summoner_id):
    base_url = f'https://{REGION}.api.riotgames.com/lol/spectator/v4/active-games/by-summoner/'
    url = f'{base_url}{summoner_id}?api_key={API_KEY}'
    response = requests.get(url)

    if response.status_code != 200:
        raise Exception(f'Given summoner is not in the match in this moment')

    return response.json()


def extract_active_match_info(active_match_data, summoner_name):
    allies = []
    enemies = []

    for participant in active_match_data['participants']:
        participant_info = {
            'summonerName': participant['summonerName'],
            'championId': participant['championId'],
            'teamId': participant['teamId'],
            'spell1Id': participant['spell1Id'],
            'spell2Id': participant['spell2Id']
        }
        if participant_info['summonerName'] == summoner_name:
            participant_team_id = participant['teamId']

    for participant in active_match_data['participants']:
        if participant['teamId'] == participant_team_id and participant['summonerName'] != summoner_name:
            allies.append(participant)
        elif participant['teamId'] != participant_team_id:
            enemies.append(participant)

    return allies, enemies
