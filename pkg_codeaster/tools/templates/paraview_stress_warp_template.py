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
renderView1.Background = [.8, .8, .85]
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

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(Input=linearstaticrmed)
warpByVector1.Vectors = ['POINTS', 'RESU____DEPL']

# show data in view
warpByVector1Display = Show(warpByVector1, renderView1)
# trace defaults for the display properties.
warpByVector1Display.ColorArrayName = [None, '']
warpByVector1Display.GlyphType = 'Arrow'
warpByVector1Display.ScalarOpacityUnitDistance = 15.22473694135239

# hide data in view
Hide(linearstaticrmed, renderView1)

# set scalar coloring
ColorBy(warpByVector1Display, ('POINTS', 'RESU____SIEQ_NOEU'))

# rescale color and/or opacity maps used to include current data range
warpByVector1Display.RescaleTransferFunctionToDataRange(True)

# show color bar/color legend
warpByVector1Display.SetScalarBarVisibility(renderView1, True)

# get color transfer function/color map for 'RESUSIEQNOEU'
rESUSIEQNOEULUT = GetColorTransferFunction('RESUSIEQNOEU')

# get opacity transfer function/opacity map for 'RESUSIEQNOEU'
rESUSIEQNOEUPWF = GetOpacityTransferFunction('RESUSIEQNOEU')

#### saving camera placements for all active views

# export view
ExportView(output_mesh, view=renderView1)
