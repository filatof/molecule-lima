from setuptools import setup, find_packages

setup(
    name='molecule-lima',
    version='0.0.1',
    description='Lima driver for Molecule',
    author='Ivan Filatof',
    author_email='filatof@gmail.com',
    url='https://github.com/filatof/molecule-lima',
    packages=find_packages(),
    install_requires=[
        'molecule>=6.0.0',
        'ansible-core>=2.12',
        'pyyaml',
    ],
    entry_points={
        'molecule.driver': [
            'molecule-lima = molecule_lima.driver:Lima',
        ],
    },
    package_data={
        'molecule_lima': [
            'playbooks/*.yml',
            'cookiecutter/**/*',
        ],
    },
    include_package_data=True,
    license='MIT',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9',
        'Programming Language :: Python :: 3.10',
        'Programming Language :: Python :: 3.11',
    ],
    python_requires='>=3.8',
)