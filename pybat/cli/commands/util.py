# Encoding: UTF-8
# Copyright (c) Marnik Bercx, University of Antwerp
# Distributed under the terms of the MIT License

from pymatgen.core import Structure
from pymatgen.analysis.transition_state import NEBAnalysis
from pymatgen.symmetry.analyzer import SpacegroupAnalyzer

"""
Utility commands for the pybat package.

"""

__author__ = "Marnik Bercx"
__copyright__ = "Copyright 2018, Marnik Bercx, University of Antwerp"
__version__ = "0.1"
__maintainer__ = "Marnik Bercx"
__email__ = "marnik.bercx@uantwerpen.be"
__date__ = "May 2018"


def show_path(directory, filename):
    """
    Show the final migration for a NEB calculation.

    Returns:

    """
    # TODO This is quite inefficient, since the NEBAnalysis script also parses the OUTCAR files. However, this was the fastest solution implementation wise.
    neb = NEBAnalysis.from_dir(directory)

    transition_structure = neb.structures[0].copy()
    for structure in neb.structures[1:]:
        for site in structure:
            transition_structure.append(site.specie, site.frac_coords)

    transition_structure.to("cif", filename + ".cif")


def conventional_structure(structure_file, fmt="cif"):
    """

    Args:
        structure_file:
        fmt:

    Returns:

    """
    structure = Structure.from_file(structure_file)
    spg = SpacegroupAnalyzer(structure)

    conv_structure_file = structure_file.split(".")[0] + "_conv" + "." + fmt
    spg.get_conventional_standard_structure().to(fmt, conv_structure_file)


def primitive_structure(structure_file, fmt="cif"):
    """

    Args:
        structure_file:
        fmt:

    Returns:

    """
    structure = Structure.from_file(structure_file)
    spg = SpacegroupAnalyzer(structure)

    prim_structure_file = structure_file.split(".")[0] + "_conv" + "." + fmt
    spg.get_primitive_standard_structure().to(fmt, prim_structure_file)


def make_supercell(structure_file, supercell, fmt="cif"):
    """

    Args:
        structure_file:
        supercell:
        fmt:

    Returns:

    """
    # Turn into list TODO add checks
    supercell_list = [int(number) for number in supercell]

    structure = Structure.from_file(structure_file)
    structure.make_supercell(supercell_list)

    super_structure_file = structure_file.split(".")[0] + "_" + supercell\
        + "." + fmt

    structure.to(fmt, super_structure_file)
