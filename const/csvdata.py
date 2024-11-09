# Read CSV file and translate into dictionaries.
# Example input file:
#"year","state","state_po","county_name","county_fips","office","candidate","party","candidatevotes","totalvotes","version","mode"
#2000,"ALABAMA","AL","AUTAUGA",1001,"US PRESIDENT","AL GORE","DEMOCRAT",4942,17208,20220315,"TOTAL"

import csv
from .const import get_state_info_by_abbr, get_special_county_id_by_name

# fn = 'countypres_2000-2020.csv'

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
def get_county_dict():
    return county_dict


# a global dictionary of the candidates with a numeric id
candidate_list = []
def get_candidate_list():
    return candidate_list

# a global dictionary of the parties with a numeric id
party_list = []
def get_party_list():
    return party_list

def get_valid_county_codes(row):
    state_po = row['state_po']
    county_fips_text = row['county_fips']
    state_id = 0
    county_code = 0
    county_fips = 0
    state_info = get_state_info_by_abbr(state_po)
    if state_info != None:
        state_id = state_info.get('state_id')

    if county_fips_text == 'NA':
        county_name = row['county_name']
        county_id = get_special_county_id_by_name(county_name) 
        if county_id == None:
            county_id = 0
            print('Error: County name not found:', county_name)       
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
    
    state_id, county_code, county_fips = get_valid_county_codes(row)

    if county_fips not in county_dict:
        county_dict[county_fips] = {
            'state_po': state_po,
            'county_name': county_name,
        }

    return


_voting_mode_list = []

def get_voting_mode_list():
    return _voting_mode_list

def update_voting_mode_dict(row):
    mode = row['mode']
    
    if mode not in _voting_mode_list:
        _voting_mode_list.append(mode)

    return


_voting_year_list = []
def get_voting_year_list():
    return _voting_year_list

def update_voting_year_list(row):
    year = row['year']
    
    if year not in _voting_year_list:
        _voting_year_list.append(year)

    return



def update_global_dicts(row):
    update_party_dict(row)
    update_candidate_list(row)
    update_county_dict(row)
    update_voting_mode_dict(row)
    update_voting_year_list(row)
    return

voting_data = {}

def update_voting_data(row):
    year = row['year']
    party = row['party']
    candidatevotes = int(row['candidatevotes'])
    totalvotes = int(row['totalvotes'])
    mode = row['mode']

    state_id, county_code, county_fips = get_valid_county_codes(row)

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

def get_voting_data():
    return voting_data

def read_csv(file_name):
    with open(file_name) as f:
        reader = csv.DictReader(f)
        for row in reader:
            # print(row)
            yield row

def read_file(file_name):
    for row in read_csv(file_name):
        update_global_dicts(row)
        update_voting_data(row)

    update_voting_data_winner()


if __name__ == '__main__':
    fn = 'countypres_2000-2020.csv'
    read_file(fn)
    # print('party_list:', party_list)
    # print('candidate_list:', candidate_list)
    print('county_dict:', county_dict)
    # print('voting_mode_list:', voting_mode_list)
    # print('state_dict:', state_dict)
    # print('state_code_dict:', state_code_dict)
    # print('voting_data:', voting_data)

    print('Done')




