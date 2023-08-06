from setuptools import setup, find_packages

setup(
    name="MDbrew",
    version="2.0.13",
    author="Knu",
    author_email="rlaalsdn753@korea.ac.kr",
    url="https://github.com/MyKnu/MDbrew",
    download_url="https://github.com/MyKnu/MDbrew/install_file/MDbrew-2.0.13.tar.gz",
    install_requies=[
        "numpy>=1.0.0",
        "pandas>=1.0.0",
        "matplotlib>=1.0.0",
        "tqdm>=1.0.0",
    ],
    description="Postprocessing tools for the MD simulation results (ex. lammps)",
    packages=find_packages(),
    keywords=["MD", "LAMMPS"],
    python_requires=">=3",
    package_data={},
    zip_safe=False,
)
