import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="youtube-split",
    version="0.0.1",
    author="William O'Rosky",
    author_email="williamorosky@gmail.com",
    description="Speaker diarization with text metadata on YouTube videos for up to 3 separate speakers.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/williamorosky/youtube-split",
    project_urls={
        "Bug Tracker": "https://github.com/pypa/sampleproject/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    python_requires=">=3.6",
)
