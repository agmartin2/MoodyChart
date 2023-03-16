from setuptools import setup

setup(
    name='MoodyChart',
    version='1.0',
    description='Plotting Moody charts',
    author='Agustin Martin Domingo',
    author_email='agustin6martin@gmail.com',
    url="https://gitlab.com/agmartin/MoodyChart",
    py_modules=['MoodyChart'],  # would be the same as name
    license="LGPL-3",
    install_requires=['matplotlib', 'numpy'], #external packages acting as dependencies
)
