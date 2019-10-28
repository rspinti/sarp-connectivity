"""Constants used in other scripts."""


# Listing of official SARP states and territories
# can be generated from the state polygon:
# df = gp.read_file(intermediate_dir / "states_prj.shp")[['STUSPS', 'STATEFP', 'NAME']].set_index('STUSPS')
# df = df.loc[df.index.isin(["AL","AR","FL","GA","KY","LA","MO","MS","NC","OK","PR","SC","TN","TX","VA"])].copy()
# SARP_STATES = df.NAME.to_dict()
# SARP_STATES_FIPS = df.STATEFP.to_list()

SARP_STATES = {
    "FL": "Florida",
    "NC": "North Carolina",
    "LA": "Louisiana",
    "GA": "Georgia",
    "AL": "Alabama",
    "TX": "Texas",
    "SC": "South Carolina",
    "OK": "Oklahoma",
    "TN": "Tennessee",
    "KY": "Kentucky",
    "AR": "Arkansas",
    "MS": "Mississippi",
    "MO": "Missouri",
    "PR": "Puerto Rico",
    "VA": "Virginia",
}

# FIPS codes for the above states
SARP_STATES_FIPS = [
    "01",
    "05",
    "12",
    "13",
    "21",
    "22",
    "28",
    "29",
    "37",
    "40",
    "45",
    "47",
    "48",
    "51",
    "72",
]


# NETWORK_TYPES determines the type of network analysis we are doing
# natural: only include waterfalls in analysis
# dams: include waterfalls and dams in analysis
# small_barriers: include waterfalls, dams, and small barriers in analysis
NETWORK_TYPES = ("natural", "dams", "small_barriers")


# Mapping of region to HUC4 IDs that are present within the SARP boundary
REGIONS = {
    "02": [7, 8],
    "03": list(range(1, 19)),
    "05": [5, 7, 9, 10, 11, 13, 14],
    "06": list(range(1, 5)),
    "07": [10, 11, 14],
    "08": list(range(1, 10)),
    "10": [24, 27, 28, 29, 30],
    "11": [1, 4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14],
    "12": list(range(1, 12)),
    "13": [3, 4, 5, 6, 7, 8, 9],
}

# Listing of regions that are connected
CONNECTED_REGIONS = ["05_06", "07_10", "08_11"]


# Group regions based on which ones flow into each other
# Note: many of these flow into region 08, which is not yet available
# The total size of the region group needs to be limited based on available memory and the size of the output shapefiles
# from the network analysis, which cannot exceed 2 GB.

REGION_GROUPS = {
    "02": ["02"],
    "03": ["03"],
    "05_06": ["05", "06"],
    "07_10": ["07", "10"],
    "08_11": ["08", "11"],
    "12": ["12"],
    "13": ["13"],
}

# All barriers that are within 10 meters of each other are reduced to the first one
# Note: Dams within 30 meters of each other are considered duplicates
DUPLICATE_TOLERANCE = 10  # meters

# Use USGS CONUS Albers (EPSG:102003): https://epsg.io/102003    (same as other SARP datasets)
# use Proj4 syntax, since GeoPandas doesn't properly recognize it's EPSG Code.
# CRS = "+proj=aea +lat_1=29.5 +lat_2=45.5 +lat_0=37.5 +lon_0=-96 +x_0=0 +y_0=0 +datum=NAD83 +units=m +no_defs"
CRS = {
    "proj": "aea",
    "lat_1": 29.5,
    "lat_2": 45.5,
    "lat_0": 37.5,
    "lon_0": -96,
    "x_0": 0,
    "y_0": 0,
    "datum": "NAD83",
    "units": "m",
    "no_defs": True,
}


# NOTE: not all feature services have all columns
DAM_COLS = [
    "SARPUniqueID",
    "SNAP2018",
    "NIDID",
    "SourceDBID",
    "Barrier_Name",
    "Other_Barrier_Name",
    "River",
    "PurposeCategory",
    "Year_Completed",
    "Height",
    "StructureCondition",
    "ConstructionMaterial",
    "DB_Source",
    "Recon",
    "PotentialFeasibility",  # only present in NC
]

