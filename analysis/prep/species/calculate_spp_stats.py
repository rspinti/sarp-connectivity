"""Extract out species information

1. Read in USFWS ECOS listing of T & E species
2. Add in species names based on taxonomic synonyms
3. Read in aggregated species / HUC12 info
4. Fix species name issues for select species
5. Assign ECOS T & E in addition to those already present from states
6. Extract out only T & E occurrences, and aggregate to number of T & E species per HUC12

Beware: Some species have incorrect spellings!  Some have many variants of common name!

"""

from pathlib import Path
from time import time
import pandas as pd
from nhdnet.io import deserialize_df, serialize_df

start = time()
data_dir = Path("data")
src_dir = data_dir / "species/source"
out_dir = data_dir / "species/derived"
qa_dir = data_dir / "species/qa"

############### Extract USFWS official listing information ######################
print("Reading T&E species list")
listed_df = pd.read_csv(
    src_dir / "ECOS_listed_aquatic_species_2018.csv",
    usecols=["ScientificName", "Status"],
).rename(columns={"ScientificName": "SNAME"})

# Fix extra spaces in species name
listed_df.SNAME = listed_df.SNAME.str.replace("  ", " ")

# Assign consistent codes
listed_df.loc[listed_df.Status == "\xa0Endangered", "official_status"] = "E"
listed_df.loc[listed_df.Status == "\xa0Threatened", "official_status"] = "T"
listed_df = listed_df.loc[
    ~listed_df.official_status.isnull(), ["SNAME", "official_status"]
]

# Manually add in species that have had a taxanomic change (that we tripped over, NOT comprehensive)
# Ignoring experimental population exemption here
# Some are listed at the subspecies level by USFWS but the taxonomy at that level is not yet accepted

missing_spps = pd.DataFrame(
    [
        # Endangered species
        ["Arcidens wheeleri", "E"],
        ["Arkansia wheeleri", "E"],
        ["Epioblasma curtisii", "E"],
        ["Epioblasma torulosa", "E"],
        ["Hamiota subangulata", "E"],
        ["Margaritifera monodonta", "E"],
        ["Marstonia pachyta", "E"],
        # Threatened species
        ["Hamiota altilis", "T"],
        ["Hamiota perovalis", "T"],
        ["Quadrula cylindrica", "T"],
        ["Troglichthys rosae", "T"],
        # listed at subspecies level at least at threatened level
        ["Theliderma cylindrica", "T"],
    ],
    columns=["SNAME", "official_status"],
)

listed_df = listed_df.append(missing_spps, ignore_index=True)


# Species with a T & E listing from states that are not updated
# because they are not listed by ECOS or NatureServe Explorer as being T & E:
# Crystallaria asprella, Etheostoma olmstedi, Fundulus jenkinsi, Notropis melanostomus, Pteronotropis welaka

# Others are under review and not listed yet according to USFWS:
# Pleurobema rubellum


endangered_df = listed_df.loc[listed_df.official_status == "E"].SNAME.unique()
threatened_df = listed_df.loc[listed_df.official_status == "T"].SNAME.unique()


############## Extract species points ######################
# Run aggregate_spp_occurrences.py first!
print("Reading Species HUC12 data")
df = deserialize_df(out_dir / "spp_HUC12_occurrence.feather")
# df = pd.read_csv(out_dir / "species_HUC12.csv", dtype={"HUC12": str}).fillna(
#     {"status": ""}
# )

print("Cleaning and aggregating data")

# Fix Atlantic sturgeon (Acipenser ox*); it has multiple variants of the wrong spelling
# There are other species that have wrong spelling, but they aren't T&E, so we aren't fixing here
index = df.SNAME.str.startswith("Acipenser oxyrhynchus")
df.loc[index, "SNAME"] = df.loc[index].SNAME.str.replace("oxyrhynchus", "oxyrinchus")


# Apply T & E status from official listing info
# Always apply E status
# Only apply T status if status is not E
df.loc[df.SNAME.isin(threatened_df) & (df.status != "E"), "status"] = "T"
df.loc[df.SNAME.isin(endangered_df), "status"] = "E"


### Temporary: join official T&E status in and cross-check
# To simplify the join, apply the highest listing to all occurrences, this is the most conservative
# Flatten to single record for each species
# listed_df = (
#     listed_df.groupby(["SNAME", "official_status"])
#     .size()
#     .reset_index()
#     .drop(columns=[0])
#     .set_index(["SNAME"])
# )
# # Write out file for verification
# df.join(listed_df, on="SNAME").fillna({"official_status": ""}).groupby(
#     ["SNAME", "status", "official_status"]
# ).size().reset_index().to_csv("data/src/tmp/spp_huc12_status.csv", index=False)


# At this point, assume that all T&E status is current, and aggregate up to count of unique T & E species per HUC12
# Then count unique species by HUC12
count_df = (
    df.loc[df.status.isin(["T", "E"])]
    .groupby(["HUC12", "SNAME"])
    .first()
    .reset_index()
    .groupby(["HUC12"])
    .size()
    .reset_index()
    .rename(columns={0: "NumTEspp"})
)

# Save counts by HUC12 to join to barriers
serialize_df(count_df, out_dir / "spp_HUC12.feather")

## generate statistics of species and status
species_stats_df = (
    df.loc[df.status.isin(["T", "E"])]
    # aggregate to unique species per HUC
    .groupby(["HUC12", "status", "SNAME"])
    .first()
    .reset_index()
    # aggregate count of HUCs per species
    .groupby(["status", "SNAME"])
    .size()
    .reset_index()
    .rename(columns={0: "CountHUC12"})
)

species_stats_df.to_csv(qa_dir / "species_stats.csv")

status_stats_df = (
    species_stats_df.groupby(["status"])
    .size()
    .reset_index()
    .rename(columns={0: "CountSpp"})
)

status_stats_df.to_csv(qa_dir / "status_stats.csv")

print("All done in {:.2}s".format(time() - start))