# -*- coding: utf-8 -*-
from setuptools import setup

packages = \
['fitscube']

package_data = \
{'': ['*']}

install_requires = \
['astropy>=5.0,<6.0', 'numpy>=1.20,<2.0', 'tqdm']

entry_points = \
{'console_scripts': ['fitscube = fitscube.fitscube:cli',
                     'stokescube = fitscube.stokescube:cli']}

setup_kwargs = {
    'name': 'fitscube',
    'version': '0.2.1',
    'description': '',
    'long_description': "# FITSCUBE\n\nFrom the [wsclean](https://wsclean.readthedocs.io/) docs:\n> WSClean does not output these images in a normal “imaging cube” like CASA does, i.e., a single fits file with several images in it. For now I’ve decided not to implement this (one of the reasons for this is that information about the synthesized beam is not properly stored in a multi-frequency fits file). One has of course the option to combine the output manually, e.g. with a simple Python script.\n\nThis is a simple Python script to combine (single-frequency or single-Stokes) FITS images manually.\n\nCurrent assumptions:\n- All files have the same WCS\n- All files have the same shape / pixel grid\n- Frequency is either a WCS axis or in the REFFREQ header keyword\n- All the relevant information is in the first header of the first image\n\n## Installation\n\nInstall from git:\n```bash\npip install git+https://github.com/AlecThomson/fitscube.git\n```\n\n## Usage\n\nCommand line:\n```bash\nfitscube -h\n# usage: fitscube [-h] [-o] [--freq-file FREQ_FILE | --freqs FREQS [FREQS ...] | --ignore-freq] file_list [file_list ...] out_cube\n\n# Fitscube: Combine single-frequency FITS files into a cube. Assumes: - All files have the same WCS - All files have the same shape / pixel grid -\n# Frequency is either a WCS axis or in the REFFREQ header keyword - All the relevant information is in the first header of the first image\n\n# positional arguments:\n#   file_list             List of FITS files to combine (in frequency order)\n#   out_cube              Output FITS file\n\n# optional arguments:\n#   -h, --help            show this help message and exit\n#   -o, --overwrite       Overwrite output file if it exists\n#   --freq-file FREQ_FILE\n#                         File containing frequencies in Hz\n#   --freqs FREQS [FREQS ...]\n#                         List of frequencies in Hz\n#   --ignore-freq         Ignore frequency information and just stack (probably not what you want)\n\nstokescube -h\n# usage: stokescube [-h] [-v STOKES_V_FILE] [--overwrite] stokes_I_file stokes_Q_file stokes_U_file output_file\n\n# Fitscube: Combine single-Stokes FITS files into a Stokes cube. Assumes: - All files have the same WCS - All files have the same shape / pixel\n# grid - All the relevant information is in the first header of the first image\n\n# positional arguments:\n#   stokes_I_file         Stokes I file\n#   stokes_Q_file         Stokes Q file\n#   stokes_U_file         Stokes U file\n#   output_file           Output file\n\n# optional arguments:\n#   -h, --help            show this help message and exit\n#   -v STOKES_V_FILE, --stokes_V_file STOKES_V_FILE\n#                         Stokes V file\n#   --overwrite           Overwrite output file if it exists\n```\n\nPython:\n```python\nfrom fitscube import combine_fits, combine_stokes\n\nhdu_list, frequencies = combine_fits(\n    ['file1.fits', 'file2.fits', 'file3.fits'],\n)\nhdus_list = combine_stokes(\n    'stokes_I.fits',\n    'stokes_Q.fits',\n    'stokes_U.fits',\n)\n\n```\n\n## Convolving to a common resolution\nSee [RACS-Tools](https://github.com/AlecThomson/RACS-tools).\n\n## License\nMIT\n\n## Contributing\nContributions are welcome. Please open an issue or pull request.\n\n## TODO\n- [ ] Add support for non-frequency axes\n- [ ] Add tracking of the PSF in header / beamtable\n- [ ] Add convolution to a common resolution via RACS-Tools",
    'author': 'Thomson, Alec (S&A, Kensington)',
    'author_email': 'AlecThomson@users.noreply.github.com',
    'maintainer': 'None',
    'maintainer_email': 'None',
    'url': 'None',
    'packages': packages,
    'package_data': package_data,
    'install_requires': install_requires,
    'entry_points': entry_points,
    'python_requires': '>=3.7,<4.0',
}


setup(**setup_kwargs)
