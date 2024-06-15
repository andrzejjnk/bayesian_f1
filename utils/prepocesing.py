def remove_practice_only_drivers(df: pd.DataFrame) -> pd.DataFrame:
    """
    Remove rows of drivers who only participated in practice sessions without racing.
    
    Args:
    df (pd.DataFrame): DataFrame containing F1 data with at least 'Pos (race)' column.
    
    Returns:
    pd.DataFrame: Cleaned DataFrame with only rows of drivers who participated in races.
    """
    # Check if 'Pos (race)' column exists
    if 'Pos (race)' not in df.columns:
        raise ValueError("DataFrame must contain 'Pos (race)' column.")
    
    # Iterate over DataFrame rows
    for index, row in df.iterrows():
        # Check if 'Pos (race)' value is missing or not a number
        if pd.isna(row['Pos (race)']) or (isinstance(row['Pos (race)'], str) and row['Pos (race)'].strip().lower() == 'nc'):
            # If missing or 'NC', drop the row
            df.drop(index, inplace=True)

    df.to_csv('test.csv', index=False)
    
    return df


def fill_missing_qualifications_data(csv_path: str) -> pd.DataFrame:
    """
    Process F1 data by filling missing qualifying times with times from previous sessions.

    Args:
    csv_path (str): Path to the input CSV file containing F1 data.

    Returns:
    pd.DataFrame: Processed DataFrame with filled qualifying times.
    """
    # Load the CSV into a DataFrame
    df = pd.read_csv(csv_path)
    
    # Function to fill missing qualifying times
    def fill_qualifying_times(row):
        if pd.isnull(row['Q3']):
            row['Q3'] = row['Q2']
        if pd.isnull(row['Q2']) and pd.isnull(row['Q3']):
            row['Q2'] = row['Q1']
            row['Q3'] = row['Q1']
        return row
    
    def fill_sprint_qualifying_times(row):
        if pd.isnull(row['SQ3']):
            row['SQ3'] = row['SQ2']
        if pd.isnull(row['SQ2']) and pd.isnull(row['SQ3']):
            row['SQ2'] = row['SQ1']
            row['SQ3'] = row['SQ1']
        return row
    
    # Function to fill missing practice times
    def fill_practice_times(row):
        if pd.isnull(row['Time (FP1)']):
            if not pd.isnull(row['Time (FP2)']):
                row['Time (FP1)'] = row['Time (FP2)']
                row['Pos (FP1)'] = row['Pos (FP2)']
                row['Gap (FP1)'] = row['Gap (FP2)']
                row['Laps (FP1)'] = row['Laps (FP2)']
            elif not pd.isnull(row['Time (FP3)']):
                row['Time (FP1)'] = row['Time (FP3)']
                row['Pos (FP1)'] = row['Pos (FP3)']
                row['Gap (FP1)'] = row['Gap (FP3)']
                row['Laps (FP1)'] = row['Laps (FP3)']
        if pd.isnull(row['Time (FP2)']) and pd.isnull(row['Time (FP3)']):
            row['Time (FP2)'] = row['Time (FP1)']
            row['Pos (FP2)'] = row['Pos (FP1)']
            row['Gap (FP2)'] = row['Gap (FP1)']
            row['Laps (FP2)'] = row['Laps (FP1)']
        if pd.isnull(row['Time (FP3)']):
            row['Time (FP3)'] = row['Time (FP2)']
            row['Pos (FP3)'] = row['Pos (FP2)']
            row['Gap (FP3)'] = row['Gap (FP2)']
            row['Laps (FP3)'] = row['Laps (FP2)']
        return row


    # Apply the function to each row
    df = df.apply(fill_qualifying_times, axis=1)
    df = df.apply(fill_sprint_qualifying_times, axis=1)
    df = df.apply(fill_practice_times, axis=1)
    # Remove rows with remaining null values in the relevant columns
    # relevant_columns = ['Q1', 'Q2', 'Q3', 'Gap (FP1)', 'Gap (FP2)', 'Gap (FP3)','Time (FP1)', 'Time (FP2)', 'Time (FP3)']
    # df = df.dropna(subset=relevant_columns)
    df.to_csv('test2.csv', index=False)

    return df


if __name__ == "__main__":
    # Example usage:
    csv_path = 'test.csv'
    data = fill_missing_qualifications_data(csv_path)
    data.info()
