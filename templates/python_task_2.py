import pandas as pd


def calculate_distance_matrix(df)->pd.DataFrame():
    """
    Calculate a distance matrix based on the dataframe, df.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Distance matrix
    """
    # Write your logic here
    pivot_df = df.pivot(index='id_start', columns='id_end', values='distance').fillna(0)

    #Convert pivot table to DataFrame and ensure symmetry by adding transposed matrix
    df = pivot_df.add(pivot_df.T, fill_value=0)

    # Set diagonal values to 0
    for col in df.columns:
        df.loc[col, col] = 0
    return df


def unroll_distance_matrix(df)->pd.DataFrame():
    """
    Unroll a distance matrix to a DataFrame in the style of the initial dataset.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Unrolled DataFrame containing columns 'id_start', 'id_end', and 'distance'.
    """
    # Write your logic here
    distance_matrix = distance_matrix.reset_index()

    #Melt the DataFrame to transform it to long format
    melted_df = pd.melt(distance_matrix, id_vars='index', var_name='id_end', value_name='distance')

    #Rename columns for clarity
    melted_df.columns = ['id_start', 'id_end', 'distance']

    #Filter out same id_start and id_end pairs
    df = melted_df[melted_df['id_start'] != melted_df['id_end']].reset_index(drop=True)

    return df


def find_ids_within_ten_percentage_threshold(df, reference_id)->pd.DataFrame():
    """
    Find all IDs whose average distance lies within 10% of the average distance of the reference ID.

    Args:
        df (pandas.DataFrame)
        reference_id (int)

    Returns:
        pandas.DataFrame: DataFrame with IDs whose average distance is within the specified percentage threshold
                          of the reference ID's average distance.
    """
    # Write your logic here
    avg_distance_reference = df[df['id_start'] == reference_value]['distance'].mean()

    #Calculate the threshold range (10% of the average distance)
    threshold = 0.1 * avg_distance_reference

    #Filter 'id_start' values within the threshold range
    within_threshold_ids = df[(df['id_start'] != reference_value) &
                              (df['distance'] >= avg_distance_reference - threshold) &
                              (df['distance'] <= avg_distance_reference + threshold)]['id_start'].unique()

    #Sort the 'id_start' values within the threshold
    value = sorted(within_threshold_ids)

    return df

def calculate_toll_rate(df)->pd.DataFrame():
    """
    Calculate toll rates for each vehicle type based on the unrolled DataFrame.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Wrie your logic here
    df['moto'] = df['distance'] * 0.8
    df['car'] = df['distance'] * 1.2
    df['rv'] = df['distance'] * 1.5
    df['bus'] = df['distance'] * 2.2
    df['truck'] = df['distance'] * 3.6
    return df


import datetime
def calculate_time_based_toll_rates(df)->pd.DataFrame():
    """
    Calculate time-based toll rates for different time intervals within a day.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame
    """
    # Write your logic here
    df['start_time'] = pd.to_datetime(df['start_time'])
    df['end_time'] = pd.to_datetime(df['end_time'])

    # Create time range objects for different time intervals
    weekdays_morning = (datetime.time(0, 0), datetime.time(10, 0))
    weekdays_afternoon = (datetime.time(10, 0), datetime.time(18, 0))
    weekdays_evening = (datetime.time(18, 0), datetime.time(23, 59, 59))
    weekends_all_day = (datetime.time(0, 0), datetime.time(23, 59, 59))

    # Define functions to apply discount factors based on time intervals
    def apply_discount(row):
        if row['start_time'].weekday() < 5:  # Weekdays (Monday to Friday)
            if weekdays_morning[0] <= row['start_time'].time() <= weekdays_morning[1]:
                return row * 0.8
            elif weekdays_afternoon[0] <= row['start_time'].time() <= weekdays_afternoon[1]:
                return row * 1.2
            elif weekdays_evening[0] <= row['start_time'].time() <= weekdays_evening[1]:
                return row * 0.8
        else:  # Weekends (Saturday and Sunday)
            return row * 0.7

    # Apply discount factors to vehicle columns based on time intervals
    vehicle_columns = ['moto', 'car', 'rv', 'bus', 'truck']
    for col in vehicle_columns:
        df[col] = df[col].apply(apply_discount)

    # Add columns for start_day and end_day
    df['start_day'] = df['start_time'].dt.day_name()
    df['end_day'] = df['end_time'].dt.day_name()
    return df
