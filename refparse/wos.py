from typing import Optional
import re


class ParseWos:
    def __init__(self, ref: str):
        self.ref = self.clean(ref)

    @staticmethod
    def clean(ref: str) -> str:
        # Remove duplicated commas. e.g. ForeRunner3D,, 2020, DOES HP MULTIJET FUS
        ref = re.sub(r",{2,}", ",", ref)

        # Remove blank spaces before commas.
        # e.g. Afshinmanesh F, 2005, EUROCON 2005: THE INTERNATIONAL CONFERENCE ON COMPUTER AS A TOOL, VOL 1 AND 2 , PROCEEDINGS, P217
        ref = re.sub(r" ,", ",", ref)
        return ref

    def parse(self):
        if self.ref.startswith("[Anonymous]"):
            return None
        elif "Patent No." in self.ref:
            return self.parse_patent()
        elif re.search(r"\d{4}, \[", self.ref):
            return self.parse_bilingual()
        else:
            return self.parse_general()

    @staticmethod
    def extract_doi(entry: str) -> Optional[str]:
        """Extract DOI from a reference entry."""
        if ", DOI [" in entry:
            doi_part = re.split(r", DOI (?=\[)", entry, maxsplit=1)[1]
            doi_list = doi_part.strip("[]").split(", ")
            doi_set = set(doi.replace("DOI ", "").lower() for doi in doi_list)
            if len(doi_set) == 1:
                doi = doi_set.pop()
            elif len(doi_set) > 1:
                doi = "; ".join(doi_set)
        elif ", DOI " in entry:
            doi_match = re.search(r"DOI (10\..*)$", entry)
            if doi_match:
                doi = doi_match.group(1).lower()
        else:
            doi = None
        return doi

    @staticmethod
    def extract_page(entry: str) -> Optional[str]:
        """Extract page number from a reference entry."""
        page_match = re.search(r", p([A-Za-z\d]+)(?=, DOI|$)", entry, flags=re.I)
        page = page_match.group(1) if page_match else None
        return page

    @staticmethod
    def extract_volume(entry: str) -> Optional[str]:
        """Extract volume number from a reference entry."""
        if re.search(", vol", entry, flags=re.I):
            volume_match = re.search(r"vol[s\.]? ([\w\-: ]+)(?=, |$)", entry, flags=re.I)
        elif re.search(", vvolume", entry, flags=re.I):
            volume_match = re.search(r", vvolume (\d+)(?=, |$)", entry, flags=re.I)
        else:
            volume_match = re.search(r", v([\w\-\. ]+)(?=(, |$))", entry, flags=re.I)
        return volume_match.group(1) if volume_match else None

    def parse_general(self) -> dict[str, Optional[str]]:
        if re.search(r", \d{4}, ", self.ref):
            parts = self.ref.split(", ", maxsplit=3)
            author = parts[0]
            year = parts[1]
            source = parts[2]
        else:
            parts = self.ref.split(", ", maxsplit=2)
            author = parts[0]
            year = None
            source = parts[1]
        volume = self.extract_volume(self.ref)
        page = self.extract_page(self.ref)
        doi = self.extract_doi(self.ref)
        return {
            "author": author,
            "year": year,
            "source": source,
            "volume": volume,
            "page": page,
            "doi": doi,
        }

    def parse_bilingual(self) -> dict[str, Optional[str]]:
        fields = re.split(r", (?![^\[]*\])", self.ref)
        author = fields[0]
        year = fields[1]
        source = fields[2]
        if author.startswith("["):
            if re.search(r"\[[A-Za-z]+ ", author):
                author_eng, author_non_eng = re.split(r" (?=[^A-Za-z]+)", author.strip("[]"), maxsplit=1)
            else:
                author_non_eng, author_eng = re.split(r"(?=[^A-Za-z]+) (?=[A-Za-z]+ )", author.strip("[]"), maxsplit=1)
        else:
            author_eng, author_non_eng = None, None
            if re.search(r"^[A-Za-z]+ ", author):
                author_eng = author
            else:
                author_non_eng = author

        if re.search(r"\[[A-Za-z]+ ", source):
            source_eng, source_non_eng = re.split(r", (?=[^A-Za-z]+)", source.strip("[]"), maxsplit=1)
        else:
            source_non_eng, source_eng = re.split(r"(?=[^A-Za-z]+), (?=[A-Za-z]+ )", source.strip("[]"), maxsplit=1)
        volume = self.extract_volume(self.ref)
        page = self.extract_page(self.ref)
        doi = self.extract_doi(self.ref)
        return {
            "author": author_eng,
            "year": year,
            "source": source_eng,
            "volume": volume,
            "page": page,
            "doi": doi,
        }

    def parse_patent(self) -> dict[str, Optional[str]]:
        """Parse a patent reference from Web of Science."""
        first_part, patent_num_part = self.ref.split(", Patent No. ")
        if patent_num_part.startswith("["):
            patent_number_str = patent_num_part.strip("[]")
            patent_number_list = patent_number_str.split(", ")
            patent_number_set = set(i.replace(",", "") for i in patent_number_list)
            patent_number = "; ".join(patent_number_set)
        else:
            patent_number = patent_num_part

        fields = first_part.split(", ", maxsplit=2)
        author = fields[0]
        year = fields[1]

        try:
            # Fan P., 2011, PT, Patent No. 2011163640
            if fields[2] == "PT":
                title = None

            # Redlich R. M., 2006, U. S. Patent, Patent No. [7,103,915, 7103915]
            elif fields[2].endswith("Patent"):
                title = None

            else:
                title = fields[2]

        except IndexError:
            # Pingchen Fan PZ, 2017, Patent No. [US9745268B2, 9745268]
            title = None

        return {
            "type": "Patent",
            "author": author,
            "year": year,
            "patent_title": title,
            "patent_number": patent_number,
        }
