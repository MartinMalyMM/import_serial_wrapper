from qtgui import CCP4TaskWidget
import sys
import os


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
        #self.createLine(['advice', 'Define Resolution Shells (semi-automated)'])
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
        self.createLine(['label', 'Load symmetry from ', 'widget', '-guiMode', 'radio', 'SYMMETRY_SOURCE'])
        self.createLine(['tip', 'Reference structure or data', 'widget', 'REFERENCEFILE'], toggle=['SYMMETRY_SOURCE', 'open', 'reference'])
        self.connectDataChanged('REFERENCEFILE', self.updateFromReferenceFile)
        self.createLine(['tip', 'Cell file from CrystFEL', 'widget', 'CELLFILE'], toggle=['SYMMETRY_SOURCE', 'open', 'cellfile'])
        self.connectDataChanged('CELLFILE', self.updateFromCellFile)
        self.createLine(['tip', 'Stream file from CrystFEL', 'widget', 'STREAMFILE'], toggle=['SYMMETRY_SOURCE', 'open', 'streamfile'])
        self.createLine(['label', 'Space group', 'widget', 'SPACEGROUP'])
        self.createLine(['label', 'Unit cell', 'widget', 'CELL', 'label', '(6 parameters divided by spaces)'])
        # TO DO: check that were given 6 floats
        self.closeSubFrame()

        self.createLine(["subtitle", "Resolution"])
        self.openSubFrame(frame=[True])
        self.createLine(['label', 'Low resolution cutoff', 'widget', 'D_MAX'])
        self.createLine(['label', 'High resolution cutoff', 'widget', 'D_MIN'])
        # TO DO: use resolution parameters not only for statistics but really cut the data
        self.closeSubFrame()

    def updateFromCellFile(self):
        def get_cell_cellfile(cellfile):
            with open(cellfile, 'r') as f:
                lines = f.readlines()
            cell = [None, None, None, None, None, None]
            cell_string = None
            for line in lines:
                try:
                    if line.split()[0] == "al" and line.split()[-1] == "deg":
                        cell[3] = float(line.split()[-2])
                    elif line.split()[0] == "be" and line.split()[-1] == "deg":
                        cell[4] = float(line.split()[-2])
                    elif line.split()[0] == "ga" and line.split()[-1] == "deg":
                        cell[5] = float(line.split()[-2])
                    elif line.split()[0] == "a" and line.split()[-1] == "A":
                        cell[0] = float(line.split()[-2])
                    elif line.split()[0] == "b" and line.split()[-1] == "A":
                        cell[1] = float(line.split()[-2])
                    elif line.split()[0] == "c" and line.split()[-1] == "A" and not "centering" in line:
                        cell[2] = float(line.split()[-2])
                except:
                    continue
            print("")
            if (cell[0] and cell[1] and cell[2] and cell[3] and cell[4] and cell[5]):
                cell_string = " ".join(map(str, cell))
                print(f"Unit cell parameters found in file {cellfile}:")
                print(cell_string)
            else:
                sys.stderr.write(
                    f"WARNING: Unit cell parameters could not be parsed from "
                    f"the file {cellfile}.\n"
                    f"Attempt to find the unit cell parameters found "
                    f"in this file: " + " ".join(map(str, cell)) + "\n")
                cell = None
            return cell, cell_string
        if os.path.isfile(self.container.inputData.CELLFILE.fullPath.__str__()):
            cell, cell_string = get_cell_cellfile(self.container.inputData.CELLFILE.fullPath.__str__())
            self.container.inputParameters.CELL.set(cell_string)
        else:
            # TO DO - ERROR
            pass

    def updateFromReferenceFile(self):
        def get_cs_reference(reference):
            from iotbx import file_reader
            file = file_reader.any_file(reference)
            try:
                cs = file.crystal_symmetry()
                spacegroup = file.crystal_symmetry().space_group().info()
                cell = file.crystal_symmetry().unit_cell().parameters()
                cell_string = " ".join(map(str, cell))
                print("")
                print(f"Symmetry from the reference file {reference}:")
                print(str(cs))
            except NotImplementedError:
                sys.stderr.write(
                    f"WARNING: Symmetry could not be found in the provided "
                    f"reference file {reference}.\n")
                return None, None, None
            return cs, spacegroup, cell_string
        if os.path.isfile(self.container.inputData.REFERENCEFILE.fullPath.__str__()):
            cs, spacegroup, cell_string = get_cs_reference(self.container.inputData.REFERENCEFILE.fullPath.__str__())
            self.container.inputParameters.SPACEGROUP.set(spacegroup)
            self.container.inputParameters.CELL.set(cell_string)
        else:
            # TO DO - ERROR
            pass
