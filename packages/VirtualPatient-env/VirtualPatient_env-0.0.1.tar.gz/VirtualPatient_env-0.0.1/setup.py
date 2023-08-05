import setuptools
from pathlib import Path

setuptools.setup(
    name='VirtualPatient_env',
    version='0.0.1',
    description="A Gym Env for 'VirtualPatient' project",
    long_description=Path("README.md").read_text(),
    long_description_content_type="text/markdown",
    packages=setuptools.find_packages(include="VirtualPatient_env*"),
    install_requires=['gym']
)