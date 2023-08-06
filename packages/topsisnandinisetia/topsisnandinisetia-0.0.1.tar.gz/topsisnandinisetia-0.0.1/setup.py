from setuptools import setup, find_packages


def readme():
    with open('README.md') as f:
        README = f.read()
    return README


setup(
    name='topsisnandinisetia',
    packages=find_packages(exclude=['tests']),
    version='0.0.1',
    license='MIT',
    description='This is a Python Package implementing TOPSIS',
    long_description=readme(),
    long_description_content_type='text/markdown',
    author='Nandini Setia',
    author_email='nandinisetia003@gmail.com',
    url='https://github.com/nandinisetia/topsis',
    keywords=['topsis', 'mcda', 'TIET'],
    install_requires=[
        'numpy',
        'pandas',
    ],
    include_package_data=True,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
    ],
)