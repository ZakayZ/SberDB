import json
import random

import requests
import pandas as pd
import time

################ champions
with open('DataSource/champion.json', 'r') as champ:
    champion_data = json.load(champ)['data']
champ_id = []
for champion in champion_data:
    champ_id.append(int(champion_data[champion]['key']))
champions = pd.DataFrame(columns=['champion_id', 'champion_nm'])
champions['champion_id'] = champ_id
champions['champion_nm'] = champion_data.keys()

################ items
with open('DataSource/item.json', 'r') as item:
    item_data = json.load(item)['data']

items = pd.DataFrame(columns=['item_id', 'item_nm', 'item_cost'])
names = []
costs = []
for item in item_data:
    names.append(item_data[item]['name'])
    costs.append(item_data[item]['gold']['total'])

items['item_id'] = item_data.keys()
items['item_nm'] = names
items['item_cost'] = costs

################ servers
server_data = {
    'server_nm': ['Brazil (BR)',
                             'Europe Nordic & East (EUNE)',
                             'Europe West (EUW)',
                             'Latin America North (LAN)',
                             'Latin America South (LAS)',
                             'North America (NA)',
                             'Oceania (OCE)',
                             'Russia (RU)',
                             'Turkey (TR)',
                             'Japan (JP)',
                             'Republic of Korea	(KR)',
                             'The Philippines (PH)',
                             'Singapore, Malaysia, & Indonesia (SG)',
                             'Taiwan, Hong Kong, and Macao (TW)',
                             'Thailand (TH)',
                             'Vietnam (VN)',
                             'Public Beta Environment (PBE)']
               }
server_data['server_id'] = range(len(server_data['server_nm']))

servers = pd.DataFrame(server_data)

################ queues
with open('DataSource/queues.json', 'r') as queues:
    queue_data = json.load(queues)

queues = pd.DataFrame(columns=['queue_id', 'queue_nm'])
queue_names = []
queue_id = []
for queue in queue_data:
    queue_id.append(int(queue['queueId']))
    if queue['description'] is None:
        queue_names.append(queue['map'])
    else:
        queue_names.append(queue['description'] + "," + queue['map'])
queues['queue_nm'] = queue_names
queues['queue_id'] = queue_id

################ match and users
user = dict()
itemlists = dict()
with open('DataSource/APIkey', 'r') as f:
    api_key = f.read()

puuide = 'esPhPVm4l8OEGcHyvSpd0LIgPxAy2xLULD6fgtsPkzzD97ScBWkRCa674IbnjQMQtlz0W5OOIX2qLg'
match_history_url = f'https://europe.api.riotgames.com/lol/match/v5/matches/by-puuid/{puuide}/ids'
params = {
    'count': 20,
    'api_key': api_key,
}
match_data = requests.get(match_history_url, params).json()
# print(match_data)
match_dict = {
    'match_id': [],
    'server_id': [],
    'queue_id': [],
    'start': [],
    'duration': [],
    'blue_win': [],
}

summoner_dict = {
    'match_id': [],
    'user_id': [],
    'champion_id': [],
    'itemlist_id': [],
    'kill_cnt': [],
    'death_cnt': [],
    'assist_cnt': [],
    'creep_stat': [],
    'level_cnt': [],
    'blue_team_flg': [],
}

matches_url = 'https://europe.api.riotgames.com/lol/match/v5/matches/'
params = {
    'api_key': api_key,
}
for match in match_data:
    match_info = requests.get(matches_url + match, params).json()['info']
    match_dict['match_id'].append(match_info['gameId'])
    match_dict['server_id'].append(7)
    match_dict['queue_id'].append(400)
    match_dict['start'].append(match_info['gameStartTimestamp'])
    match_dict['duration'].append(match_info['gameDuration'])
    match_dict['blue_win'].append(match_info['teams'][0]['win'])
    for participant in match_info['participants']:
        summoner_dict['match_id'].append(match_info['gameId'])
        if participant['summonerName'] not in user:
            user[participant['summonerName']] = len(user)
        summoner_dict['user_id'].append(user[participant['summonerName']])
        summoner_dict['champion_id'].append(participant['championId'])
        part_items = (participant['item0'], participant['item1'], participant['item2'], participant['item3'],
                 participant['item4'], participant['item5'])
        if part_items not in itemlists:
            itemlists[part_items] = len(itemlists)
        summoner_dict['itemlist_id'].append(itemlists[part_items])
        summoner_dict['kill_cnt'].append(participant['kills'])
        summoner_dict['death_cnt'].append(participant['deaths'])
        summoner_dict['assist_cnt'].append(participant['assists'])
        summoner_dict['creep_stat'].append(participant['neutralMinionsKilled'])
        summoner_dict['level_cnt'].append(participant['champLevel'])
        summoner_dict['blue_team_flg'].append(participant['teamId'] == 100)

    time.sleep(0.05)
print(match_dict)
match = pd.DataFrame(match_dict).set_index('match_id')

################ user
users = pd.DataFrame()
users['user_id'] = user.values()
users['user_nm'] = user.keys()
users['server_id'] = [7] * len(user)

################ summoner
summoner = pd.DataFrame(summoner_dict)

################ itemlists
rows = {
    'itemlist_id': [],
    'slot_num': [],
    'item_id': []
}
for part_items in itemlists:
    for idx, item in enumerate(part_items, 1):
        if item == 0:
            continue
        rows['itemlist_id'].append(itemlists[part_items])
        rows['slot_num'].append(idx)
        rows['item_id'].append(item)

itemlist = pd.DataFrame(rows).set_index(['itemlist_id', 'slot_num'])

################ rating
rows = {
    'user_id': [],
    'league_point_cnt': [],
}
for user_name in user:
    rows['user_id'].append(user[user_name])
    rows['league_point_cnt'].append(random.Random().randint(1800, 2500))
rating = pd.DataFrame(rows)


# print(champions, items, servers, queues, match, user)
champions.to_csv('champion.csv')
items.to_csv('item.csv')
servers.to_csv('server.csv')
queues.to_csv('queue.csv')
match.to_csv('match.csv')
users.to_csv('user.csv')
summoner.to_csv('summoner.csv')
itemlist.to_csv('itemlist.csv')
rating.to_csv('rating.csv')
