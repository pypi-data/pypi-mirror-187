from setuptools import setup, find_packages

VERSION = '0.0.2'
DESCRIPTION = 'Safaricom Q-OPS Automation tracker '

# Setting up
setup(
    name="q-ops-tracker_safaricom",
    version=VERSION,
    author="Justus Mwangi Gitari (j_siri)",
    author_email="mwangijustus12@gmail.com",
    license='MIT',
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    #long_description=open('README.txt').read() + '\n\n'+open('CHANGELOG.txt').read(),
    packages=find_packages(),
    install_requires=['requests', 'robotframework'],
    keywords=['python', 'q-ops', 'safaricom', 'quality ops', 'quality engineering', 'tracker'],
    classifiers=[
        "Development Status :: 5 - Production/Stable",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3",
        "Operating System :: Unix",
        "Operating System :: MacOS :: MacOS X",
        "Operating System :: Microsoft :: Windows",
    ]
)