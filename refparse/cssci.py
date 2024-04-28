import re
from typing import Optional


class ParseCssci:
    def __init__(self, ref: str):
        self.ref = self.clean(ref)
        self.dot_count = self.ref.count(".")

    @staticmethod
    def clean(ref: str) -> str:
        return re.sub(r"^\d*\.", "", ref)

    def parse(self):
        # Web resource
        if re.search(r"\.\d{4}$", self.ref):
            return self.parse_web()

        if re.search(r"[\u4e00-\u9fa5]", self.ref):
            if "GB/" in self.ref:
                return self.parse_standard()

            elif self.ref[-3:] == "出版社":
                return self.parse_book()

            elif ":学位论文." in self.ref:
                return self.parse_thesis()

            # Newspaper
            elif re.search(r"[^\d]\.\d{1,2}\.\d{1,2}", self.ref):
                return self.parse_newspaper()

            # Patent 1
            elif re.search(r"\.CN\d{9}[A-Z]$", self.ref):
                return self.parse_patent1()

            # Patent 2
            elif re.search(r"^一种", self.ref):
                return self.parse_patent2()

            else:
                return self.parse_paper()
        else:
            return self.parse_english()

    def parse_web(self) -> dict[str, Optional[str]]:
        if self.dot_count == 2:
            author, title, year = self.ref.split(".")
        elif self.dot_count > 2:
            author = self.ref.split(".", 1)[0]
            year = self.ref.rsplit(".", 1)[1]
            title = self.ref.replace(author + ".", "").replace("." + year, "")
        if author == "":
            author = None
        return {"type": "web", "author": author, "title": title, "year": year}

    def parse_standard(self) -> dict[str, Optional[str]]:
        if "出版社" in self.ref:
            year = None
            if self.dot_count == 2:
                author, title, source = self.ref.split(".")
            elif self.dot_count > 2:
                author = self.ref.split(".", 1)[0]
                source = self.ref.rsplit(".", 1)[1]
                title = self.ref.split(".", 1)[1].replace("." + source, "")
        else:
            source = None
            author = self.ref.split(".", 1)[0]
            if re.search(r",\d{4}$", self.ref):
                year = self.ref[-4:]
                title = self.ref.split(".", 1)[1].replace("," + year, "")
            else:
                year = None
                title = self.ref.split(".", 1)[1]

        if author == "":
            author = None
        if title.startswith("GB/"):
            identifier, title = re.split(r"[,，] ?", title, 1)
        else:
            title, identifier = re.split(r":(?=GB)", title, 1)
        return {
            "type": "standard",
            "author": author,
            "title": title,
            "source": source,
            "year": year,
            "identifier": identifier,
        }

    def parse_book(self) -> dict[str, Optional[str]]:
        author, title, source = self.ref.split(".")
        return {"type": "book", "author": author, "title": title, "source": source}

    def parse_thesis(self) -> dict[str, Optional[str]]:
        author, title, other = self.ref.split(".", 2)
        title = title[:-5]
        source, year = other.split(",")
        year = year if len(year) == 4 else year[:4]
        return {"type": "thesis", "author": author, "title": title, "source": source, "year": year}

    def parse_newspaper(self) -> dict[str, Optional[str]]:
        author, title, source, date = self.ref.split(".", 3)
        if author == "":
            author = None
        date = date.split("(", 1)[0]
        return {"type": "newspaper", "author": author, "title": title, "source": source, "date": date}

    def parse_patent1(self) -> dict[str, Optional[str]]:
        title, identifier = self.ref.split(".", 1)
        return {"type": "patent", "title": title, "identifier": identifier}

    def parse_patent2(self) -> dict[str, Optional[str]]:
        title, other = self.ref.split(":", 1)
        identifier = other.rsplit(".", 1)[0]
        identifier = re.sub(r"^[^\d]*(?=\d)", "", identifier)
        return {"type": "patent", "title": title, "identifier": identifier}

    def parse_paper(self) -> dict[str, Optional[str]]:
        author, title, source, year, volume_issue = self.ref.split(".", 4)
        if volume_issue.startswith("("):
            volume = None
            issue = volume_issue.strip("()")
        else:
            volume, issue = volume_issue.split("(")
            issue = issue.strip(")")
        return {
            "type": "paper",
            "author": author,
            "title": title,
            "source": source,
            "year": year,
            "volume": volume,
            "issue": issue,
        }

    def parse_english(self) -> dict[str, Optional[str]]:
        def split_author_title(ref_left: str):
            if ".." in self.ref:
                author, title = ref_left.split("..", 1)
                author += "."

            else:
                dot_count = ref_left.count(".")
                if dot_count == 1:
                    author, title = ref_left.split(".", 1)

                elif dot_count > 1:
                    author, title = ref_left.rsplit(".", 1)
                else:
                    author, title = None, None
            return author, title

        # English book
        if re.search(r":[A-Z]", self.ref):
            try:
                ref_left, year_page = re.split(r",(?=\d{4})", self.ref, 1)
            except ValueError:
                ref_left = self.ref
                year = None
                page = None
            else:
                year = year_page[:4]
                page = year_page[5:]

            if re.search(r"\.[A-Z][A-Za-z()]+:", ref_left):
                ref_left, source = ref_left.rsplit(".", 1)

            elif re.search(r"\.(?:[A-Z][A-Za-z]+ ){1,2}[A-Z][A-Za-z]+:[A-Z]", ref_left):
                ref_left, source = ref_left.rsplit(".", 1)

            else:
                ref_left, source = ref_left.rsplit(":", 1)

            author, title = split_author_title(ref_left)
            return {
                "type": "english-book",
                "author": author,
                "title": title,
                "source": source,
                "year": year,
                "page": page,
            }

        # English paper
        ref_left, year_volume_issue = re.split(r"\.(?=\d{4})", self.ref, 1)
        year = year_volume_issue.split(".", 1)[0]
        issue = year_volume_issue.split("(", 1)[1].strip(")")
        if ".(" in year_volume_issue:
            volume = None
        else:
            volume = year_volume_issue.split("(", 1)[0][5:]

        ref_left, source = ref_left.rsplit(".", 1)
        author, title = split_author_title(ref_left)

        return {
            "type": "english-paper",
            "author": author,
            "title": title,
            "source": source,
            "year": year,
            "volume": volume,
            "issue": issue,
        }
