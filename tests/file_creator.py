#!/usr/bin/python3
# -*- coding: utf-8 -*-

import os


class FileTestCreator(object):

    def create(self):
        root = "TestCase"
        os.makedirs(root)
        self.create_file(root, "file with é è.txt")
        self.create_file(root, "file_with_underscore.txt")
        self.create_file(root, "file.with.dots.txt")
        self.create_file(root, "l'appostrophe.txt")

        folder1 = os.path.join(root, "FOLDER1")
        os.makedirs(folder1)
        self.create_file(folder1, "folder1-file1.txt")
        self.create_file(folder1, "folder1-sub file #2.txt")

        subfolder1 = os.path.join(folder1, "sub fOlder_1")
        os.makedirs(subfolder1)
        self.create_file(subfolder1, "sub file 1.txt")
        self.create_file(subfolder1, "sub file 2.txt")

    def create_file(self, parent, name):
        directory = os.path.join(parent, name)
        file = open(directory, 'w+')
        file.writelines(name + '\n')
        file.close()

if __name__ == '__main__':
    FileTestCreator().create()
