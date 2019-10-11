from collections import OrderedDict

# Summary unit fields
UNIT_FIELDS = ["HUC6", "HUC8", "HUC12", "State", "County", "ECO3", "ECO4"]

# metric fields that are only valid for barriers with networks
METRIC_FIELDS = [
    "StreamOrder",
    "Landcover",
    "Sinuosity",
    "SizeClasses",
    "UpstreamMiles",
    "DownstreamMiles",
    "GainMiles",
    "TotalNetworkMiles",
]

TIER_FIELDS = [
    "SE_NC_tier",
    "SE_WC_tier",
    "SE_NCWC_tier",
    "State_NC_tier",
    "State_WC_tier",
    "State_NCWC_tier",
]

# Only present when custom prioritization is performed
CUSTOM_TIER_FIELDS = ["NC_tier", "WC_tier", "NCWC_tier"]


### Fields ONLY used for filtering
# other fields below in *_CORE may be used for filtering too
FILTER_FIELDS = [
    "GainMilesClass",
    "SinuosityClass",
    # "LandcoverClass", # not currently used
    "TESppClass",
    "StreamOrderClass",
]

DAM_FILTER_FIELDS = FILTER_FIELDS + [
    "HeightClass",
    # TODO: should these be classes?
    # "Condition",
    # "Construction",
    # "Purpose",
    # "Recon",
    # "Feasibility",
]

SB_FILTER_FIELDS = FILTER_FIELDS = [
    "ConditionClass",
    "SeverityClass",
    "CrossingTypeClass",
    "RoadTypeClass",
]


### Fields used for export


DAM_CORE_FIELDS = [
    "lat",
    "lon",
    "SARPUniqueID",
    "Name",
    "NIDID",
    "Source",
    "Year",
    "River",
    "Height",
    # Recon is intentionally omitted from download below
    "Recon",
    "Feasibility",
    "Construction",
    "Purpose",
    "Condition",
    "Basin",
    "TESpp",
]

DAM_API_FIELDS = (
    DAM_CORE_FIELDS
    + UNIT_FIELDS
    + ["HasNetwork"]
    + METRIC_FIELDS
    + TIER_FIELDS
    + DAM_FILTER_FIELDS
    + ["COUNTYFIPS"]
)

DAM_EXPORT_FIELDS = (
    DAM_CORE_FIELDS
    + UNIT_FIELDS
    + ["HasNetwork"]
    + METRIC_FIELDS
    + TIER_FIELDS
    + CUSTOM_TIER_FIELDS
)
# remove recon
DAM_EXPORT_FIELDS.remove("Recon")


SB_CORE_FIELDS = [
    "lat",
    "lon",
    "SARPID",
    "Name",
    "CrossingCode",
    "LocalID",
    "Source",
    "Stream",
    "Road",
    "RoadType",
    "CrossingType",
    "Condition",
    "PotentialProject",
    "Basin",
    "TESpp",
]

SB_API_FIELDS = (
    SB_CORE_FIELDS
    + UNIT_FIELDS
    + ["HasNetwork"]
    + METRIC_FIELDS
    + TIER_FIELDS
    + SB_FILTER_FIELDS
    + ["COUNTYFIPS"]
)

SB_EXPORT_FIELDS = (
    SB_CORE_FIELDS
    + ["SeverityClass"]
    + UNIT_FIELDS
    + ["HasNetwork"]
    + METRIC_FIELDS
    + TIER_FIELDS
    + CUSTOM_TIER_FIELDS
)


#     # Original dams fields
#     # ID and source info
#     "SARPID",
#     "NIDID",
#     "Source",
#     # Basic info
#     "Name",
#     "County",
#     "State",
#     # Species info
#     "RareSpp",
#     # River info
#     "River",
#     "StreamOrder",
#     "NHDplusVersion",
#     "HasNetwork",
#     # Location info
#     "ProtectedLand",  # TODO: OwnerType
#     "HUC6",
#     "HUC8",
#     "HUC12",
#     "ECO3",
#     "ECO4",
#     # Dam info
#     "Height",
#     "Year",
#     "Construction",
#     "Purpose",
#     "Condition",
#     # "Recon",  # intentionally omitted
#     "Feasibility",
#     # Metrics
#     "GainMiles",
#     "UpstreamMiles",
#     "DownstreamMiles",
#     "TotalNetworkMiles",
#     "Landcover",
#     "Sinuosity",
#     "SizeClasses",
#     # Tiers
#     "NC_tier",
#     "WC_tier",
#     "NCWC_tier",
#     "SE_NC_tier",
#     "SE_WC_tier",
#     "SE_NCWC_tier",
#     "State_NC_tier",
#     "State_WC_tier",
#     "State_NCWC_tier",


# BARRIER_EXPORT_FIELDS = [
#     "lat",
#     "lon",
#     # ID and source info
#     "SARPID",
#     "CrossingCode",
#     "LocalID",
#     "Source",
#     # Basic info
#     "Name",
#     "County",
#     "State",
#     "Basin",
#     # Species info
#     "RareSpp",
#     # River info
#     "Stream",
#     "HasNetwork",
#     # Road info
#     "Road",
#     "RoadType",
#     # Barrier info
#     "CrossingType",
#     "Condition",
#     "PotentialProject",
#     "SeverityClass",
#     # Location info
#     "ProtectedLand",
#     "HUC6",
#     "HUC8",
#     "HUC12",
#     "ECO3",
#     "ECO4",
#     # Metrics
#     "GainMiles",
#     "UpstreamMiles",
#     "DownstreamMiles",
#     "TotalNetworkMiles",
#     "Landcover",
#     "Sinuosity",
#     "SizeClasses",
#     # Tiers
#     "NC_tier",
#     "WC_tier",
#     "NCWC_tier",
#     "SE_NC_tier",
#     "SE_WC_tier",
#     "SE_NCWC_tier",
#     "State_NC_tier",
#     "State_WC_tier",
#     "State_NCWC_tier",
# ]


