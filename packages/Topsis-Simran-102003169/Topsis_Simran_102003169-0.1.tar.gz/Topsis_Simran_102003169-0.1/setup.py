from distutils.core import setup
setup(
    # How you named your package folder (MyLib)
    name='Topsis_Simran_102003169',
    packages=['Topsis_Simran_102003169'],   # Chose the same as "name"
    version='0.1',      # Start with a small number and increase it with every change you make
    # Chose a license from here: https://help.github.com/articles/licensing-a-repository
    license='MIT',
    # Give a short description about your library
    description='This package is implimentation of multi-criteria decision analysis using topsis',
    author='Simran Bhalla',                   # Type in your name
    author_email='simranbhalla0307@gmail.com',      # Type in your E-Mail
    # Provide either the link to your github or to your website
    url='https://github.com/simranbhalla3/Topsis_Simran_102003169',
    # I explain this later on
    download_url='https://github.com/simranbhalla3/Topsis_Simran_102003169/archive/refs/tags/v_0.1.tar.gz',
    keywords=['topsis'],   # Keywords that define your package best
    install_requires=[            # I get to this in a second
        'numpy',
        'pandas',
        ''
    ],
    classifiers=[
        # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        'Development Status :: 3 - Alpha',
        # Define that your audience are developers
        'Intended Audience :: Developers',
        'Topic :: Software Development :: Build Tools',
        'License :: OSI Approved :: MIT License',   # Again, pick a license
        # Specify which pyhton versions that you want to support
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
    ],
)
