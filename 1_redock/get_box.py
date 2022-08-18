from rdkit import Chem
from rdkit.Chem import rdMolTransforms

ligand_file="6w63_B_X77.sdf"
box_size=30

lig=Chem.MolFromMolFile(ligand_file)
conf=lig.GetConformer()
center=rdMolTransforms.ComputeCentroid(conf)
(cx, cy, cz) = (center.x, center.y, center.z)

bs=box_size
bs=float(bs)

print("%5.3f, %5.3f, %5.3f, %5.3f, %5.3f, %5.3f"%(cx, cy, cz, bs, bs, bs))
