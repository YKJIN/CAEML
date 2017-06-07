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
# get active view
renderView1 = GetActiveViewOrCreate('RenderView')

# Properties modified on renderView1
renderView1.Background = [.8, .8, .85]

# get active source.
linearstaticrmed = GetActiveSource()

# get display properties
linearstaticrmedDisplay = GetDisplayProperties(linearstaticrmed, view=renderView1)

# change representation type
linearstaticrmedDisplay.SetRepresentationType('Surface With Edges')

#### saving camera placements for all active views

# current camera placement for renderView1
renderView1.CameraPosition = [69.00427232320222, 186.6726632332498, 23.97463051452144]
renderView1.CameraFocalPoint = [0.08055850000001052, -0.0956169999999718, 49.99999999999985]
renderView1.CameraViewUp = [0.938964144124796, -0.3431889275346425, 0.023826373320573736]
renderView1.CameraParallelScale = 51.96412826406998

# export view
ExportView(output_mesh, view=renderView1)
