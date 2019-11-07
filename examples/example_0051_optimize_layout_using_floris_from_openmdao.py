#
# Copyright 2019 NREL
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may not use
# this file except in compliance with the License. You may obtain a copy of the
# License at http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software distributed
# under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
# CONDITIONS OF ANY KIND, either express or implied. See the License for the
# specific language governing permissions and limitations under the License.
#

# Try out calling floris from OpenMDAO

import numpy as np
import floris.tools as wfct
import openmdao.api as om

# Initialize the FLORIS OpenMDAO interface
fi = wfct.floris_utilities.FlorisInterface("example_input.json", mode='python', openmdao=True)

# get OpenMDAO component
FlorisComponent = fi._floris_openMDAO()

# set up OpenMDAO problem
prob = om.Problem()

# set up indep var comp for optimization design variables
indeps = prob.model.add_subsystem('indeps', om.IndepVarComp(), promotes=['*'])
indeps.add_output('turbineX', fi.layout_x, units='m')
indeps.add_output('turbineY', fi.layout_y, units='m')

# add floris to the OpenMDAO problem
prob.model.add_subsystem('floris', FlorisComponent(fi=fi), promotes=['*'])

# set up objective component
obj_comp = om.ExecComp('obj = -AEP')
prob.model.add_subsystem('obj_comp', obj_comp, promotes=['obj', 'AEP'])

# setup the optimizer
prob.driver = om.ScipyOptimizeDriver()
prob.driver.options['optimizer'] = 'SLSQP'
prob.driver.options['tol'] = 1e-6

# set up design variable
prob.model.add_design_var('turbineX', lower=np.min(fi.layout_x-100), upper=np.max(fi.layout_x+100))
prob.model.add_design_var('turbineY', lower=np.min(fi.layout_y-100), upper=np.max(fi.layout_y+100))
prob.model.add_objective('obj', scaler=1E-10)

# Ask OpenMDAO to finite-difference across the model to compute the gradients for the optimizer
prob.model.approx_totals()

# setup model
prob.setup()

# define wind rose information
prob['wind_direction'] = 270.
prob['wind_frequency'] = 1.
prob['wind_speed'] = 8.0

# get initial aep value
prob.run_model()
aep_init = np.copy(prob['AEP'])

# run optimization problem
prob.run_driver()

# Print AEP
print('Initial AEP: ', aep_init)
print('Final AEP : ', prob['AEP'])
print('Percent improvement: ', 100.*((prob['AEP']/aep_init)-1.))
