from nba_api.stats.endpoints import commonteamroster, playergamelogs
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
# import asyncio
# import aiohttp



# Get all players by team ID
def get_player_ids_by_team_id(team_id: str):
    team_roster = commonteamroster.CommonTeamRoster(team_id=1610612745)
    return team_roster.get_data_frames()[0]["PLAYER_ID"].tolist()


# Get players stats from recent n games
def get_players_stats(player_ids: list, season: str = "2023-24", last_n_games: int = 10, opp_team_id: str = None, dateTo: str = None):
    args = [(player_id, last_n_games) for player_id in player_ids]
    
    # with ThreadPoolExecutor(max_workers=5) as executor:
    #     results = executor.map(lambda p: _get_player_stats(*p), args)
        
    #     try:
    #         print(next(results))
    #         return results
    #     except Exception as e:
    #         print("Error:", e)
        
    results = []
    for player_id in player_ids:
        results.append(_get_player_stats(player_id, season=season, last_n_games=last_n_games, opp_team_id=opp_team_id, dateTo=dateTo))
    
    to_return = pd.concat(results)
    to_return["GAME_DATE"] = pd.to_datetime(to_return["GAME_DATE"]).dt.date
    
    return to_return
        
# Get players stats from recent n games
def _get_player_stats(player_id: str, season: str = "2023-24", last_n_games: int = 10, opp_team_id: str = None, dateTo: str = None):
    playergamelogs_df = playergamelogs.PlayerGameLogs(
                                                        player_id_nullable=player_id,
                                                        last_n_games_nullable=last_n_games,
                                                        season_nullable=season,
                                                        opp_team_id_nullable=opp_team_id,
                                                        date_to_nullable=dateTo
                                                    ).get_data_frames()[0]
    
    return playergamelogs_df[["PLAYER_ID", "PLAYER_NAME", "GAME_DATE", "MATCHUP", "PTS", "FG3M", "REB", "AST", "TOV", "STL", "BLK"]]
    
    