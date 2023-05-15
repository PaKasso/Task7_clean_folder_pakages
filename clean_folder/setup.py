from setuptools import setup

setup(
    name='clean-folder',
    version='1.0',
    author='PavloV_PaKasso',
    author_email='your_email@example.com',
    description='Clean folder script',
    packages=['clean_folder'],
    entry_points={
        'console_scripts': ['clean-folder=clean_folder.clean:main']
    },
)