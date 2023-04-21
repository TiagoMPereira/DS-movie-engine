import setuptools

with open('requirements.txt') as f:
    required = f.read().splitlines()
setuptools.setup(
    name='movie_engine',
    version='0.1.2',
    packages=setuptools.find_packages(),
    author='morales',
    author_email='tiago.pereira@gec.inatel.br',
    description='Movies recomender package',
    install_requires=required,
    # package_data={'':['*.csv', '*.txt', '*.pkl']},
    include_package_data=True
)