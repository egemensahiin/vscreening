import npyscreen
import multiprocessing
import functions
from datetime import datetime as dt


class TerminalUI(npyscreen.NPSApp):

    def main(self):
        self.numCPUs = multiprocessing.cpu_count()
        self.defaultProjectName = "Project" + dt.now().strftime("%d%m%Y%H%M%S")

        self.firstPage()
        self.configPage()

    def firstPage(self):
        # Create the TUI environment as a form. Name displays as a header.
        formFirst = npyscreen.Form(name = "Virtual Screening TUI")
        description = formFirst.add(npyscreen.FixedText,
                               value = "\t\tThis program performs virtual screening with a receptor and a set of ligands.")
        seperator0 = formFirst.add(npyscreen.FixedText, value = "---------Select files-----")
        fileProtein = formFirst.add(npyscreen.TitleFilenameCombo, name = "Protein:")
        fileSet = formFirst.add(npyscreen.TitleFilenameCombo, name = "Ligand Set:")
        seperator2 = formFirst.add(npyscreen.FixedText, value = "----------Settings--------")
        selectPrep = formFirst.add(npyscreen.TitleSelectOne,
                               max_height=4, value = [0,], name="Preparation Method:",
                               values = ["OpenBabel","AutoDock Scripts"], scroll_exit=True)
        selectCores = formFirst.add(npyscreen.TitleSlider, lowest=1, out_of=self.numCPUs,
                                     value = self.numCPUs, name = "Number of CPU:")
        textProjectName = formFirst.add(npyscreen.TitleText, name = "Project Name:", value = self.defaultProjectName)
        selectConf = formFirst.add(npyscreen.TitleSelectOne,
                               max_height=4, value = [0,], name="Config Method:",
                               values = ["From file","Manual entry"], scroll_exit=True)
        formFirst.edit()

        self.protein = fileProtein.value
        self.ligandSet = fileSet.value
        self.prep = selectPrep.value[0] # return 0 for openbabel and 1 for autodock scripts
        self.cores = int(selectCores.value)
        self.configMethod = selectConf.value[0]
        self.projectName = textProjectName.value

    def configPage(self):
        formConfig = npyscreen.Form(name = "Virtual Screening TUI")
        seperator1 = formConfig.add(npyscreen.FixedText, value = "---------Config-----------")
        if self.configMethod == 1:
            textSizeX = formConfig.add(npyscreen.TitleText, name = "Size X:")
            textSizeY = formConfig.add(npyscreen.TitleText, name = "Size Y:")
            textSizeZ = formConfig.add(npyscreen.TitleText, name = "Size Z:")
            textCenterX = formConfig.add(npyscreen.TitleText, name = "Center X:")
            textCenterY = formConfig.add(npyscreen.TitleText, name = "Center Y:")
            textCenterZ = formConfig.add(npyscreen.TitleText, name = "Center Z:")
            textExhaust = formConfig.add(npyscreen.TitleText, name = "Exhaustiveness:")
            formConfig.edit()
            self.sizeX = textSizeX.value
            self.sizeY = textSizeY.value
            self.sizeZ = textSizeZ.value
            self.centerX = textCenterX.value
            self.centerY = textCenterY.value
            self.centerZ = textCenterZ.value
            self.exhaustiveness = textExhaust.value

        elif self.configMethod == 0:
            selectConfigFile = formConfig.add(npyscreen.TitleFilenameCombo, name = "Config File")
            formConfig.edit()
            self.configFile = selectConfigFile.value


if __name__ == "__main__":
    TuiApp = TerminalUI()
    TuiApp.run()
    functions.makeDir(dirname = TuiApp.projectName)
    functions.prepareLigands(TuiApp.ligandSet, TuiApp.prep)
    if TuiApp.configMethod == 1:
        functions.writeConfig(
            TuiApp.protein, TuiApp.sizeX, TuiApp.sizeY, TuiApp.sizeZ, TuiApp.centerX, TuiApp.centerY, TuiApp.centerZ, TuiApp.exhaustiveness)
        functions.runVina(TuiApp.cores, TuiApp.protein)
    elif TuiApp.configMethod == 0:
        functions.runVina(TuiApp.cores, TuiApp.protein, TuiApp.configFile)
    functions.writeLog(logName = TuiApp.projectName.lower() + ".log")
