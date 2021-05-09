from setuptools import setup

setup(
    name='PySychonaut',
    version='0.5.1',
    packages=['pysychonaut'],
    url='https://github.com/OpenJarbas/PySychonaut',
    license='apache2.0',
    author='jarbasAI',
    author_email='jarbasai@mailfence.com',
    description='unnoficial erowid, psychonaut wiki and ask_the_caterpillar apis',
    install_requires=["lxml", "beautifulsoup4", "requests"]
)
