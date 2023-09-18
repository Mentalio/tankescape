from setuptools import setup
import os
import shutil

APP = ['main.py']

LEVELS_FILES = [('levels', [f'levels/{i}.json' for i in range(0, 16)])]
ASSETS = [('assets', [f'assets/{file_name}' for file_name in os.listdir('assets') if os.path.isfile(f'assets/{file_name}')])]
ASSETS_MISC = ['save.json']

DATA_FILES = LEVELS_FILES + ASSETS + ASSETS_MISC

OPTIONS = {
    'iconfile': 'tank_escape.icns'
}

setup(
    app=APP,
    name='Tank Escape',
    data_files=DATA_FILES,
    options={'py2app': OPTIONS},
    setup_requires=['py2app'],
    version='1.0',
    description='Sneak your way through the facility to retrieve the data and win the war',
    author='Mentalio',
    author_email='maxim@stankiewicz.id.au'
)

current_path = os.path.dirname(os.path.abspath(__file__))

destination_dir = os.path.abspath(os.path.join(current_path, "dist/Tank Escape.app"))

shutil.rmtree('build')
shutil.move(destination_dir, current_path)
shutil.rmtree('dist')