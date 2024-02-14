from setuptools import setup

import versioneer

requirements = []

setup(
    name="jr-dolfin-utils",
    version=versioneer.get_version(),
    cmdclass=versioneer.get_cmdclass(),
    description="Various utilities for legacy dolfin",
    license="MIT",
    author="Jørgen Riseth",
    author_email="jnriseth@gmail.com",
    url="https://github.com/jorgenriseth/jr-dolfin-utils",
    packages=["jr_dolfin_utils"],
    install_requires=requirements,
    keywords="jr-dolfin-utils",
    classifiers=[
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
    ],
)
