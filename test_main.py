from unittest import TestCase

from main import replace_content, BlogEntry, fetch_and_parse_rss_feed

EXPECTED_CONTENT = "This is expected content in target block"

EXPECTED_RESULT = """#Header

<!-- blog starts -->
""" + EXPECTED_CONTENT + """
<!-- blog ends -->

And some content **not** to replace."""


class Test(TestCase):
    def test_replace_content_for_block(self):
        # given
        test_readme_file = open("testREADME.md", "r")

        # when
        replaced_content = replace_content(
            content=test_readme_file.read(),
            block_marker="blog",
            new_content=EXPECTED_CONTENT
        )

        # then
        self.assertEqual(
            EXPECTED_RESULT,
            replaced_content
        )

        test_readme_file.close()

    def test_parse_xml_rss(self):
        # given
        expected_entries = [
            BlogEntry(
                title='Flutter Day 1 - Getting to Know Dart',
                url='https://medium.com/@kamaldgrt/flutter-diaries-day-1-getting-to-know-dart-376e28fa3a8',
                published='22-8-2020'
            ),
        ]

        # when
        parsed = fetch_and_parse_rss_feed('@kamaldgrt')

        # then
        self.assertEqual(parsed, expected_entries)
