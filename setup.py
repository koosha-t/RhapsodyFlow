import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r") as req:
    external_packages = req.read()

setuptools.setup(
    name = "RhapsodyFlow",
    version = "0.0.1",
    author = "Koosha Tahmasebipour",
    author_email = "kooshi.ml@gmail.com",
    description = "Transforming emotions into captivating melodies. Immerse yourself in a world where the language of music transcends boundaries, as RhapsodyFlow weaves your feelings into enchanting compositions. Embrace the power of expression and let your emotions sing with RhapsodyFlow.",
    long_description = long_description,
    url="",
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    install_requires=external_packages,
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.9",
)