import re
from typing import Optional


class ParseCssci:
    def __init__(self, ref: str):
        self.ref = ref

    @staticmethod
    def clean(ref: str) -> str:
        ref = ref.strip(".")
        ref = re.sub(r"^\d*\.", "", ref)
        # Remove unwanted info from newspaper ref
        # e.g. 3.郑晋鸣.南京城东五高校建图书馆联合体.光明日报.04.24(7)
        if re.search(r"\.\d{1,2}\.\d{1,2}(?=\(|$)", ref):
            ref = re.split(r"\.(?=\d+\.)", ref, 1)[0]
        return ref

    @staticmethod
    def drop(ref: str) -> Optional[str]:
        if re.search(r"^\d+\.\d", ref):
            return None

        elif re.search(r"^\d+\.\.$", ref):
            return None

        # e.g. 2..Campbell v. Acuff-Rose Music, Inc., 510 U. S. 569 (1994),1994
        elif re.search(r"\d{4}\),\d{4}", ref) and re.search(r"^\d+\.\.", ref):
            return None

        # Drop patent
        # e.g. 26.图书上下架机器人.CN102152293A
        elif re.search(r"\.CN\d{9}[A-Z]$", ref):
            return None

        # e.g. 9.一种基于RFID技术的自动式图书智能盘点机器人:201620075212.0.2016-01-25
        elif re.search(r"^\d+\.一种", ref):
            return None
        else:
            return ref

    def extract(self, pattern: str, ref: Optional[str] = None, flags=0) -> Optional[str]:
        if not ref:
            ref = self.ref
        match = re.search(pattern, ref, flags)
        return match.group(1) if match else None

    def extract_author(self) -> Optional[str]:
        if re.search(r"[A-Z]\.\.", self.ref):
            author = self.extract(r"^(.*\.)\.")

        elif re.search(r"^\.", self.ref):
            author = None

        else:
            author = self.ref.split(".", 1)[0]
        return author

    def parse(self) -> Optional[dict[str, Optional[str]]]:
        if self.drop(self.ref):
            self.ref = self.clean(self.ref)
            dot_count = self.ref.count(".")
            if dot_count == 0:
                return {
                    "author": None,
                    "title": self.ref,
                    "source": None,
                    "year": None,
                    "volume": None,
                    "issue": None,
                }

            volume, issue, page = None, None, None
            year = self.extract(r"[\.,](\d{4})\b")
            if year:
                volume = self.extract(r"[\.,]\d{4}\.(\d+)\b")
                issue = self.extract(r"\((\d+)\)$")
                if not (volume and issue):
                    # e.g. 22.邓万云.利用Internet开拓我州科技信息服务新领域,2006:204-208
                    page = self.extract(r":([\d-]+)$")

            author = self.extract_author()
            # 1..2021年度江苏省公共图书馆大数据统计报告
            ref_left = re.split(r"[\.,](?=\d{4}\b)", self.ref, 1)[0]
            if author:
                ref_left = ref_left.replace(author + ".", "", 1)
            else:
                ref_left = ref_left[1:]
            try:
                title, source = ref_left.rsplit(".", 1)
            except:
                title = ref_left
                source = None
            else:
                # e.g. 4..Society 5.0——科学技术政策——内阁府.2020
                if re.search(r"^\d", source):
                    title = title + "." + source
                    source = None
            return {
                "author": author,
                "title": title,
                "source": source,
                "year": year,
                "volume": volume,
                "issue": issue,
                "page": page,
            }