SMALL_BARRIER_COLS = [
    "SARPUniqueID",
    "AnalysisId",
    "SNAP2018",
    "LocalID",
    "Crossing_Code",
    "StreamName",
    "Road",
    "RoadTypeId",
    "CrossingTypeId",
    "CrossingConditionId",
    "Potential_Project",
    "Source",
    # Not used:
    # "NumberOfStructures",
    # "CrossingComment",
    # "Assessed", # check me
    # "SRI_Score",
    # "Coffman_Strong",
    # "Coffman_Medium",
    # "Coffman_Weak",
    # "SARP_Score",
    # "SE_AOP",
    # "NumberRareSpeciesHUC12", # we add this later
]


# Used to filter small barriers by Potential_Project (small barriers)
# based on guidance from Kat
KEEP_POTENTIAL_PROJECT = [
    "Severe Barrier",
    "Moderate Barrier",
    "Inaccessible",
    "Significant Barrier",
    "Indeterminate",
    "Potential Project",
    "Proposed Project",
]

# "No Upstream Habitat", "No Upstream Channel" excluded intentionally from above


# Used to filter Potential_Project (small barriers)
# These are DROPPED from all analysis and mapping
DROP_POTENTIAL_PROJECT = ["No", "No Barrier", "No Crossing", "Past Project"]


# Used to filter small barriers and dams by SNAP2018, based on guidance from Kat
# Note: dropped barriers are still shown on the map, but not included in the network analysis
# Note: 0 value indicates N/A
DROP_SNAP2018 = [6, 8]

# These are excluded from network analysis / prioritization, but included for mapping
EXCLUDE_SNAP2018 = [5, 10]

# Used to filter dams by Recon
# based on guidance from Kat
DROP_RECON = [5, 7, 19]
DROP_FEASIBILITY = [7, 8]

# These are excluded from network analysis / prioritization, but included for mapping
EXCLUDE_RECON = [16]

# Applies to Recon values, omitted values should be filtered out
RECON_TO_FEASIBILITY = {
    0: 0,
    1: 3,
    2: 3,
    3: 2,
    4: 1,
    5: 7,  # should be removed from analysis
    6: 2,
    7: 8,  # should be removed from analysis
    8: 6,
    9: 6,
    10: 6,
    11: 4,
    13: 6,
    14: 4,
    15: 5,
    16: 9,
    17: 6,
    18: 6,
    19: 10,  # should be removed from analysis
    20: 5,
    21: 6,
}

# Associated recon values
# FEASIBILITY = {
#   0: 'Not assessed',
#   1: 'Not feasible',
#   2: 'Likely infeasible',
#   3: 'Possibly feasible',
#   4: 'Likely feasible',
#   5: 'No conservation benefit',
#   6: 'Unknown',
#   # not shown to user
#   # 6: 'Unknown',
#   # 7: 'Error',
#   # 8: 'Dam removed for conservation benefit'
#   # 9: 'Invasive species barrier',
#   # 10: 'Proposed dam'
# }


POTENTIAL_TO_SEVERITY = {
    "Inaccessible": 0,
    "Indeterminate": 0,
    "Insignificant Barrier": 1,
    "Minor Barrier": 1,
    "Moderate Barrier": 2,
    "No Barrier": 1,  # removed from processing
    "No Crossing": 1,
    "No Upstream Channel": 1,
    "No Upstream Habitat": 1,
    "Not Scored": 0,
    "No": 1,
    "Past Project": 0,  # removed from processing
    "Potential Project": 0,
    "Proposed Project": 0,
    "Severe Barrier": 3,
    "Significant Barrier": 3,
    "Small Project": 0,
    "SRI Only": 0,
}

CROSSING_TYPE_TO_DOMAIN = {
    "Bridge": 2,
    "Bridge Adequate": 2,
    "Buried Stream": 6,
    "Culvert": 3,
    "Dam": 5,
    "Ford": 4,
    "Inaccessible": 0,
    "Multiple Culvert": 3,
    "Multiple Culverts": 3,
    "Natural Ford": 4,
    "No Crossing": 1,
    "No Upstream Channel": 1,
    "Other": 0,
    "Partially Inaccessible": 0,
    "Removed Crossing": 1,
    "Slab": 4,
    "Unknown": 0,
    "Vented Ford": 4,
    "Vented Slab": 4,
}

