from setuptools import find_packages, setup

setup(
    name='edabox',
    version='1.0.1.2',
    description='Python Library to Gain Insight into Datasets',
    author='Poushali Mukherjee',
    license='MIT',
    url='https://github.com/poushalimukherjee/edabox',
    packages=find_packages(),
    install_requires=['pandas','colorama', 'matplotlib', 'seaborn'],
    setup_requires=['pytest-runner'],
    tests_require=['pytest'],
    test_suite='tests'
)