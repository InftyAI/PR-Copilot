from copilot.pipelines.templates.summary_template import SUMMARY_USER_PROMPT


def test_summary_template():
    want = """
PR Title: Hello World
PR Description: Hello World
PR Commits: Hello World

PR Diffs:
```text
-def add(a, b):
-    return a + b
+def add(a, b, c):
+    return a + b + c
```

Response(must be a valid YAML, and nothing else):
"""
    diff = """-def add(a, b):
-    return a + b
+def add(a, b, c):
+    return a + b + c"""

    got = SUMMARY_USER_PROMPT.format(
        title="Hello World",
        description="Hello World",
        commit_messages="Hello World",
        pr_diffs=diff,
    )

    assert want == got
