import h5py
f = h5py.File('myfile.hdf5')
dset = f.create_dataset("MyDataset", (100, 5), 'i')
dset[...] = 42
f.close()