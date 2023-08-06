from setuptools import setup, find_packages

setup(
    name="terka",
    version="0.0.1",
    packages=find_packages(),
    install_requires=[
        "sqlalchemy", "pyaml", "rich"
    ],
    setup_requires=["pytest-runner"],
    tests_requires=["pytest"],
    entry_points={
        "console_scripts": [
            "terka=src.cli.main:main"
        ]
    }
)
