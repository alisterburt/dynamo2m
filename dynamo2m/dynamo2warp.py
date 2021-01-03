import click
import dynamotable
import starfile
import pandas as pd
from eulerangles import convert_eulers
from .utils import sanitise_micrograph_name, sanitise_m_starfile_name


def dynamo2warp(input_table_file, table_map_file, output_star_file):
    # Read table file into dataframe
    table = dynamotable.read(input_table_file, table_map_file)

    # Prep data for star file in dict
    data = {}

    # extract xyz into dict with relion style headings
    for axis in ('x', 'y', 'z'):
        heading = f'rlnCoordinate{axis.upper()}'
        shift_axis = f'd{axis}'
        data[heading] = table[axis] + table[shift_axis]

    # extract and convert eulerangles
    eulers_dynamo = table[['tdrot', 'tilt', 'narot']].to_numpy()
    eulers_warp = convert_eulers(eulers_dynamo,
                                 source_meta='dynamo',
                                 target_meta='warp')
    data['rlnAngleRot'] = eulers_warp[:, 0]
    data['rlnAngleTilt'] = eulers_warp[:, 1]
    data['rlnAnglePsi'] = eulers_warp[:, 2]

    # extract and sanitise micrograph names to ensure compatibility with M
    data['rlnMicrographName'] = table['tomo_file'].apply(sanitise_micrograph_name)

    # convert dict to dataframe
    df = pd.DataFrame.from_dict(data)

    # write out STAR file
    starfile.write(df, output_star_file, overwrite=True)

    # echo to console
    click.echo(
        f"Done! Converted '{input_table_file}' to RELION/Warp compatible STAR file '{output_star_file}'")

    return

@click.command()
@click.option('--input_table_file', '-i',
              prompt='Input Dynamo table file',
              type=click.Path(),
              required=True)
@click.option('--table_map_file', '-tm',
              prompt='Input Dynamo table map file',
              type=click.Path(),
              required=True)
@click.option('--output_star_file', '-o',
              prompt='Output STAR file',
              type=click.Path(),
              required=True)
def cli(input_table_file, table_map_file, output_star_file):
    dynamo2warp(input_table_file, table_map_file, output_star_file)
