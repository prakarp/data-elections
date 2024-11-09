import pandas as pd

# Define a custom DataFrame subclass for custom methods
class ElectionDataFrame(pd.DataFrame):
    # Ensure that __finalize__ returns the subclass type on DataFrame operations
    _internal_names = pd.DataFrame._internal_names
    _internal_names_set = set(_internal_names)

    @property
    def _constructor(self):
        return ElectionDataFrame
    
    def prepare_data(self):
        """Sort and normalize capitalization for consistency."""
        self.sort_values(by=['year', 'county_fips', 'party', 'mode'], inplace=True)
        self['county_name'] = self['county_name'].str.upper()
        self['party'] = self['party'].str.upper()
        return self

    def query_data(self, year=None, county_name=None, party=None):
        """Filter data based on year, county name, and party."""
        query_df = self
        if year is not None:
            query_df = query_df[query_df['year'] == year]
        if county_name is not None:
            query_df = query_df[query_df['county_name'] == county_name.upper()]
        if party is not None:
            query_df = query_df[query_df['party'] == party.upper()]
        return query_df.pipe(ElectionDataFrame)

    def aggregate_data_per_state(self):
        """Aggregate data by summing votes for each candidate per state and year."""
        return self.groupby(['year', 'state', 'candidate']).agg({
            'candidatevotes': 'sum',
            'totalvotes': 'sum',
            'party': 'first',
            'state_po': 'first'
        }).pipe(ElectionDataFrame)

    def filter_data2(self, years=None, parties=None):
        """Filter data based on year, state, and candidate."""
        filtered_df = self
        if years is not None:
            filtered_df = filtered_df[filtered_df['year'].isin(years)]
        if parties is not None:
            filtered_df = filtered_df[filtered_df['party'].isin(parties)]
        return filtered_df.pipe(ElectionDataFrame)

    def filter_data(self, years=None, parties=None):
        """Filter data based on year, state, and candidate"""
        conditions = pd.Series([True] * len(self), index=self.index)

        if years is not None:
            conditions &= self['year'].isin(years)
        if parties is not None:
            conditions &= self['party'].isin(parties)

        return self[conditions].pipe(ElectionDataFrame)
    
    def add_percentage(self):
        """Add a percentage column of candidate votes to total votes."""
        self['percentage'] = (self['candidatevotes'] / self['totalvotes']).mul(100).round(2)
        return self

    def combine_votes_per_state(self):
        """Combine votes for each candidate per state and year."""
        return self.pivot_table(index=['year', 'state'], columns=['party'],
                        values=['candidatevotes', 'totalvotes', 'percentage']).reset_index().pipe(ElectionDataFrame)  
    
    def combine_votes_per_county(self):
        """Combine votes for each candidate per county and year."""
        return self.pivot_table(index=['year', 'state', 'county_name'], columns=['party'],
                        values=['candidatevotes', 'totalvotes', 'percentage']).reset_index().pipe(ElectionDataFrame)

    
    def calculate_winner2(self):
        """Calculate the winner based on the candidate with the most votes, modifying self.data in place."""
    
        # Assuming self.data holds the DataFrame
        result = self.filter_data(years=None, parties=['REPUBLICAN', 'DEMOCRAT']).aggregate_data_per_state().add_percentage().combine_votes_per_state()        
        result['winner'] = result.apply(
            lambda x: 'REPUBLICAN' if x['candidatevotes']['REPUBLICAN'] > x['candidatevotes']['DEMOCRAT'] else 'DEMOCRAT', 
            axis=1)

        return result

# Load and prepare the data
file_name = 'countypres_2000-2020.csv'
df = pd.read_csv(file_name, dtype={'year': int, 'county_fips': str, 'party': str, 'mode': str, 'candidate': str, 'state': str, 'state_po': str})
df = ElectionDataFrame(df).prepare_data()

# Example queries
# result = df.query_data(year=2000, county_name='AUTAUGA', party='DEMOCRAT')
# print(result)

# Get unique values from specific columns
"""
print(df['mode'].unique())
print(df['party'].unique())
print(df['candidate'].unique())
print(df['state'].unique())
print(df['year'].unique())
print(df['state_po'].unique())

"""



# Aggregate and add percentage
# result_2020 = df.filter_data(year=2020)
# result_2020_states = result_2020.aggregate_data().add_percentage()

# print(result_2020_states)

result = df.calculate_winner2()
print (result)

print("OLD CODE")
# filter data based on party and year
result = df.filter_data(years=None, parties=['REPUBLICAN', 'DEMOCRAT'])
# print(result)
# Combine votes with the new method

result = result.aggregate_data_per_state().add_percentage().combine_votes_per_state()

result['winner'] = result.apply(
    lambda x: 'REPUBLICAN' if x['candidatevotes']['REPUBLICAN'] > x['candidatevotes']['DEMOCRAT'] else 'DEMOCRAT', 
    axis=1)
 


print("Results with the percentage of votes for Democrats and Republicans in 2020")
# result = result.add_percentage()
# print(result.add_percentage())
print(result)
print(result.columns.values)


newcolumns = []
for col in result.columns.values:
    newcolumns.append('_'.join(filter(None, map(str,col))))
print(newcolumns)


result.columns = newcolumns
print(result.columns.values)
result = result.drop(columns=['totalvotes_REPUBLICAN'])
result.rename(columns={'totalvotes_DEMOCRAT':'totalvotes'}, inplace=True)

# result.column_names = ['_'.join(map(str,col)).strip('_') for col in result.columns.values]  
result.to_csv('states_2020_result.csv', index=False)

# 2020 ALABAMA   DONALD J TRUMP            1441170     2323282   REPUBLICAN       AL       62.03
#               JOSEPH R BIDEN JR          849624     2323282     DEMOCRAT       AL       36.57

# Filter rows for each condition and find states that satisfy all conditions
df = result
condition_2012 = (df['year'] == 2012) & (df['winner'] == 'DEMOCRAT')
condition_2016 = (df['year'] == 2016) & (df['winner'] == 'REPUBLICAN')
condition_2020 = (df['year'] == 2020) & (df['winner'] == 'DEMOCRAT')

# Find states that satisfy all conditions
states_2012 = df[condition_2012]['state']
states_2016 = df[condition_2016]['state']
states_2020 = df[condition_2020]['state']

print ("States that satisfy the conditions for 2012:", states_2012)
print ("States that satisfy the conditions for 2016:", states_2016)
print ("States that satisfy the conditions for 2020:", states_2020)

# Find states that satisfy all conditions
swing_states = set(states_2012) & set(states_2016) & set(states_2020)

print("Swing states:", swing_states)
