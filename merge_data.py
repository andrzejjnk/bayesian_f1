import os
import pandas as pd
import re
from typing import Dict, List
from utils.lib import *

# paths to csv files with data
path_drivers = 'data/drivers.csv'
paths_fastest_laps = {2022: "data/2022/fastest_laps/", 2023: "data/2023/fastest_laps/", 2024: "data/2024/fastest_laps/"} 
paths_pit_stop_summary = {2022: "data/2022/pit_stop_summary/", 2023: "data/2023/pit_stop_summary/", 2024: "data/2024/pit_stop_summary/"} 
paths_practice_1 = {2022: "data/2022/practice_1/", 2023: "data/2023/practice_1/", 2024: "data/2024/practice_1/"} 
paths_practice_2 = {2022: "data/2022/practice_2/", 2023: "data/2023/practice_2/", 2024: "data/2024/practice_2/"} 
paths_practice_3= {2022: "data/2022/practice_3/", 2023: "data/2023/practice_3/", 2024: "data/2024/practice_3/"} 
paths_qualifying = {2022: "data/2022/qualifying/", 2023: "data/2023/qualifying/", 2024: "data/2024/qualifying/"} 
paths_race_result = {2022: "data/2022/race_result/", 2023: "data/2023/race_result/", 2024: "data/2024/race_result/"} 
paths_sprint_grid = {2022: "data/2022/sprint_grid/", 2023: "data/2023/sprint_grid/", 2024: "data/2024/sprint_grid/"} 
paths_sprint_qualifying = {2023: "data/2023/sprint_qualifying/", 2024: "data/2024/sprint_qualifying/"} 
paths_sprint_results = {2022: "data/2022/sprint_results/", 2023: "data/2023/sprint_results/", 2024: "data/2024/sprint_results/"} 
paths_starting_grid = {2022: "data/2022/starting_grid/", 2023: "data/2023/starting_grid/", 2024: "data/2024/starting_grid/"}
path_weather_summary = 'weather_data/Weather_Summary.csv'
merged_csv_files_per_race_path = 'merged_data/'
# years = [2022, 2023, 2024]
years = [2024, 2023, 2022]


def map_round_to_race(row):
    year = row['Year']
    round_number = row['Round Number']
    return race_orders[year].get(round_number, 'Unknown')


def add_weather_to_merged_files(years: List[int], weather_summary_csv_path: str, output_dir: str = 'merged_data') -> None:
    weather_data = pd.read_csv(weather_summary_csv_path)
    weather_data['Race'] = weather_data.apply(map_round_to_race, axis=1)
    for year in years:
        year_data = weather_data[weather_data['Year'] == year]
        for _, row in year_data.iterrows():
            race = row['Race']
            weather_info = row.drop(['Year', 'Round Number', 'Race']).to_dict()
            
            merged_file_path = os.path.join(output_dir, f'{year}_{race}_merged_results.csv')
            if os.path.exists(merged_file_path):
                merged_data = pd.read_csv(merged_file_path)
                for column, value in weather_info.items():
                    merged_data[column] = value
                merged_data.to_csv(merged_file_path, index=False)
                print(f"Added weather data to {merged_file_path}")
            else:
                print(f"File {merged_file_path} does not exist. Skipping.")


# def merge_csv_files_per_race(paths_race_result: Dict[int, str], paths_qualifying: Dict[int, str], paths_practice_1: Dict[int, str], paths_practice_2: Dict[int, str], paths_practice_3: Dict[int, str], paths_sprint_results: Dict[int, str], paths_sprint_qualifying: Dict[int, str], weather_csv_path: str) -> None:
#     weather_data = pd.read_csv(weather_csv_path)
#     weather_data['Race'] = weather_data.apply(map_round_to_race, axis=1)

#     for year, race_path in paths_race_result.items():
#         qualifying_path = paths_qualifying[year]
#         practice_1_path = paths_practice_1[year]
#         practice_2_path = paths_practice_2[year]
#         practice_3_path = paths_practice_3[year]
#         sprint_results_path = paths_sprint_results[year]
#         if year in (2023 , 2024):
#             sprint_quali_results_path = paths_sprint_qualifying[year]

#         race_files = os.listdir(race_path)
        
#         for file in race_files:
#             race_results = pd.read_csv(os.path.join(race_path, file))
#             race = os.path.splitext(file)[0]
#             qualifying_file = file.replace('race_result', 'qualifying')
#             qualifying_results = pd.read_csv(os.path.join(qualifying_path, qualifying_file))

