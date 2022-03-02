from setuptools import find_packages, setup

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name='flask-validity',
    packages=find_packages(include=['validity']),
    version='1.0.0',
    description='The robust validation library for flask',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/alphasofthub/validity",
    project_urls={
        "Bug Tracker": "https://github.com/alphasofthub/validity/issues",
    },
    author='Muhammad Umer Farooq',
    license='MIT',
    include_package_data=True,
    package_data={
        "validity": ["locale/*.json"],
    },
    platforms='any',
    zip_safe=False,
    install_requires=['flask==2.0.1'],
    setup_requires=['pytest-runner', 'flask==2.0.1'],
    tests_require=['pytest==4.4.1', 'flask==2.0.1'],
    test_suite='tests',
)
