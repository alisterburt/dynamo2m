from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal
import dynamotable

from dynamo2m import warp2dynamo

data_dir = Path(__file__).parent / '..' / 'test_data' / 'warp2dynamo'
star_file = data_dir / 'example.star'


def test_warp2dynamo(tmp_path):
    output_file = str(tmp_path / 'warp2dynamo.tbl')
    warp2dynamo(warp_star_file=star_file, output_dynamo_table_file=output_file, extracted_box_size=128)
    df = dynamotable.read(output_file)
    assert df.shape == (1399, 42)

    euler_sample = {
        'tdrot': {1: -175.26000000000005,
                  2: 159.70999999999995,
                  3: -172.37,
                  4: -159.26999999999995},
        'tilt': {1: 15.24499999999999,
                 2: 19.961000000000013,
                 3: 12.364999999999993,
                 4: 23.17700000000001},
        'narot': {1: 46.303999999999995,
                  2: 134.29999999999998,
                  3: 161.13,
                  4: 32.63100000000001}}

    xyz_sample = {
        'x': {1: 1534.5,
              2: 1558.5,
              3: 1534.5,
              4: 1522.5},
        'y': {1: 1105.5,
              2: 1105.5,
              3: 1105.5,
              4: 1041.285},
        'z': {1: 972.344,
              2: 972.285,
              3: 975.284,
              4: 958.5}
    }

    assert_frame_equal(df[['tdrot', 'tilt', 'narot']][1:5], pd.DataFrame.from_dict(euler_sample))
    assert_frame_equal(df[['x', 'y', 'z']][1:5], pd.DataFrame.from_dict(xyz_sample))
