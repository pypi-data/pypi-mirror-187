from distutils.core import setup
setup(
  name = 'pythmath',         # How you named your package folder (MyLib)
  packages = ['pythmath'],   # Chose the same as "name"
  version = '0.2.5',      # Start with a small number and increase it with every change you make
  license='MIT',        # Chose a license from here: https://help.github.com/articles/licensing-a-repository
  description = 'Pure Mathematics library which performs basic math operations such as sin, cos, tan and it also '
                'includes basic statistical functions such as mean, median mode etc.,',   # Give a short description
  # about your library
  author = 'Roshaan Mehmood',                   # Type in your name
  author_email = 'roshaan55@gmail.com',      # Type in your E-Mail
  url = 'https://github.com/roshaan55/pycamdetector',   # Provide either the link to your github or to your website
  download_url = 'https://github.com/roshaan55/pycamdetector/archive/refs/tags/v_0.6.5.tar.gz',    # I explain this later on
  keywords = ['pythmath', 'mathlibrary', 'sine', 'area of triangle', 'area of circle', 'area of square'],   # Keywords that define your package best
  install_requires=[            # I get to this in a second
          '',
      ],
  classifiers=[
    'Development Status :: 3 - Alpha',      # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
    'Intended Audience :: Developers',      # Define that your audience are developers
    'Topic :: Software Development :: Build Tools',
    'License :: OSI Approved :: MIT License',   # Again, pick a license
    'Programming Language :: Python :: 3.6',      #Specify which pyhton versions that you want to support
    'Programming Language :: Python :: 3.7',
    'Programming Language :: Python :: 3.8',
    'Programming Language :: Python :: 3.9',
  ],
)