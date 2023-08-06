# MolLayers

## Introduction

MolLayers is a python package that implements the Layers algorithm (Karampudi & Bahadur, 2015) which is freely available as a [web-application](http://www.csb.iitkgp.ac.in/applications/mol_layers/main). The purpose of developing MolLayers as a package is two-fold. One is to simplify the adaptability of Layers algorithm (Karampudi & Bahadur, 2015) by leveraging the file parsers provided in biopython library (Cock et al., 2009). Two is to facilitate a seamless integration of Layers algorithm in researchers’ biomolecular structural analysis pipeline without depending on web-application. 
Even though the web-application was developed to free the user from technical details and simplify the usage of the algorithm, it is also not an optimal solution when large scale analysis involving hundreds of biomolecules is desired. MolLayers as a python package, simplifies the availability of Layers algorithm besides gaining the capability of accepting multiple file formats like pdb, cif and mmtf that are supported by biopython.


## Installation

MolLayers is developed in Python v3.10 and should work with all compatible versions (python v3.0 - v3.10). MolLayers is available for installation via python’s pip command. The pre-requisite packages are biopython (v1.79), mmtf-python (v1.0) will be automatically installed. The package is OS independent, thanks to Python community. 
pip command usage:
```
$ pip install MolLayers
```

## Usage

After successful installation, MolLayers can be used in few lines of codes as shown below

```
$ from MolLayers import engine
$ data = engine.Layers(‘local/path/1a2y.pdb’)
$ data.calc_surface(peel_layers=True)
```

The above three lines of code is the minimal that is needed to run the Layers algorithm provided by MolLayers package. A little bit more details on the package are as follows:

## Input details: 

MolLayers can accept two different inputs:
a)	Local file with ‘.pdb’, ‘.cif’, ‘.mmtf’ file formats as input. 
b)	Fetched file using biopython library. This will help integrate the MolLayers package in native code of the user.

## Output details:

MolLayers output is defined by two schemas:
1)	data.calc_surface(): only surface of the molecule shall be extracted and the name of the output will be ‘pdb_id.surf1’. The output directory can be specified using the out_dir parameter, if not provided the output will be save to the current working directory from the which the python code is executed.
2)	data.calc_surface(peel_layers=True): peel_layers=True is the flag that invokes repeated peeling of molecular atoms as layers. This results in more that one layer of atoms, hence the numbering is used to distinguish the layers. The first layer is the surface layer which is labelled with extension .surf1, followed by second layer labelled with extension .surf2 and so on. For a given molecule the .surf1 is the surface layer and the .surfx where x could be any highest number given to a layer is the core of the molecule according to Layers algorithm. 

Another parameter critical to Layers algorithm is cut_off which is assigned to a default value of 1.52 as proposed in Layers algorithm. If cut_off value is changed from default to custom value, the Layers algorithm will sample the surface of the molecule and the peel_layers parameter will be turned off. This cut_off parameter can be used to fine tune the sampling fineness for a molecule. The output file when cut_off parameter is changed is assigned with an output file with extension having ‘sampl_cut_off_value.pdb’. For example, if cut_off value is set to 3, then the output filename for pdb_id: 1a2y will look like 1a2y_sampl_3.pdb. The cut_off value can be either integer or float values.
One additional file type that ends with extension ‘pdb_id.RTP’ is also provided with layers number assigned to the residues. The way the assignment of layer number to residue happens is, first the atoms of a residue are parsed for all the layer numbers assigned to its atoms. Then the residue will take the layer number from the atom with the highest layer number among its atoms. This is what is emphasized in the Layers algorithm, as the protein folds an amino acid residue anchors its position in the folding structure by burying its atoms in the deeper layers of the structure. Hence, the position of the residue is stabilized by that anchored atom, and this atom would have a highest layer number with respect to its other atoms belonging to the same residue. If a residue is not spread across multiple layers, then all atoms of that residue will have same layer number. This way a Residue Transition Pattern (RTP) can be generated for any given structure. The file with the extension ‘.RTP’ captures the RTP of a molecule as assigned by the Layers algorithm.

## Variants in Usage:

Here I show three different ways in which MolLayers can be accessed based on the input source and two different ways based on output specifications.

### Working with Local file
```
$ from MolLayers import engine
$ data = engine.Layers(‘local/path/1a2y.pdb’)
$ data.calc_surface(peel_layers=True)
```

Here the input file is locally stored and the path along with the filename are provided.

### Fetch file from database
```
$ from MolLayers import engine
$ from Bio.PDB.mmtf import MMTFParser
$ structure=MMTFParser.get_structure_from_url(`1a2y`)
$ data=engine.Layers(structure)
$ data.calc_surface(peel_layers=True)
```
Here the input file is fetched from the online database and a variable named ‘structure’ which can be any other name as you wish in your code can be assigned with the procured structure and pass it to the engine module. For any fetched file the ‘pdb’ format is used by default.

## Surface extraction 

Besides extracting the layers for a molecule, Layers algorithm can also sample the molecular surface at tuneable coarseness. For this the input parameter is cut_off with default value of 1.52 Angstroms.  If cut_off value is increase from 1.52, then Layers is automatically redirected to surface sampling rather than surface peeling. The peel_layers=True is valid only when the cut_off value is set to default. Any variation in cut_off value from default will turn off the peel_layers parameter even if it passed as True. The cut_off variable can be passed like:
```
$data=engine.Layers(‘test/1a2y.pdb’, cut_off = i)
$data.calc_surface()
```
### OR
```
$for i in range(2,10):
$	data=engine.Layers(‘test/1a2y.pdb’, cut_off = i)
$	data.calc_surface()
```
### OR
```
$for i in range(2,10):
$	data=engine.Layers(‘test/1a2y.pdb’)
$	data.calc_surface(cut_off = i)
```
In all the above cases, the MolLayers package will invoke the necessary functions to process the molecule. The initialization of structure file should be in the control of loop, as some parameters has to be initialized essentially resetting the environment and sample the protein without allowing any previous parameter variation to effect the current sampling cut_off. If peel_layers parameter is not activated, or in other words if data.calc_surface() is called without passing any parameters then surface layer will only be calculated.

## Output Usage Variant 1:

Output path can be given using the parameter out_dir. Default value for out_dir is current directory. Only the path needs to be specified, the output filename will be extracted from the structure_id and the file format will be retained, which means an input file in pdb format will result in output file in pdb format.
```
$data.calc_surface(out_dir=’user/defined/path’)
```

The provided path may or may not end with ‘/’, the package will adjust the out_dir path with ending slash. Forward slash shall be used irrespective of the Operating System (OS). 

## Output Usage Variant 2:

With all the output parameters provided the usage of the module will look like this:
```
$data.calc_surface(peel_layers=True,out_dir=’user/defined/path’)
```

### OR
```
$data.calc_surface(out_dir=’user/defined/path’,cut_off=3)
```
## Conclusion

MolLayers is an open-source package available with GNU GPL V3 license. It facilitates working with multiple file formats provided through biopython package. MolLayers is a simple to use module with all inner workings hidden from user and simplifies adapting Layers algorithm in their workflow seamlessly.

## How to cite:
If you use MolLayers package, please cite the following:
1)	MolLayers article (yet to be published)
2)	Karampudi, N., Bahadur, R. Layers: A molecular surface peeling algorithm and its applications to analyze protein structures. Sci Rep 5, 16141 (2015). https://doi.org/10.1038/srep16141

