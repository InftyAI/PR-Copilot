from copilot.providers.github_provider import (
    convert_to_diff_url,
    convert_to_pull_pr_url,
    convert_to_pull_commit_url,
    convert_to_comment_url,
    split_line_break,
)


class TestGithubUtil:
    def test_convert_urls(self):
        test_cases = [
            {
                "former_url": "https://github.com/kubernetes/kubernetes/pull/120252",
                "func": convert_to_diff_url,
                "target_url": "https://patch-diff.githubusercontent.com/raw/kubernetes/kubernetes/pull/120252.diff",
            },
            {
                "former_url": "https://github.com/kubernetes/kubernetes/pull/120252",
                "func": convert_to_pull_pr_url,
                "target_url": "https://api.github.com/repos/kubernetes/kubernetes/pulls/120252",
            },
            {
                "former_url": "https://github.com/kubernetes/kubernetes/pull/120252",
                "func": convert_to_pull_commit_url,
                "target_url": "https://api.github.com/repos/kubernetes/kubernetes/pulls/120252/commits",
            },
        ]

        for tc in test_cases:
            assert tc["func"](url=tc["former_url"]) == tc["target_url"]

    def test_convert_to_diff_url(self):
        former_url = "https://github.com/kubernetes/kubernetes/pull/120252"
        target_url = "https://patch-diff.githubusercontent.com/raw/kubernetes/kubernetes/pull/120252.diff"
        assert convert_to_diff_url(url=former_url) == target_url

    def test_convert_to_pull_pr_url(self):
        former_url = "https://github.com/kubernetes/kubernetes/pull/120252"
        target_url = "https://api.github.com/repos/kubernetes/kubernetes/pulls/120252"
        assert convert_to_pull_pr_url(former_url) == target_url

    def test_convert_to_pull_commit_url(self):
        former_url = "https://github.com/kubernetes/kubernetes/pull/120252"
        target_url = (
            "https://api.github.com/repos/kubernetes/kubernetes/pulls/120252/commits"
        )
        assert convert_to_pull_commit_url(former_url) == target_url

    def test_split_line_break(self):
        former_content = "Rename listers.go to faker_listers.go\n\nSigned-off-by: kerthcet <kerthcet@gmail.com>"
        target_content = "Rename listers.go to faker_listers.go"

        assert split_line_break(former_content) == target_content
        assert split_line_break(target_content) == target_content

    def test_convert_to_commit_url(self):
        former_url = "https://github.com/InftyAI/llmlite/pull/28"
        target_url = "https://api.github.com/repos/InftyAI/llmlite/issues/28/comments"
        assert convert_to_comment_url(former_url) == target_url
