.. _configuration file format:

===========================
 Configuration File Format
===========================

The configuration file for Mergify should be named ``.mergify.yml`` and must be
placed in the root directory of your GitHub repository. Mergify uses the
default repository branch configured on GitHub to read the configuration file —
usually ``master``. The file format is `YAML <http://yaml.org/>`_.

The file main entry is a dictionary whose key is named ``pull_request_rules``.
The value of the ``pull_request_rules`` key must be a list of dictionary.

Each dictionnary must have the following keys:

.. list-table::
   :header-rows: 1
   :widths: 1 1 2

   * - Key Name
     - Value Type
     - Value Description
   * - ``name``
     - string
     - The name of the rule. This is not used by the engine directly, but is
       used when reporting information about a rule.
   * - ``conditions``
     - array of :ref:`Conditions`
     - A list of :ref:`Conditions` string that must match against the pull
       request for the rule to be applied.
   * - ``actions``
     - dictionary of :ref:`Actions`
     - A dictionnary made of :ref:`Actions` that will be executed on the
       matching pull requests.


Example Rules
-------------

You can define more specific rules based on the large number of criterias
available: pull request author, base branch, labels, files, etc.

Here's a few example that should help you getting started.

Automatic Merge for Automatic Pull Requests
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some pull request might be created automatically by other tools, such as
`Dependabot <https://dependabot.com/>`_. You might decide that there's no need
to manually review and approve those pull request as long as your continuous
integration system validates them.

Therefore, you could write a rule such as:

.. code-block:: yaml

    pull_request_rules:
      - name: automatic merge for Dependabot pull requests on master
        conditions:
          - author=dependabot[bot]
          - status-success=continuous-integration/travis-ci
          - base=master
        actions:
          merge:
            method: merge

That would automatically merge any pull request created by Dependabot for the
``master`` branch where Travis CI passes.

Less Strict Rules for Stable Branches
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some projects like having easier review requirements for stable/maintenance
branches. That usually means having e.g. 2 review requested for merging into
master, but only one for a stable branch, since those pull request are
essentially backport from ``master``.

To automate the merge in this case, you could write some rules along those:

.. code-block:: yaml

    pull_request_rules:
      - name: automatic merge for master when reviewed and CI passes
        conditions:
          - status-success=continuous-integration/travis-ci
          - "#approved-reviews-by>=2"
          - base=master
        actions:
          merge:
            method: merge
      - name: automatic merge for stable branches
        conditions:
          - status-success=continuous-integration/travis-ci
          - "#approved-reviews-by>=1"
          - base~=^stable/
        actions:
          merge:
            method: merge


Using Labels to Enable/Disable merge
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Some developers are not comfortable with having a final step before merging the
code. In that case, you can add a condition using a ``label``:

.. code-block:: yaml

    pull_request_rules:
      - name: automatic merge for master when reviewed and CI passes
        conditions:
          - status-success=continuous-integration/travis-ci
          - "#approved-reviews-by>=2"
          - base=master
          - label=ready-to-merge
        actions:
          merge:
            method: merge

As soon as the pull request has been approved by 2 contributors and gets the
`label <https://help.github.com/articles/labeling-issues-and-pull-requests/>`_
``ready-to-be-merged``, the pull request will be merged by Mergify.

On the other hand, some developers wants an option to disable the automatic
merge feature with a label. This can be useful to indicate that a pull request
labelled as ``work-in-progress`` should not be merged:

.. code-block:: yaml

    pull_request_rules:
      - name: automatic merge for master when reviewed and CI passes
        conditions:
          - status-success=continuous-integration/travis-ci
          - "#approved-reviews-by>=2"
          - base=master
          - label!=work-in-progress
        actions:
          merge:
            method: merge

In that case, if a pull request gets labelled with ``work-in-progress``, it
won't be merged, even if approved by 2 contributors and having Travis CI
passing.

Removing Stale Reviews
~~~~~~~~~~~~~~~~~~~~~~

When a pull request is updated, GitHub does not remove the possibly outdated
reviews approvals or changes request. It's a good idea to remove them as soon
as the pull request gets updated with new commits.

.. code-block:: yaml

    pull_request_rules:
      - name: remove outdated reviews
        conditions:
          - base=master
        actions:
          dismiss_reviews:
