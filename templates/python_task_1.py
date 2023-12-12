import pandas as pd


def generate_car_matrix(df)->pd.DataFrame:
    """
    Creates a DataFrame  for id combinations.

    Args:
        df (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Matrix generated with 'car' values, 
                          where 'id_1' and 'id_2' are used as indices and columns respectively.
    """
    # Write your logic here
    df = df.pivot(index='id_1', columns='id_2', values='car').fillna(0)
    
    # Replace the diagonal values with 0
    for i in range(min(df.shape)):
        df.iloc[i, i] = 0
    
    return df


def get_type_count(df)->dict:
    """
    Categorizes 'car' values into types and returns a dictionary of counts.

    Args:
        df (pandas.DataFrame)

    Returns:
        dict: A dictionary with car types as keys and their counts as values.
    """
    # Write your logic here
    df['car_type'] = pd.cut(df['car'], bins=[-float('inf'), 15, 25, float('inf')],
                            labels=['low', 'medium', 'high'], right=False)

    #calculate the count of occurrences for each 'car_type' category
    type_counts = df['car_type'].value_counts().to_dict()

    #sort the dictionary alphabetically based on keys
    ans = sorted(type_counts.items())
    return dict()


def get_bus_indexes(df)->list:
    """
    Returns the indexes where the 'bus' values are greater than twice the mean.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of indexes where 'bus' values exceed twice the mean.
    """
    # Write your logic here
    bus_mean = df['bus'].mean()
    
    #identify indices where 'bus' values are greater than twice 
    bus_indexes = df[df['bus'] > 2 * bus_mean].index.tolist()
    
    #sort the indices in ascending order
    bus_indexes.sort()
    return list()


def filter_routes(df)->list:
    """
    Filters and returns routes with average 'truck' values greater than 7.

    Args:
        df (pandas.DataFrame)

    Returns:
        list: List of route names with average 'truck' values greater than 7.
    """
    # Write your logic here
    route_avg_truck = df.groupby('route')['truck'].mean()
    
    #Filter routes where the average of 'truck' column is greater than 7
    filtered_routes = route_avg_truck[route_avg_truck > 7].index.tolist()
    
    #Sort the list of filtered routes
    filtered_routes.sort()
    return list()


def multiply_matrix(matrix)->pd.DataFrame:
    """
    Multiplies matrix values with custom conditions.

    Args:
        matrix (pandas.DataFrame)

    Returns:
        pandas.DataFrame: Modified matrix with values multiplied based on custom conditions.
    """
    # Write your logic here
    df = df.copy(deep=True)
    
    #Apply the specified logic to modify values in the DataFrame
    df = df.applymap(lambda x: x * 0.75 if x > 20 else x * 1.25)
    
    #Round the modified values to 1 decimal place
    df = df.round(1)
    return matrix


def time_check(df)->pd.Series:
    """
    Use shared dataset-2 to verify the completeness of the data by checking whether the timestamps for each unique (`id`, `id_2`) pair cover a full 24-hour and 7 days period

    Args:
        df (pandas.DataFrame)

    Returns:
        pd.Series: return a boolean series
    """
    # Write your logic here
    try:
        # Combine date and time columns to create datetime columns
        df['start_datetime'] = pd.to_datetime(df['startDay'] + ' ' + df['startTime'], errors='coerce')
        df['end_datetime'] = pd.to_datetime(df['endDay'] + ' ' + df['endTime'], errors='coerce')

        # Drop rows with invalid timestamps
        df = df.dropna(subset=['start_datetime', 'end_datetime'])

        # Calculate time differences
        df['time_diff'] = (df['end_datetime'] - df['start_datetime']).dt.total_seconds()

        # Group by (id, id_2) pairs and check completeness of timestamps
        completeness_check = df.groupby(['id', 'id_2']).apply(
            lambda x: (
                (x['time_diff'].min() >= 0) and 
                (x['time_diff'].max() >= 86399) and 
                (x['start_datetime'].dt.weekday.min() == 0) and 
                (x['start_datetime'].dt.weekday.max() == 6)
            )  
        )

        return completeness_check
    except Exception as e:
        print("Error:", e)
    return pd.Series()
