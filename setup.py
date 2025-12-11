from setuptools import setup, find_packages

setup(
    name="lyzr-automata",
    version="0.1.3",
    packages=find_packages(),
    install_requires=[
        "openai==1.30.5",
        "requests==2.31.0", 
        "python-dotenv==1.0.1"
    ],
    author="lyzr",
    description="low-code multi-agent automation framework",
    long_description=open("README.md").read(),
    long_description_content_type="check Readme file",
    url="https://github.com/lyzrcore/lyzr-automata",
    license="MIT",
        classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.8.1, <3.12",
)
