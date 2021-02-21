import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(name='job_site_analysis',
    version='0.1',
    author='Matt Walsh',
    author_email='git@mattwalsh.dev',
    license='MIT',
    description='ETL and analyse data from a job site',
    long_description=long_description,
    long_description_content_type="text/markdown",
    url='http://github.com/mattwalshdev/job_site_analysis',
    packages=['job_site_analysis'],
    zip_safe=False,
)
