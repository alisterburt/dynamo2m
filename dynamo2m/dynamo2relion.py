#!python
import click
import dynamotable
import starfile
import pandas as pd
from eulerangles import convert_eulers
from os import path

def dynamo2relion(input_table_file, binning_factor, output_star_file):
    # Try to find table_map_file automatically if it was not provided
    table_map_file = path.join(
            path.dirname(input_table_file),
            'indices_column20.doc')
    if path.isfile(table_map_file):
        click.echo('Automatically found table map file, will use it')
    else:
        table_map_file = None

    # Read dynamotable and prepare STAR data
    table = dynamotable.read(input_table_file, table_map_file)
    data = {}

    # Convert coordinates and adjust for binning
    for axis in 'xyz':
        heading = f'rlnCoordinate{axis.upper()}'
        shift_axis = f'd{axis}'
        data[heading] = (table[axis] + table[shift_axis]) * binning_factor
    
    # Convert eulerangles
    eulers_dynamo = table[['tdrot', 'tilt', 'narot']].to_numpy()
    eulers_relion = convert_eulers(
            eulers_dynamo,
            source_meta='dynamo',
            target_meta='relion')
    data['rlnAngleRot'] = eulers_relion[:, 0]
    data['rlnAngleTilt'] = eulers_relion[:, 1]
    data['rlnAnglePsi'] = eulers_relion[:, 2]

    # rlnTomoName
    tomo_map = {}
    tomos = table['tomo'].unique()
    tomo_files = table['tomo_file'].unique() if 'tomo_file' in table.columns else None
    for tomo_idx, tomo in enumerate(tomos):
        prompt = f"Enter rlnTomoName for tomogram {tomo}"
        if tomo_files is not None:
            prompt += f" at '{tomo_files[tomo_idx]}'"
        tomo_map[tomo] = click.prompt(prompt)
    data['rlnTomoName'] = table['tomo'].transform(tomo_map.get)

    # Create STAR file and write
    df = pd.DataFrame.from_dict(data)
    starfile.write(df, output_star_file, overwrite=True)
    click.echo(
        f"Done! Converted '{input_table_file}' to RELION 4.0 compatible STAR file '{output_star_file}'")

@click.command()
@click.option('--input_table_file', '-i',
              prompt='Input Dynamo table file',
              type=click.Path(dir_okay=False, exists=True),
              required=True)
@click.option('--binning_factor', '-b',
              prompt='Tomogram binning factor',
              type=int,
              default=1,
              required=False)
@click.option('--output_star_file', '-o',
              prompt='Output STAR file',
              type=click.Path(),
              default='<input table file>.star',
              required=False)
def cli(input_table_file, binning_factor, output_star_file):
    if output_star_file == '<input table file>.star':
        output_star_file = path.splitext(input_table_file)[0] + '.star'
    dynamo2relion(input_table_file, binning_factor, output_star_file)

if __name__ == '__main__':
    cli()