#             practice_1_file = file.replace('qualifying', 'practice_1')
#             practice_1_results = pd.read_csv(os.path.join(practice_1_path, practice_1_file))

#             practice_2_results_selected = pd.DataFrame(columns=['Pos (FP2)', 'No', 'Driver', 'Car', 'Time (FP2)', 'Gap (FP2)', 'Laps (FP2)'])
#             practice_3_results_selected = pd.DataFrame(columns=['Pos (FP3)', 'No', 'Driver', 'Car', 'Time (FP3)', 'Gap (FP3)', 'Laps (FP3)'])
#             sprint_results_selected = pd.DataFrame(columns=['Pos (Sprint)', 'No', 'Driver', 'Car', 'Laps (Sprint)', 'Time/Retired (Sprint)', 'Points (Sprint)'])
#             sprint_qualifying_results_selected = pd.DataFrame(columns=['Pos (Sprint Quali)','No','Driver','Car','SQ1','SQ2','SQ3','Laps (Sprint Quali)'])

#             is_sprint_weekend = 0

#             try:
#                 practice_2_file = file.replace('practice_1', 'practice_2')
#                 practice_2_results = pd.read_csv(os.path.join(practice_2_path, practice_2_file))
#                 practice_2_results_selected = practice_2_results[['Pos', 'No', 'Driver', 'Car', 'Time', 'Gap', 'Laps']].copy()
#                 practice_2_results_selected.rename(columns={'Pos': 'Pos (FP2)', 'Laps': 'Laps (FP2)', 'Time': 'Time (FP2)', 'Gap': 'Gap (FP2)'}, inplace=True)
#             except Exception as e:
#                 print(f'Sprint weekend so there is no practice 2 data: {e}')
#                 is_sprint_weekend = 1

#             try:
#                 practice_3_file = file.replace('practice_2', 'practice_3')
#                 practice_3_results = pd.read_csv(os.path.join(practice_3_path, practice_3_file))
#                 practice_3_results_selected = practice_3_results[['Pos', 'No', 'Driver', 'Car', 'Time', 'Gap', 'Laps']].copy()
#                 practice_3_results_selected.rename(columns={'Pos': 'Pos (FP3)', 'Laps': 'Laps (FP3)', 'Time': 'Time (FP3)', 'Gap': 'Gap (FP3)'}, inplace=True)
#             except Exception as e:
#                 print(f'Sprint weekend so there is no practice 3 data: {e}')
#                 is_sprint_weekend = 1

#             if is_sprint_weekend:
#                 try:
#                     sprint_file = file.replace('race_result', 'sprint_results')
#                     sprint_results = pd.read_csv(os.path.join(sprint_results_path, sprint_file))
#                     sprint_results_selected = sprint_results[['Pos', 'No', 'Driver', 'Car', 'Laps', 'Time/Retired', 'PTS']].copy()
#                     sprint_results_selected.rename(columns={'Pos': 'Pos (Sprint)', 'Laps': 'Laps (Sprint)', 'Time/Retired': 'Time/Retired (Sprint)', 'PTS': 'Points (Sprint)'}, inplace=True)

#                     if year in (2023, 2024):
#                         sprint_qualifying_file = file.replace('sprint_results', 'sprint_qualifying')
#                         sprint_qualifying_results = pd.read_csv(os.path.join(sprint_quali_results_path, sprint_qualifying_file))
#                         sprint_qualifying_results_selected = sprint_qualifying_results[['Pos','No','Driver','Car','Q1','Q2','Q3','Laps']].copy()
#                         sprint_qualifying_results_selected.rename(columns={'Pos': 'Pos (Sprint Quali)', 'Laps': 'Laps (Sprint Quali)', 'Q1': 'SQ1', 'Q2': 'SQ2', 'Q3': 'SQ3', 'Laps': 'Laps (Sprint Quali)'}, inplace=True)
#                 except Exception as e:
#                     print(f'Error loading sprint results: {e}')
#                     sprint_results_selected = pd.DataFrame(columns=['Pos (Sprint)', 'No', 'Driver', 'Car', 'Laps (Sprint)', 'Time/Retired (Sprint)', 'Points (Sprint)'])
#                     sprint_qualifying_results_selected = pd.DataFrame(columns=['Pos (Sprint Quali)','No','Driver','Car','SQ1','SQ2','SQ3','Laps (Sprint Quali)'])

#             race_results_selected = race_results[['No', 'Driver', 'Car', 'Pos', 'Laps', 'Time/Retired', 'PTS']].copy()
#             race_results_selected.rename(columns={'PTS': 'Points'}, inplace=True)
#             qualifying_results_selected = qualifying_results[['No', 'Driver', 'Car', 'Pos', 'Q1', 'Q2', 'Q3']].copy()
#             practice_1_results_selected = practice_1_results[['Pos', 'No', 'Driver', 'Car', 'Time', 'Gap', 'Laps']].copy()

