from autoytdl.version import __version__
try:
    from setuptools import setup, find_namespace_packages
except ModuleNotFoundError as ex:
    print(ex.msg)
    exit(1)


with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="auto-ytdl",
    version=__version__,
    author="michaelb",
    author_email="michael.bleuez22@gmail.com",
    description="A simple, configurable youtube-dl wrapper to download and manage youtube audio auto download, package-manager style",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/michaelb/auto-ytdl",
    packages=find_namespace_packages(),
    install_requires=['youtube-dlc', 'ffmpeg',
                      'toml', 'pathlib', 'argparse', 'toml', 'music_tag'],
    entry_points={
        'console_scripts': [
            'aytdl = autoytdl.AYTDL:main'
        ]
    },
    include_package_data=True,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GPLv3 License",
        "Operating System :: OS Independent",
        "Environment :: Console",
        "Topic :: Multimedia :: Sound/Audio",
        "License :: OSI Approved :: GPLv3 License"
    ],
    license='GPLv3',
    python_requires='>=3.5',
)
