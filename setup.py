from pathlib import Path
from typing import List

from setuptools import find_packages, setup

HYPEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    """
    This function returns the list of requirements.
    """
    requirements_file = Path(__file__).parent / file_path
    requirements = []

    if requirements_file.exists():
        with requirements_file.open() as file_obj:
            requirements = [line.strip() for line in file_obj.readlines()]

        requirements = [req for req in requirements if req and not req.startswith('#')]

        if HYPEN_E_DOT in requirements:
            requirements.remove(HYPEN_E_DOT)

    return requirements


setup(
    name='mlproject',
    version='0.0.1',
    author='dhiraj',
    author_email='Dhirajhawaldar61@gmail.com',
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt'),
)