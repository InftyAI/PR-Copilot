import re


def parse_content(content: str) -> str:
    """
    Remove useless messages from the content, like words wrapped by <!-- -->.
    """
    if content is None:
        return None

    append = True
    res = ""

    for line in content.splitlines():
        pattern = re.compile(r"<!--([\s\S]*)-->")
        line = pattern.sub("", line)

        if "<!--" in line:
            append = False

        if append:
            res += line + "\n"

        if "-->" in line:
            append = True

    return res
