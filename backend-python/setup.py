from setuptools import setup, find_packages

setup(
    name="app",
    version="0.1.0",
    packages=find_packages(include=['app', 'app.*']),
    install_requires=[
        "fastapi",
        "uvicorn",
        "motor",
        "redis",
        "beautifulsoup4",
        "pydantic",
        "pydantic-settings",
        "neo4j",
        "python-dotenv",
    ],
) 
