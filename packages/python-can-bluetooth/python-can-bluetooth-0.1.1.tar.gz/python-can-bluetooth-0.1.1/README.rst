python-can-bluetooth
====================
|release| |python_implementation| |ci| |coverage| |downloads|

.. |release| image:: https://img.shields.io/pypi/v/python-can-bluetooth.svg
   :target: https://pypi.python.org/pypi/python-can-bluetooth/
   :alt: Latest Version on PyPi

.. |python_implementation| image:: https://img.shields.io/pypi/implementation/python-can-bluetooth
   :target: https://pypi.python.org/pypi/python-can-bluetooth/
   :alt: Supported Python implementations
   
.. |downloads| image:: https://pepy.tech/badge/python-can-bluetooth
   :target: https://pepy.tech/project/python-can-bluetooth
   :alt: Downloads on PePy
   
.. |coverage| image:: https://coveralls.io/repos/github/MattWoodhead/python-can-bluetooth/badge.svg?branch=main
   :target: https://coveralls.io/github/MattWoodhead/python-can-bluetooth?branch=main
   
.. |ci| image:: https://github.com/MattWoodhead/python-can-bluetooth/actions/workflows/tox.yml/badge.svg
   :target: https://github.com/MattWoodhead/python-can-bluetooth/actions/workflows/tox.yml


This module is a plugin for the python-can_. module, that allows the use of CAN messages transmitted over a Bluetooth SPP connection. It is similar to the CAN over serial protocol included in the python-can_. package, but includes additional error checking to ensure messages are not corrupted during transmission.


Installation
------------

Install using pip::

    $ pip install python-can-bluetooth


Usage
-----

In general, useage is largely the same as with the main python-can_ library, using the interface designation of "bluetooth".

Create python-can bus with the Bluetooth interface:

.. code-block:: python

    import can

    bus = can.Bus(interface="bluetooth", channel="COM4", bitrate=250000, echo=False)

Some examples are present in the python-can-bluetooth/examples_ directory in the repository.


.. _python-can: https://python-can.readthedocs.org/en/stable/

.. _examples: https://github.com/MattWoodhead/python-can-bluetooth/tree/main/examples
