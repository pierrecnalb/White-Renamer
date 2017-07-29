#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os


def make_standard_files(root):
    os.makedirs(root)
    _create_file(root, "file with é è.txt")
    _create_file(root, "file_with_underscore.txt")
    _create_file(root, "file.with.dots.txt")
    _create_file(root, "l'appostrophe.txt")
    folder1 = os.path.join(root, "FOLDER1")
    os.makedirs(folder1)
    _create_file(folder1, "folder1-file1.txt")
    _create_file(folder1, "folder1-sub file #2.txt")
    subfolder1 = os.path.join(folder1, "sub fOlder_1")
    os.makedirs(subfolder1)
    _create_file(subfolder1, "sub file 1.txt")
    _create_file(subfolder1, "sub file 2.txt")


def _create_file(parent, name):
    filename = os.path.join(parent, name)
    with open(filename, 'w+') as file:
        file.writelines(name + '\n')
