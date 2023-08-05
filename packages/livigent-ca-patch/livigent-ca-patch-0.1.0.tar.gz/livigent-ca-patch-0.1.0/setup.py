from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="livigent-ca-patch",
    version='0.1.0',
    author="Moshe Dicker",
    author_email='dickermoshe@gmail.com',
    description="Make requests, pip and dependant packages work on devices with Livigent.",
    url='https://github.com/dickermoshe/livigent-ca-patch',
    license='GNU General Public License v3.0',
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=[
        'pip-system-certs',
        'requests'
    ],
    packages=find_packages(),
    python_requires=">=3.10",
)
