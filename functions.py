import subprocess
import os, sys
import glob

vinaBinary = "../bin/vina"
adScriptLocation = subprocess.getoutput("locate prepare_ligand4")

def makeDir(dirname):
    os.mkdir(dirname)
#     for fileName in args:
#         with open(fileName, 'r') as toMove:
#             with open(os.getcwd() + dirname, 'a') as copy:
#                 copy.write(toMove.read())
    os.chdir(dirname)

def prepareLigands(ligandSet, method):
    subprocess.call(f"obabel {ligandSet} -opdb -O ligand.pdb -m --error-level 3", shell=True )
    pdbList = glob.glob(os.getcwd() + "/ligand*.pdb")
    for ligand in pdbList:
        if method == 0:
            subprocess.call(f"obabel {ligand} -opdbqt -O {ligand}.pdbqt -m -h --error-level 3", shell=True )
        elif method == 1:
            subprocess.call(f"{adScriptLocation} -l {ligand} -A hydrogens", shell=True)

def writeConfig(protein, size_x, size_y, size_z, center_x, center_y, center_z, exhaustiveness):
    with open("conf.txt", "a") as configFile:
        configFile.write(f"receptor={protein}\n")
        configFile.write(f"size_x={size_x}\n")
        configFile.write(f"size_y={size_y}\n")
        configFile.write(f"size_z={size_z}\n")
        configFile.write(f"center_x={center_x}\n")
        configFile.write(f"center_y={center_y}\n")
        configFile.write(f"center_z={center_z}\n")
        configFile.write(f"exhaustiveness={exhaustiveness}")

def runVina(cores, receptor, config = os.getcwd() + "/conf.txt"):
    pdbqtList = glob.glob(os.getcwd() + "/ligand*.pdbqt")
    for ligand in pdbqtList:
        subprocess.call(f"{vinaBinary} --receptor {receptor} --ligand {ligand} --config {config} --cpu {str(cores)} --log {ligand.split('.')[0] + '.log'}",shell=True )

def writeLog(logName):
    with open(logName + ".csv", 'a') as totalLogFile:
        totalLogFile.write('Name,affinity,rmsd,rmsdub\n')
        logsList = glob.glob(os.getcwd() + "/ligand*.log")
        for log in logsList:
            with open(log, 'r') as logFile:
                ligandName = log.split(".")[0].split("/")[-1]
                csvLines = []
                content = logFile.readlines()[26:34]
                for lineCont in content:
                    affinity = lineCont[12:17].strip()
                    rmsd = lineCont[22:28].strip()
                    rmsdub = lineCont[33:].strip()
                    values = f"{ligandName},{affinity},{rmsd},{rmsdub}\n"
                    csvLines.append(values)
            for lineCSV in csvLines:
                totalLogFile.write(lineCSV)
