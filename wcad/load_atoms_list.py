import sys
import logging
import json
from object_types.atom import GammaAtom

def main( file_name ):
    # Read atoms produced by wcad.
    with open(file_name) as f:
        atoms_from_file = f.read()

    # Split into single atom entries.
    atoms_from_file = atoms_from_file.split('{')
    # print atoms_from_file[1]

    # Read each atom from string.
    atoms = list()
    for atom in atoms_from_file:
        if atom == '':
            continue
        atom = str('{' + atom)  # Add missing curly bracket used for splitting.
        # print atom

        # Atoms were stored by json.dumps(...).
        basic_entry = json.loads(atom)
        # print basic_entry

        if basic_entry['atom_type'] == "GammaAtom":
            atom_obj = GammaAtom(basic_entry['k'], basic_entry['theta'],
                                 basic_entry['fs'], basic_entry['amp'],
                                 basic_entry['pos'], basic_entry['length'])
            atom_obj.id = basic_entry['atom']
        else:
            logging.error("Unknown type of atom:", basic_entry['atom_type'])
            return None

        # Append new atom to the atoms list.
        atoms.append(atom_obj)

    # At this point all atoms are stored in the atoms list.
    return atoms