import re
from dataclasses import dataclass

import feedparser

MAX_FETCHED_BLOG_POSTS = 5
README_FILE_NAME = 'README.md'


@dataclass
class BlogEntry:
    title: str
    url: str
    published: str


def fetch_and_parse_rss_feed(rss_feed: str) -> list:
    entries = feedparser.parse(rss_feed)["entries"][:MAX_FETCHED_BLOG_POSTS]
    return [
        BlogEntry(
            title=entry["title"],
            url=entry["link"],
            published=parse_date(entry),
        )
        for entry in entries
    ]


def parse_date(entry):
    published = entry["published_parsed"]

    return f'{published.tm_mday}-{published.tm_mon}-{published.tm_year}'


def parse_to_markdown(blog_entries: list) -> str:
    return "\n".join([
        f'* [{entry.title}]({entry.url}) - {entry.published}'
        for entry in blog_entries
    ])


def replace_content(content: str, block_marker: str, new_content: str) -> str:
    expression = re.compile(
        r"<!\-\- {} starts \-\->.*<!\-\- {} ends \-\->".format(block_marker, block_marker),
        re.DOTALL,
    )
    chunk = "<!-- {} starts -->\n{}\n<!-- {} ends -->".format(block_marker, new_content, block_marker)

    return expression.sub(chunk, content)


if __name__ == "__main__":
    entries = fetch_and_parse_rss_feed("https://medium.com/feed/@kamaldgrt")

    new_content_markdown = parse_to_markdown(entries)

    replaced_content = replace_content(open(README_FILE_NAME, 'r').read(), "blog", new_content_markdown)

    print(replaced_content)

    open(README_FILE_NAME, 'w').write(replaced_content)
