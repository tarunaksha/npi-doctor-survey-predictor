def filter_doctors_by_time(df, input_time, hour_tolerance=1, prob_threshold=0.5):
    """
    Filter the dataframe to select doctors based on:
    - Their login hour being within `hour_tolerance` of the input time's hour.
    - Their attendance probability exceeding `prob_threshold`.
    """
    input_hour = input_time.hour
    filtered_df = df[(df['login_hour'] - input_hour).abs() <= hour_tolerance]
    filtered_df = filtered_df[filtered_df['attendance_prob'] > prob_threshold]
    return filtered_df
