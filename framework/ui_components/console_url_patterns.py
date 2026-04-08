"""
Compiled regex patterns for OpenShift console URLs.

These are passed to Playwright ``Page.wait_for_url`` via ``BasePage._verify_page_regex``.
Each pattern may match as a substring of the full URL (query strings and hashes allowed).
"""

import re

PIPELINES_NS_URL = re.compile(r"pipelines/ns/[^/?#]+")

PIPELINES_OVERVIEW_URL = re.compile(r"pipelines-overview/(?:all-namespaces|ns/[^/?#]+)")

TASKS_URL = re.compile(r"tasks/(?:all-namespaces|ns/[^/?#]+)")

TRIGGERS_URL = re.compile(r"triggers/(?:all-namespaces|ns/[^/?#]+)")
