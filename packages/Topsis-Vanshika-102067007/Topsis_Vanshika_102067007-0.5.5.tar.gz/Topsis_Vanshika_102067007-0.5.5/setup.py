import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="Topsis_Vanshika_102067007",
    version="0.5.5",
    description="This a Topsis package.",
    long_description=README,
    url="",
    author="Vanshika Gupta",
    author_email="vgupta4_be20@thapar.edu",
    packages=["topsis"],
    include_package_data=True,
    install_requires=['pandas','numpy'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)