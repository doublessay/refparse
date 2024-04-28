import re
from typing import Optional


class ParseScopus:
    def __init__(self, ref: str):
        self.ref = ref

    @staticmethod
    def clean(ref: str) -> str:
        # Remove duplicate comma
        # e.g. Scimago Journal & Country Rank,, (2022)
        ref = re.sub(r",{2,}", ",", ref)

        # Remove duplicate blank
        # e.g. Huang J., Zhou M., Yang D., Extracting chatbot knowledge from online discussion forums,  International Joint Conference on artificial intelligence, (2007)
        ref = re.sub(r" {2,}", " ", ref)

        # Remove duplicate dot
        # e.g. Von Wangenheim C.G., et al.., Creating software process capability/maturity models, IEEE Software, 27, 4, pp. 92-94, (2010)
        ref = re.sub(r"\.{2,}", ".", ref)

        # Remove individual no. info
        # e.g. Making Open Science a Reality, OECD Science, Technology, and Industry Policy Papers, No. 25, (2015)
        ref = re.sub(r"(?<=[^\d]), no\.? [^,]+", "", ref, flags=re.I)

        # Remove individual suppl. info
        # e.g. Webb R., Gong J.G., Rusbridge S.M., Control of ovarian function in cattle, J. Reprod. Fert., SUPPL. 45, pp. 141-156, (1992)
        ref = re.sub(r"(?<=[^\d]), suppl\.? [^,]+", "", ref, flags=re.I)

        # Replace "Pp" with "pp"
        # e.g. Trisovic A., Cluster analysis of open research data and a case for replication metadata, 2022 IEEE 18Th International Conference on E-Science (E-Science), Pp. 423–424, (2022)
        ref = re.sub(r"(?<=, )Pp(?=\.)", "pp", ref)

        # Replace ", et al." with ", Et al."
        # e.g. Von Wangenheim C.G., et al.., Creating software process capability/maturity models, IEEE Software, 27, 4, pp. 92-94, (2010)
        ref = ref.replace(", et al.", ", Et al.")

        # Remove issue symbol
        ref = re.sub(r"\bno\.? ([^,]+)", r"\1", ref, flags=re.I)
        ref = re.sub(r"\bsuppl\.? ([^,]+)", r"\1", ref, flags=re.I)

        # Remove volume symbol
        ref = re.sub(r"\bvol\.? ([^,]+)", r"\1", ref, flags=re.I)

        # Add page symbol
        if re.search(r", \d+-\d+, \(", ref):
            if not re.search(r", \d{4}-\d{4}, ", ref):
                match = re.search(r", (\d+-\d+), ", ref).group(1)
                if re.search(r"\d, \d+-", ref):
                    a, b = (int(i) for i in match.split("-"))
                    # Exclude possible issue
                    if b - a != 1:
                        ref = ref.replace(match, f"pp. {match}", 1)
                else:
                    ref = ref.replace(match, f"pp. {match}", 1)
        return ref

    @staticmethod
    def drop(ref: str) -> Optional[str]:
        # Not start with [A-Z\d]
        if not re.search(r"^[A-Za-z\d]", ref):
            return None

        # Not include year info
        elif not re.search(r"\(\d{4}\)$", ref):
            return None

        # Not include English chars
        elif not re.search(r"[A-Za-z]", ref):
            return None

        # Count of "(" and ")" not equal
        elif ref.count("(") != ref.count(")"):
            return None

        # Don't parse patent
        elif re.search(r", Patent No\.", ref):
            return None

        # Don't parse thesis
        elif re.search(r" thesis,", ref, flags=re.I):
            return None

        else:
            return ref

    def parse(self) -> Optional[dict[str, Optional[str]]]:
        if self.drop(self.ref):
            self.ref = self.clean(self.ref)
            comma_count = self.ref.count(", ")
            # Reference info is incomplete
            if comma_count < 3:
                return self.parse_missing()
            else:
                return self.parse_general()

    def extract(self, pattern: str, ref: Optional[str] = None, flags=0) -> Optional[str]:
        if not ref:
            ref = self.ref
        match = re.search(pattern, ref, flags)
        return match.group(1) if match else None

    def extract_year(self) -> Optional[str]:
        pattern = r", \((\d{4})\)$"
        return self.extract(pattern)

    def extract_page(self) -> Optional[str]:
        pattern = r", pp\. ([a-z\d–-]+), "
        return self.extract(pattern, flags=re.I)

    def extract_issue(self) -> Optional[str]:
        pattern = r" \d+, ([a-z]?[\d–-]+), (?=pp|\()"
        return self.extract(pattern, flags=re.I)

    def extract_volume(self) -> Optional[str]:
        pattern = r", ([a-z]?\d+), (?=[a-z]?\d|pp|\()"
        return self.extract(pattern, flags=re.I)

    def extract_source(self, volume: Optional[str], page: Optional[str]) -> Optional[str]:
        source = None

        # Put off when encountering conference ref
        conf_pattern = r"conference|conf\.|proceeding|proc\.|committee|convention|congress|symposium"
        if re.search(conf_pattern, self.ref, flags=re.I):
            pass

        # Put off if source may contain comma
        elif re.search(r", [^\(]+\)", self.ref):
            pass

        elif volume:
            source = self.extract(f", ([A-Z][^,]+), {volume}")
        elif not source and page:
            source = self.extract(r", ([A-Z][^,]+), pp")
        elif not source:
            source = self.extract(r", ([A-Za-z\.]+), \(")

        if source and source.startswith("("):
            source = None
        return source

    def extract_author(self):
        if ", Et al." in self.ref:
            author = re.split(r", Et al\., ", self.ref, 1)[0]

        elif re.search(r"[A-Z]\., ", self.ref):
            sep_match = [i.end() for i in re.finditer(r"[A-Z]\., ", self.ref)]
            sep_match_count = len(sep_match)
            if sep_match_count == 1:
                author = re.split(r"(?<=[A-Z]\.), ", self.ref, 1)[0]
            elif sep_match_count > 1:
                last = sep_match[-1]
                second_to_last = sep_match[-2]
                third_to_last = sep_match[-3] if sep_match_count > 2 else 0

                # Here the threshold is a experienced value
                if (last - second_to_last) / (second_to_last - third_to_last) > 3:
                    sep_loc = second_to_last
                else:
                    sep_loc = last
                author = self.ref[: sep_loc - 2]

        else:
            author = self.extract(r"^((?:[A-Z][A-Za-z\-\.']*,? ?)+)(?=, [A-Z\d])")
            if not author:
                author = self.extract(r"^([A-Z][A-Za-z_-]+), ")
        return author

    def parse_general(self) -> dict[str, Optional[str]]:
        year = self.extract_year()
        page = self.extract_page()
        issue = self.extract_issue()
        volume = self.extract_volume()
        source = self.extract_source(volume, page)
        author = self.extract_author()
        title = "unknown"

        # Field source may erroneous
        if source and author:
            # Treat last author as source
            # e.g. Islam N., Ray B., Pasandideh F., pp. 270-276, (2020)
            if source in author:
                if source.count(" ") <= 1:
                    title = None
                    source = None
                # e.g. Lei C., Wu Y., Sankaranarayanan A.C., Chang S.M., Guo B., Sasaki N., Kobayashi H., Sun C.W., Ozeki Y., Goda K., IEEE Photonics J., 9, (2017)
                else:
                    title = None
                    author = author.rsplit(", ", 1)[0]

            # Treat title as source
            elif f"Et al., {source[:20]}" in self.ref or f"{author[-5:]}, {source[:20]}" in self.ref:
                if source.count(" ") > 3:
                    title = source
                    source = None
                else:
                    title = None

        # Extract title info
        if title == "unknown":
            # Remove other fields info
            if source:
                repr_str = re.match(r"([A-Za-z\d\. ]{,20})", source)[1]
                ref_left = re.sub(f", {repr_str}.*$", "", self.ref)
            elif volume:
                ref_left = re.sub(f", {volume}.*$", "", self.ref)
            elif page:
                ref_left = re.sub(f", pp.*$", "", self.ref)
            else:
                ref_left = self.ref[:-8]

            if author:
                bare_ref_left = ref_left.replace(", Et al.", "")
                if len(author) < len(bare_ref_left):
                    ref_left = bare_ref_left.replace(author, "", 1).lstrip(", ")
                    if not source:
                        # e.g. Hansen V.L., Changing Gods in Medieval China, 1127-1276, (1990)
                        if re.search(r", \d+\-", ref_left):
                            title = ref_left

                        elif re.search(r", [A-Z\d]", ref_left):
                            title, source = re.split(r", (?=[A-Z\d])", ref_left, 1)

                        # e.g. Amodei D., Olah C., Steinhardt J., Christiano P., Schulman J., Mane D., Concrete Problems in Ai Safety., (2016)
                        # End with "." and less than 5 words in this piece will be seemed as source
                        elif ref_left.endswith(".") and ref_left.count(" ") < 4:
                            source = ref_left
                            title = None
                        else:
                            title = ref_left
                    else:
                        title = ref_left
                else:
                    title = None
            else:
                if not source:
                    if re.search(r", [A-Z\d]", ref_left):
                        title, source = re.split(r", (?=[A-Z\d])", ref_left, 1)
                    else:
                        title = ref_left
                else:
                    title = ref_left

        return {
            "author": author,
            "title": title,
            "source": source,
            "volume": volume,
            "issue": issue,
            "page": page,
            "year": year,
        }

    def parse_missing(self) -> Optional[dict[str, Optional[str]]]:
        author = None
        title = None
        source = None
        page = None

        # e.g. "Boyce D.E., Giddins G., (2022)"
        if re.search(r"[A-Z]\., \(", self.ref):
            author, year = self.ref.rsplit(", ", 1)

        # e.g. Morris K., 2018/2019 Data Summary of Wet Nitrogen Deposition at Rocky Mountain National Park, (2021)
        elif re.search(r"[A-Z]\.?, [A-Z\d]", self.ref):
            author, title, year = self.ref.split(", ")

        # e.g. COMEST, Preliminary study on the ethics of Artificial Intelligence, (2019)
        elif re.search(r"^[A-Z]+, [A-Z\d]", self.ref):
            author, title, year = self.ref.split(", ", 2)

        elif re.search(r"[a-z], [A-Z\d]", self.ref):
            parts = self.ref.split(", ")
            # e.g. ACM Policy Council, Statement on algorithmic transparency and accountability, (2017)
            if parts[0].count(" ") <= parts[1].count(" "):
                author, title, year = parts
            else:
                # e.g. MIT Media Lab, Moral Machine, (2016)
                if re.search(r"^[A-Z]+\b", self.ref):
                    author, title, year = parts
                # e.g. DroneHunter: Net Gun Drone Capture: Products, Fortem Technologies, (2021)
                else:
                    title, source, year = parts

        elif ", pp." in self.ref:
            # e.g. Ahn H., pp. 709-715, (2006)
            if "., " in self.ref:
                author, page, year = self.ref.split(", ", 2)
            else:
                # e.g. Consolidated Version of the Treaty on European Union, pp. 13-46, (2009)
                title, page, year = self.ref.split(", ", 2)
            page = page[4:]

        # e.g. IIC, the Keck Awards, (2012)
        elif re.search(r", [a-z]", self.ref):
            title, year = self.ref.rsplit(", ", 1)

        elif self.ref.count(", ") == 1:
            title, year = self.ref.split(", ", 1)

        try:
            year = year.strip("()")
        except UnboundLocalError:
            return None
        else:
            return {
                "author": author,
                "title": title,
                "source": source,
                "volume": None,
                "issue": None,
                "page": page,
                "year": year,
            }
