from pathlib import Path

import click
import pandas as pd
import starfile


# @click.command()
# @click.option('--star_file', '-s', prompt='Input STAR file')
def cli(star_file):
    """Downgrade RELION 3.1 STAR file to RELION 3.0 format for Warp
    """
    star = starfile.read(star_file)

    # Get pixel size (ang/px)
    pixel_size = float(star['optics']['rlnImagePixelSize'])

    # Get necessary data from 3.1 style star file (RELION 3.0 style expected by warp for particle extraction)
    data = star['particles']
    xyz_headings = [f'rlnCoordinate{axis}' for axis in 'XYZ']
    shift_headings = [f'rlnOrigin{axis}Angst' for axis in 'XYZ']
    euler_headings = [f'rlnAngle{euler}' for euler in ('Rot', 'Tilt', 'Psi')]

    xyz = data[xyz_headings]
    shifts_ang = data[shift_headings]
    data_out = {}
    eulers = data[euler_headings]
    data_out['rlnMicrographName'] = data['rlnMicrographName']

    # Get shifts in pixels (RELION 3.0 style)
    shifts_px = shifts_ang / pixel_size

    # update XYZ positions
    xyz_shifted = xyz.to_numpy() + shifts_px

    # Write star file
    df = pd.DataFrame.from_dict(data_out, orient='columns')
    for idx in range(3):
        df[xyz_headings[idx]] = xyz_shifted.to_numpy()[:, idx]

    for idx in range(3):
        df[euler_headings[idx]] = eulers.to_numpy()[:, idx]

    star_file = Path(star_file)
    stem = star_file.stem
    output_filename = star_file.parent / (str(stem) + '_rln3.0.star')
    starfile.write(df, output_filename, overwrite=True)

    click.echo(f'Done! Wrote RELION 3.0 format STAR file to {output_filename}')
    return


if __name__ == '__main__':
    star = 'test_data/relion_star_downgrade/relion3.1.star'
    cli(star)
