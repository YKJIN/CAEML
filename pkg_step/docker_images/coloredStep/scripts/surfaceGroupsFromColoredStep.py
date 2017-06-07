__copyright__ = "Copyright 2017 Renumics GmbH (http://www.renumics.com)"
import os
import yaml

import argparse

from util.StepXcafImporter import StepImporter, logger


def getFaces(path):
    test = StepImporter(path)
    i = 1
    for face in test.faces:
        color = face.color
        # logger.info("Test face  {3} with face color: {0}, {1}, {2}".format(color.red, color.green, color.blue, i))
        logger.info("Test face  {1} with face color order: {0}".format(color.GetOrderValue(), i))
        i = i + 1

    return test.faces


def list_dir(tmpWorkdir):
    if os.path.exists(tmpWorkdir):
        for root, dirs, files in os.walk(tmpWorkdir):
            level = root.replace(tmpWorkdir, '').count(os.sep)
            indent = ' ' * 4 * (level)
            print('{}{}/'.format(indent, os.path.basename(root)))
            subindent = ' ' * 4 * (level + 1)
            for f in files:
                print('{}{}'.format(subindent, f))


if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument("inputStep")
    args = parser.parse_args()

    inputStep = args.inputStep
    logger.info("Input Step File: {}".format(inputStep))

    faces = getFaces(inputStep)
    face_dict = {}
    surfaces = []
    i = 1
    for face in faces:
        surfaces.append(str(i))
        if not face.color.GetOrderValue() in face_dict:
            face_dict[face.color.GetOrderValue()] = [str(i)]  # new list with one item
        else:
            face_dict[face.color.GetOrderValue()].append(str(i))
        i = i + 1

    surface_groups = [{"name": int(255 * key), 'surfaces': group} for key, group in face_dict.items()]
    step = {'surfaceGroups': surface_groups, 'surfaces': surfaces, 'filename': os.path.basename(inputStep)}
    logger.info("Writing yaml file to {}".format(os.path.abspath('/data/stepMeta.yml')))
    with open('/data/stepMeta.yml', 'w') as ymlFile:
        ymlFile.write(yaml.dump(step))
    logger.info("yaml wrote")
