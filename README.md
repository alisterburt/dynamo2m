# dynamo2m
`dynamo2m` is a set of Python scripts to interface the subtomogram averaging software 
[Dynamo](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Main_Page) 
with the 
multi particle refinement cryo-EM software [M](http://www.warpem.com/warp/?page_id=1614).

It forms part of the image processing pipeline described in the following [preprint]().


## Motivation
Dynamo is a tomography specific software package with many useful tools for subtomogram averaging including...

- Flexible [subtomogram averaging](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Dcp_GUI) workflows
- Ways to [visualise](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Walkthrough_for_lattices_on_vesicles#Merging_the_tables) subtomogram averaging results
- Interactive tools for [initial model generation](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Starters_guide#Initial_model_generation)
- [Automated tilt-series alignment](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Walkthrough_on_command_line_based_tilt_series_alignment)
- [PCA based classification and analysis tools](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Walkthrough_on_PCA_through_the_command_line)
- [Geometric modelling and visualisation tools](https://wiki.dynamo.biozentrum.unibas.ch/w/index.php/Model) for particle picking and tomogram annotation

M is a software package which allows one to perform multi-particle refinements with the aim of correcting for various 
sample deformations which can occur during imaging, it currently holds the record for high resolution 
single particle analysis from frame-series and tilt-series data.

The ability to easily combine these software packages is the goal of the scripts provided in this package.

## Scripts
- `dynamo2warp` for the conversion of Dynamo metadata to facilitate extraction of particles in Warp
- `warp2dynamo` for the conversion of Warp STAR files into Dynamo compatible metadata
- `starfile_rescale` can rescale the metadata in STAR files (necessary to get around bugs in beta versions of M)
- Conversion to Excel speadsheet (.xlsx)


## Installation
Installation is available directly from the [Python package index](https://pypi.org/project/dynamo2m/)
```
pip install dynamo2m
```


## Usage
Each of the scripts can be invoked directly from the command line an interactive command line interface. 

For example
```
dynamo2warp
```

```
Input Dynamo table file: example.tbl
Input Dynamo table map file: example.doc
Output STAR file: test.star
Done! Converted 'example.tbl' to RELION/Warp compatible STAR file 'test_data.star'

```

Alternatively, options can be passed directly at the command line, this is detailed in the help provided with each script

```
dynamo2warp --help
```

```
Usage: dynamo2warp [OPTIONS]

Options:
  -i, --input_table_file PATH  [required]
  -tm, --table_map_file PATH   [required]
  -o, --output_star_file PATH  [required]
  --help                       Show this message and exit.

```
