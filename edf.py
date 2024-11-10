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
            'state_po': 'first',
            'county_fips': 'first'
        }).pipe(ElectionDataFrame)

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
        return self.pivot_table(index=['year', 'state', 'state_po', 'county_name', 'county_fips'], columns=['party'],
                        values=['candidatevotes', 'totalvotes', 'percentage']).reset_index().pipe(ElectionDataFrame)

    
    def calculate_winner_state(self):
        """Calculate the winner based on the candidate with the most votes, modifying self.data in place."""
    
        # Assuming self.data holds the DataFrame
        result = self.filter_data(years=None, parties=['REPUBLICAN', 'DEMOCRAT'])
        result = result.aggregate_data_per_state().add_percentage().combine_votes_per_state()
        result['winner'] = result.apply(
            lambda x: 'REPUBLICAN' if x['candidatevotes']['REPUBLICAN'] > x['candidatevotes']['DEMOCRAT'] else 'DEMOCRAT', 
            axis=1)

        return result
    
    def calculate_winner_county(self):
        """Calculate the winner based on the candidate with the most votes, modifying self.data in place."""
    
        # Assuming self.data holds the DataFrame
        result = self.filter_data(years=None, parties=['REPUBLICAN', 'DEMOCRAT'])
        # print (result)
        result = result.add_percentage()
        # print(result)
        result = result.combine_votes_per_county()
        result['winner'] = result.apply(
            lambda x: 'REPUBLICAN' if x['candidatevotes']['REPUBLICAN'] > x['candidatevotes']['DEMOCRAT'] else 'DEMOCRAT', 
            axis=1)

        return result
 
    def flatten_pivoted_table(self):
        """Flatten a pivoted table to a regular DataFrame."""     
        newcolumns = []
        for col in result.columns.values:
            newcolumns.append('_'.join(filter(None, map(str,col))))
        self.columns = newcolumns
        self.drop(columns=['totalvotes_REPUBLICAN'], inplace=True)
        self.rename(columns={'totalvotes_DEMOCRAT':'totalvotes'}, inplace=True)
        return self

    def find_swing_states(self):
        df = self
        condition_2012 = (df['year'] == 2012) & (df['winner'] == 'DEMOCRAT')
        condition_2016 = (df['year'] == 2016) & (df['winner'] == 'REPUBLICAN')
        condition_2020 = (df['year'] == 2020) & (df['winner'] == 'DEMOCRAT')

        # Find states that satisfy all conditions
        states_2012 = df[condition_2012]['state']
        states_2016 = df[condition_2016]['state']
        states_2020 = df[condition_2020]['state']

        # print ("States that satisfy the conditions for 2012:", states_2012)
        # print ("States that satisfy the conditions for 2016:", states_2016)
        # print ("States that satisfy the conditions for 2020:", states_2020)

        # Find states that satisfy all conditions
        swing_states = set(states_2012) & set(states_2016) & set(states_2020)
        return swing_states
        # print("Swing states:", swing_states)


    def find_swing_counties(self):
        df = self
        condition_2012 = (df['year'] == 2012) & (df['winner'] == 'DEMOCRAT')
        condition_2016 = (df['year'] == 2016) & (df['winner'] == 'REPUBLICAN')
        condition_2020 = (df['year'] == 2020) & (df['winner'] == 'DEMOCRAT')

        # Find states that satisfy all conditions
        elections_2012 = df[condition_2012] 
        elections_2016 = df[condition_2016]
        elections_2020 = df[condition_2020]

        # Find states that satisfy all conditions
        swing_elections = set(elections_2012) & set(elections_2016) & set(elections_2020)
        print(swing_elections)
        swing_elections = set(elections_2012['county_name']) & \
                set(elections_2016['county_name']) & set(elections_2020['county_name'])
        return swing_elections
        # print("Swing states:", swing_states)'state',

    
    def find_swing_counties_df(self):
        # Define conditions for each year and winner
        condition_2012 = (self['year'] == 2012) & (self['winner'] == 'DEMOCRAT')
        condition_2016 = (self['year'] == 2016) & (self['winner'] == 'REPUBLICAN')
        condition_2020 = (self['year'] == 2020) & (self['winner'] == 'DEMOCRAT')

        # Filter data to find counties meeting each condition
        elections_2012 = self[condition_2012]
        elections_2016 = self[condition_2016]
        elections_2020 = self[condition_2020]

        # Find swing counties that are in all three filtered datasets
        swing_county_keys = set(elections_2012['county_fips']) & \
                            set(elections_2016['county_fips']) & \
                            set(elections_2020['county_fips'])
        print("Swing county keys:", swing_county_keys)
        swing_df = self[(self['county_fips'].isin(swing_county_keys) & (self['year'] == 2020))]  
        print("Swing DF:\n", swing_df)
        # Get unique county information for swing counties (consistent columns)
        county_info = swing_df[['state', 'state_po', 'county_fips', 'county_name']]
        print("County info:\n", county_info)
        # Merge the county information with the election results for each year
        result_df = county_info.merge(
            swing_df[['county_fips']],
            on='county_fips',
            how='left'
        )
        
        return swing_df.reset_index().pipe(ElectionDataFrame)

# Define a custom DataFrame subclass for custom methods

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

result = df.calculate_winner_state()
# print (result)
#      year          state candidatevotes            percentage            totalvotes                 winner
# party                            DEMOCRAT REPUBLICAN   DEMOCRAT REPUBLICAN   DEMOCRAT REPUBLICAN            
# 0      2000        ALABAMA         695602     944409      41.59      56.47    1672551    1672551  REPUBLICAN
# 1      2000         ALASKA          79004     167398      27.67      58.63     285530     285530  REPUBLICAN


result = result.flatten_pivoted_table()
# print(result)
# [306 rows x 9 columns]
#     year          state  candidatevotes_DEMOCRAT  candidatevotes_REPUBLICAN  percentage_DEMOCRAT  percentage_REPUBLICAN  totalvotes      winner
#0    2000        ALABAMA                   695602                     944409                41.59                  56.47     1672551  REPUBLICAN
#1    2000         ALASKA                    79004                     167398                27.67                  58.63      285530  REPUBLICAN

result.to_csv('states_2020_result.csv', index=False)

# 2020 ALABAMA   DONALD J TRUMP            1441170     2323282   REPUBLICAN       AL       62.03
#               JOSEPH R BIDEN JR          849624     2323282     DEMOCRAT       AL       36.57

# print("Swing states:", result.find_swing_states())

result = df.calculate_winner_county()
# print(result)
result = result.flatten_pivoted_table()
print(result)
# swing_counties = result.find_swing_counties()
# print("Swing counties:", swing_counties)

# print(result)
swing_counties_df = result.find_swing_counties_df()
print(swing_counties_df)
