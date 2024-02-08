from setuptools import setup, find_packages

setup(
    name="lyzr-automata",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "openai==1.3.4",
        "requests==2.31.0",
        "asyncio==3.4.3",
        
    ],
    author="lyzr",
    description="low-code multi-agent automation framework",
    long_description=open("README.md").read(),
    long_description_content_type="check Readme file",
    url="https://github.com/lyzrcore/lyzr-automata",
    license="MIT",
)
