from setuptools import setup, find_packages
setup(
    name="tillvisionio",
    use_scm_version=True,
    setup_requires=['setuptools_scm'],
    packages=find_packages(exclude=["^\."]),
    package_data={"tillvisionio": ["textfsm_templates/*.txt"]},
    install_requires=[
                      "textfsm>=0.4.1",
                      "numpy>=1.16.3"
                      ],
    python_requires=">=3.7"
)
