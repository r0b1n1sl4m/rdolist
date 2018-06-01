from setuptools import setup

setup(
    name="rdolist",
    version="1.0",
    packages=['cli', 'cli.commands'],
    include_package_data=True,
    install_requires=[
        'click'
    ],
    entry_points="""
        [console_scripts]
        rdolist=cli.cli:cli
    """
)
