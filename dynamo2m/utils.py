import re
from pathlib import Path


def sanitise_micrograph_name(micrograph_name: str) -> str:
    """
    Replaces tomogram name from warp reconstructions with corresponding tomostar file if appropriate
    Ensures compatibility with M for subsequent STAR files
    :param micrograph_name:
    :return:
    """
    return re.sub(r".mrc_\d+.\d+Apx.mrc", ".mrc.tomostar", micrograph_name)


def sanitise_m_starfile_name(starfile_name: str) -> str:
    """
    Makes sure STAR filename is properly formatted for import into M (requires _data.star)
    :param starfile_name:
    :return:
    """
    if starfile_name.endswith('_data.star'):
        return starfile_name
    elif starfile_name.endswith('.star') and not starfile_name.endswith('_data.star'):
        return re.sub(r".star", "_data.star", starfile_name)
    else:
        return starfile_name + '_data.star'


def sanitise_dynamo_table_filename(table_file_name: str) -> str:
    """
    Make sure table file ends in .tbl
    :param table_file_name:
    :return:
    """
    if not table_file_name.endswith('.tbl'):
        table_file_name += '.tbl'

    return table_file_name


def reextract_table_filename(table_file_name: str) -> str:
    """

    :param table_file_name:
    :return:
    """
    return table_file_name.replace('.tbl', '.reextract.tbl')


def extract_tomostar_from_image_name(filename: str) -> str:
    """
    from a given filename, expected to be from the 'rlnImageName' column of a STAR file output by M
    extract the tomogram name
    :param filename:
    :return:
    """
    p = Path(filename)
    tomo_name = p.parts[-2]
    tomostar = tomo_name + '.tomostar'
    return tomostar
