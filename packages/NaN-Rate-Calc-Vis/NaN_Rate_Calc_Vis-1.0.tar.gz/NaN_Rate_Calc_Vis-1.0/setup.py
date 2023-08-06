from setuptools import setup, find_packages

setup(
    name='NaN_Rate_Calc_Vis',
    version='1.0',
    description='Calculate, analyze and visualize the NaN values in a given Dataframe',
    packages=find_packages(),
    install_requires=[
        'pandas',
        'matplotlib'
    ],
    author='Maxim Kiesel',
    author_email='maxim.kiese@yahoo.com',
    url='https://github.com/maximkiesel1/Package_PyPi_NaN_Calc_Visual',
    license='MIT',
    zip_safe=False,
)