#             qualifying_results_selected.rename(columns={'Pos': 'Pos (qualifying)'}, inplace=True)
#             race_results_selected.rename(columns={'Pos': 'Pos (race)', 'Laps': 'Laps (race)'}, inplace=True)
#             practice_1_results_selected.rename(columns={'Pos': 'Pos (FP1)', 'Laps': 'Laps (FP1)', 'Time': 'Time (FP1)', 'Gap': 'Gap (FP1)'}, inplace=True)

#             if qualifying_results_selected is not None:
#                 merged_results = pd.merge(race_results_selected, qualifying_results_selected, on=['No', 'Driver', 'Car'], how='inner')
#             if practice_1_results_selected is not None:
#                 merged_results = pd.merge(merged_results, practice_1_results_selected, on=['No', 'Driver', 'Car'], how='inner')
#             if practice_2_results_selected is not None:
#                 merged_results = pd.merge(merged_results, practice_2_results_selected, on=['No', 'Driver', 'Car'], how='left')
#             if practice_3_results_selected is not None:
#                 merged_results = pd.merge(merged_results, practice_3_results_selected, on=['No', 'Driver', 'Car'], how='left')
#             if sprint_results_selected is not None:
#                 merged_results = pd.merge(merged_results, sprint_results_selected, on=['No', 'Driver', 'Car'], how='left')
#             if sprint_qualifying_results_selected is not None:
#                 merged_results = pd.merge(merged_results, sprint_qualifying_results_selected, on=['No', 'Driver', 'Car'], how='left')

#             race_weather_data = weather_data[(weather_data['Year'] == year) & (weather_data['Race'] == race)].drop(['Year', 'Round Number', 'Race'], axis=1)
#             for column in race_weather_data.columns:
#                 merged_results[column] = race_weather_data[column].values[0]

#             merged_results.insert(0, 'Year', year)
#             merged_results.insert(1, 'Race', race)

#             output_path = os.path.join('merged_data', f'{year}_{race}_merged_results.csv')
#             # os.makedirs('merged_data', exist_ok=True)
#             merged_results.to_csv(output_path, index=False)
#             print("All csv files per race were successfully merged!")


