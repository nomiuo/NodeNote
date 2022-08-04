from setuptools import setup

setup(
    name="smiley",
    packages=["smiley", "tests"],
    python_requires="==3.7.9",
    install_requires=[
        "PySide6==6.2.4",
    ],
    extras_require={"linting": ["pylama", "black"]},
)
