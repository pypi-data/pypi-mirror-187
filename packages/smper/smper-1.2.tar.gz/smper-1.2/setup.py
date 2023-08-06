from setuptools import setup,find_namespace_packages
from os import listdir
setup(name='smper',

      version='1.2',

      url='https://github.com/parlorsky/sempaiper',

      license='MIT',

      author='Levap Vobayr',

      author_email='tffriend015@gmail.com',

      description='',
      packages=find_namespace_packages(where="src"),
      package_dir={"": "src"},
      package_data={**{
        f"smper.q1_1.{x}": ["*.jpg"] for x in range(1,len(listdir('src/smper/q1_1'))+1)
        },**{
        f"smper.q2_1.{x}": ["*.jpg"] for x in range(1,len(listdir('src/smper/q2_1'))+1)
        },**{
        f"smper.q3_1.{x}": ["*.jpg"] for x in range(1,len(listdir('src/smper/q3_1'))+1)
        }},


      zip_safe=False)
