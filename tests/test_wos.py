import pytest
from refparse.wos import ParseWos


test_doi_data = [
    ("Yao J, 2008, SCIENCE, V321, P930, DOI 10.1126/science.1157566", "10.1126/science.1157566"),
    (
        "Jiang HM, 2017, NAT CHEM BIOL, V13, P994, DOI [10.1038/NCHEMBIO.2442, 10.1038/nchembio.2442]",
        "10.1038/nchembio.2442",
    ),
    (
        "Du K-K., 2013, J CHINA U POSTS TELE, V20, P96, DOI DOI 10.1016/S1005-8885(13)60240-X",
        "10.1016/s1005-8885(13)60240-x",
    ),
]

test_page_data = [
    ("Habibi M, 2017, BIOINFORMATICS, V33, pI37, DOI 10.1093/bioinformatics/btx228", "I37"),
    ("Vaswani A., 2017, ADV NEURAL INFORM PR, P30", "30"),
]

test_volume_data = [
    ("Habibi M, 2017, BIOINFORMATICS, V33, pI37, DOI 10.1093/bioinformatics/btx228", "33"),
    ("Krallinger M., 2015, J CHEMINFORM, V7", "7"),
    ("Berg B.L., 2009, QUALITATIVE RES METH, V7th", "7th"),
    ("Lefebvre C., 2019, COCHRANE HDB SYSTEMA, V2nd ed., P67", "2nd ed."),
    ("Schmidt V., 1979, SEPM (Soc. Sediment. Geol.) Spec. Publ., VVolume 26, P175", "26"),
]

test_general_data = [
    (
        "Morin F., AISTATS 2005",
        {
            "author": "Morin F.",
            "year": None,
            "source": "AISTATS 2005",
            "volume": None,
            "page": None,
            "doi": None,
        },
    ),
    (
        "Boden Mikael, 2001, DALLAS PROJECT",
        {
            "author": "Boden Mikael",
            "year": "2001",
            "source": "DALLAS PROJECT",
            "volume": None,
            "page": None,
            "doi": None,
        },
    ),
    (
        "Bengio Yoshua, IEEE T NEURAL NETWOR, V5, P157",
        {
            "author": "Bengio Yoshua",
            "year": None,
            "source": "IEEE T NEURAL NETWOR",
            "volume": "5",
            "page": "157",
            "doi": None,
        },
    ),
    (
        "Rajpurkar P., 2016, PROC C EMPIRICAL MET, V2016, P2383, DOI DOI 10.18653/V1/D16-1264",
        {
            "author": "Rajpurkar P.",
            "year": "2016",
            "source": "PROC C EMPIRICAL MET",
            "volume": "2016",
            "page": "2383",
            "doi": "10.18653/v1/d16-1264",
        },
    ),
]

test_bilingual_data = [
    (
        "Poggio Tomaso, 2017, [International Journal of Automation and Computing, 国际自动化与计算杂志], V14, P503",
        {
            "author": "Poggio Tomaso",
            "year": "2017",
            "source": "International Journal of Automation and Computing",
            "volume": "14",
            "page": "503",
            "doi": None,
        },
    ),
    (
        "Kim Kyung Ja, 2019, [English Teaching, 영어교육], V74, P249",
        {
            "author": "Kim Kyung Ja",
            "year": "2019",
            "source": "English Teaching",
            "volume": "74",
            "page": "249",
            "doi": None,
        },
    ),
]

test_patent_data = [
    (
        "Fan P., 2011, PT, Patent No. 2011163640",
        {"type": "Patent", "author": "Fan P.", "year": "2011", "patent_title": None, "patent_number": "2011163640"},
    ),
    (
        "Redlich R. M., 2006, U. S. Patent, Patent No. [7,103,915, 7103915]",
        {"type": "Patent", "author": "Redlich R. M.", "year": "2006", "patent_title": None, "patent_number": "7103915"},
    ),
    (
        "Watanabe K., 1995, Low calorie foodstuff, aqueous paste composition, as well as production process thereof, Patent No. 5690981A",
        {
            "type": "Patent",
            "author": "Watanabe K.",
            "year": "1995",
            "patent_title": "Low calorie foodstuff, aqueous paste composition, as well as production process thereof",
            "patent_number": "5690981A",
        },
    ),
]

test_parse_data = [
    ("[Anonymous], 2017, NATURE, DOI DOI 10.1038/NATURE.2017.22094", None),
    (
        "Dodd SK., 2013, Patent No. 2013/171639 A1",
        {
            "type": "Patent",
            "author": "Dodd SK.",
            "year": "2013",
            "patent_title": None,
            "patent_number": "2013/171639 A1",
        },
    ),
    (
        "Wang X, 2019, BIOINFORMATICS, V35, P1745, DOI 10.1093/bioinformatics/bty869",
        {
            "author": "Wang X",
            "year": "2019",
            "source": "BIOINFORMATICS",
            "volume": "35",
            "page": "1745",
            "doi": "10.1093/bioinformatics/bty869",
        },
    ),
]


@pytest.mark.parametrize("input, expected", test_doi_data)
def test_extract_doi(input, expected):
    assert ParseWos.extract_doi(input) == expected


@pytest.mark.parametrize("input, expected", test_page_data)
def test_extract_page(input, expected):
    assert ParseWos.extract_page(input) == expected


@pytest.mark.parametrize("input, expected", test_volume_data)
def test_extract_volume(input, expected):
    assert ParseWos.extract_volume(input) == expected


@pytest.mark.parametrize("input, expected", test_general_data)
def test_parse_general(input, expected):
    assert ParseWos(input).parse_general() == expected


@pytest.mark.parametrize("input, expected", test_bilingual_data)
def test_parse_bilingual(input, expected):
    assert ParseWos(input).parse_bilingual() == expected


@pytest.mark.parametrize("input, expected", test_patent_data)
def test_parse_patent(input, expected):
    assert ParseWos(input).parse_patent() == expected


@pytest.mark.parametrize("input, expected", test_parse_data)
def test_parse(input, expected):
    assert ParseWos(input).parse() == expected
