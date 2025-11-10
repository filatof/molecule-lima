"""Setup for molecule-lima.
"""

from setuptools import setup, find_packages
import os

# Read version from __init__.py
here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, "src", "molecule_lima", "__init__.py"), "r", encoding="utf-8") as f:
    for line in f:
        if line.startswith("__version__"):
            about["__version__"] = line.split('"')[1]
            break

# Read long description from README
with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="molecule-lima",
    version=about["__version__"],
    author="Ivan Filatof",
    author_email="filatof@gmail.com",
    description="Molecule driver for Lima VM",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/filatof/molecule-lima",
    project_urls={
        "Bug Tracker": "https://github.com/filatof/molecule-lima/issues",
        "Source": "https://github.com/filatof/molecule-lima",
        "Documentation": "https://github.com/filatof/molecule-lima#readme",
        "Changelog": "https://github.com/filatof/molecule-lima/blob/main/CHANGELOG.md",
    },
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    package_data={
        "molecule_lima": [
            "playbooks/*.yml",
            "playbooks/common/*.yml",
        ],
    },
    include_package_data=True,
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Programming Language :: Python :: 3.13",
        "Topic :: Software Development :: Testing",
        "Topic :: System :: Systems Administration",
        "Framework :: Ansible",
        "Framework :: Pytest",
    ],
    keywords=[
        "molecule",
        "proxmox",
        "lxc",
        "containers",
        "ansible",
        "testing",
        "infrastructure",
    ],
    python_requires=">=3.8",
    install_requires=[
        "molecule>=6.0.0",
        "ansible-core>=2.12",
        "proxmoxer>=2.0.0",
        "requests>=2.20.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "pylint>=2.17.0",
            "mypy>=1.0.0",
            "tox>=4.0.0",
        ],
        "test": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "pytest-mock>=3.10.0",
        ],
    },
    entry_points={
        "molecule.driver": [
            "molecule-lima = molecule_lima.driver:Lima",
        ],
    },
    zip_safe=False,
)