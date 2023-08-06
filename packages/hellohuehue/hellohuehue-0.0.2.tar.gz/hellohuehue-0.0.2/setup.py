from setuptools import setup, find_packages


VERSION = '0.0.2'
DESCRIPTION = 'Hello Pypi huehue package'

# Setting up
setup(
    name="hellohuehue",
    version=VERSION,
    author="Anant Mishra",
    author_email="amishra_be20@thapar.edu",
    description=DESCRIPTION,
    packages=find_packages(),
    install_requires=[],
    keywords=['python', 'video', 'stream', 'video stream', 'camera stream', 'sockets'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)
