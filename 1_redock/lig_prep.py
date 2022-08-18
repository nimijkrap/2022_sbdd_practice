from meeko import MoleculePreparation
from rdkit import Chem

ligand_file="6w63_B_X77.sdf"
mol=Chem.MolFromMolFile(ligand_file)
preparator=MoleculePreparation()
preparator.prepare(mol)
preparator.write_pdbqt_file("ligand.pdbqt")

