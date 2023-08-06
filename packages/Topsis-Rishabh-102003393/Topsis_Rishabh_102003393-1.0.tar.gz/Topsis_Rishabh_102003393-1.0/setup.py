import pathlib
from setuptools import setup

HERE = pathlib.Path(__file__).parent
README = (HERE / "README.md").read_text()
setup(
    name="Topsis_Rishabh_102003393",
    version="1.0",
    description="This a Topsis package,TOPSIS (technique for order performance by similarity to ideal solution) is a useful technique in dealing with multi-attribute or multi-criteria decision making (MADM/MCDM) problems in the real world ",
    long_description=README,
    author="Rishabh Handoo",
    author_email="rhandoo_be20@thapar.edu",
    packages=["topsis"],
    include_package_data=True,
    install_requires=['pandas'],
    entry_points={
        "console_scripts": [
            "topsis=topsis.__main__:main",
        ]
    },
)