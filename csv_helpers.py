import pandas as pd
from teams_to_id import teams_to_id

def load_csv(file_path: str):
    return pd.read_csv(file_path)

def process_csv(df: pd.DataFrame, curr_year: str = "2022", next_year: str = "2023"):
    df['Result'] = 'L'
    df.loc[df.groupby(df.index // 2)['Final'].idxmax(), 'Result'] = 'W'
    # Transform the 'Date' column
    df['Date'] = df['Date'].apply(convert_date)

    # Add 'team_id' column based on 'Team' column and 'team_ids' dictionary
    df['team_id'] = df['Team'].map(teams_to_id)
    
    # Add 'opp_team' and 'opp_team_id' columns
    # For each pair (VH pairs), assign the opposite team and team ID
    df['opp_team'] = df['Team'].shift(-1)
    df.loc[df.index % 2 == 0, 'opp_team'] = df['Team'].shift(-1)
    df.loc[df.index % 2 == 1, 'opp_team'] = df['Team'].shift(1)

    df['opp_team_id'] = df['opp_team'].map(teams_to_id)

    # Ensure the DataFrame columns are in the desired order, including new columns
    df = df[['Date', 'VH', 'Team', 'team_id', 'opp_team', 'opp_team_id', '1st', '2nd', '3rd', '4th', 'Final', 'Open', 'Close', 'ML', 'Result']]
    
    # df = df[['Date', 'VH', 'Team', 'team_id', '1st', '2nd', '3rd', '4th', 'Final', 'Open', 'Close', 'ML', 'Result']]


    return df

def save_csv(df: pd.DataFrame, file_path: str):
    df.to_csv(file_path, index=False)
    
# Function to convert date from MMDD to YYYY-MM-DD format
def convert_date(date: str, curr_year: str = "2022", next_year: str = "2023"):
    month, day = divmod(date, 100)
    year = curr_year if month > 6 else next_year  # Assuming the year flips based on the month
    return f"{year}-{month:02d}-{day:02d}"