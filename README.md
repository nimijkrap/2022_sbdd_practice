# 2022_sbdd_practice
sbdd practice files for 2022 workshop


# Set environment

```bash
$ conda create -n sbdd_practice python=3.7
$ conda activate sbdd_practice
$ conda config --env --add channels conda-forge
$ conda install -c conda-forge numpy swig boost-cpp sphinx sphinx_rtd_theme scipy rdkit openmm openbabel pdbfixer pymol-open-source
$ pip install vina meeko
```

# Practice Summary 

## PDB 다운로드
PDB ID: 6W63, 7VTH, 7VU6

Download PDB files from the PDB website
[RCSB PDB: Homepage](https://www.rcsb.org/)

or 

```bash
$ wget [https://files.rcsb.org/download/6W63.pdb](https://files.rcsb.org/download/6W63.pdb)
```

## 1. Re-docking 
Receptor - 3CL protease (PDB ID: 6w63)
Ligand - 3CL protease inhibitor X77 (PDB ID: 6w63)

```bash
$ python pdb_prep.py
$ python lig_prep.py
$ python get_box.py
$ python simple_run.py
$ pymol *.pdbqt
```

Analysis docking model wih PyMol
```
$ rms /ligand////*, /ligand_vina_out////*
$ split_states ligand_vina_out
$ rms /ligand////*,/ligand_vina_out_0001////*
```

## 2. Docking ligands to receptor (PDB ID: 6w63)

```bash
$ python run_docking.py
$ pymol pdb/7vth.pdb, 7vu6.pdb, receptor.pdbqt, *_vina_out.pdbqt
```

```
align 7vu6, receptor
align 7vth, receptor
```

