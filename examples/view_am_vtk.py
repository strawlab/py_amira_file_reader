import py_amira_file_reader.read_amira as read_amira
import numpy as np

import vtk
import argparse

def show_file(fname,gpu=False):
    data = read_amira.read_amira( fname )
    dlist = data['data']
    merged = {}
    for row in dlist:
        merged.update(row)
    buf = merged['data']
    arr = np.fromstring( buf, dtype=np.uint8 )
    os = merged['define']['Lattice']
    arr.shape = os[2], os[1], os[0]
    arr = np.swapaxes(arr, 0, 2)

    if 1:
        id2name = {}
        id2color = {}
        tdict = merged['Parameters']['Materials']
        for name in tdict:
            namedict=tdict[name]
            this_id = namedict['Id']
            id2name[this_id] = name
            id2color[this_id] = namedict.get('Color',[1.0,1.0,1.0])
        dictRGB= id2color

    if 1:
        # from http://www.vtk.org/Wiki/VTK/Examples/Python/vtkWithNumpy

        # For VTK to be able to use the data, it must be stored as a VTK-image. This can be done by the vtkImageImport-class which
        # imports raw data and stores it.
        dataImporter = vtk.vtkImageImport()
        # The preaviusly created array is converted to a string of chars and imported.
        data_string = arr.tostring()
        dataImporter.CopyImportVoidPointer(data_string, len(data_string))
        # The type of the newly imported data is set to unsigned char (uint8)
        dataImporter.SetDataScalarTypeToUnsignedChar()
        # Because the data that is imported only contains an intensity value (it isnt RGB-coded or someting similar), the importer
        # must be told this is the case.
        dataImporter.SetNumberOfScalarComponents(1)

        dataImporter.SetDataExtent (0, os[2]-1, 0, os[1]-1, 0, os[0]-1)
        dataImporter.SetWholeExtent(0, os[2]-1, 0, os[1]-1, 0, os[0]-1)

    if 1:
        # from https://pyscience.wordpress.com/2014/11/16/volume-rendering-with-python-and-vtk/

        # Opacity of the different volumes (between 0.0 and 1.0)
        volOpacityDef = 0.25

        if 1:
            funcColor = vtk.vtkColorTransferFunction()

            for idx in id2color.keys():
                funcColor.AddRGBPoint(idx,
                                      id2color[idx][0],
                                      id2color[idx][1],
                                      id2color[idx][2])

        if 1:
            funcOpacityScalar = vtk.vtkPiecewiseFunction()

            for idx in dictRGB.keys():
                funcOpacityScalar.AddPoint(idx, volOpacityDef if idx!=0 else 0.0)


        if 1:
            funcOpacityGradient = vtk.vtkPiecewiseFunction()

            funcOpacityGradient.AddPoint(1,   0.0)
            funcOpacityGradient.AddPoint(5,   0.1)
            funcOpacityGradient.AddPoint(100,   1.0)

        if 1:
            propVolume = vtk.vtkVolumeProperty()
            propVolume.ShadeOff()
            propVolume.SetColor(funcColor)
            propVolume.SetScalarOpacity(funcOpacityScalar)
            propVolume.SetGradientOpacity(funcOpacityGradient)
            propVolume.SetInterpolationTypeToLinear()

        if 1:
            if not gpu:
                funcRayCast = vtk.vtkVolumeRayCastCompositeFunction()
                funcRayCast.SetCompositeMethodToClassifyFirst()

                mapperVolume = vtk.vtkVolumeRayCastMapper()
                mapperVolume.SetVolumeRayCastFunction(funcRayCast)
            else:
                mapperVolume = vtk.vtkGPUVolumeRayCastMapper()
                mapperVolume.SetBlendModeToMaximumIntensity();
                mapperVolume.SetSampleDistance(0.1)
                mapperVolume.SetAutoAdjustSampleDistances(0)

            mapperVolume.SetInputConnection(dataImporter.GetOutputPort())

            actorVolume = vtk.vtkVolume()
            actorVolume.SetMapper(mapperVolume)
            actorVolume.SetProperty(propVolume)

    if 1:
        # most from http://www.vtk.org/Wiki/VTK/Examples/Python/vtkWithNumpy

        renderer = vtk.vtkRenderer()
        renderWin = vtk.vtkRenderWindow()
        renderWin.AddRenderer(renderer)

        renderInteractor = vtk.vtkRenderWindowInteractor()
        renderInteractor.SetRenderWindow(renderWin)

        renderer.AddActor(actorVolume)
        renderer.SetBackground(0,0,0)
        renderWin.SetSize(800, 600)

        renderInteractor.Initialize()
        # Because nothing will be rendered without any input, we order the first render manually before control is handed over to the main-loop.
        renderWin.Render()
        renderInteractor.Start()

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('FILE', type=str, help='The file to show')
    parser.add_argument(
        '--gpu', action='store_true', default=False,
        help='use GPU rendering',)
    args = parser.parse_args()
    show_file(args.FILE,gpu=args.gpu)

if __name__=='__main__':
    main()
