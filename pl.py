import pandas as pd

file_name = 'countypres_2000-2020.csv'

# Read the CSV file
df_unsorted = pd.read_csv(file_name)


df = df_unsorted.sort_values(by=['year', 'county_fips', 'party', 'mode'])

# Ensure consistent capitalization (optional)
df['county_name'] = df['county_name'].str.upper()
df['party'] = df['party'].str.upper()

# Query examples
def query_data(year=None, county_name=None, party=None):
    query_df = df
    if year is not None:
        query_df = query_df[query_df['year'] == year]
    if county_name is not None:
        query_df = query_df[query_df['county_name'] == county_name.upper()]
    if party is not None:
        query_df = query_df[query_df['party'] == party.upper()]
    return query_df

# Example usage
# result = query_data(year=2000, county_name='AUTAUGA', party='DEMOCRAT')
# print(result)

unique_modes = df['mode'].unique()
# print(unique_modes)

unique_parties = df['party'].unique()
# print(unique_parties)

unique_candidates = df['candidate'].unique()
# print(unique_candidates)

unique_states = df['state'].unique()
# print(unique_states)

unique_years = df['year'].unique()
# print(unique_years)

unique_state_po = df['state_po'].unique()
# print(unique_state_po)

