import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="HealthCheck_Pinger",
    version="0.0.3",
    author="Gregorek85",
    author_email="grerad@gmail.com",
    description="easily ping HealthCheck server",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Gregorek85/HealthCheck_Pinger",
    project_urls={
        "Bug Tracker": "https://github.com/Gregorek85/HealthCheck_Pinger/issues"
    },
    license="MIT",
    packages=["HealthCheck_Pinger"],
)
