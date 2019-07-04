__version__ = '0.1.1'

import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cctvproxy",
    version=__version__,
    author='Sergei S.',
    author_email="s@makeitwork.cz",
    description="CCTV camera image proxy",
    long_description=long_description,
    long_description_content_type='text/markdown',
    url="https://github.com/divi255/cctvproxy",
    packages=setuptools.find_packages(),
    license='MIT',
    install_requires=['requests', 'cherrypy', 'pyyaml'],
    scripts=['cctv-proxy.sh'],
    include_package_data=True,
    classifiers=(
        'Programming Language :: Python :: 3',
        'License :: OSI Approved :: MIT License',
        'Topic :: Communications',
    ),
)
