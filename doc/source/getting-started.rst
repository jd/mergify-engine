===============
Getting Started
===============

Installation
------------

In order to work, Mergify needs access to your account and to be enabled. To do
so, start by logging in using your GitHub account at
https://mergify.io/dashboard. On first login, you will be asked to give
some permissions on your behalf for Mergify to work.

Once this is done, you need to enable the Mergify GitHub Application on the
repositories you want. Go to https://github.com/apps/mergify/installations/new
and enroll repositories where you want Mergify to be enabled.

Configuration
-------------

Basics
~~~~~~

In order for Mergify to apply your rules to your pull requests, you need to
create a configuration file. The configuration file should be created in the
root directory of each enabled repository and named ``.mergify.yml``.

Here's how to create a file with a minimal content to enable Mergify:

.. code-block:: shell

    $ cd myrepository
    $ echo "pull_request_rules:" > .mergify.yml
    $ git add .mergify.yml
    $ git commit -m "Enable mergify.io"
    $ git push

Since this file does not contain any specific rules, Mergify won't do anything.

Creating Rules
~~~~~~~~~~~~~~

Therefore, a more realistic example of the ``.mergify.yml`` file would look
like :

.. code-block:: yaml

    pull_request_rules:
      - name: automatic merge on CI success and review
        conditions:
          - status-success=continuous-integration/travis-ci
          - "#approved-reviews-by>=2"
        actions:
          merge:
            method: merge

.. warning::

   The ``#`` character is considered as the comment delimiter in YAML. ``#`` is
   also the length operator in Mergify's conditions system, therefore don't
   forget to use ``"`` around the condition.

The ``name`` of the rule is not used directly by Mergify, but is really useful
when Mergify will report its status and for debugging rules. We advise setting
an explicity name that makes sense to you.

The key ``conditions`` defines the list of conditions that a pull request must
match in order for the engine to execute the actions. In this example, there
are 2 conditions to be met for the rule to be applied to a pull request:

- ``status-success``, which contains all check services that successfully run
  on this pull request, must contains ``continuous-integration/travis-ci``.
  That would mean that the Travis CI reported a success status check.

- ``approved-reviews-by``, which contains the list of collaborators that
  approved the pull request, must have at least 2 members (note the ``#``
  length operator).

Therefore, in this example, two reviewers must approve the pull request and the
Travis CI must pass before Mergify executes the action — which is merging the
pull request here.

The automatic merge of the pull request is enabled by specifying the ``merge``
action with a ``method`` parameter containing the merge method to use.

You can define any number rules with any of the available conditions criterias;
each rule that match will see the action being executed, respecting the order
they are defined.

Fore more details about the configuration file format, check
:ref:`configuration file format`.

Mergify is now ready, what happens next?
----------------------------------------

When a contributor sends a pull request to the repository, Mergify will post a
status check about the state of the pull request according to the defined
rules.

.. image:: _static/mergify-status-ko.png
   :alt: status check

.. note::

   When a pull request changes the configuration of Mergify, the ``mergify/pr``
   status is built with the current configuration (without the pull request
   change). To validate the Mergify configuration change an additional status is
   posted named ``mergify/future-config-checker``.

When all the criterias of the rules are satisfied, Mergify will merge the base
branch into the pull request if the pull request is not up-to-date with the
base branch. This is made to ensure that the pull request is tested one last
time while being up-to-date with the base branch.

Once the required services status are approved, Mergify will automatically
merge the pull request:

.. image:: _static/mergify-merge.png
   :alt: merge

Now, that Mergify. is setup, you can go back on what matters for your project
and let us babysit your pull requests!
