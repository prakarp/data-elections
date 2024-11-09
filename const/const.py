# const_data/const.py

state_id_abbr_list = {
    1:  'AL',  # Alabama
    2:  'AK',  # Alaska
    4:  'AZ',  # Arizona
    5:  'AR',  # Arkansas
    6:  'CA',  # California
    8:  'CO',  # Colorado
    9:  'CT',  # Connecticut
    10: 'DE',  # Delaware
    11: 'DC',  # District of Columbia
    12: 'FL',  # Florida
    13: 'GA',  # Georgia
    15: 'HI',  # Hawaii
    16: 'ID',  # Idaho
    17: 'IL',  # Illinois
    18: 'IN',  # Indiana
    19: 'IA',  # Iowa
    20: 'KS',  # Kansas
    21: 'KY',  # Kentucky
    22: 'LA',  # Louisiana
    23: 'ME',  # Maine
    24: 'MD',  # Maryland
    25: 'MA',  # Massachusetts
    26: 'MI',  # Michigan
    27: 'MN',  # Minnesota
    28: 'MS',  # Mississippi
    29: 'MO',  # Missouri
    30: 'MT',  # Montana
    31: 'NE',  # Nebraska
    32: 'NV',  # Nevada
    33: 'NH',  # New Hampshire
    34: 'NJ',  # New Jersey
    35: 'NM',  # New Mexico
    36: 'NY',  # New York
    37: 'NC',  # North Carolina
    38: 'ND',  # North Dakota
    39: 'OH',  # Ohio
    40: 'OK',  # Oklahoma
    41: 'OR',  # Oregon
    42: 'PA',  # Pennsylvania
    44: 'RI',  # Rhode Island
    45: 'SC',  # South Carolina
    46: 'SD',  # South Dakota
    47: 'TN',  # Tennessee
    48: 'TX',  # Texas
    49: 'UT',  # Utah
    50: 'VT',  # Vermont
    51: 'VA',  # Virginia
    53: 'WA',  # Washington
    54: 'WV',  # West Virginia
    55: 'WI',  # Wisconsin
    56: 'WY',  # Wyoming
    60: 'AS',  # American Samoa
    66: 'GU',  # Guam
    69: 'MP',  # Northern Mariana Islands
    72: 'PR',  # Puerto Rico
    78: 'VI',  # U.S. Virgin Islands
}

state_id_name_list = {
    1: 'Alabama',
    2: 'Alaska',
    4: 'Arizona',
    5: 'Arkansas',
    6: 'California',
    8: 'Colorado',
    9: 'Connecticut',
    10: 'Delaware',
    11: 'District of Columbia',
    12: 'Florida',
    13: 'Georgia',
    15: 'Hawaii',
    16: 'Idaho',
    17: 'Illinois',
    18: 'Indiana',
    19: 'Iowa',
    20: 'Kansas',
    21: 'Kentucky',
    22: 'Louisiana',
    23: 'Maine',
    24: 'Maryland',
    25: 'Massachusetts',
    26: 'Michigan',
    27: 'Minnesota',
    28: 'Mississippi',
    29: 'Missouri',
    30: 'Montana',
    31: 'Nebraska',
    32: 'Nevada',
    33: 'New Hampshire',
    34: 'New Jersey',
    35: 'New Mexico',
    36: 'New York',
    37: 'North Carolina',
    38: 'North Dakota',
    39: 'Ohio',
    40: 'Oklahoma',
    41: 'Oregon',
    42: 'Pennsylvania',
    44: 'Rhode Island',
    45: 'South Carolina',
    46: 'South Dakota',
    47: 'Tennessee',
    48: 'Texas',
    49: 'Utah',
    50: 'Vermont',
    51: 'Virginia',
    53: 'Washington',
    54: 'West Virginia',
    55: 'Wisconsin',
    56: 'Wyoming',
    60: 'American Samoa',
    66: 'Guam',
    69: 'Northern Mariana Islands',
    72: 'Puerto Rico',
    78: 'U.S. Virgin Islands',
}


_special_county_id_by_name = {
    'MAINE UOCAVA': 999,
    'STATEWIDE WRITEIN': 998,
    'FEDERAL PRECINCT': 997,
}

_special_county_name_by_id = {}
_state_fips_info_by_id = {}
_state_fips_info_by_abbr = {}

def get_state_dict():
    return _state_fips_info_by_abbr

def init_state_info():
    for state_id, state_abbr in state_id_abbr_list.items():
        _state_fips_info_by_id[state_id] = {
            'state_abbr': state_abbr,
            'state_name': state_id_name_list[state_id],
        }

   
    for state_id, state_abbr in state_id_abbr_list.items():
        _state_fips_info_by_abbr[state_abbr] = {
            'state_id':    state_id,
            'state_name': state_id_name_list[state_id],
        }

    for county_name, county_id in _special_county_id_by_name.items():
        _special_county_name_by_id[county_id] = county_name

def get_state_info(state_id):
    if state_id in _state_fips_info_by_id:
        return _state_fips_info_by_id[state_id]
    else:
        return None

def get_state_info_by_abbr(state_abbr):
    if state_abbr in _state_fips_info_by_abbr:
        return _state_fips_info_by_abbr[state_abbr]
    else:
        return None

def get_special_county_id_by_name(county_name):
    if county_name in _special_county_id_by_name:
        return _special_county_id_by_name[county_name]
    else:
        return None
    
def get_special_county_name_by_id(county_id):
    if county_id in _special_county_name_by_id:
        return _special_county_name_by_id[county_id]
    else:
        return None
    

_initialized = False
if not _initialized:
    init_state_info()
    _initialized = True
