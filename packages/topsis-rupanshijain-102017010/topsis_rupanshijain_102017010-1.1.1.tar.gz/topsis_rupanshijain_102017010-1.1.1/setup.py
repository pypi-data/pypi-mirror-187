from distutils.core import setup


def readme():
    with open("README.md") as f:
        README = f.read()
    return README


setup(
    name="topsis_rupanshijain_102017010",
    packages=["topsis_rupanshijain_102017010"],
    version="1.1.1",
    license="MIT",
    description="TOPSIS method for multi-criteria decision making",
    long_description=readme(),
    long_description_content_type="text/markdown",
    author="Rupanshi Jain",
    author_email="rupanshijain45678@gmail.com",
    url="https://github.com/rdotjain/topsis_rupanshi_102017010",
    download_url="https://github.com/rdotjain/topsis_rupanshi_102017010/archive/refs/tags/v_111.tar.gz",
    keywords=["topsis", "MCDM"],
    install_requires=[
        "pandas",
        "numpy",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
    ],
)
