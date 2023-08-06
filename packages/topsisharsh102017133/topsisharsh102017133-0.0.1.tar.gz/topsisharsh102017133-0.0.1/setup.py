from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='topsisharsh102017133',
    packages=find_packages(exclude=['tests']),
    version='0.0.1',
    license='MIT',
    description='This is a Python Package implementing TOPSIS',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Harsh garg',
    author_email='hgarg_be20@thapar.edu',
    url='',
    keywords=['topsis', 'mcda', 'TIET'],
    install_requires=[
        'numpy',
        'pandas',
    ],
    entry_points={
        "console_scripts":[
            "topsis=src.__main__:topsiss",
        ]
    },
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
    ],
)