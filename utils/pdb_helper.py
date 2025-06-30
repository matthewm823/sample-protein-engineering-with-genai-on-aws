from io import StringIO
import biotite.structure.io.pdb as pdb

def structure_to_pdb_str(structure):
    stream = StringIO()
    pdbFile = pdb.PDBFile()
    pdbFile.set_structure(structure)
    pdbFile.write(stream)
    return stream.getvalue()