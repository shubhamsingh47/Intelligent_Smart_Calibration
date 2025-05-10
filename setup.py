from setuptools import find_packages, setup
from typing import List

HYPHEN_E_DOT = '-e .'


def get_requirements(file_path: str) -> List[str]:
    requirements = []
    with open(file_path) as file_object:
        requirements = file_object.readlines()
        requirements = [require.replace("\n", "") for require in requirements]

        if HYPHEN_E_DOT in requirements:
            requirements.remove(HYPHEN_E_DOT)

    return requirements


setup(
    name="Intelligent_calibration",
    version="0.0.1",
    author="Shubham Singh",
    author_email="shubham47047@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements('requirements.txt')

)
