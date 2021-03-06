"""Create networks by first cutting flowlines at barriers, then traversing upstream to
determine upstream networks to upstream-most endpoints or upstream barriers.

After networks are created, summary statistics are calculated.

The final outputs of this process are a set of network-related files for each region
and network type (dams or small barriers):

data/networks/<region>/<network type>/*
"""

from pathlib import Path
import os
from time import time
from itertools import product

import geopandas as gp
import pandas as pd
import numpy as np
from shapely.geometry import MultiLineString
from geofeather import from_geofeather, to_geofeather

from nhdnet.nhd.cut import cut_flowlines
from nhdnet.nhd.network import generate_networks
from nhdnet.io import deserialize_df, to_shp, serialize_df

from analysis.constants import REGION_GROUPS, NETWORK_TYPES, CONNECTED_REGIONS

from analysis.network.lib.stats import calculate_network_stats
from analysis.network.lib.barriers import read_barriers, save_barriers
from analysis.network.lib.flowlines import cut_flowlines_at_barriers, save_cut_flowlines
from analysis.network.lib.networks import create_networks

data_dir = Path("data")

start = time()
# FIXME
for region, network_type in product(REGION_GROUPS.keys(), NETWORK_TYPES[1:2]):
    print(
        "\n\n###### Processing region {0}: {1} networks #####".format(
            region, network_type
        )
    )

    out_dir = data_dir / "networks" / region / network_type

    if region in CONNECTED_REGIONS:
        out_dir = out_dir / "raw"

    if not os.path.exists(out_dir):
        os.makedirs(out_dir)

    region_start = time()

    ##################### Read Barrier data #################
    print("------------------- Preparing Barriers ----------")

    barriers = read_barriers(region, network_type)
    save_barriers(out_dir, barriers)

    ##################### Cut flowlines at barriers #################
    print("------------------- Cutting Flowlines -----------")
    flowlines, joins, barrier_joins = cut_flowlines_at_barriers(region, barriers)

    barrier_joins = barrier_joins.join(barriers.kind)

    save_cut_flowlines(out_dir, flowlines, joins, barrier_joins)

    ##################### Create networks #################
    # IMPORTANT: the following analysis allows for multiple upstream networks from an origin or barrier
    # this happens when the barrier is perfectly snapped to the junction of >= 2 upstream networks.
    # When this is encountered, these networks are merged together and assigned the ID of the first segment
    # of the first upstream network.

    print("------------------- Creating networks -----------")
    network_start = time()

    network_df = create_networks(flowlines, joins, barrier_joins)

    # For any barriers that had multiple upstreams, those were coalesced to a single network above
    # So drop any dangling upstream references (those that are not in networks and non-zero)
    # NOTE: these are not persisted because we want the original barrier_joins to reflect multiple upstreams
    barrier_joins = barrier_joins.loc[
        barrier_joins.upstream_id.isin(network_df.index)
        | (barrier_joins.upstream_id == 0)
    ].copy()

    print(
        "{0:,} networks created in {1:.2f}s".format(
            len(network_df.index.unique()), time() - network_start
        )
    )

    print("Serializing network segments")
    serialize_df(
        network_df.drop(columns=["geometry"]).reset_index(),
        out_dir / "network_segments.feather",
    )

    ##################### Network stats #################
    print("------------------- Calculating network stats -----------")

    stats_start = time()

    network_stats = calculate_network_stats(network_df, barrier_joins)
    # WARNING: because not all flowlines have associated catchments, they are missing
    # natfldpln

    print("done calculating network stats in {0:.2f}".format(time() - stats_start))

    serialize_df(network_stats.reset_index(), out_dir / "network_stats.feather")

    #### Calculate up and downstream network attributes for barriers

    print("calculating upstream and downstream networks for barriers")

    upstream_networks = (
        barrier_joins[["upstream_id"]]
        .join(network_stats, on="upstream_id")
        .rename(
            columns={
                "upstream_id": "upNetID",
                "miles": "TotalUpstreamMiles",
                "free_miles": "FreeUpstreamMiles",
            }
        )
    )

    downstream_networks = (
        barrier_joins[["downstream_id"]]
        .join(
            network_df.reset_index().set_index("lineID").networkID, on="downstream_id"
        )
        .join(
            network_stats[["free_miles", "miles"]].rename(
                columns={
                    "free_miles": "FreeDownstreamMiles",
                    "miles": "TotalDownstreamMiles",
                }
            ),
            on="networkID",
        )
        .rename(columns={"networkID": "downNetID"})
        .drop(columns=["downstream_id"])
    )

    # Note: the join creates duplicates if there are multiple upstream or downstream
    # networks for a given barrier, so we drop these duplicates after the join just to be sure.
    barrier_networks = (
        upstream_networks.join(downstream_networks)
        .join(barriers[["id", "kind"]])
        .drop(columns=["barrier", "up_ndams", "up_nwfs", "up_sbs"], errors="ignore")
        .fillna(0)
        .drop_duplicates()
    )

    # Fix data types after all the joins
    for col in ["upNetID", "downNetID", "segments"]:
        barrier_networks[col] = barrier_networks[col].astype("uint32")

    for col in [
        "TotalUpstreamMiles",
        "FreeUpstreamMiles",
        "TotalDownstreamMiles",
        "FreeDownstreamMiles",
        "sinuosity",
        "natfldpln",
    ]:
        barrier_networks[col] = barrier_networks[col].astype("float32")

    barrier_networks.sizeclasses = barrier_networks.sizeclasses.astype("uint8")

    serialize_df(barrier_networks.reset_index(), out_dir / "barriers_network.feather")

    # TODO: if downstream network extends off this HUC, it will be null in the above and AbsoluteGainMin will be wrong

    ##################### Dissolve networks on networkID ########################
    print("Dissolving networks")
    dissolve_start = time()

    dissolved_lines = (
        network_df[["geometry"]]
        .groupby(level=0)
        .geometry.apply(list)
        .apply(MultiLineString)
    )

    networks = (
        gp.GeoDataFrame(network_stats.join(dissolved_lines), crs=flowlines.crs)
        .reset_index()
        .sort_values(by="networkID")
    )

    print("Network dissolve done in {0:.2f}".format(time() - dissolve_start))

    print("Serializing network")
    to_geofeather(networks.reset_index(drop=True), out_dir / "network.feather")

    if not region in CONNECTED_REGIONS:
        print("Writing dissolved network shapefile")
        to_shp(networks, out_dir / "network.shp")

    print("Region done in {:.2f}s".format(time() - region_start))

print("All done in {:.2f}s".format(time() - start))

