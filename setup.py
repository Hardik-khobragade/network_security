from setuptools import find_packages,setup
from typing import List


def get_requirements()-> List[str]:
    requirement_lst=[]
    requirement=''
    try: 
        with open('requirements.txt') as file:
            lines=file.readlines()
            for line in lines:
                requirement=line.strip()
                    
                if requirement and requirement!= "-e .":
                    requirement_lst.append(requirement)
                
    except FileNotFoundError:
        print("requirement.txt not found")
        
    return requirement_lst

print(get_requirements())


setup(
    name="networksecurity",
    version="0.1.0",
    author="Hardik Khobragade",
    author_email="hardikkhobragade78@gmail.com",
    packages=find_packages(),
    install_requires=get_requirements(),
)