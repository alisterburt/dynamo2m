import click
import numpy as np
import pandas as pd
import starfile
import dynamotable
from eulerangles import euler2euler

from .utils import sanitise_dynamo_table_filename, reextract_table_filename, extract_tomostar_from_image_name


@click.command()
@click.option('--input_star_file', '-i', 'm_star_file',
              prompt='Input M STAR file',
              type=click.Path(exists=True),
              required=True)
@click.option('--output_table_file', '-o', 'dynamo_table_file',
              type=click.Path(exists=False),
              prompt='Output dynamo table file')
@click.option('--extracted_box_size', '-bs', 'extracted_box_size',
              prompt='Extracted box size (px)',
              type=int,
              required=True)
def cli(m_star_file, dynamo_table_file, extracted_box_size):
    """
    CLI for converting an M STAR file into a dynamo table file Outputs a few things 1) dynamo table and
    corresponding table map (.doc) 2) dynamo STAR file as data container (to avoid reextraction) 3) a separate table
    for reextraction as a dynamo data folder (STAR container didn't work in my hands for alignment projects)
    :param extracted_box_size:
    :param m_star_file:
    :param dynamo_table_file:
    :return:
    """
    # Read STAR file
    relion_star = starfile.read(m_star_file)

    # Initialise empty dict for dynamo
    dynamo_data = {}

    # Get XYZ positions and put into data
    for axis in ('x', 'y', 'z'):
        relion_heading = 'rlnCoordinate' + axis.upper()
        dynamo_data[axis] = relion_star[relion_heading]

    # Get euler angles and convert to dynamo convention (only if eulers present in STAR file)
    if 'rlnAngleRot' in relion_star.columns:
        eulers_relion = relion_star[['rlnAngleRot', 'rlnAngleTilt', 'rlnAnglePsi']].to_numpy()
        eulers_dynamo = euler2euler(eulers_relion, source_convention='relion', target_convention='dynamo')

        dynamo_data['tdrot'] = eulers_dynamo[:, 0]
        dynamo_data['tilt'] = eulers_dynamo[:, 1]
        dynamo_data['narot'] = eulers_dynamo[:, 2]

    # Add tomogram info
    dynamo_data['tomo_file'] = relion_star['rlnImageName'].apply(extract_tomostar_from_image_name)

    # Convert to DataFrame
    df = pd.DataFrame.from_dict(dynamo_data)

    # Write table file
    dynamo_table_file = sanitise_dynamo_table_filename(dynamo_table_file)
    click.echo(f"Writing out Dynamo table file '{dynamo_table_file}' and corresponding table map file with appropriate info...\n")
    dynamotable.write(df, dynamo_table_file)

    # Write out dynamo STAR file to avoid reextraction
    dynamo_star_name = dynamo_table_file + '.star'
    click.echo(f"Writing out Dynamo format STAR file '{dynamo_star_name}' to avoid reextraction...\n")

    tags = [x+1 for x in range(df.shape[0])]
    particle_files = relion_star['rlnImageName']
    dynamo_star = {'tag' : tags,
                    'particleFile' : particle_files }
    dynamo_star = pd.DataFrame.from_dict(dynamo_star)

    starfile.write(dynamo_star, dynamo_star_name)

    # Write out reextraction table and .doc file (STAR files with mrc volumes didn't work in dynamo 1.1.509 in my hands)
    # Get extraction table name
    reextraction_table_name = reextract_table_filename(dynamo_table_file)

    # Change xyz positions to match centers of extracted boxes
    for axis in ('x', 'y', 'z'):
        df[axis] = np.ones_like(df[axis]) * (extracted_box_size / 2)

    # Change tomo_file to point to individual particles and make tomo equal to tags
    df['tomo_file'] = relion_star['rlnImageName']
    df['tomo'] = df['tag']

    # Write
    click.echo(f"Writing out table and table map to facilitate reextraction if dynamo STAR file doesn't work...")
    click.echo(f"General reextraction command: dtcrop <tomogram_table_map.doc> <tableForAllTomograms>  <outputfolder> <sidelength> -asBoxes 1")
    extraction_command = f"dtcrop {reextraction_table_name.replace('.tbl', '.doc')} {reextraction_table_name}  <outputfolder> {extracted_box_size} -asBoxes 1"
    click.echo(f"Extraction command for your data: {extraction_command}")
    dynamotable.write(df, reextraction_table_name)

    click.echo(f"\nDone! Converted M output '{m_star_file}' into Dynamo input files")
    return




