from setuptools import setup, find_packages

setup(
    name="genesis-ui",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "gradio>=4.1.1",
        "numpy>=1.24.0",
        "torch>=2.1.1",
    ],
    extras_require={
        "test": [
            "coverage>=7.3.2",
            "pytest>=7.4.3",
            "pytest-cov>=4.1.0",
        ],
    },
    python_requires=">=3.8",
)
