# Read CSV file and translate into dictionaries.
# Example input file:
#"year","state","state_po","county_name","county_fips","office","candidate","party","candidatevotes","totalvotes","version","mode"
#2000,"ALABAMA","AL","AUTAUGA",1001,"US PRESIDENT","AL GORE","DEMOCRAT",4942,17208,20220315,"TOTAL"

import csv


import const as const

fn = 'countypres_2000-2020.csv'

# declare a sqlalchemy table for a list of all parties whose id
# will be referred to in the candidate table
# party_id, party_name

# declare a sqlalchemy table for a list of all candidates
# candidate_id, candidate_name, party_id

# declare a sqlalchemy table for a list of all counties
# county_id, state, state_po, county

# declare a sqlalchemy table for the election results
# election_id, year, county_id, candidate


# declare a global county dictionary
county_dict = {}

# a global dictionary of the candidates with a numeric id
candidate_list = []

# a global dictionary of the parties with a numeric id
party_list = []

# a global dict the states 
state_dict = {}
state_code_dict = {}

def get_state_code(state_abbr):
    for state_fips_code, state_abbr_code in state_fips.items():
        if state_abbr_code == state_abbr:
            return state_fips_code
    return 0

def get_county_codes(row):
    state_po = row['state_po']
    county_fips_text = row['county_fips']
    state_id = 0
    county_code = 0
    county_fips = 0
    state_id = get_state_code(state_po)

    if county_fips_text == 'NA':
        county_name = row['county_name']
        county_id = const.get_special_county_id_by_name(county_name)        
        county_fips = state_id + county_id
    else:         
        county_fips = int(row['county_fips'])

    county_code = county_fips % 1000

    return state_id, county_code, county_fips


def update_party_dict(row):
    party = row['party']
    
    if party not in party_list:
        party_list.append(party)
        
    return


def update_candidate_list(row):
    candidate = row['candidate']
    
    if candidate not in candidate_list:
        candidate_list.append(candidate)

    return



def update_county_dict(row):
    state_po = row['state_po']
    county_name = row['county_name']
    # county_fips = row['county_fips']
    
    state_id, county_code, county_fips = get_county_codes(row)

    if county_fips not in county_dict:
        county_dict[county_fips] = {
            'state_po': state_po,
            'county_name': county_name,
        }

    return


voting_mode_list = []

def update_voting_mode_dict(row):
    mode = row['mode']
    
    if mode not in voting_mode_list:
        voting_mode_list.append(mode)

    return

def update_global_dicts(row):
    update_party_dict(row)
    update_candidate_list(row)
    update_county_dict(row)
    update_voting_mode_dict(row)
    return


# voting data dictionary.
# for each county_Fips:
#  for each year
#    - total votes
#    - winning party
#    - for each party
#      - candidate votes if total is on the line, if not, add the provisional and other vote types
#      - a boolean flag if total is found. If a TOTAL votes row is found, that takes precedence over
#        provisional and other vote types.
#      - a percentage of the votes for that party. 

voting_data = {}

def update_voting_data(row):
    year = row['year']
    party = row['party']
    candidatevotes = int(row['candidatevotes'])
    totalvotes = int(row['totalvotes'])
    mode = row['mode']

    state_id, county_code, county_fips = get_county_codes(row)

    if county_fips not in voting_data:
        voting_data[county_fips] = {}

    if year not in voting_data[county_fips]:
        voting_data[county_fips][year] = {
            'total_votes': totalvotes,
            'winning_party': -1,
            'parties': {},
        }

    if party not in voting_data[county_fips][year]['parties']:
        voting_data[county_fips][year]['parties'][party] = {
            'candidate_votes': 0,
            'percentage': 0,
        }

    if mode == 'TOTAL':
        voting_data[county_fips][year]['parties'][party]['candidate_votes'] = candidatevotes
        if totalvotes > 0:
            voting_data[county_fips][year]['parties'][party]['percentage'] = candidatevotes / totalvotes
        else:
            voting_data[county_fips][year]['parties'][party]['percentage'] = 0
    else:
        voting_data[county_fips][year]['parties'][party]['candidate_votes'] += candidatevotes
        total_candidate_votes = voting_data[county_fips][year]['parties'][party]['candidate_votes']
        if totalvotes > 0:
            voting_data[county_fips][year]['parties'][party]['percentage'] = total_candidate_votes / totalvotes
        else:
            voting_data[county_fips][year]['parties'][party]['percentage'] = 0

    return

def update_voting_data_winner():
    for county_fips, item in voting_data.items():
        for year in item:
            party_list = voting_data[county_fips][year]['parties']
            winning_party = -1
            winning_party_votes = 0
            for party in party_list:
                if party_list[party]['candidate_votes'] > winning_party_votes:
                    winning_party_votes = party_list[party]['candidate_votes']
                    winning_party = party
            voting_data[county_fips][year]['winning_party'] = winning_party

    return


def read_csv(file_name):
    with open(file_name) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print(row)
            yield row

def read_file(file_name):
    for row in read_csv(fn):
        update_global_dicts(row)
        update_voting_data(row)

    update_voting_data_winner()


def main():
    read_file(fn)
    # print('party_list:', party_list)
    # print('candidate_list:', candidate_list)
    print('county_dict:', county_dict)
    # print('voting_mode_list:', voting_mode_list)
    # print('state_dict:', state_dict)
    # print('state_code_dict:', state_code_dict)
    # print('voting_data:', voting_data)


if __name__ == '__main__':
    main()
    print('Done')





