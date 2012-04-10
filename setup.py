import os
from setuptools import setup, find_packages


VERSION = "0.1"

setup(
    name = "django-css-usage",
    version = VERSION,
    author="Julian Bez",
    url = "https://github.com/webjunkie/django-css-usage",
    description = """Django-css-usage parses a given CSS file and outputs CSS rules
    that likely won't apply to any template""",
    packages=find_packages(),
    namespace_packages = [],
    include_package_data = True,
    zip_safe=False,
    license="None",
    install_requires = ["cssutils"]
)
