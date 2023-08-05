import setuptools

setuptools.setup(
    name='cluster_model',
    version='0.1',
    author='Denaldo Lapi',
    author_email='denaldo98@gmail.com',
    description='Class for wrapping a cluster model from the river package for BERTopic Online Topic Modeling',
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url='https://github.com/denaldo98/cluster_model',
    license='MIT',
    packages=['cluster_model'],
    install_requires=['river'],
)
