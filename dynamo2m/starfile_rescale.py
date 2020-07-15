### Rescale the pixel size in STAR files from WARP/M ###

import click
import starfile


@click.command()
@click.option('--input_star_file', '-i',
              prompt='Input STAR file',
              type=click.Path(exists=True),
              required=True,
              )
@click.option('--output_star_file', '-o',
              prompt='Output STAR file',
              type=click.Path(exists=False),
              required=True,
              )
@click.option('--input_apix', '-i',
              prompt='Pixel size in Angstroms of input STAR file',
              type=float,
              required=True,
              )
@click.option('--output_apix', '-o',
              prompt='Pixel size in Angstroms of output STAR file',
              type=float,
              required=True,
              )
def cli(input_star_file, output_star_file, input_apix, output_apix):
    # Read input star file into dataframe
    star = starfile.read(input_star_file)

    # Define columns which we would like to rescale
    columns_to_rescale = ['rlnCoordinateX', 'rlnCoordinateY', 'rlnCoordinateZ',
                          'wrpCoordinateX', 'wrpCoordinateY', 'wrpCoordinateZ',
                          'wrpCoordinateX1', 'wrpCoordinateY1', 'wrpCoordinateZ1']

    # Find columns which are present in dataframe
    columns_to_rescale = filter(lambda x: x in star.columns, columns_to_rescale)

    # Calculate rescaling factor
    rescaling_factor = input_apix / output_apix

    # Rescale columns
    star[columns_to_rescale] *= rescaling_factor

    # Write out STAR file
    starfile.write(star, output_star_file)
    return


