
# File: mkpline.py 
# Author(s): Andrew Williams
# Created: Wed Feb 17 06:44:20 EST 2021 
# Description:
# Acknowledgements:
# Copyright (c) 2021-2022 Carnegie Mellon University
# This code is subject to the license terms contained in the code repo.

import json
import sys,platform
import os,secrets

def createCell(src,ecount = 0):
    newCell = {}
    newCell["cell_type"] = "code" if ecount > 0 else "markdown"
    newCell["id"] = secrets.token_hex(4)
    if ecount > 0:
        newCell["execution_count"] = ecount
        newCell["outputs"] = []
    newCell["metadata"] = {}
    newCell["source"] = src.splitlines(True)
    return newCell


if len(sys.argv) != 3:
    print("Usage: {} <input json> <script name>".format(sys.argv[0]))
    exit(0)

infile = sys.argv[1]
outfile = sys.argv[2]

pipef = None

with open(infile,'r') as rf:
    pipef = json.loads(rf.read())

if not pipef:
    print("Could not read json file: {}!".format(infile))

cells = []

celltext = "Prepare Dependencies"

cells.append(createCell(celltext))

celltext = """# Dependencies
import sys,os,json

# D3M dependencies
from d3m import index, utils
from d3m.metadata.base import ArgumentType,Metadata
from d3m.metadata.pipeline import Pipeline, PrimitiveStep
from d3m.container.dataset import D3MDatasetLoader, Dataset
from d3m.metadata import base as metadata_base, problem"""
    
script = celltext

cells.append(createCell(celltext,1))

evar = os.path.abspath(os.path.join(os.path.dirname( infile ), '..', 'environment_variables.json'))

env_dict = {}

with open(evar,'r') as fp:
    env_dict = json.load(fp)

celltext = (
    f"\noutput_path = \"{env_dict['D3MOUTPUTDIR']}\"\n\n"
    f"volumes_dir = \"{env_dict['D3MSTATICDIR']}\"\n"
    f"dataset_base = \"{env_dict['D3MINPUTDIR']}\"\n"
)

cells.append(createCell(celltext,2))

script += """

if len(sys.argv) != 3:
    print("Usage: {} <output_dir> <output csv>".format(sys.argv[0]))
    exit()

# Get output path
output_path = sys.argv[1]

# Get environment variables
env_dict = {}
for search_dir in os.listdir(output_path):
    search_dir_path = os.path.join(output_path, search_dir)
    filepath = os.path.join(search_dir_path, 'environment_variables.json')

    with open(filepath, 'r') as fp:
        env_dict = json.load(fp)

volumes_dir = env_dict['D3MSTATICDIR']

# Dataset info
dataset_base = env_dict['D3MINPUTDIR']"""

celltext = """

# functions
def prim_arg_find(primitive, method: str) -> set:
        return set(primitive.metadata.query()['primitive_code']['instance_methods'][method]['arguments'])

def get_training_arguments(prim,args):
    tap = prim_arg_find(prim,"set_training_data")
    targs = {}
    for param, value in args.items():
        if param in tap:
            targs[param] = value

    return targs

def get_output_arguments(prim,args):
    oap = prim_arg_find(prim,"produce")
    oargs = {}
    for param, value in args.items():
        if param in oap:
            oargs[param] = value

    return oargs

def get_primitive_volumes(volumes_dir, primitive_class):
    volumes = {}
    for entry in primitive_class.metadata.get_volumes():
        volume_path = os.path.join(volumes_dir, entry['file_digest'])
        volumes[entry['key']] = volume_path
    return volumes

def load_dataset(dBase: str,setName: str):
    uri = 'file://{dataset_uri}'.format(dataset_uri=os.path.abspath(dBase +'/{sn}/dataset_{sn}/datasetDoc.json'.format(sn=setName)))
    loader = D3MDatasetLoader()
    return loader.load(uri)

def add_metadata(dataset,problem_desc):
    for data in problem_desc['inputs']:
        targets = data['targets']
        for target in targets:
            semantic_types = list(dataset.metadata.query((target['resource_id'], metadata_base.ALL_ELEMENTS, target['column_index'])).get('semantic_types', []))
            if 'https://metadata.datadrivendiscovery.org/types/Target' not in semantic_types:
                semantic_types.append('https://metadata.datadrivendiscovery.org/types/Target')
                dataset.metadata = dataset.metadata.update((target['resource_id'], metadata_base.ALL_ELEMENTS, target['column_index']), {'semantic_types': semantic_types})
            if 'https://metadata.datadrivendiscovery.org/types/TrueTarget' not in semantic_types:
                semantic_types.append('https://metadata.datadrivendiscovery.org/types/TrueTarget')
                dataset.metadata = dataset.metadata.update((target['resource_id'], metadata_base.ALL_ELEMENTS, target['column_index']), {'semantic_types': semantic_types})
            dataset.metadata = dataset.metadata.remove_semantic_type((target['resource_id'], 
            metadata_base.ALL_ELEMENTS, target['column_index']),'https://metadata.datadrivendiscovery.org/types/Attribute',)

# Load training dataset
dataset = load_dataset(dataset_base,'TRAIN')

# Load the problem documentation
dataset_problem_loc = '{dataset_uri}'.format(dataset_uri=os.path.abspath(dataset_base +'/TRAIN/problem_TRAIN/problemDoc.json'))
with open(dataset_problem_loc) as file:
        problem_doc = json.load(file)
problem_desc = problem.Problem.load(utils.path_to_uri(dataset_problem_loc))

# Add the problem metadata
add_metadata(dataset,problem_desc)

"""

script += celltext

cells.append(createCell(celltext,3))

prims = []

celltext = """
# Load Primitives

"""

