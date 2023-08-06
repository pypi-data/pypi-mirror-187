from setuptools import setup, find_packages
import io

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
	name="ml2ipa",
	version="1.0.2",
	description="A linguistic tool that generates IPA pronunciation for Malayalam words",
	long_description=long_description,
    long_description_content_type='text/markdown',
	author="Elaine Mary Rose",
	author_email="elainerose311@gmail.com",
	url="https://github.com/erose311/ml2ipa",
	#packages=['TransLitML'],
	packages=find_packages(),
	license="MIT",
	classifiers=[
		"Intended Audience :: Developers",
		"Programming Language :: Python :: 3.9",
		"Operating System :: OS Independent",
		"Topic :: Software Development :: Libraries :: Python Modules"
	]
)