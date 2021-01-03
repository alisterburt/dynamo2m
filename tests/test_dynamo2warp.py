from pathlib import Path

import pandas as pd
from pandas.testing import assert_frame_equal

import starfile

from dynamo2m import dynamo2warp

data_dir = Path(__file__).parent / '..' / 'test_data' / 'dynamo2warp'
table_file = data_dir / 'example.tbl'
doc_file = data_dir / 'example.doc'


def test_dynamo2warp(tmp_path):
    output_file = tmp_path / 'dynamo2warp.star'
    dynamo2warp(input_table_file=table_file, table_map_file=doc_file, output_star_file=output_file)

    df = starfile.read(output_file)
    assert df.shape == (4934, 7)
    xyz_sample = {
        'rlnCoordinateX': {1: 536.6156, 2: 524.35252, 3: 523.738, 4: 528.2961},
        'rlnCoordinateY': {1: 370.5493, 2: 362.3147, 3: 376.7746, 4: 369.7624},
        'rlnCoordinateZ': {1: 319.70611, 2: 321.8937, 3: 324.2958, 4: 323.2949}
    }

    euler_sample ={
        'rlnAngleRot': {1: -155.676, 2: 159.44, 3: 144.73, 4: 114.09},
        'rlnAngleTilt': {1: 8.4212, 2: 7.7828, 3: 5.4919, 4: 7.7122},
        'rlnAnglePsi': {1: -157.3, 2: -108.68, 3: -93.8, 4: -124.29}
    }

    assert_frame_equal(df[['rlnCoordinateX', 'rlnCoordinateY', 'rlnCoordinateZ']][1:5],
                       pd.DataFrame.from_dict(xyz_sample))

    assert_frame_equal(df[['rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']][1:5],
                       pd.DataFrame.from_dict(euler_sample))
