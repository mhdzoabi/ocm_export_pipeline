
def map_stations(df):
    stations_df_mapped = df
    stations_df_mapped = stations_df_mapped[["ID"]]
    stations_df_mapped.rename(columns={'ID': 'id'})
    return stations_df_mapped