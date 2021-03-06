from pathlib import Path
from time import time

from geofeather import from_geofeather, to_geofeather

from nhdnet.io import deserialize_df, to_shp, serialize_df
from analysis.constants import REGION_GROUPS

# ID ranges for each type
WATERFALLS_ID = 1e6
DAMS_ID = 2 * 1e6
SB_ID = 3 * 1e6


barriers_dir = Path("data/barriers/snapped")


def read_barriers(region, mode):
    """Read files created by prep_dams.py, prep_waterfalls.py, prep_small_barriers.py
    Merge together and assign uniqueID for internal use in network analysis

    NOTE: barriers on loops are dropped

    Parameters
    ----------
    region : str
        region group identifier, e.g., "02"
    mode : str
        One of "natural", "dams", "small_barriers"

    Returns
    -------
    GeoDataFrame
        Merged barriers file
    """

    start = time()

    print("Reading waterfalls")
    wf = from_geofeather(barriers_dir / "waterfalls.feather")
    wf = wf.loc[wf.HUC2.isin(REGION_GROUPS[region])].copy()
    print("Selected {:,} waterfalls".format(len(wf)))

    wf["barrierID"] = WATERFALLS_ID + wf.id
    wf["kind"] = "waterfall"

    barriers = wf

    if mode != "natural":
        print("Reading dams")
        dams = from_geofeather(barriers_dir / "dams.feather")
        dams = dams.loc[dams.HUC2.isin(REGION_GROUPS[region])].copy()
        print("Selected {:,} dams".format(len(dams)))

        dams["barrierID"] = DAMS_ID + dams.id
        dams["kind"] = "dam"

        if len(dams):
            barriers = barriers.append(dams, ignore_index=True, sort=False)

    if mode == "small_barriers":
        print("Reading small barriers")
        sb = from_geofeather(barriers_dir / "small_barriers.feather")
        sb = sb.loc[sb.HUC2.isin(REGION_GROUPS[region])].copy()
        print("Selected {:,} small barriers".format(len(sb)))

        sb["barrierID"] = SB_ID + sb.id
        sb["kind"] = "small_barrier"

        if len(sb):
            barriers = barriers.append(sb, ignore_index=True, sort=False)

    # Update dtypes
    # TODO: not neeed after rerun of prep_*.py scripts
    barriers.id = barriers.id.astype("uint32")
    barriers.lineID = barriers.lineID.astype("uint32")
    barriers.NHDPlusID = barriers.NHDPlusID.astype("uint64")

    barriers.barrierID = barriers.barrierID.astype("uint64")

    ix = barriers.loop == True
    print("Found {:,} barriers on loops, dropping".format(ix.sum()))
    barriers = barriers.loc[~ix].copy()

    print("Extracted {:,} barriers in {:.2f}s".format(len(barriers), time() - start))

    return barriers[
        ["geometry", "id", "lineID", "NHDPlusID", "barrierID", "kind"]
    ].set_index("barrierID", drop=False)


def save_barriers(out_dir, barriers):
    """Save consolidated barriers to disk for QA.

    Parameters
    ----------
    out_dir : str
    barriers : GeoDataFrame
    """

    print("Serializing {:,} barriers...".format(len(barriers)))
    start = time()

    tmp = barriers.reset_index(drop=True)
    to_geofeather(tmp, out_dir / "barriers.feather")
    to_shp(tmp, out_dir / "barriers.shp")

    print("Done serializing barriers in {:.2f}s".format(time() - start))
