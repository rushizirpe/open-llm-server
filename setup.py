from setuptools import setup, find_packages

setup(
    name="open-llm-server",
    version="1.0.0",
    packages=find_packages() + ['scripts'],
    package_data={'scripts': ['*.py']},
    include_package_data=True,
    install_requires=[
        "fastapi",
        "uvicorn",
        "torch",
        "transformers",
        "pydantic",
        "pydantic-settings",
        "requests",
        "psutil",
        "numpy"
    ],
    entry_points={
        "console_scripts": [
            "llm-server=scripts.launch:main",
        ],
    },
    author="Rishi Zirpe",
    author_email="zirperishi@gmail.com",
    description="An open-source LLM server",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/rushizirpe/open-llm-server",
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.8',
)