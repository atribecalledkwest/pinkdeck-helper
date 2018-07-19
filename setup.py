from setuptools import setup, find_packages

def get_requirements():
	with open("requirements.txt", "r") as f:
		return [requirement.strip() for requirement in f.read().split("\n") if requirement.strip() != ""]

def get_version():
	with open("VERSION", "r") as f:
		return f.read().strip()

setup(
	name="pinkdeck-helper",
	version=get_version(),
	install_requires=get_requirements(),
	python_requires=">3.4",
	entry_points={
		"console_scripts": [
            "pinkdeck=pinkdeck.scripts.cli:main"
		]
	}
)
