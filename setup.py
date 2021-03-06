"""Setup configuration."""
import setuptools

with open("README.md", "r") as fh:
    LONG = fh.read()
setuptools.setup(
    name="pyhassbian",
    version="0.2.2",
    author="Joakim Sorensen",
    author_email="ludeeus@gmail.com",
    description="",
    long_description=LONG,
    long_description_content_type="text/markdown",
    install_requires=['aiohttp', 'requests', 'click', 'aiohttp-basicauth'],
    url="https://github.com/ludeeus/pyhassbian",
    packages=setuptools.find_packages(),
    package_data={'': ['./static/*']},
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
    entry_points={
        'console_scripts': [
            'pyhassbian = pyhassbian.cli:cli'
        ]
    }
)
