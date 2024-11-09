from const import const, csvdata

import json

file_name = 'countypres_2000-2020.csv'
csvdata.read_file(file_name)

# print (csvdata.get_county_dict())

def write_json_file(file_name, data, indexed=False, sortKeys=False):
    with open(file_name, 'w') as f:
        if indexed:
            indexed_data = { str(i+1): data[i] for i in range(len(data)) }
            json.dump(indexed_data, f, indent=4)
        else:
            json.dump(data, f, indent=4)

county_dict = csvdata.get_county_dict()        
write_json_file('county_id.json', county_dict, indexed=False)



write_json_file('party_id.json', csvdata.get_party_list(), indexed=True)
write_json_file('candidate_id.json', csvdata.get_candidate_list(), indexed=True)
write_json_file('state_id.json', const.get_state_dict(), indexed=False)
write_json_file('voting_mode_id.json', csvdata.get_voting_mode_list(), indexed=True)
write_json_file('voting_year_id.json', csvdata.get_voting_year_list(), indexed=True)
write_json_file('voting_data.json', csvdata.get_voting_data(), indexed=False, sortKeys=True)