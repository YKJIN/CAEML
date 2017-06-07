__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
#### import the simple module from the paraview

from paraview.simple import *

# get arguments from command line
input_mesh = '{{input_mesh}}'
output_mesh = '/data/output.x3d'

#### disable automatic camera reset on 'Show'
paraview.simple._DisableFirstRenderCameraReset()

# create a new 'MED Reader'
linearstaticrmed = MEDReader(FileName=input_mesh)
linearstaticrmed.AllArrays = ['TS0/MAIL/ComSup0/RESU____DEPL@@][@@P1', 'TS0/MAIL/ComSup0/RESU____SIEQ_NOEU@@][@@P1',
                              'TS0/MAIL/ComSup0/RESU____SIGM_NOEU@@][@@P1']
linearstaticrmed.AllTimeSteps = ['0000']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1419, 857]

# show data in view
linearstaticrmedDisplay = Show(linearstaticrmed, renderView1)
# trace defaults for the display properties.
linearstaticrmedDisplay.ColorArrayName = [None, '']
linearstaticrmedDisplay.GlyphType = 'Arrow'
linearstaticrmedDisplay.ScalarOpacityUnitDistance = 13.502432893096229

# reset view to fit data
renderView1.ResetCamera()

# create a new 'Extract Cells By Region'
extractCellsByRegion1 = ExtractCellsByRegion(Input=linearstaticrmed)
extractCellsByRegion1.IntersectWith = 'Plane'

# init the 'Plane' selected for 'IntersectWith'
extractCellsByRegion1.IntersectWith.Origin = [0.08055849999999953, -0.09561699999999984, 50.0]

# Properties modified on extractCellsByRegion1.IntersectWith
extractCellsByRegion1.IntersectWith.Origin = [0.0805584999999995, -0.0956169999999998, 50.0]

# Properties modified on extractCellsByRegion1.IntersectWith
extractCellsByRegion1.IntersectWith.Origin = [0.0805584999999995, -0.0956169999999998, 50.0]

# show data in view
extractCellsByRegion1Display = Show(extractCellsByRegion1, renderView1)
# trace defaults for the display properties.
extractCellsByRegion1Display.ColorArrayName = [None, '']
extractCellsByRegion1Display.GlyphType = 'Arrow'
extractCellsByRegion1Display.ScalarOpacityUnitDistance = 20.282245895943433

# hide data in view
Hide(linearstaticrmed, renderView1)

# change solid color
extractCellsByRegion1Display.DiffuseColor = [0.3333333333333333, 0.6666666666666666, 1.0]

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [178.45414098651304, -43.00158652773645, -31.560600384844772]
renderView1.CameraFocalPoint = [0.08055849999999036, -0.09561700000000196, 50.000000000000014]
renderView1.CameraViewUp = [-0.19803649140474777, -0.9768601570729392, 0.08078230991702263]
renderView1.CameraParallelScale = 51.96412826406998
renderView1.Background = [.8, .8, .85]

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).

# export view
ExportView(output_mesh, view=renderView1)
