from distutils.core import setup

setup(
    name='Batch Windows Application Compatability Settings Tool',
    version='1.0',
    packages=['pywin32'],
    url='https://github.com/Robert-McGinley/Batch_Windows_Compatibility_Settings_Tool',
    license='Apache-2.0',
    author='Robert McGinley',
    author_email='robert.mcginley@gmail.com',
    description='Searches for executable files recursively in a given path or the current working directory, of which are then added to the Windows Application Compatibility Settings with "Run as Administrator" and "Windows 7" mode properties. Developed under Windows 8 with Python 2.7.2 32bit'
)
