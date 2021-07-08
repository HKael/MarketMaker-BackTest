
=========
CHANGELOG
=========

----------
06.07.2021
----------

Added
-----

- ``data.py`` Spread is calculated within the `order_book` function.
- ``data.py`` Added function `continuous_ob` to generate continuous orderbook compatible timestamps.
- ``maker.py`` with `xemm_signal` as cross-exchange market maker signal generator for backtesting.

----------
05.07.2021
----------

Added
-----

- ``README.rst`` as a short readme file.
- ``main.py`` Auxiliary codes for reading JSON
- ``main.py`` A quick calculation of historical spread.

Modified
--------

- ``NOTES.rst`` Compacted information and droped other general notes and ideas for the moment.


----------
02.07.2021
----------

Added
-----

- Base repository files ``.gitignore`` and ``CHANGELOG.rst``
- ``requirements.txt`` file with libraries and versions
- fees_schedule, order_book, functions in ``data.py``
- ``main.py`` file for main tests
- ouput options in order_book method contained in ``data.py``

Planned
-------

- Time-Block of 1 second, to calculate average spread in each market
- Spread Timeseries barplot
