from pathlib import Path

from nhdnet.io import deserialize_gdf, deserialize_sindex
from nhdnet.geometry.lines import snap_to_line


nhd_dir = Path("data/nhd/flowlines")


def snap_by_region(df, regions, default_tolerance=None):
    """Snap barriers based on nearest flowline within tolerance.

    If available, a 'tolerance' column is used to define the tolerance to snap by;
    otherwise, default_tolerance must be provided.

    Parameters
    ----------
    df : GeoDataFrame
        Input barriers to be snapped
    regions : dict
        Dictionary of region IDs to list of units in region
    default_tolerance : float, optional (default: None)
        distance within which to allow snapping to flowlines

    Returns
    -------
    GeoDataFrame
        snapped barriers (unsnapped are dropped) with additional fields from snapping:
        lineID, NHDPlusID, snap_dist, nearby
    """

    if "tolerance" not in df.columns and default_tolerance is None:
        raise ValueError(
            "Either 'tolerance' column or default_tolerance must be defined"
        )

    merged = None

    for region in regions:

        print("\n----- {} ------\n".format(region))
        region_dir = nhd_dir / region

        # Extract out waterfalls in this HUC
        in_region = df.loc[df.HUC2.isin(regions[region])]
        print("Selected {:,} barriers in region".format(len(in_region)))

        if len(in_region) == 0:
            continue

        print("Reading flowlines")
        flowlines = (
            deserialize_gdf(
                region_dir / "flowline.feather",
                columns=["geometry", "lineID", "NHDPlusID", "streamorder", "sizeclass"],
            )
            .rename(columns={"streamorder": "StreamOrder", "sizeclass": "SizeClass"})
            .set_index("lineID", drop=False)
        )
        print("Read {:,} flowlines".format(len(flowlines)))

        print("Reading spatial index on flowlines")
        sindex = deserialize_sindex(region_dir / "flowline.sidx")

        print("Snapping to flowlines")
        if "tolerance" in df.columns:
            # Snap for each tolerance level
            snapped = None
            for tolerance in df.tolerance.unique():

                at_tolerance = in_region.loc[in_region.tolerance == tolerance]

                if not len(at_tolerance):
                    continue

                print("snapping {} barriers by {}".format(len(at_tolerance), tolerance))

                temp = snap_to_line(
                    at_tolerance, flowlines, tolerance=tolerance, sindex=sindex
                )
                print("snapped {} barriers".format(len(temp)))

                if snapped is None:
                    snapped = temp

                else:
                    snapped = snapped.append(temp, ignore_index=True, sort=False)

        else:
            snapped = snap_to_line(
                in_region, flowlines, tolerance=default_tolerance, sindex=sindex
            )

        print("{:,} barriers were successfully snapped".format(len(snapped)))

        if merged is None:
            merged = snapped
        else:
            merged = merged.append(snapped, sort=False, ignore_index=True)

    return merged


def update_from_snapped(df, snapped):
    """Update snapped coordinates into dataset.

    Parameters
    ----------
    df : GeoDataFrame
        Master dataset to update with snapped coordinates
    snapped : GeoDataFrame
        Snapped dataset with coordinates to apply

    Returns
    -------
    GeoDataFrame
    """

    df["snapped"] = False
    df = df.join(
        snapped.set_index("id")[
            ["geometry", "snap_dist", "lineID", "NHDPlusID", "StreamOrder", "SizeClass"]
        ],
        on="id",
        rsuffix="_snapped",
    )
    idx = df.loc[df.lineID.notnull()].index
    df.loc[idx, "geometry"] = df.loc[idx].geometry_snapped
    df.loc[idx, "snapped"] = True
    df = df.drop(columns=["geometry_snapped"])

    return df
