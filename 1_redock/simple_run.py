from vina import Vina

v = Vina(sf_name='vina')

#set receptor
v.set_receptor('receptor.pdbqt')

#set docking box
v.compute_vina_maps(center=[-20.096, 18.844, -27.394], box_size=[30, 30, 30])

#set ligand
v.set_ligand_from_file('ligand.pdbqt')

# Score the current pose
energy = v.score()
print('Score before minimization: %.3f (kcal/mol)' % energy[0])

# Minimized locally the current pose
energy_minimized = v.optimize()
print('Score after minimization : %.3f (kcal/mol)' % energy_minimized[0])
v.write_pose('ligand_minimized.pdbqt', overwrite=True)

# Dock the ligand
v.dock(exhaustiveness=32, n_poses=10)
v.write_poses('ligand_vina_out.pdbqt', n_poses=5, overwrite=True)

# optimization after docking
print(v.optimize()[0])
v.write_pose('ligand_vina_out_optimized.pdbqt', overwrite=True)

