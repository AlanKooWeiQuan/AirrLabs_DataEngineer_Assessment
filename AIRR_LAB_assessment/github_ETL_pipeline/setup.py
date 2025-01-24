from setuptools import find_packages, setup

setup(
    name="github_ETL_pipeline",
    packages=find_packages(exclude=["github_ETL_pipeline_tests"]),
    install_requires=[
        "dagster",
        "dagster-cloud"
    ],
    extras_require={"dev": ["dagster-webserver", "pytest"]},
)
