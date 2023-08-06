from setuptools import find_packages, setup
setup(
    name='pyTerminalproccesosx',
    packages=find_packages(include=['mac_terminal', 'linux_terminal', 'info']),
    version='0.1.0',
    description='Hello everyone!This module will help you change brightness, output , connecting'
                ' to wifi-network, bluetooth device.You can use this utility for your python project.',
    author='aaaleX',
    license='MIT',
)