ROAD_TYPE_TO_DOMAIN = {
    "Asphalt": 2,
    "Concrete": 2,
    "Dirt": 1,
    "Driveway": 0,
    "Gravel": 1,
    "Other": 0,
    "Paved": 2,
    "Railroad": 3,
    "Trail": 1,
    "Unknown": 0,
    "Unpaved": 1,
    "No Data": 0,
    "Nodata": 0,
}

BARRIER_CONDITION_TO_DOMAIN = {"Failing": 1, "New": 4, "OK": 3, "Poor": 2, "Unknown": 0}

OWNERTYPE_TO_DOMAIN = {
    # Unknown types are not useful
    # "Unknown": 0,
    # "Designation": 0,
    "US Fish and Wildlife Service": 1,
    "USDA Forest Service": 2,
    "Federal Land": 3,
    "State Land": 4,
    "Local Land": 5,
    "Joint Ownership": 5,
    "Regional Agency Special Distribution": 5,
    "Native American Land": 6,
    "Easement": 7,
    "Private Conservation Land": 8,
}

# Map of owner type domain above to whether or not the land is
# considered public
OWNERTYPE_TO_PUBLIC_LAND = {
    1: True,
    2: True,
    3: True,
    4: True,
    5: True
}

# NHDPlusIDs to exclude when extracting flowlines (e.g., within Chesapeake Bay)
# indexed by HUC4
EXCLUDE_IDs = {
    "0208": [
        10000300159048,
        10000300159054,
        10000300023678,
        10000300023872,
        10000300023338,
        10000300023343,
        10000300023344,
        10000300023751,
        10000300023796,
        10000300023044,
        10000300010841,
        10000300010844,
        10000300010705,
        10000300010710,
        10000300011010,
        10000300011011,
        10000300011331,
        10000300011550,
        10000300011333,
        10000300023605,
        10000300023609,
        10000300023611,
        10000300011392,
        10000300011393,
        10000300010853,
        10000300011551,
        10000300023671,
        10000300011238,
        10000300011539,
        10000300011540,
        10000300011541,
        10000300011542,
        10000300011543,
        10000300011139,
        10000300011145,
        10000300011147,
        10000300011458,
        10000300011461,
        10000300011224,
        10000300011229,
        10000300011468,
        10000300011401,
        10000300011159,
        10000300011474,
        10000300023462,
        10000300023448,
        10000300023449,
        10000300023450,
        10000300011412,
        10000300022700,
        10000300022871,
        10000300023629,
        10000300023001,
        10000300023002,
        10000300023554,
        10000300023556,
        10000300023562,
        10000300022879,
        10000300022883,
        10000300047458,
        10000300048203,
        10000300047698,
        10000300048402,
        10000300048099,
        10000300048104,
        10000300048406,
        10000300048407,
        10000300049081,
        10000300048274,
        10000300047694,
        10000300047549,
        10000300047550,
        10000300047553,
        10000300047864,
        10000300047865,
        10000300047868,
        10000300048115,
        10000300048117,
        10000300048196,
        10000300048014,
        10000300048281,
        10000300048287,
        10000300048319,
        10000300048343,
        10000300048344,
        10000300036845,
        10000300036846,
        10000300035145,
        10000300035239,
        10000300035246,
        10000300035382,
        10000300035247,
        10000300035547,
        10000300035892,
        10000300036061,
        10000300035895,
        10000300035897,
        10000300036110,
        10000300036114,
        10000300036115,
        10000300024440,
        10000300035703,
        10000300035705,
        10000300035712,
        10000300035983,
        10000300035960,
        10000300035961,
        10000300035385,
        10000300035788,
        10000300035966,
        10000300036029,
        10000300036030,
        10000300036032,
        10000300036049,
        10000300036060,
        10000300000017,
        10000300000018,
        10000300072994,
        10000300073105,
        10000300073826,
        10000300072115,
        10000300072216,
        10000300072365,
        10000300072369,
        10000300073003,
        10000300073009,
        10000300072929,
        10000300073210,
        10000300073212,
        10000300072839,
        10000300073082,
        10000300072222,
        10000300072223,
        10000300072227,
        10000300072372,
        10000300072752,
        10000300072536,
        10000300072674,
        10000300072679,
        10000300072973,
        10000300059754,
        10000300060020,
        10000300059988,
        10000300060329,
        10000300060497,
        10000300060411,
        10000300060502,
        10000300060508,
        10000300060566,
        10000300060801,
        10000300061419,
        10000300059755,
        10000300059835,
        10000300059992,
        10000300059839,
        10000300060317,
        10000300060318,
        10000300060319,
        10000300060843,
        10000300060160,
        10000300060412,
        10000300060414,
        10000300060623,
        10000300060496,
        10000300060662,
        10000300060720,
        10000300060723,
        10000300060654,
        10000300060655,
        10000300060666,
        10000300122213,
        10000300122218,
        10000300122219,
        10000300122236,
        10000300122246,
        10000300133758,
        10000300133917,
        10000300133920,
        10000300135354,
        10000300135355,
        10000300133750,
        10000300133755,
        10000300133756,
        10000300109007,
        10000300109010,
        10000300133879,
        10000300133885,
        10000300134508,
        10000300121595,
        10000300109615,
        10000300109848,
        10000300109850,
        10000300134240,
        10000300134241,
        10000300134242,
        10000300134251,
        10000300134645,
        10000300109822,
        10000300109855,
        10000300134438,
        10000300134440,
        10000300134443,
        10000300134444,
        10000300134452,
        10000300134632,
        10000300134637,
        10000300134711,
        10000300121892,
        10000300121418,
        10000300134630,
        10000300121420,
        10000300121421,
        10000300121566,
        10000300121570,
        10000300122141,
        10000300122152,
        10000300122153,
        10000300122169,
        10000300122003,
        10000300122085,
        10000300122407,
        10000300121989,
        10000300121990,
        10000300122005,
        10000300122295,
        10000300097714,
        10000300097717,
        10000300085365,
        10000300097629,
        10000300097635,
        10000300097025,
        10000300096794,
        10000300097053,
        10000300097055,
        10000300097320,
        10000300097323,
        10000300097326,
        10000300097571,
        10000300097577,
        10000300097338,
        10000300097589,
        10000300097566,
        10000300097570,
        10000300097586,
        10000300097824,
        10000300097826,
        10000300097194,
        10000300097197,
        10000300097496,
        10000300097497,
        10000300097753,
        10000300097756,
        10000300158432,
        10000300158395,
        10000300158397,
        10000300158398,
        10000300158908,
        10000300158902,
        10000300159102,
        10000300159109,
        10000300134592,
        10000300134580,
        10000300134582,
        10000300158835,
        10000300158248,
        10000300158250,
        10000300158251,
        10000300158256,
        10000300158257,
        10000300158562,
        10000300159026,
        10000300159032,
        10000300158723,
        10000300158736,
        10000300158971,
        10000300121561,
        10000300121562,
        10000300121565,
        10000300096871,
        10000300096872,
        10000300096882,
        10000300096883,
        10000300109245,
        10000300109545,
        10000300097416,
        10000300097660,
        10000300109770,
        10000300097657,
        10000300097659,
        10000300109765,
        10000300109980,
        10000300109089,
        10000300109091,
        10000300109094,
        10000300109095,
        10000300109097,
        10000300109098,
        10000300109100,
        10000300109689,
        10000300109690,
        10000300109697,
        10000300109908,
        10000300109920,
        10000300109922,
        10000300109929,
        10000300109620,
        10000300109912,
        10000300146450,
        10000300146452,
        10000300146453,
        10000300146448,
        10000300146697,
        10000300146701,
        10000300146763,
        10000300145965,
        10000300145966,
        10000300145884,
        10000300145970,
        10000300146548,
        10000300084569,
        10000300084821,
        10000300084669,
        10000300084670,
        10000300084672,
        10000300084970,
        10000300085270,
        10000300085276,
        10000300085279,
        10000300085291,
        10000300085517,
        10000300085501,
        10000300085506,
        10000300085189,
        10000300085190,
        10000300085191,
        10000300085418,
        10000300085436,
        10000300086164,
        10000300171260,
        10000300171261,
        10000300170631,
        10000300171475,
        10000300171477,
        10000300171481,
        10000300171486,
        10000300170622,
        10000300170626,
        10000300170632,
        10000300171172,
        10000300171376,
        10000300171398,
        10000300171409,
        10000300171410,
        10000300171595,
        10000300047692,
        10000300170769,
        10000300170770,
        10000300170772,
        10000300170802,
        10000300171075,
        10000300171077,
        10000300171079,
        10000300171082,
        10000300171092,
        10000300171093,
        10000300171331,
        10000300171333,
        10000300171334,
        10000300171335,
        10000300171336,
        10000300171338,
        10000300171325,
        10000300171544,
        10000300172152,
        10000300195878,
        10000300195793,
        10000300195845,
        10000300195847,
        10000300195957,
        10000300195958,
        10000300195967,
        10000300195635,
        10000300195083,
        10000300195084,
        10000300195086,
        10000300195087,
        10000300183000,
        10000300183022,
        10000300183024,
        10000300195727,
        10000300195730,
        10000300183313,
        10000300183314,
        10000300195784,
        10000300183187,
        10000300195547,
        10000300195939,
        10000300195943,
        10000300183496,
        10000300195552,
        10000300195944,
        10000300183686,
        10000300183688,
        10000300060315,
        10000300072214,
        10000300194874,
        10000300195259,
        10000300182860,
        10000300182868,
        10000300182869,
        10000300182870,
        10000300182853,
        10000300183609,
        10000300183631,
        10000300195074,
        10000300195076,
        10000300183604,
        10000300183819,
        10000300195538,
        10000300195539,
        10000300195540,
        10000300195221,
        10000300195223,
        10000300195225,
        10000300195229,
        10000300146098,
        10000300146101,
        10000300146104,
        10000300195639,
        10000300146097,
        10000300146632,
        10000300146633,
        10000300146634,
        10000300146851,
        10000300146636,
        10000300146829,
        10000300146830,
        10000300146840,
        10000300195866,
        10000300195867,
        10000300195869,
        10000300195222,
        10000300109099,
        10000300084972,
        10000300097624,
        10000300085503,
        10000300122212,
        10000300195998,
        10000300195786,
        10000300194983,
        10000300182862,
        10000300146282,
        10000300097417,
        10000300072969,
        10000300121569,
        10000300109847,
        10000300097021,
        10000300109816,
        10000300097592,
        10000300134435,
        10000300023360,
        10000300011137,
        10000300011396,
        10000300023003,
        10000300011007,
        10000300023015,
        10000300010061,
        10000300010324,
        10000300010325,
        10000300010078,
        10000300010278,
        10000300022273,
        10000300022551,
        10000300022556,
        10000300022557,
        10000300010492,
        10000300010399,
        10000300022728,
        10000300022729,
        10000300010600,
        10000300010607,
        10000300010608,
        10000300022496,
        10000300022642,
        10000300012256,
        10000300012257,
        10000300012258,
        10000300022366,
        10000300022210,
        10000300022777,
        10000300046827,
        10000300046834,
        10000300046856,
        10000300049073,
        10000300049078,
        10000300047349,
        10000300047224,
        10000300047226,
        10000300047196,
        10000300046863,
        10000300046764,
        10000300046796,
        10000300047158,
        10000300047381,
        10000300047383,
        10000300047386,
        10000300047388,
        10000300047227,
        10000300047259,
        10000300047448,
        10000300047449,
        10000300036839,
        10000300036840,
        10000300036841,
        10000300036842,
        10000300035035,
        10000300024436,
        10000300034579,
        10000300034360,
        10000300034500,
        10000300034505,
        10000300034531,
        10000300034532,
        10000300034559,
        10000300034793,
        10000300034794,
        10000300034836,
        10000300035080,
        10000300035082,
        10000300034596,
        10000300034402,
        10000300034629,
        10000300034873,
        10000300009951,
        10000300000014,
        10000300072109,
        10000300072111,
        10000300072112,
        10000300072056,
        10000300071275,
        10000300071524,
        10000300071598,
        10000300073819,
        10000300071547,
        10000300071549,
        10000300071842,
        10000300071884,
        10000300072059,
        10000300061414,
        10000300059496,
        10000300059500,
        10000300059742,
        10000300059692,
        10000300059027,
        10000300061415,
        10000300061416,
        10000300061417,
        10000300061418,
        10000300058945,
        10000300058947,
        10000300059178,
        10000300059401,
        10000300059269,
        10000300133653,
        10000300133155,
        10000300123001,
        10000300135349,
        10000300135350,
        10000300135351,
        10000300133744,
        10000300133374,
        10000300133605,
        10000300133606,
        10000300133608,
        10000300135348,
        10000300132912,
        10000300132913,
        10000300133332,
        10000300132958,
        10000300132959,
        10000300132960,
        10000300133413,
        10000300133114,
        10000300133415,
        10000300133416,
        10000300098407,
        10000300098408,
        10000300098409,
        10000300083861,
        10000300084327,
        10000300096276,
        10000300096065,
        10000300096550,
        10000300096201,
        10000300096226,
        10000300096520,
        10000300096725,
        10000300096786,
        10000300096789,
        10000300096443,
        10000300096727,
        10000300096730,
        10000300098410,
        10000300098402,
        10000300098403,
        10000300157870,
        10000300157871,
        10000300157872,
        10000300157930,
        10000300157896,
        10000300157897,
        10000300158132,
        10000300158134,
        10000300159823,
        10000300159824,
        10000300159827,
        10000300159820,
        10000300159821,
        10000300157539,
        10000300158006,
        10000300158007,
        10000300157955,
        10000300157960,
        10000300120520,
        10000300096118,
        10000300108438,
        10000300121050,
        10000300108460,
        10000300108439,
        10000300108686,
        10000300108713,
        10000300108950,
        10000300108542,
        10000300120653,
        10000300120698,
        10000300121065,
        10000300110629,
        10000300110630,
        10000300110631,
        10000300110632,
        10000300110633,
        10000300110634,
        10000300121299,
        10000300121300,
        10000300120701,
        10000300120395,
        10000300121017,
        10000300121018,
        10000300147501,
        10000300147503,
        10000300147504,
        10000300147505,
        10000300147506,
        10000300147507,
        10000300147508,
        10000300145275,
        10000300145371,
        10000300145621,
        10000300145625,
        10000300145626,
        10000300145628,
        10000300145881,
        10000300083821,
        10000300084566,
        10000300084568,
        10000300083990,
        10000300083991,
        10000300084251,
        10000300084282,
        10000300084550,
        10000300083717,
        10000300083951,
        10000300083952,
        10000300084519,
        10000300084415,
        10000300086161,
        10000300169932,
        10000300170463,
        10000300170465,
        10000300169895,
        10000300169905,
        10000300170352,
        10000300035141,
        10000300046807,
        10000300170236,
        10000300181891,
        10000300181978,
        10000300182024,
        10000300182719,
        10000300182526,
        10000300182138,
        10000300182142,
        10000300182195,
        10000300172146,
        10000300172147,
        10000300182759,
        10000300172150,
        10000300169768,
        10000300170309,
        10000300170312,
        10000300169995,
        10000300170271,
        10000300182510,
        10000300169969,
        10000300182767,
        10000300182768,
        10000300170539,
        10000300170543,
        10000300182171,
        10000300194764,
        10000300194979,
        10000300194980,
        10000300194691,
        10000300194188,
        10000300194265,
        10000300194266,
        10000300194267,
        10000300184380,
        10000300184381,
        10000300184382,
        10000300184383,
        10000300194303,
        10000300059608,
        10000300071548,
        10000300059159,
        10000300194916,
        10000300194978,
        10000300145117,
        10000300194726,
        10000300145329,
        10000300145551,
        10000300145586,
        10000300145818,
        10000300145777,
        10000300145817,
        10000300194660,
        10000300182194,
        10000300194425,
        10000300145315,
        10000300121066,
        10000300098406,
        10000300121020,
        10000300108477,
        10000300169896,
        10000300170237,
        10000300182520,
        10000300182755,
        10000300170538,
        10000300157873,
        10000300194372,
        10000300120789,
        10000300071399,
        10000300072110,
        10000300121155,
        10000300109005,
        10000300132783,
        10000300132908,
        10000300022868,
        10000300022558,
        10000300022296,
        10000300133102,
        10000300133944,
        10000300084854,
        10000300183048,
        10000300097885,
        10000300183298,
    ]
}

