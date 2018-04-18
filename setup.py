from setuptools import setup

setup(
    name='py_erowid',
    version='0.2',
    packages=['pyerowid'],
    url='https://github.com/JarbasAl/py_erowid',
    license='MIT',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='unnoficial erowid api',
    install_requires=["lxml", "bs4"]
)
