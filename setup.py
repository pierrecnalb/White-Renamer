import sys
from setuptools import setup
import whiterenamer

if sys.version_info.major < 3:
    print('This package is compatible with Python 3 and above.')
    exit(4)

setup(
    name = "whiterenamer",
    version = whiterenamer.__version__,
    description = "User friendly batch renamer",
    author = "Pierre Blanc",
    author_email = "pierrecnalb@mailbox.org",
    url = 'https://github.com/pierrecnalb/White-Renamer',
    license='GNU Public General License',
    packages = ['whiterenamer', 'whiterenamer.ui', 'whiterenamer.model', 'whiterenamer.doc'],
    zip_safe = False,
    entry_points={ 'console_scripts': [ 'whiterenamer = whiterenamer:start', ] },
    include_package_data = True,
    #data_file = [('usr/share/applications/', ['whiterenamer.desktop']),
    #             ('usr/share/menu/', ['whiterenamer']),
    #             ('usr/share/pixmaps/', ['whiterenamer.png']),
    #             ('usr/share/pixmaps/', ['whiterenamer.xpm'])],
    #test_suite="nose.collector",
    #tests_require="nose",
    keywords='batch renamer gui simple exif photo music metadata',
    install_requires=['mutagen', 'exifread'],
)
