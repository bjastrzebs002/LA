from riot_api import get_summoner_id, get_active_match_data, extract_active_match_info
from chatgpt import generate_advice


def job(summoner_name):
    try:
        summoner_id = get_summoner_id(summoner_name)
        active_match_data = get_active_match_data(summoner_id)
        ally_data, enemy_data = extract_active_match_info(active_match_data, summoner_name)

        participant_data = {
            'summonerName': summoner_name,
            'championId': next(participant['championId'] for participant in active_match_data['participants'] if
                               participant['summonerName'] == summoner_name),
        }

        advice = generate_advice(participant_data, ally_data, enemy_data)
        return advice
    except Exception as e:
        raise Exception(e)
