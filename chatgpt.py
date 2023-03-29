import time

import openai
from riot_api import get_champion_data
from secrets import get_secret_param


# Set up the OpenAI API client
openai.api_key = get_secret_param("openai_api_key")
champion_id_name_map = get_champion_data()
language = "english"


def generate_advice(participant_data, ally_data, enemy_data):
    participant_champion_name = champion_id_name_map[participant_data['championId']]
    ally_champion_names = [champion_id_name_map[ally['championId']] for ally in ally_data]
    enemy_champion_names = [champion_id_name_map[enemy['championId']] for enemy in enemy_data]

    prompt = (
        f"As a {participant_champion_name}, playing with allies {', '.join(ally_champion_names)}, "
        f"how should I play against these enemy champions: {', '.join(enemy_champion_names)}? "
        f"1. How should I play in early game "
        f"2. What should I buy against these enemies "
        f"3. How to use my skills combinations (combo) against enemies "
        f"4. How to play in late game state against these enemies "
        f"Translate your answer to {language} "
        f"In your response start from: 'You are playing champion <player_champion> with <ally_champions> against <enemy_champions>'. Each sentence should be in the next line."
    )

    # response = openai.Completion.create(
    #     engine="text-davinci-003",
    #     prompt=prompt,
    #     max_tokens=1000,
    #     n=1,
    #     stop=None,
    #     temperature=0.5,
    # )
    time.sleep(10)
    # advice = response.choices[0].text.strip()
    advice = "This is the advice"
    return advice
