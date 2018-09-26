.. _Actions:

=========
 Actions
=========

When a pull request matches the list of :ref:`Conditions` of a rule, the
actions set in the rule are executed by Mergify. The actions should be put
under the ``actions`` key in the ``pull_request_rules`` entry — see
:ref:`configuration file format`.

The list of available actions is listed below, with their parameters:

.. _merge action:

merge
=====

The ``merge`` action merges the pull request into its base branch. The
``merge`` action takes the following parameter:

.. list-table::
   :header-rows: 1
   :widths: 1 1 1 2

   * - Key Name
     - Value Type
     - Default
     - Value Description
   * - ``method``
     - string
     - ``merge``
     - Merge method to use. Possible values are ``merge``, ``squash`` or
       ``rebase``.
   * - ``rebase_fallback``
     - string
     - ``merge``
     - If ``method`` is set to ``rebase``, but the pull request cannot be
       rebased, the method defined in ``rebase_fallback`` will be used instead.
       Possible values are ``merge``, ``squash``, ``none``.
   * - ``strict``
     - Boolean
     - ``false``
     - If set to ``true``, :ref:`strict merge` will be enabled: the pull
       request will be merged only once up-to-date with its base branch.

.. _backport action:

backport
=========

It is common for software to have (some of) their major versions maintained
over an extended period. Developers usually create stable branches that are
maintained for a while by cherry-picking patches from the development branch.

This process is called *backporting* as it implies that bug fixes merged into
the development branch are ported back to the stable branch. The stable branch
can then be used to release a new minor version of the software, fixing some of
its bugs.

As this process of backporting patches can be tedious, Mergify automates this
mechanism to save developers' time and ease their duty.

The ``backport`` action copies the pull request into another branch *once the
pull request has been merged*. The ``backport`` action takes the following
parameter:

.. list-table::
   :header-rows: 1
   :widths: 1 1 1 2

   * - Key Name
     - Value Type
     - Default
     - Value Description
   * - ``branches``
     - array of string
     - ``[]``
     - The list of branches the pull request should be copied to.


Examples
========

Simple merge
------------

The simplest merge action should be:

.. code-block:: yaml

     actions:
       merge:

That will merge using the default values. If you to specify the merge method,
you can use:

.. code-block:: yaml

     actions:
       merge:
         method: merge

Rebase Merge with No Fallback
-----------------------------

If you use the rebase merge method and prefer to fail when the rebase fail
rather than merging, use this:

.. code-block:: yaml

     actions:
       merge:
         method: rebase
         rebase_fallback: null
