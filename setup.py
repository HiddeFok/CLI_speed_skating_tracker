from setuptools import setup


# TODO: add description, dependencies, etc
setup(
    entry_points={
        "console_scripts": [
            "SkateTracker = src.main:main"
        ]
    }
)