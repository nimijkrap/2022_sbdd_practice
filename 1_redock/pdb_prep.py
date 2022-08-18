from pdbfixer import PDBFixer
from openmm.app import PDBFile
import os

pdbfile="6w63.pdb"

fixer = PDBFixer(filename=pdbfile)

#print(list(fixer.topology.chains()))

# Remain only chains we are interested in
"""
Ex1) remain only first chain: fixer.removeChains(range(1,len(list(fixer.topology.chains()))))
Ex2) remove chain 1,2: fixer.removeChains([1,2])
"""
fixer.removeChains(range(1,len(list(fixer.topology.chains()))))


# replace nonstandard residues
fixer.findNonstandardResidues()
fixer.replaceNonstandardResidues()

#remove Heteroges including waters
fixer.removeHeterogens(False)

#add hydrogens
fixer.addMissingHydrogens(7.0)

PDBFile.writeFile(fixer.topology, fixer.positions, open('receptor.pdb', 'w'), keepIds=True)

os.system("obabel -ipdb receptor.pdb -opdbqt -Oreceptor.pdbqt -p 7.0 -xr")
