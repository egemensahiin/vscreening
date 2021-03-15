# vscreen
A simple script and a TUI written in python to perform virtual screening
## Dependencies
- **AutoDock Vina** (binary located at bin) 
- **Open Babel**
- **npyscreen** library (for TUI)
## Usage
### Command Line Interface
- To use CLI, be sure about that you have the propper permissions for vscreen script:
> $ chmod +x vscreen
- After you give permissions, run ./vina -h to see options and basic usage
> $ ./vina -h
> USAGE: $0 -p PROTEIN -l LIGANDS -c CONFIG [-hv][-n NAME]
> ./vina, does virtual screenin by using AutoDock vina.
> Files for protein, database file that contains ligands
> and configuration file must be provided.
>   -p PROTEIN    .pdbqt file that provides proteins.
>   -l LIGANDS	  Database file which contains ligand structures
>                 (.mol, .sdf etc.)
>   -c CONFIG     Configuration file that specify the size and
>                 the position of the grid (and other optional
>                 parameters).
> 	-s			  AutoDock scripts conversion (default obabel).
> 	-x NUM		  Number of CPU's to use. Default is blank (max).
>   -n NAME       Specify a name for your project.
>   -h            Write out this message.
>   -v            Verbose output
### Terminal User Interface
- To run TUI you should install npyscreen by:
> $ pip3 install npyscreen
- Then just type:
> $ python3.7 main.py
- The TUI explains itself so you should just choose what you need and run it.
##TODO
- Add an automated docking process with ./bin/autodock* binaries and AutoDock Scripts.
- Sort the total logs given by the TUI according to the binding energy of conformations.
- Do some error handling (especially for the situation of the absence of AutoDockScripts).
- Add command line arguments for TUI such as --help etc.
