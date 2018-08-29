# -*- encoding: utf-8 -*-
#
# Copyright © 2018 Julien Danjou <jd@mergify.io>
#
# Licensed under the Apache License, Version 2.0 (the "License"); you may
# not use this file except in compliance with the License. You may obtain
# a copy of the License at
#
#      http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS, WITHOUT
# WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied. See the
# License for the specific language governing permissions and limitations
# under the License.
import pyparsing


git_branch = pyparsing.CharsNotIn("~^: []\\")
github_login = pyparsing.CharsNotIn(" /")
text = pyparsing.dblQuotedString | pyparsing.CharsNotIn(" ")
status_check = pyparsing.CharsNotIn(" ")
milestone = pyparsing.CharsNotIn(" ")

operators = (
    pyparsing.Literal(":").setParseAction(pyparsing.replaceWith("=")) |
    pyparsing.Literal("=") |
    pyparsing.Literal("==") |
    pyparsing.Literal("!=") |
    pyparsing.Literal("≠") |
    pyparsing.Literal("~=") |
    pyparsing.Literal(">=") |
    pyparsing.Literal("≥") |
    pyparsing.Literal("<=") |
    pyparsing.Literal("≤") |
    pyparsing.Literal("<") |
    pyparsing.Literal(">")
)


def _token_to_dict(s, loc, toks):
    not_, key_op, key, op, value = toks
    if key_op == "#":
        value = int(value)
    d = {op: (key_op + key, value)}
    if not_:
        return {"-": d}
    return d


head = "head" + operators + git_branch
base = "base" + operators + git_branch
author = "author" + operators + github_login
merged_by = "merged-by" + operators + github_login
body = "body" + operators + text
assignee = "assignee" + operators + github_login
label = "label" + operators + text
locked = (
    "locked" +
    pyparsing.Empty().setParseAction(pyparsing.replaceWith("=")) +
    pyparsing.Empty().setParseAction(pyparsing.replaceWith(True))
)
title = "title" + operators + text
files = "files" + operators + text
milestone = "milestone" + operators + milestone
review_requests = "review-requested" + operators + github_login
review_approved_by = "review-approved-by" + operators + github_login
review_dismissed_by = "review-dismissed-by" + operators + github_login
review_changes_requested_by = (
    "review-changes-requested-by" + operators + github_login
)
review_commented_by = "review-commented-by" + operators + github_login
status_success = "status-success" + operators + status_check
status_pending = "status-pending" + operators + status_check
status_failure = "status-failure" + operators + status_check

search = (
    pyparsing.Optional(
        (pyparsing.Literal("-").setParseAction(pyparsing.replaceWith(True)) |
         pyparsing.Literal("¬").setParseAction(pyparsing.replaceWith(True)) |
         pyparsing.Literal("+").setParseAction(pyparsing.replaceWith(False))),
        default=False
    ) +
    pyparsing.Optional("#", default="") +
    (head | base | author | merged_by | body | assignee | label | locked |
     title | files | review_requests |
     review_approved_by | review_dismissed_by |
     review_changes_requested_by | review_commented_by |
     status_success | status_pending | status_failure)
).setParseAction(_token_to_dict)
