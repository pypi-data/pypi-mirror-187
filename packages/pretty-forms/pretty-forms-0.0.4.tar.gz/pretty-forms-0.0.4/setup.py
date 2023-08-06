from setuptools import setup, find_packages

setup(
        name="pretty-forms",
        version="0.0.4",
        license="BSD",
        author="Jorge Monforte González",
        author_email="yo@llou.net",
        packages=find_packages(),
        package_dir={'.':'.'},
        include_package_data=True,
        url="https://github.com/llou/pretty-forms",
        keywords="django bulma",
        install_requires=['django'],
)



