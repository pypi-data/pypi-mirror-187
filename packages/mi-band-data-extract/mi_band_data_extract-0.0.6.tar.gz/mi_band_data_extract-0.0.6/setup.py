import setuptools

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

__version__ = "0.0.6"

REPO_NAME = "mi-band-data-extract"
AUTHOR_USER_NAME =  "SurajpratapsinghSayar"
SRC_REPO = "mi_band_data_extract"
AUTHOR_EMAIL = "sunnysayar@outlook.com"

setuptools.setup(
    name=SRC_REPO,
    version=__version__,
    author=AUTHOR_USER_NAME,
    author_email=AUTHOR_EMAIL,
    description="Package to extract data from Mi Band data files.",
    long_description=long_description,
    long_description_content = "text/md",
    url=f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}",
    project_urls={
        "Bug Tracker": f"https://github.com/{AUTHOR_USER_NAME}/{REPO_NAME}/issues"
    },
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src")
)
