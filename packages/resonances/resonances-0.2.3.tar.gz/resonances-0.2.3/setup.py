# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['resonances',
 'resonances.data',
 'resonances.experiment',
 'resonances.matrix',
 'resonances.resonance']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.2.1,<6.0.0',
 'matplotlib>=3.6.3,<4.0.0',
 'numpy>=1.24.1,<2.0.0',
 'pandas>=1.5.3,<2.0.0',
 'rebound>=3.23.2,<4.0.0',
 'scipy>=1.10.0,<2.0.0',
 'seaborn>=0.12.2,<0.13.0']

entry_points = \
{'console_scripts': ['ain = '
                     'resonances.experiment.console:asteroids_in_resonance',
                     'asteroids-in-resonance = '
                     'resonances.experiment.console:asteroids_in_resonance',
                     'ia = resonances.experiment.console:asteroids',
                     'identify-asteroids = '
                     'resonances.experiment.console:asteroids',
                     'identify-quick = resonances.experiment.console:quick',
                     'identify-resonances = '
                     'resonances.experiment.console:identifier',
                     'iq = resonances.experiment.console:quick',
                     'ir = resonances.experiment.console:identifier',
                     'simulation-shape = '
                     'resonances.experiment.console:calc_shape',
                     'ss = resonances.experiment.console:calc_shape']}

setup_kwargs = {
    'name': 'resonances',
    'version': '0.2.3',
    'description': 'Identification of mean-motion resonances',
    'long_description': '# Mean-Motion Resonances\n\n[![Code style: black](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)\n[![Resonances](https://github.com/smirik/resonances/actions/workflows/ci.yml/badge.svg?branch=main)](https://github.com/smirik/resonances/actions/workflows/ci.yml)\n\n`resonances` is an open-source package dedicated to the identification of mean-motion resonances of small bodies. Many examples are for the Solar system; however, you might use the package for any possible planetary system, including exoplanets.\n\nFor more information, [read the documentation](https://smirik.github.io/resonances/).\n\n**Note:** while this app has many functional and integration tests built in, it is still in the dev stage. Hence, it might include some inconsistencies. So, any community help is appreciated!\n\n## Features\n\nThe package:\n\n- can automatically identify two-body and three-body mean-motion resonance in the Solar system,\n- accurately differentiates different types of resonances (pure, transient, uncertain),\n- provides an interface for mass tasks (i.e. find resonant areas in a planetary system),\n- can plot time series and periodograms,\n- and, yeah, it is well tested ;)\n\nIt actively uses [REBOUND integrator](https://rebound.readthedocs.io) maintained by Hanno Rein and others.\n\n## Installation\n\nTo install resonances on your system, follow the instructions on the appropriate [installation guide](https://smirik.github.io/resonances/install/)\n\n## Mean-motion resonances\n\nFor those who are not familiar with the mean-motion resonances, here is the list of papers used to develop this package:\n\n### Papers about the automatic identification of resonant asteroids\n\n1. Smirnov, E. A. & Shevchenko, I. I. Massive identification of asteroids in three-body resonances. Icarus 222, 220–228 (2013).\n1. Smirnov, E. A., Dovgalev, I. S. & Popova, E. A. Asteroids in three-body mean motion resonances with planets. Icarus (2017) doi:10.1016/j.icarus.2017.09.032.\n1. Smirnov, E. A. & Dovgalev, I. S. Identification of Asteroids in Two-Body Resonances. Solar System Research 52, 347–354 (2018).\n1. Nesvorný, D. & Morbidelli, A. Three-Body Mean Motion Resonances and the Chaotic Structure of the Asteroid Belt. The Astronomical Journal 116, 3029–3037 (1998).\n\n### Papers about mean-motion resonances\n\n1. Chirikov, B. V. A universal instability of many-dimensional oscillator systems. Physics reports 52, 263–379 (1979).\n1. Gallardo, T. Strength, stability and three dimensional structure of mean motion resonances in the solar system. Icarus 317, 121–134 (2019).\n1. Gallardo, T. Atlas of the mean motion resonances in the Solar System. Icarus 184, 29–38 (2006).\n1. Gallardo, T., Coito, L. & Badano, L. Planetary and satellite three body mean motion resonances. Icarus 274, 83–98 (2016).\n1. Milani, A., Cellino, A., Knezevic, Z., Novaković, B. & Spoto, F. Asteroid families classification: Exploiting very large datasets. Icarus 239, 46–73 (2014).\n1. Murray, N. & Holman, M. Diffusive chaos in the outer asteroid belt. The Astronomical Journal 114, 1246 (1997).\n1. Murray, N., Holman, M. & Potter, M. On the Origin of Chaos in the Asteroid Belt. The Astronomical Journal 116, 2583–2589 (1998).\n1. Shevchenko, I. I. On the Lyapunov exponents of the asteroidal motion subject to resonances and encounters. Proc. IAU 2, 15–30 (2006).\n\n### Books\n\n1. Murray, C. D. & Dermott, S. F. Solar system dynamics. (Cambridge Univ. Press, 2012).\n1. Morbidelli, A. Modern celestial mechanics: aspects of solar system dynamics. (2002).\n\n## References\n\nWhenever you use this package, we are kindly asking you to refer to one of the following papers (please choose the appropriate):\n\n1. **The package itself**: to be published\n1. **The Libration module and automatic identification of librations**: to be published\n1. **Mass identification of mean-motion resonances:** Smirnov, E. A., Dovgalev, I. S. & Popova, E. A. Asteroids in three-body mean motion resonances with planets. Icarus (2017) doi:10.1016/j.icarus.2017.09.032.\n\n## Authors\n\nThe authors of the package:\n\n- [Evgeny Smirnov](https://github.com/smirik) ([FB](https://facebook.com/smirik), [Telegram](https://t.me/smirik))\n\n## Acknowledgement\n\n- Many thanks to the co-authors of the papers (prof. I.\xa0I. Shevchenko, I.\xa0Dovgalev Dr.\xa0E.\xa0Popova).\n- The creators of [REBOUND integrator](https://rebound.readthedocs.io).\n- The creators of [Astropy](http://astropy.org).\n- The creators of `numpy`, `scipy`, `pandas`, and `matplotlib`.\n\n## Contributing\n\nFeel free to contribute to the code by sending pull requests [to the repository](https://github.com/smirik/resonances).\n\n## License\n\nMIT\n',
    'author': 'Evgeny Smirnov',
    'author_email': 'smirik@gmail.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'http://smirik.github.io/resonances/',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.8.1,<3.12',
}


setup(**setup_kwargs)
