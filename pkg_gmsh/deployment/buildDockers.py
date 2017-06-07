__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import shlex

import yaml

import caeml.common.helper as helper

# Read YAML file
with open("config.yaml", 'r') as stream:
    config = yaml.load(stream)

    images = config['docker_images']

    for image in images:
        path = os.path.abspath(os.path.join(os.path.realpath(__file__), "../../docker_images", images[image]['path']))
        name = images[image]['name']
        repository = images[image]['repository']
        print("Building docker container...")
        if images[image]['cache']:
            commandArgs = shlex.split("docker build -t " + repository + "/" + name + " " + path)
            sts = helper.runFromCommandLineWithConsoleOutput(commandArgs)
        else:
            commandArgs = shlex.split("docker build --no-cache -t " + repository + "/" + name + " " + path)
            sts = helper.runFromCommandLineWithConsoleOutput(commandArgs)

        print("Pushing docker container...")
        commandArgs = shlex.split("docker push " + repository + "/" + name)
        sts = helper.runFromCommandLine(commandArgs)
        print("Image pushed")

print("All images pushed")
