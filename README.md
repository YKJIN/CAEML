# [CAEML](https://www.renumics.com/caeml) 

The Computer Aided Engineering Middleware Library (CAEML) is a Python library for building and running simulation workflows. CAEML is developed by [Renumics](http://www.renumics.com) and is currently in early beta state. 

* **Simplicity:** CAEML is intended to offer numerical analysts a Lego-like access to simulation modules. Thanks to a Linux container-based architecture, even complex CAE environments can be installed in minutes. The high-level Python API allows you to get started within hours and enables the migration of your existing workflows within a few days. A customizable data model helps you to quickly integrate your modules such as meshers or solvers. 
* **Scalability:** Whether you are working on your own or you are setting up a CAE environment for a large enterprise - CAEML will adapt to your needs. A scalable simulation data management on top of a NoSQL database is integrated out-of-the-box. The Linux container-based runtime allows the seamless transition to cloud infrastructures. 
* **Community:** Do you feel that you are spending too much time on software integration and scripting? We firmly believe that the CAE community heavily suffers from the re-inventing the wheel syndrome. We also believe that an open source CAE middleware is the right way to tackle this problem. We'd be happy if you support this cause by testing CAEML, by reporting an issue, by publishing your own package or by using CAEML in your awesome product.

If you have any questions, comments or suggestions please [get in touch](info@renumics.com).

## Installation

CAEML needs Python3 as well as a working docker installation. For further information please use the [installation instructions](https://github.com/Renumics/CAEML/wiki/getting-started) on the CAEML wiki.

## Example

CAEML contains numerous example and test cases, please refer to the wiki to [get started](https://github.com/Renumics/CAEML/wiki/getting-started). This workflow adds two numbers to a vector and multiplies the results and gives a first impression on how CAEML works:

```python
import caeml
import settings
import caeml.common.workflow
import caeml.tools
import testproject.tests.base
from caeml.api import workflowBuilder
from caeml.api import workflowRunner

#init systems
caeml.init(settings)

#create workflow and steps
workflow = workflowBuilder.createWorkflow('TestWorkflow')
sumStep1 = workflowBuilder.createToolStep('add', workflow, 'Add0')
sumStep2 = workflowBuilder.createToolStep('add', workflow)
multiplyStep1 = workflowBuilder.createToolStep('multiply', workflow, 'finalMulti')
sumListStep1 = workflowBuilder.createToolStep('addList', workflow)

# connect steps
workflowBuilder.connectPorts(sumListStep1.outputPorts['sum'], sumStep1.inputPorts['addend2'])
workflowBuilder.connectPorts(sumStep1.outputPorts['sum'], sumStep2.inputPorts['addend2'])
workflowBuilder.connectPorts(sumStep2.outputPorts['sum'], multiplyStep1.inputPorts['factor1'])

# set constants
sumListStep1.inputPorts['addends'].fixed_value = [1, 2, 3, 4, 5, 6]
sumStep1.inputPorts['addend1'].fixed_value = 2
sumStep2.inputPorts['addend1'].fixed_value = 100
multiplyStep1.inputPorts['factor2'].fixed_value = 23

#execute workflow
workflowState = workflowRunner.executeAsync(workflow)
result = workflowState.findPortState(multiplyStep1.outputPorts['product']).getEvaluation()
print(result)

```

### License

CAEML is licensed under the Apache License, Version 2.0.
