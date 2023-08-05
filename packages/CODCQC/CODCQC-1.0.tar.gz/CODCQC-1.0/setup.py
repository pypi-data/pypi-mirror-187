import setuptools

with open("README.md",'r',encoding='utf-8') as fh:
    long_description=fh.read()


setuptools.setup(
    name="CODCQC",
    version="1.0",
    author ="Zhetao Tan; Lijing Cheng",
    author_email = "tanzhetao@mail.iap.ac.cn",
    description = "A climatology-based quality control algorithms for ocean temperature in-situ observations (Tan et al., 2023)",
    long_description = long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/zqtzt/CODCQC/",
    include_package_data=True,
    package_data={'CODCQC':['tests/WOD18_mat_temp_data/*.mat','tests/WOD18_netCDF_temp_data/*.nc','tests/*.txt']},
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    install_requires=['numpy >= 1.20.1','gsw >=3.0.3','scipy >=1.5.2','netCDF4 >= 1.5.4','h5py >=2.10.0'],
    python_requires='>=3.7',
)