from setuptools import setup

with open("README.md", "r") as rea:
    readme = rea.read()

setup(name='dataway',
    version='0.0.2',
    license='MIT License',
    author='Anselmo Oliveira',
    long_description=readme,
    long_description_content_type="text/markdown",
    author_email='anselmo.oliveira@dataway.info',
    keywords='analytics dataway atlas',
    description=u'Biblioteca para de apoio para realização de webscraping em tabelas',
    packages=['dataway'],
    install_requires= ['requests', 'Pandas'],)
