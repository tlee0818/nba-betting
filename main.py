from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.static import teams
from teams_to_id import teams_to_id
import players_fn as p

print(p.get_player_ids_by_team_id("1610612746"))