=====================
``gs.recipe.postfix``
=====================
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
A ``zc.buildout`` recipe the Postfix configuration for GroupServer
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

:Author: `Michael JasonSmith`_
:Contact: Michael JasonSmith <mpj17@onlinegroups.net>
:Date: 2014-10-22
:Organization: `GroupServer.org`_
:Copyright: This document is licensed under a
  `Creative Commons Attribution-Share Alike 4.0 International License`_
  by `OnlineGroups.net`_.

Introduction
============

This product provides a ``zc.buildout`` recipe_ for creating the
default Postfix_ configuration files for GroupServer_.

Recipe
======

Calling the recipe is done by ``buildout``. It is configured like
other ``zc.buildout`` recipes::

  [setup-postfix]
  # Create the Postfix configuration files for GroupServer
  recipe = gs.recipe.postfix
  smtp2gs_path = ${buildout:directory}/bin/smtp2gs
  site = ${config:host}

Parameters
----------

Two values must be provided to the recipe.

``smtp2gs_path``:
  The path to the ``smtp2gs`` script.

``site``:
  The host-name of the GroupServer site.

To parameters are **optional.**

``port``: 
  The default port that the GroupServer site is running on. If
  omitted (the default) the standard port will be used
  [#standard]_.

``use_ssl``:
  If set to ``false``, ``no``, or ``off`` (the default) then
  ``smtp2gs`` will use HTTP to communicate with the server. If
  set to any other value then HTTPS (TLS) will be used.

When the recipe is run it will create a directory
``postfix_config`` within the GroupServer installation
directory. Within the ``postfix_config`` directory a
``groupserver.virtual`` file is created [#virtual]_ to create the
virtual-host mapping and a ``groupserver.aliases`` file is
created [#aliases]_ to call ``smtp2gs`` [#smtp2gs]_.

Lock file
---------

To prevent the recipe from being run more than once a *lock file*
is created, ``var/setup-postfix.cfg``, within the GroupServer
installation directory. (The name is actually taken from the name
of the section in the configuration file.)

Resources
=========

- Code repository: https://github.com/groupserver/gs.recipe.postfix
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#virtual] See `the virtual(5) man page 
              <http://www.postfix.org/virtual.5.html>`_
.. [#aliases] See `the aliases(5) man page
              <http://www.postfix.org/aliases.5.html>`_
.. [#smtp2gs] See 
              <https://github.com/groupserver/gs.group.messages.add.smtp2gs>
.. [#standard] The definition of what constitutes a *standard*
               port is left to a combination of the ``smtp2gs``,
               ``gs.form`` and the standard Python ``http``
               module.
.. _Postfix: http://www.postfix.org/
.. _GroupServer: http://groupserver.org/
.. _GroupServer.org: http://groupserver.org/
.. _OnlineGroups.Net: https://onlinegroups.net
.. _Michael JasonSmith: http://groupserver.org/p/mpj17
..  _Creative Commons Attribution-Share Alike 4.0 International License:
    http://creativecommons.org/licenses/by-sa/4.0/

..  LocalWords:  TLS groupserver html www smtp ssl postfix