def merge_csv_files_per_race(paths_race_result: Dict[int, str], paths_qualifying: Dict[int, str], paths_practice_1: Dict[int, str], paths_practice_2: Dict[int, str], paths_practice_3: Dict[int, str], paths_sprint_results: Dict[int, str], paths_sprint_qualifying: Dict[int, str], weather_csv_path: str) -> None:
    weather_data = pd.read_csv(weather_csv_path)
    weather_data['Race'] = weather_data.apply(map_round_to_race, axis=1)

    for year, race_path in paths_race_result.items():
        qualifying_path = paths_qualifying[year]
        practice_1_path = paths_practice_1[year]
        practice_2_path = paths_practice_2[year]
        practice_3_path = paths_practice_3[year]
        sprint_results_path = paths_sprint_results[year]
        if year in (2023 , 2024):
            sprint_quali_results_path = paths_sprint_qualifying[year]

        race_files = os.listdir(race_path)
        
        for file in race_files:
            race_results = pd.read_csv(os.path.join(race_path, file))
            race = os.path.splitext(file)[0]
            qualifying_file = file.replace('race_result', 'qualifying')
            qualifying_results = pd.read_csv(os.path.join(qualifying_path, qualifying_file))

            practice_1_file = file.replace('qualifying', 'practice_1')
            practice_1_results = pd.read_csv(os.path.join(practice_1_path, practice_1_file))

            practice_2_results_selected = pd.DataFrame(columns=['Pos (FP2)', 'No', 'Driver', 'Car', 'Time (FP2)', 'Gap (FP2)', 'Laps (FP2)'])
            practice_3_results_selected = pd.DataFrame(columns=['Pos (FP3)', 'No', 'Driver', 'Car', 'Time (FP3)', 'Gap (FP3)', 'Laps (FP3)'])
            sprint_results_selected = pd.DataFrame(columns=['Pos (Sprint)', 'No', 'Driver', 'Car', 'Laps (Sprint)', 'Time/Retired (Sprint)', 'Points (Sprint)'])
            sprint_qualifying_results_selected = pd.DataFrame(columns=['Pos (Sprint Quali)','No','Driver','Car','SQ1','SQ2','SQ3','Laps (Sprint Quali)'])

            is_sprint_weekend = 0

            try:
                practice_2_file = file.replace('practice_1', 'practice_2')
                practice_2_results = pd.read_csv(os.path.join(practice_2_path, practice_2_file))
                practice_2_results_selected = practice_2_results[['Pos', 'No', 'Driver', 'Car', 'Time', 'Gap', 'Laps']].copy()
                practice_2_results_selected.rename(columns={'Pos': 'Pos (FP2)', 'Laps': 'Laps (FP2)', 'Time': 'Time (FP2)', 'Gap': 'Gap (FP2)'}, inplace=True)
            except Exception as e:
                print(f'Sprint weekend so there is no practice 2 data: {e}')
                is_sprint_weekend = 1

            try:
                practice_3_file = file.replace('practice_2', 'practice_3')
                practice_3_results = pd.read_csv(os.path.join(practice_3_path, practice_3_file))
                practice_3_results_selected = practice_3_results[['Pos', 'No', 'Driver', 'Car', 'Time', 'Gap', 'Laps']].copy()
                practice_3_results_selected.rename(columns={'Pos': 'Pos (FP3)', 'Laps': 'Laps (FP3)', 'Time': 'Time (FP3)', 'Gap': 'Gap (FP3)'}, inplace=True)
            except Exception as e:
                print(f'Sprint weekend so there is no practice 3 data: {e}')
                is_sprint_weekend = 1

            if is_sprint_weekend:
                try:
                    sprint_file = file.replace('race_result', 'sprint_results')
                    sprint_results = pd.read_csv(os.path.join(sprint_results_path, sprint_file))
                    sprint_results_selected = sprint_results[['Pos', 'No', 'Driver', 'Car', 'Laps', 'Time/Retired', 'PTS']].copy()
                    sprint_results_selected.rename(columns={'Pos': 'Pos (Sprint)', 'Laps': 'Laps (Sprint)', 'Time/Retired': 'Time/Retired (Sprint)', 'PTS': 'Points (Sprint)'}, inplace=True)

                    if year in (2023, 2024):
                        sprint_qualifying_file = file.replace('sprint_results', 'sprint_qualifying')
                        sprint_qualifying_results = pd.read_csv(os.path.join(sprint_quali_results_path, sprint_qualifying_file))
                        sprint_qualifying_results_selected = sprint_qualifying_results[['Pos','No','Driver','Car','Q1','Q2','Q3','Laps']].copy()
                        sprint_qualifying_results_selected.rename(columns={'Pos': 'Pos (Sprint Quali)', 'Laps': 'Laps (Sprint Quali)', 'Q1': 'SQ1', 'Q2': 'SQ2', 'Q3': 'SQ3', 'Laps': 'Laps (Sprint Quali)'}, inplace=True)
                except Exception as e:
                    print(f'Error loading sprint results: {e}')
                    sprint_results_selected = pd.DataFrame(columns=['Pos (Sprint)', 'No', 'Driver', 'Car', 'Laps (Sprint)', 'Time/Retired (Sprint)', 'Points (Sprint)'])
                    sprint_qualifying_results_selected = pd.DataFrame(columns=['Pos (Sprint Quali)','No','Driver','Car','SQ1','SQ2','SQ3','Laps (Sprint Quali)'])

            race_results_selected = race_results[['No', 'Driver', 'Car', 'Pos', 'Laps', 'Time/Retired', 'PTS']].copy()
            race_results_selected.rename(columns={'PTS': 'Points'}, inplace=True)
            qualifying_results_selected = qualifying_results[['No', 'Driver', 'Car', 'Pos', 'Q1', 'Q2', 'Q3']].copy()
            practice_1_results_selected = practice_1_results[['Pos', 'No', 'Driver', 'Car', 'Time', 'Gap', 'Laps']].copy()

            qualifying_results_selected.rename(columns={'Pos': 'Pos (qualifying)'}, inplace=True)
            race_results_selected.rename(columns={'Pos': 'Pos (race)', 'Laps': 'Laps (race)'}, inplace=True)
            practice_1_results_selected.rename(columns={'Pos': 'Pos (FP1)', 'Laps': 'Laps (FP1)', 'Time': 'Time (FP1)', 'Gap': 'Gap (FP1)'}, inplace=True)

            merged_results = race_results_selected
            if qualifying_results_selected is not None:
                merged_results = pd.merge(merged_results, qualifying_results_selected, on=['No', 'Driver', 'Car'], how='outer')
            if practice_1_results_selected is not None:
                merged_results = pd.merge(merged_results, practice_1_results_selected, on=['No', 'Driver', 'Car'], how='outer')
            if practice_2_results_selected is not None:
                merged_results = pd.merge(merged_results, practice_2_results_selected, on=['No', 'Driver', 'Car'], how='outer')
            if practice_3_results_selected is not None:
                merged_results = pd.merge(merged_results, practice_3_results_selected, on=['No', 'Driver', 'Car'], how='outer')
            if sprint_results_selected is not None:
                merged_results = pd.merge(merged_results, sprint_results_selected, on=['No', 'Driver', 'Car'], how='outer')
            if sprint_qualifying_results_selected is not None:
                merged_results = pd.merge(merged_results, sprint_qualifying_results_selected, on=['No', 'Driver', 'Car'], how='outer')

            race_weather_data = weather_data[(weather_data['Year'] == year) & (weather_data['Race'] == race)].drop(['Year', 'Round Number', 'Race'], axis=1)
            for column in race_weather_data.columns:
                merged_results[column] = race_weather_data[column].values[0]

            merged_results.insert(0, 'Year', year)
            merged_results.insert(1, 'Race', race)

            output_path = os.path.join('merged_data', f'{year}_{race}_merged_results.csv')
            os.makedirs('merged_data', exist_ok=True)
            merged_results.to_csv(output_path, index=False)
            print(f"All csv files for {year} {race} were successfully merged!")


