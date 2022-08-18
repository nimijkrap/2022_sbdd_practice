from vina import Vina
from rdkit import Chem
from rdkit.Chem import AllChem
from rdkit.six import StringIO
from meeko import MoleculePreparation, PDBQTMolecule

def read_smiles_file(filename):
    """
    read multiple smiles from the file having "name, smiles"
    """
    ligands=dict()
    f=open(filename,"r")
    lines=f.readlines()
    for l in lines:
        title, smi = l.rstrip().split(",")
        ligands[title]=smi
        f.close()
    return ligands

def convert_smi_to_pdbqt(smiles):
    """
    covert SMILES(string) to 3D structure in PDBQT format(string)
    """
    # Read smiles
    mol=Chem.MolFromSmiles(smiles)
    # Add hydrogens
    mol_h=Chem.AddHs(mol)
    # Generate 3D structure
    params=AllChem.ETKDGv3()
    AllChem.EmbedMultipleConfs(mol_h, 1, params)

    # Convert to PDBQT using meeko
    preparator=MoleculePreparation()
    preparator.prepare(mol_h)
    ligand_prepared = preparator.write_pdbqt_string()

    return ligand_prepared


def convert_vina_output_pdbqt_to_sdf(pdbqt_string):

    pdbqt_mol = PDBQTMolecule(pdbqt_string, skip_typing=True)
    output_string=''

    # RDKit mol from SMILES in docking output PDBQT remarks
    if pdbqt_mol._pose_data['smiles'] is None:
        msg = "\n\n    \"REMARK SMILES\" not found in input pdbqt string.\n"
        raise RuntimeError(msg)
    sio = StringIO()
    f = Chem.SDWriter(sio)
    for pose in pdbqt_mol:
        rdmol = pose.export_rdkit_mol()
        f.write(rdmol)
    f.close()
    output_string += sio.getvalue()
    output_format = 'sdf'

    return output_string

if __name__=="__main__":
    v = Vina(sf_name='vina')
    v.set_receptor('receptor.pdbqt')
    v.compute_vina_maps(center=[-20.096, 18.844, -27.394], box_size=[20, 20, 20])
    
    # Score the current pose
    ligand_dict=read_smiles_file("smiles.csv")
    f=open("results.csv", "w")
    for cpd_name in ligand_dict.keys():
        ligand_smiles=ligand_dict[cpd_name]
        ligand_pdbqt=convert_smi_to_pdbqt(ligand_smiles)
        v.set_ligand_from_string(ligand_pdbqt)
        v.dock(exhaustiveness=8, n_poses=20)
        scores=v.score()[0]
        f.write("%s,%s,%f\n"%(cpd_name,ligand_smiles,v.score()[0]))
        v.write_poses('%s_vina_out.pdbqt'%(cpd_name), n_poses=5, overwrite=True)
