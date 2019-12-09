import setuptools

meta = {}

with open("README.md", "r") as fh:
    long_description = fh.read()

with open("rancher_config_volume/version.py") as f:
    exec(f.read(), meta)

requires = [
    "requests>=2.21.0"
]

setuptools.setup(
    name="rancher-config-volume",
    version=meta["__version__"],
    author="Shawn Seymour",
    author_email="shawn@devshawn.com",
    description="Provide a generic configuration file via the Rancher metadata API.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/devshawn/rancher-config-volume",
    license="Apache License 2.0",
    packages=["rancher_config_volume"],
    install_requires=requires,
    entry_points={
        "console_scripts": ["rancher-config-volume=rancher_config_volume.generate:main"],
    },
    keywords=("rancher", "docker", "config", "volume", "compose"),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
        "Natural Language :: English",
        "Operating System :: MacOS",
        "Operating System :: Unix",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
)
