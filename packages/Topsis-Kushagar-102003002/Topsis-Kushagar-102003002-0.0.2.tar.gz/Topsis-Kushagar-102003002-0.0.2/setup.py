import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="Topsis-Kushagar-102003002",
    version="0.0.2",
    author="Kushagar Bansal",
    description="It is a package for performing TOPSIS analysis",
    long_description=long_description,
    long_description_content_type="text/markdown",
    license="MIT",
    packages=["Topsis_Kushagar"],
    include_package_data=True,
    install_requires='pandas',
    pythhon_requires='>=3.6',
    entry_points={
        "console_scripts": [
            "topsis=Topsis_Kushagar.102003002:main",
        ]
    },
)