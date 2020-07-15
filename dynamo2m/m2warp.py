### Conversion of STAR files output by M into RELION compatible STAR files ###
# GOAL: Rerun refinements after running M refinements
# Requires
#  - starfile (depends on pandas),
#  - click
# tested and working against warp v1.0.7
# M coordinates are in Angstroms, use 1apix in the dialogue box when reextracting particles in WARP

import click
import starfile


@click.command()
@click.option('--input_star_file', '-i',
              prompt='Input STAR file',
              type=click.Path(exists=True),
              required=True)
@click.option('--output_star_file', '-o',
              prompt='Output STAR file',
              type=click.Path(exists=False),
              required=True)
def cli(input_star_file, output_star_file):
    # Read star file
    star = starfile.read(input_star_file)

    # Change necessary column headings
    column_names = {'wrpCoordinateX1' : 'rlnCoordinateX',
                          'wrpCoordinateY1' : 'rlnCoordinateY',
                          'wrpCoordinateZ1' : 'rlnCoordinateZ',
                          'wrpAngleRot1' : 'rlnAngleRot',
                          'wrpAngleTilt1' : 'rlnAngleTilt',
                          'wrpAnglePsi1' : 'rlnAnglePsi',
                          'wrpSourceName' : 'rlnMicrographName' }

    star.rename(columns=column_names, inplace=True)

    # Remove unnecessary columns (to avoid problems if you want to run relion refinements
    star.drop(labels=['wrpSourceHash', 'wrpRandomSubset'], axis='columns', inplace=True)

    # Write out STAR file
    starfile.write(star, output_star_file)

    # Echo status to prompt
    click.echo(f"RELION format STAR file written to '{output_star_file}'")

    return