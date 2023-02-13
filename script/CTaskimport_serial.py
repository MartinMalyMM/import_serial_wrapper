from qtgui import CCP4TaskWidget

class CTaskimport_serial(CCP4TaskWidget.CTaskWidget):

    TASKNAME = 'import_serial'
    TASKVERSION = 1.0
    TASKMODULE =['data_entry']
    TASKTITLE = 'Import Serial'
    SHORTTASKTITLE = "Import Serial Data"
    DESCRIPTION = 'Import merged data from CrystFEL'
    WHATNEXT = []


    def __init__(self,parent):
        CCP4TaskWidget.CTaskWidget.__init__(self,parent)


    #@QtCore.Slot()
    #def updateFromCifFile(self):
    #    #print 'CTaskCif2mtz.updateFromCifFile',self.container.inputData.HKLIN.fileContent
    #    self.container.inputData.SPACEGROUPCELL.cell.set(self.container.inputData.HKLIN.fileContent.cell)
    #    self.container.inputData.SPACEGROUPCELL.spaceGroup.set(self.container.inputData.HKLIN.fileContent.spaceGroup)


    def drawContents(self):
        #self.setProgramHelpFile('cif2mtz')
        # TO DO: help
        self.openFolder(folderFunction='inputData', title='Input Data', followFrom=False)
        self.createLine(['tip', 'Merged data file (I)', 'widget', 'HKLIN'])
        # TO DO: display .hkl filen in the window
        self.createLine(["subtitle", "Half data sets for calculation of statistics"])
        self.openSubFrame(frame=[True])
        self.createLine(['tip', 'Merged data file (I)', 'widget', 'HKLIN1'])
        self.createLine(['tip', 'Merged data file (I)', 'widget', 'HKLIN2'])
        self.createLine(['label', 'Number of resolution bins', 'widget', 'N_BINS'])
        self.closeSubFrame()
        self.createLine(["subtitle", "Symmetry"])
        self.openSubFrame(frame=[True])
        self.createLine(['label', 'Space group', 'widget', 'SPACEGROUP'])
        self.createLine(['label', 'Unit cell', 'widget', 'CELL', 'label', '(specify 6 parameters divided by spaces)'])
        # TO DO: check that were given 6 floats
        # TO DO: determine cell automatically from stream file
        self.closeSubFrame()
        self.createLine(["subtitle", "Resolution"])
        self.openSubFrame(frame=[True])
        self.createLine(['label', 'Low resolution cutoff', 'widget', 'D_MAX'])
        self.createLine(['label', 'High resolution cutoff', 'widget', 'D_MIN'])
        # TO DO: use resolution parameters not only for statistics but really cut the data
        self.closeSubFrame()
