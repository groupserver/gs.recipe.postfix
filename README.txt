The GroupServer_ recipe for creating the default Postfix_ configuration
files. A ``groupserver.virtual`` file is created [#virtual]_ to create the
virtual-host mapping and a ``groupserver.aliases`` file is created
[#aliases]_ to call ``smtp2gs`` [#smtp2gs]_.

- Code repository: https://source.iopen.net/groupserver/gs.recipe.postfix
- Questions and comments to http://groupserver.org/groups/development
- Report bugs at https://redmine.iopen.net/projects/groupserver

.. [#virtual] See `the virtual(5) man page 
              <http://www.postfix.org/virtual.5.html>`_
.. [#aliases] See `the aliases(5) man page
              <http://www.postfix.org/aliases.5.html>`_
.. [#smtp2gs] See 
        <https://source.iopen.net/groupserver/gs.group.messages.add.smtp2gs>
.. _GroupServer: http://groupserver.org
.. _Postfix: http://www.postfix.org/
