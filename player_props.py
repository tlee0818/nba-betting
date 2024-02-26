import requests
import urllib
from datetime import datetime
import json
from dotenv import load_dotenv
import os

load_dotenv()

BASE_URL = 'https://api.prop-odds.com'
API_KEY = os.getenv('PROP_ODDS_API_KEY')
ALL_MARKETS = ["final_score", "first_half_moneyline", "first_half_spread", "first_half_spread_alternate", "first_half_team_over_under", "first_half_total_alternate",\
            "first_half_total_over_under", "first_quarter_moneyline", "first_quarter_spread", "first_quarter_total", "has_overtime", "moneyline", "moneyline_regulation",\
            "player_assists_over_under", "player_assists_points_over_under", "player_assists_points_rebounds_over_under", "player_assists_rebounds_over_under",\
            "player_blocks_over_under", "player_blocks_steals_over_under", "player_double_double", "player_first_basket", "player_first_basket_method", \
            "player_first_team_basket", "player_min_assists", "player_min_assists_points", "player_min_assists_points_rebounds", "player_min_blocks", \
            "player_min_points", "player_min_points_and_rebounds", "player_min_rebounds", "player_min_steals", "player_min_threes", "player_most_points", \
            "player_points_over_under", "player_points_rebounds_over_under", "player_rebounds_over_under", "player_steals_over_under", "player_threes_over_under", \
            "player_triple_double", "player_turnovers_over_under", "second_half_moneyline", "second_half_spread", "second_half_spread_alternate", "second_half_team_over_under", \
            "second_half_total_over_under", "spread", "spread_alternate", "team_odd_even", "team_over_under", "team_over_under_alternate", "total_odd_even", "total_odd_even_first_half",\
            "total_over_under", "total_over_under_alternate"]

INTEREST_MARKETS = ["player_assists_over_under", "player_blocks_over_under", "player_points_over_under", "player_rebounds_over_under",\
                    "player_steals_over_under", "player_threes_over_under", "player_turnovers_over_under"]


def get_request(url):
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()

    print('Request failed with status:', response.status_code)
    return {}


def get_nba_games(time):
    query_params = {
        'date': time.strftime('%Y-%m-%d'),
        'tz': 'America/New_York',
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/games/nba?' + params
    return get_request(url)


def get_game_info(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/game/' + game_id + '?' + params
    return get_request(url)


def get_markets(game_id):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/markets/' + game_id + '?' + params
    return get_request(url)


def get_most_recent_odds(game_id, market):
    query_params = {
        'api_key': API_KEY,
    }
    params = urllib.parse.urlencode(query_params)
    url = BASE_URL + '/beta/odds/' + game_id + '/' + market + '?' + params
    return get_request(url)


def main():
    games = get_nba_games(datetime.now())
    if len(games['games']) == 0:
        print('No games scheduled for today.')
        return

    for game in games['games']:
        game_id = game['game_id']
        home_team = game['home_team']
        away_team = game['away_team']
        
        for market in INTEREST_MARKETS:
            
            all_odds = get_most_recent_odds(game_id, market)["sportsbooks"]
            # find the dictionary where bookie_key is "draftkings"
            draftkings_odds = next((d for d in all_odds if d.get('bookie_key') == 'draftkings'), None)
                        
            result = {
                "home_team": home_team,
                "away_team": away_team,
                "market": market,
                "odds": draftkings_odds["market"]["outcomes"]
            
            }

            with open('player_props_examp.json', 'w') as f:
                json.dump(result, f, indent=4)
            break
        break



if __name__ == '__main__':
    main()
