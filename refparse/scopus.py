import re
from typing import Optional


class ParseScopus:
    def __init__(self, ref: str):
        self.ref = ref

    @staticmethod
    def clean(ref: str) -> str:
        # e.g. Anglada Lluis, Abadal Ernest, ¿Qué es la ciencia abierta?, Anuario ThinkEPI, 12, pp. 292-298, (2018)
        if "¿" in ref:
            ref = ref.replace("¿", "")

        # e.g. Hoffmann S., Schonbrodt F., Elsas R., Wilson R.[., Strasser U., Boulesteix A.-L., The multiplicity of analysis strategies jeopardizes replicability: Lessons learned across disciplines, Royal Society Open Science, 8, 4, (2021)
        if "[." in ref:
            ref = re.sub(r"\[\.(?=,)", "", ref)

        # remove redundant comma
        # Scimago Journal & Country Rank,, (2022)
        ref = re.sub(r",{2,}", ",", ref)

        # remove version info
        # e.g. Robinson M., Henry M., Morris A., asapdiscovery/COVID_moonshot_submissions: Initial release for zenodo, version v0.1, Zenodo, (2023)
        ref = re.sub(r", version [v\d\.]+(?=, )", "", ref, flags=re.I)

        # remove No. info
        # e.g. Making Open Science a Reality, OECD Science, Technology, and Industry Policy Papers, No. 25, (2015)
        ref = re.sub(r", no\. [\d/]+(?=, )", "", ref, flags=re.I)

        # replace "Pp" with "pp"
        # e.g. Trisovic A., Cluster analysis of open research data and a case for replication metadata, 2022 IEEE 18Th International Conference on E-Science (E-Science), Pp. 423–424, (2022)
        ref = re.sub(r"(?<=, )Pp(?=\.)", "pp", ref)
        return ref

    def parse(self) -> Optional[dict[str, Optional[str]]]:
        # only include year info
        # e.g. (2021)
        if self.ref.startswith("("):
            return None

        # not include year info
        # e.g. 25, pp. 279-283
        elif not re.search(r"\d{4}\)$", self.ref):
            return None

        # e.g. 4, 1, (2020)
        elif not re.search(r"[A-Za-z]", self.ref):
            return None

        # e.g. Caldwell A.R., Vigotsky A.D., Tenan M.S., Radel R., Mellor D.T., Kreutzer A., Lahart I.M., Mills J.P., Boisgontier M.P., Moving sport and exercise science forward: A call for the adoption of more transparent research practices, Sports Medicine (Auckland, N.Z.), 50, 3, pp. 449-459, (2020)
        elif re.search(r", (?=[^()]*\))", self.ref):
            return None

        # e.g. Rethinking Education. Towards a Global Common Good? UNESCO. Retrieved October 28, 2015, (2015)
        elif re.search(r"(?:^|[,\.] ?)Retrieved", self.ref):
            return None

        else:
            self.ref = self.clean(self.ref)
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
        pattern = r", pp\. ([A-Za-z\d-]+), "
        return self.extract(pattern, None)

    def extract_volume_issue(self) -> tuple[Optional[str], Optional[str]]:
        # e.g. Scheub H., A review of African oral traditions and literature, Afr Stud Rev, 28, 2-3, pp. 1-72, (1985)
        pattern = r", ([\d, -]+), (?=pp|\()"
        volume_issue = self.extract(pattern)
        if volume_issue:
            if ", " in volume_issue:
                volume, issue = volume_issue.split(", ")
            else:
                volume = volume_issue
                issue = None
        else:
            # e.g. Winter G., Et al., DIALS: Implementation and evaluation of a new integration package, Acta Cryst, D74, pp. 85-97, (2018)
            volume = self.extract(r", (D\d+), ")
            issue = None
        return volume, issue

    def extract_source(self, volume: Optional[str], page: Optional[str]) -> Optional[str]:
        source = self.extract(r", ([^,]*Journal of[^,]*), ")
        if not source:
            if volume:
                source = self.extract(f", ([^,]+), {volume}")
            elif not source and page:
                source = self.extract(r", ([^,]+), pp")
            elif not source:
                # only include a small part of conditions here
                source = self.extract(r", ([A-Za-z\.]+), \(")
        return source

    def extract_author(self) -> Optional[str]:
        def find_sep_loc(sep_loc_list: list[int]) -> int:
            """Process multiple `., ` match"""
            folds = [round(sep_loc_list[i] / sep_loc_list[i - 1], 2) for i in range(1, len(sep_loc_list))]
            max_fold = max(folds)
            max_fold_loc = folds.index(max_fold)
            if max_fold > 3 and (max_fold_loc + 1) / len(sep_loc_list) >= 0.5:
                return sep_loc_list[max_fold_loc]
            else:
                return sep_loc_list[-1]

        pattern1 = r", Et al\., "
        pattern2 = r"(?<=\.), "
        pattern3 = r"^((?:[A-Z][A-Za-z\-\.]*,? ?)+)(?=, [A-Z\d])"
        if re.search(pattern1, self.ref):
            author = re.split(pattern1, self.ref, 1)[0]

        elif re.search(pattern2, self.ref):
            sep_match = [i.end() for i in re.finditer(pattern2, self.ref)]
            sep_match_count = len(sep_match)
            if sep_match_count == 1:
                author = re.split(pattern2, self.ref, 1)[0]
            elif sep_match_count > 1:
                sep_loc = find_sep_loc(sep_match)
                author = self.ref[: sep_loc - 2]
        else:
            author = self.extract(pattern3)
        return author

    def parse_general(self) -> dict[str, Optional[str]]:
        comma_count = self.ref.count(", ")
        if comma_count < 3:
            author = None
            title = None
            source = None
            page = None
            if comma_count == 2:
                author_sep_count = len(re.findall(r"(?<=[A-Z])\., ", self.ref))
                # e.g. "Boyce D.E., Giddins G., (2022)"
                if author_sep_count > 1:
                    author, year = self.ref.rsplit(", ", 1)

                # e.g. Morris K., 2018/2019 Data Summary of Wet Nitrogen Deposition at Rocky Mountain National Park, (2021)
                elif author_sep_count == 1:
                    author, title, year = self.ref.split(", ", 2)

                # e.g. "RDF Database Systems, pp. 9-40, (2015)"
                elif re.search(r", pp", self.ref):
                    title, page, year = self.ref.split(", ", 2)
                    page = page[4:]

                elif re.search(r", [a-z]", self.ref):
                    # e.g. IIC, the Keck Awards, (2012)
                    title, year = self.ref.rsplit(", ", 1)
                else:
                    title, source, year = self.ref.split(", ", 2)

            elif comma_count == 1:
                # e.g. Proposal preparation instructions., (2022)
                if re.search("[A-Z]\., \(", self.ref):
                    author, year = self.ref.split(", ")
                else:
                    title, year = self.ref.split(", ")
            year = year.strip("()")
            return {
                "author": author,
                "title": title,
                "source": source,
                "volume": None,
                "issue": None,
                "page": page,
                "year": year,
            }

        elif comma_count >= 3:
            year = self.extract_year()
            page = self.extract_page()
            volume, issue = self.extract_volume_issue()
            source = self.extract_source(volume, page)
            author = self.extract_author()

            if source:
                # e.g. Kirkham J.J., Penfold N.C., Murphy F., Boutron I., Ioannidis J.P., Polka J., Moher D., Systematic examination of preprint platforms for use in the medical and biomedical sciences setting, BMJ, (Open), 10, (2020)
                if source.startswith("("):
                    ref_left = re.sub(r", \(.*$", "", self.ref)
                else:
                    source_without_bracket = source.split("(", 1)[0]
                    ref_left = re.sub(f", {source_without_bracket[:5]}.*$", "", self.ref)
            elif volume:
                ref_left = re.sub(f", {volume}.*$", "", self.ref)
            elif page:
                ref_left = re.sub(f", pp.*$", "", self.ref)
            else:
                ref_left = self.ref[:-8]

            if author:
                if len(author) >= len(ref_left):
                    title = None
                else:
                    ref_left = ref_left.replace(author, "").replace("Et al.", "").lstrip(", ")
                    if ", " in ref_left and not source:
                        title, source = ref_left.split(", ", 1)
                    else:
                        title = ref_left
            else:
                title = ref_left
            title = title if title else None
            return {
                "author": author,
                "title": title,
                "source": source,
                "volume": volume,
                "issue": issue,
                "page": page,
                "year": year,
            }
