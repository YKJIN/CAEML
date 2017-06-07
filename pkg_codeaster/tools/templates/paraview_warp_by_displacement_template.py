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
# linearstaticrmed.AllArrays = ['TS0/MAIL/ComSup0/RESU____DEPL@@][@@P1', 'TS0/MAIL/ComSup0/RESU____SIEQ_NOEU@@][@@P1', 'TS0/MAIL/ComSup0/RESU____SIGM_NOEU@@][@@P1']
# linearstaticrmed.AllTimeSteps = ['0000']

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [651, 536]

# show data in view
linearstaticrmedDisplay = Show(linearstaticrmed, renderView1)
# trace defaults for the display properties.
linearstaticrmedDisplay.ColorArrayName = [None, '']
linearstaticrmedDisplay.GlyphType = 'Arrow'
linearstaticrmedDisplay.ScalarOpacityUnitDistance = 13.502432893096229

# reset view to fit data
renderView1.ResetCamera()

# Properties modified on renderView1
renderView1.Background = [.8, .8, .85]

# create a new 'Warp By Vector'
warpByVector1 = WarpByVector(Input=linearstaticrmed)
# warpByVector1.Vectors = ['POINTS', 'RESU____DEPL']

# show data in view
warpByVector1Display = Show(warpByVector1, renderView1)
# trace defaults for the display properties.
warpByVector1Display.ColorArrayName = [None, '']
warpByVector1Display.GlyphType = 'Arrow'
warpByVector1Display.ScalarOpacityUnitDistance = 15.22473694135239

# hide data in view
Hide(linearstaticrmed, renderView1)

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [187.31082623634293, -67.5139941615459, 76.6416581617086]
renderView1.CameraFocalPoint = [0.08055849999999953, -0.09561699999999984, 50.0]
renderView1.CameraViewUp = [-0.32334955262215526, -0.940223925638622, -0.10688328436079707]
renderView1.CameraParallelScale = 51.96412826406998

# get active view
renderView1 = GetActiveViewOrCreate('RenderView')
# uncomment following to set a specific view size
# renderView1.ViewSize = [1230, 557]

# export view
ExportView(output_mesh, view=renderView1)

#### uncomment the following to render all views
# RenderAllViews()
# alternatively, if you want to write images, you can use SaveScreenshot(...).