def get_race_order(race: str, year: int) -> int | float:
    for round_number, race_name in race_orders[year].items():
        if race_name == race:
            return round_number
    return float('inf')


# def sort_csv_by_race_order(csv_path: str, year: int) -> None:
#     df = pd.read_csv(csv_path)
#     df['Race Order'] = df['Race'].apply(lambda x: get_race_order(x, year))
#     df_sorted = df.sort_values(by=['Year', 'Race Order'])
#     df_sorted.drop(columns=['Race Order'], inplace=True)
#     df_sorted.to_csv(csv_path, index=False)
#     print(f"Sorted CSV file saved at {csv_path}")

def sort_csv_by_race_order(csv_path: str, year: int) -> None:
    df = pd.read_csv(csv_path)

    df_year = df[df['Year'] == year].copy()
    df_year['Race Order'] = df_year['Race'].apply(lambda x: get_race_order(x, year))
    
    df_year_sorted = df_year.sort_values(by=['Race Order'])
    df_year_sorted.drop(columns=['Race Order'], inplace=True)
    
    df_other_years = df[df['Year'] != year]

    df_sorted = pd.concat([df_year_sorted, df_other_years], ignore_index=True)
    
    df_sorted.to_csv(csv_path, index=False)
    print(f"Sorted CSV file saved at {csv_path} for year {year}")


def main_csv_merge(path: str, output_file: str) -> None:
    try:
        df_merged = pd.DataFrame()
        files = os.listdir(path)
        for file in files:
            if file.endswith('.csv'):
                file_path = os.path.join(path, file)
                df = pd.read_csv(file_path)
                df_merged = pd.concat([df_merged, df], ignore_index=True)
        df_merged.to_csv(output_file, index=False)
        print(f'{output_file} was successfully created and filled with data!')
        for year in years:
            sort_csv_by_race_order(output_file, year)
        # sort_csv_by_race_order(output_file, 2022)
    except Exception as e:
        print(f"Cannot merge csv files: {e}")


def format_csv_time(file_path, time_columns):
    df = pd.read_csv(file_path)
    
    time_pattern = r'(\d+:)?\d+:\d+\.\d+'
    
    for col in time_columns:
        df[col] = df[col].apply(lambda x: re.sub(time_pattern, lambda m: m.group(0).replace('.', ':'), str(x)))
    
    df.to_csv(file_path, index=False)
    print("Formatted CSV file saved at:", file_path)



if __name__=="__main__":
    os.makedirs('merged_data', exist_ok=True)
    add_weather_to_merged_files(years, path_weather_summary)
    merge_csv_files_per_race(paths_race_result, paths_qualifying, paths_practice_1, paths_practice_2, paths_practice_3, paths_sprint_results, paths_sprint_qualifying, path_weather_summary)
    main_csv_merge(merged_csv_files_per_race_path, 'final_f1_data.csv')
    time_columns = ['Q1', 'Q2', 'Q3', 'Time (FP1)', 'Time (FP2)', 'Time (FP3)', 'Time/Retired (Sprint)', 'Time/Retired', 'SQ1','SQ2','SQ3']
    file_path = 'final_f1_data.csv'
    format_csv_time(file_path, time_columns)
