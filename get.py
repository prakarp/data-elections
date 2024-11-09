import json
from const import const

with open('voting_data.json') as f:
    voting_data = json.load(f)

with open('county_id.json') as f:
    county_id = json.load(f)

with open('party_id.json') as f:
    party_id = json.load(f)

with open('candidate_id.json') as f:
    candidate_id = json.load(f)

with open('state_id.json') as f:
    state_id = json.load(f)

with open('voting_mode_id.json') as f:
    voting_mode_id = json.load(f)

with open('voting_year_id.json') as f:
    voting_year_id = json.load(f)

swing_to_blue_counties_list = []
swing_to_red_counties_list = []
red_counties_list = []
notso_red_counties_list = []
blue_counties_list = []
notso_blue_counties_list = []

for county_fips, county_data in voting_data.items():
    if '2016' not in county_data or '2020' not in county_data:
        print('Skipping county:', county_fips)
        continue
        
    y2016 = county_data['2016']
    y2020 = county_data['2020']
    
    republican = 'REPUBLICAN'
    democrat = 'DEMOCRAT'
    percentage = 'percentage'

    y2016_winner = y2016['winning_party']
    y2020_winner = y2020['winning_party']

    y2016_parties = y2016['parties']
    y2020_parties = y2020['parties']
                         
    if y2016_winner == republican and y2020_winner == republican:
        # both times it was republican, but check if the margin increased.
        if y2016_parties[republican][percentage] > y2020_parties[republican][percentage]:
            red_counties_list.append(county_fips)
        else:
            notso_red_counties_list.append(county_fips)
    elif y2016_winner == democrat and y2020_winner == democrat:
        # both times it was democrat, but check if the margin increased.
        if y2016_parties[democrat][percentage] > y2020_parties[democrat][percentage]:
            blue_counties_list.append(county_fips)
        else:
            notso_blue_counties_list.append(county_fips)
    elif y2016_winner == republican and y2020_winner == democrat:
        swing_to_blue_counties_list.append(county_fips)
    elif y2016_winner == democrat and y2020_winner == republican:
        swing_to_red_counties_list.append(county_fips)

print('Red Counties:', red_counties_list)
print('Blue Counties:', blue_counties_list)

print('Swing to red Counties:', swing_to_red_counties_list)
print('Swing to blue Counties:', swing_to_blue_counties_list)

def get_county_data_with_details(state_abbr, county_name):
    state_id = const.get_state_info_by_abbr(state_abbr)['state_id']
    county_id = const.get_