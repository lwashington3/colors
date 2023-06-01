from setuptools import setup


with open("README.md", 'r') as f:
	long_description = f.read()


project_name = "colors"
git_url = f"https://github.com/lwashington3/{project_name}"


setup(
	name=project_name,
	version="1.1.0b2",
	author="Len Washington III",
	description="Custom Colors module",
	include_package_data=True,
	long_description=long_description,
	long_description_content_type="test/markdown",
	url=git_url,
	project_urls={
		"Bug Tracker": f"{git_url}/issues"
	},
	license="MIT",
	packages=[project_name],
)
