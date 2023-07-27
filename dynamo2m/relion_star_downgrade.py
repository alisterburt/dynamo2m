from pathlib import Path

import click
import pandas as pd
import starfile


def relion_star_downgrade(star_file, output_star_file):
    """Downgrade RELION 3.1 STAR file to RELION 3.0 format for Warp
    """
    star = starfile.read(star_file)

    # Merge optics info into particles dataframe
    data = star['particles'].merge(star['optics'])

    # Get necessary data from 3.1 style star file
    # (RELION 3.0 style expected by warp for particle extraction)
    xyz_headings = [f'rlnCoordinate{axis}' for axis in 'XYZ']
    shift_headings = [f'rlnOrigin{axis}Angst' for axis in 'XYZ']
    euler_headings = [f'rlnAngle{euler}' for euler in ('Rot', 'Tilt', 'Psi')]

    xyz = data[xyz_headings].to_numpy()
    shifts_ang = data[shift_headings].to_numpy()
    pixel_size = data['rlnImagePixelSize'].to_numpy().reshape((-1, 1))
    eulers = data[euler_headings].to_numpy()
    data_out = {}
    data_out['rlnMicrographName'] = data['rlnMicrographName']

    # Get shifts in pixels (RELION 3.0 style)
    shifts_px = shifts_ang / pixel_size

    # update XYZ positions
    xyz_shifted = xyz - shifts_px

    # Create output DataFrame
    df = pd.DataFrame.from_dict(data_out, orient='columns')
    for idx in range(3):
        df[xyz_headings[idx]] = xyz_shifted[:, idx]

    for idx in range(3):
        df[euler_headings[idx]] = eulers[:, idx]

    if output_star_file is None:

        # Derive output filename
        star_file = Path(star_file)
        stem = star_file.stem
        output_filename = star_file.parent / (str(stem) + '_rln3.0.star')

    else:

        output_filename = output_star_file

    # Write output
    starfile.write(df, output_filename, overwrite=True)
    click.echo(f'Done! Wrote RELION 3.0 format STAR file to {output_filename}')
    return


@click.command()
@click.option('--star_file', '-s', type=click.Path(exists=True), default=None, help='Input STAR file')
@click.option('--output_star_file', '-o', type=click.Path(), default=None, help='Output STAR file')
def cli(star_file, output_star_file):
    if star_file is None:
        star_file = click.prompt('Input STAR file', type=click.Path(exists=True))

        if output_star_file is None:
            output_star_file = click.prompt('Output STAR file', type=click.Path())

    relion_star_downgrade(star_file, output_star_file)