for step in pipef['steps']:
    prim = {}
    modpath = step['primitive']['python_path'].split('.')
    prim['module'] = '.'.join(modpath[:-1])
    prim['class'] = modpath[-1]
    prim['iname'] = ''.join([x.capitalize() for x in modpath[-2].split('_')]) + 'Primitive'
    prims.append(prim)

# now write the primitive loaders

for prim in prims:
    celltext += 'from ' + prim['module'] + ' import ' + prim['class'] + ' as ' + prim['iname'] + '\n'

cells.append(createCell(celltext,4))
    
script += celltext
    
celltext = """

# Models for solving
models = []

# Build the primitive steps

steps = []

"""

script += celltext

cells.append(createCell(celltext,5))

ecounter = 6

for idx, step in enumerate(pipef['steps']):
    pname = ''.join([x.capitalize() for x in step['primitive']['python_path'].split('.')[-2].split('_')])
    celltext = '# Step #{}: {}\n'.format(idx,pname)

    celltext += 'step = {}\n'
    
    pargs = {}
    # Add arguments
    for arg,val in step['arguments'].items():
        pargs[arg] = val['data']

    celltext += "step['args'] = {}\n".format(str(pargs))
        
    # Add hyperparameters
    chparms = {}
    if 'hyperparams' in step:
        for key,val in step['hyperparams'].items():
            chparms[key] = val['data']

    # Set up the model
    celltext += 'custom_hyper = {}\n'.format(str(chparms))
    celltext += 'prim_hypers = {}Primitive.metadata.query()["primitive_code"]["class_type_arguments"]["Hyperparams"]\n'.format(pname)
    celltext += 'primitive = {}Primitive\n'.format(pname)
    
    celltext += """
method_arguments = primitive.metadata.query()['primitive_code'].get('instance_methods', {}).get('__init__', {}).get('arguments', [])
if 'volumes' in method_arguments:
    volumes = get_primitive_volumes(volumes_dir, primitive)
    model = primitive(volumes=volumes, hyperparams=prim_hypers(prim_hypers.defaults(), **custom_hyper))
else:
    model = primitive(hyperparams=prim_hypers(prim_hypers.defaults(), **custom_hyper))
"""
    celltext += "step['model'] = model #{}Primitive(hyperparams=prim_hypers(prim_hypers.defaults(),**custom_hyper))\n".format(pname)
    celltext += "step['training_args'] = get_training_arguments({}Primitive,step['args'])\n".format(pname)
    celltext += "step['output_args'] = get_output_arguments({}Primitive,step['args'])\n".format(pname)
    celltext += "step['name'] = '{}'\n".format(pname)
    celltext += "step['outputs'] = {}\n"
    celltext += "steps.append(step)\n\n"
    script += celltext
    cells.append(createCell(celltext,ecounter))
    ecounter += 1


celltext = """
# Now build the json and train the models
outputs = {}
out = dataset

"""

# Build inputs
for inum,inp in enumerate(pipef['inputs']):
    celltext += "outputs['inputs.{}'] = out\n".format(inum)    
    
celltext += '\n'

script += celltext

cells.append(createCell(celltext,ecounter))
ecounter += 1

celltext = """
# Train models
for idx, step in enumerate(steps):

    # Get output arguments
    for key,val in step['output_args'].items():
        step['outputs'][key] = outputs[val]

    # Train model
    if step['training_args']:
        for key,val in step['training_args'].items():
            step['training_args'][key] = outputs[val]
        step['model'].set_training_data(**step['training_args'])
        step['model'].fit()
        print("Fit model for {} Primitive".format(step['name']))
        
    print("Producing for: {}".format(step['name']))
    out = step['model'].produce(**step['outputs']).value
    outputs['steps.{}.produce'.format(idx)] = out

"""

cells.append(createCell(celltext,ecounter))
ecounter += 1

script += celltext

script += 'print("\\nRUNNING TESTS\\n\\n")\n'

celltext ="""
# Load testing dataset
dataset = load_dataset(dataset_base,'TEST')

# Add problem metadata
add_metadata(dataset,problem_desc)

out = dataset
"""

celltext += 'outputs = {}\n'

for inum,inp in enumerate(pipef['inputs']):
    celltext += "outputs['inputs.{}'] = out\n".format(inum)

script += celltext

cells.append(createCell(celltext,ecounter))
ecounter += 1

celltext = """
# Test models
for idx, step in enumerate(steps):

    # Get output arguments
    for key,val in step['output_args'].items():
        step['outputs'][key] = outputs[val]

    print("Producing for: {}".format(step['name']))
    out = step['model'].produce(**step['outputs']).value
    outputs['steps.{}.produce'.format(idx)] = out

"""
script += celltext

cells.append(createCell(celltext,ecounter))
ecounter += 1

script += """
# Write output
out.to_csv(sys.argv[2])
"""

with open(outfile,'w') as f:
    f.write(script)

jsonout = {}

jsonout["cells"] = cells

# set the Notebook metadata
mdata = {}

kspec = {"display_name": "Python 3 (ipykernel)",
   "language": "python",
   "name": "python3"}
linfo = {
   "codemirror_mode": {
    "name": "ipython",
    "version": 3
   },
    "file_extension": ".py",
    "mimetype": "text/x-python",
    "name": "python",
    "nbconvert_exporter": "python",
    "pygments_lexer": "ipython3"
}
linfo["version"] = platform.python_version()
mdata["kernelspec"] = kspec
mdata["language_info"] = linfo
jsonout["nbformat"] = 4
jsonout["nbformat_minor"] = 5

jsonout["metadata"] = mdata

with open(outfile + '.ipynb', 'w', encoding='utf-8') as f:
    json.dump(jsonout, f, ensure_ascii=False, indent=1)
