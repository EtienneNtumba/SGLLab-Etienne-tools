from setuptools import setup, find_packages

setup(
    name='SGLLab-Etienne-tools',
    version='1.0.0',
    author='Etienne Kabongo Ntumba',
    author_email='etienne.kabongo@mail.com',
    description='Tools for comparing and masking aligned microbial genomes',
    long_description=open('README.md').read(),
    long_description_content_type='text/markdown',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'biopython'
    ],
    entry_points={
        'console_scripts': [
            'sgllab-diff=SGLLabEtienne.aligned_genomes_diff_same_region:main',
            'sgllab-mask=SGLLabEtienne.mask_differences:main',
            'sgllab-count=SGLLabEtienne.count_scenarios_from_table:main',
            'sgllab-merge=SGLLabEtienne.merge_scenario_count:main',
        ]
    },
    classifiers=[
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.7',
)