### Domains for coded values in exported data


# typos fixed and trailing periods removed
RECON_DOMAIN = {
    0: "Not yet evaluated",  # added
    1: "Good candidate for removal. Move forward with landowner contact",  # expanded acronym
    2: "Dam needs follow-up with landowner",
    3: "Removal is unlikely.  Social conditions unfavorable",
    4: "Removal is extremely infeasible.  Large reservoirs, etc.",
    5: "Dam may be removed or error",
    6: "Infeasible in short term via landowner contact",
    7: "Dam was deliberately removed",
    8: "Dam location is incorrect and needs to be moved",  # fixed phrasing
    9: "Dam is breached and no impoundment visible",
    10: "Dam was once considered, need to revisit",
    11: "Removal planned",
    13: "Unsure, need second opinion",
    14: "Take immediate action, abandoned-looking dam in poor condition",
    15: "No conservation benefit",
    16: "Invasive species barrier",
    17: "Risky for mussels",
    18: "Dam failed",
    19: "Proposed dam",
    20: "Farm pond - no conservation benefit",
    21: "Potential thermal issues",
}

# Created here to capture values below
FEASIBILITY_DOMAIN = {
    # -1: "N/A",  # These are filtered out in preprocessing - not barriers
    0: "Not assessed",
    1: "Not feasible",
    2: "Likely infeasible",
    3: "Possibly feasible",
    4: "Likely feasible",
    5: "No conservation benefit",
    # not shown to user
    6: "Unknown",
    7: "Error",
    8: "Dam removed for conservation benefit",
}


PURPOSE_DOMAIN = {
    0: "Unknown",  # added
    1: "Agriculture",
    2: "Flood Control",
    3: "Water Supply",
    4: "Navigation",
    5: "Recreation",
    6: "Hydropower",
    7: "Aquatic Resource Management",
    8: "Other",
    9: "Tailings",
    10: "Not Rated",
    13: "Mine or Industrial Waste",
    11: "Grade Stabilization",
}

CONSTRUCTION_DOMAIN = {
    0: "Unknown",  # added
    1: "Cement",
    2: "Concrete/Roller-compacted Concrete",
    3: "Masonry/Stone",
    4: "Steel",
    5: "Timber",
    6: "Earthfill (Gravel, Sand, Silt, Clay)",
    7: "Rockfill (Rock, Composite)",
    8: "Corrugated Metal",
    9: "Polyvinyl chloride (PVC)",
    10: "Cast Iron",
    11: "Other",
}

DAM_CONDITION_DOMAIN = {
    0: "Not Rated",
    1: "Satisfactory",
    2: "Fair",
    3: "Poor",
    4: "Unsatisfactory",
}


# Created here
# Height in feet
HEIGHT_DOMAIN = {
    0: "Unknown",
    1: "< 5",
    2: "5 - 10",
    3: "10 - 25",
    4: "25 - 50",
    5: "50 - 100",
    6: ">= 100",
}

GAINMILES_DOMAIN = {
    # -1: "no network", # filter this out
    0: "< 1",
    1: "1 - 5",
    2: "5 - 10",
    3: "10 - 25",
    4: "25 - 100",
    5: ">= 100",
}

RARESPP_DOMAIN = {0: "0", 1: "1", 2: "1 - 4", 3: "5 - 9", 4: ">= 10"}

LANDCOVER_DOMAIN = {
    # -1: "no network", # filter this out
    0: "< 50",
    1: "50 - 75",
    2: "75 - 90",
    3: ">= 90",
}

SINUOSITY_DOMAIN = {
    # -1: "no network", # filter this out
    0: "low",  # <1.2
    1: "moderate",  # 1.2 - 1.5
    2: "high",  # > 1.5
}

STREAM_ORDER_DOMAIN = {
    # -1: "no network", # filter this out
    1: "1",
    2: "2",
    3: "3",
    4: "4",
    5: "5",
    6: ">= 6",
}

BARRIER_SEVERITY_DOMAIN = {
    0: "Unknown",
    1: "Not a barrier",  # includes minor barriers
    2: "Moderate barrier",
    3: "Major barrier",
}

CROSSING_TYPE_DOMAIN = {
    0: "Unknown",
    1: "Not a barrier",
    2: "Bridge",
    3: "Culvert",
    4: "Ford",
    5: "Dam",
    6: "Buried stream",
}


ROAD_TYPE_DOMAIN = {0: "Unknown", 1: "Unpaved", 2: "Paved", 3: "Railroad"}

BARRIER_CONDITION_DOMAIN = {0: "Unknown", 1: "Failing", 2: "Poor", 3: "OK", 4: "New"}

OWNERTYPE_DOMAIN = {
    # 0: "Unknown",
    1: "US Fish and Wildlife Service land",
    2: "USDA Forest Service land",
    3: "Federal land",
    4: "State land",
    5: "Joint Ownership or Regional land",
    6: "Native American land",
    7: "Private easement",
    8: "Other private conservation land",
}

BOOLEAN_DOMAIN = {False: "no", True: "yes"}
