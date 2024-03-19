import pytest

from refparse.scopus import ParseScopus

test_clean_data = [
    (
        "Anglada Lluis, Abadal Ernest, ¿Qué es la ciencia abierta?, Anuario ThinkEPI, 12, pp. 292-298, (2018)",
        "Anglada Lluis, Abadal Ernest, Qué es la ciencia abierta?, Anuario ThinkEPI, 12, pp. 292-298, (2018)",
    ),
    (
        "Hoffmann S., Schonbrodt F., Elsas R., Wilson R.[., Strasser U., Boulesteix A.-L., The multiplicity of analysis strategies jeopardizes replicability: Lessons learned across disciplines, Royal Society Open Science, 8, 4, (2021)",
        "Hoffmann S., Schonbrodt F., Elsas R., Wilson R., Strasser U., Boulesteix A.-L., The multiplicity of analysis strategies jeopardizes replicability: Lessons learned across disciplines, Royal Society Open Science, 8, 4, (2021)",
    ),
    (
        "Scimago Journal & Country Rank,, (2022)",
        "Scimago Journal & Country Rank, (2022)",
    ),
    (
        "Robinson M., Henry M., Morris A., asapdiscovery/COVID_moonshot_submissions: Initial release for zenodo, version v0.1, Zenodo, (2023)",
        "Robinson M., Henry M., Morris A., asapdiscovery/COVID_moonshot_submissions: Initial release for zenodo, Zenodo, (2023)",
    ),
    (
        "Making Open Science a Reality, OECD Science, Technology, and Industry Policy Papers, No. 25, (2015)",
        "Making Open Science a Reality, OECD Science, Technology, and Industry Policy Papers, (2015)",
    ),
    (
        "Automotive radar dataset for deep learning based 3d object detection. In: 2019 16th european radar conference (EuRAD), Pp. 129–132, (2019)",
        "Automotive radar dataset for deep learning based 3d object detection. In: 2019 16th european radar conference (EuRAD), pp. 129–132, (2019)",
    ),
]

test_year_data = [
    ("Braude S.E., ESP and psychokinesis. A philosophical examination, (1979)", "1979"),
]

test_page_data = [
    (
        "Hardwicke T.E., Ioannidis J.P.A., Mapping the universe of registered reports, Nature Human Behaviour, 2, 11, pp. 793-796, (2018)",
        "793-796",
    ),
    (
        "Sayers EW, Cavanaugh M, Clark K, Ostell J, Pruitt KD, Karsch-Mizrachi I., GenBank, Nucleic Acids Res, 48, pp. D84-D86, (2020)",
        "D84-D86",
    ),
]

test_volume_issue_data = [
    (
        "Foster ED, Deardorff A., Open science framework (OSF), J Med Lib Assoc, 105, (2017)",
        ("105", None),
    ),
    (
        "Chambers CD, Tzavella L., The past, present and future of Registered Reports, Nat Hum Behav, 6, pp. 29-42, (2022)",
        ("6", None),
    ),
    (
        "Lodwick L., Sowing the seeds of future research: Data sharing, citation and reuse in archaeobotany, Open Quaternary, 5, 1, (2019)",
        ("5", "1"),
    ),
    (
        "Samuel G., Derrick G., Defining ethical standards for the application of digital tools to population health research, Bull World Health Organ, 98, 4, pp. 239-244, (2020)",
        ("98", "4"),
    ),
    (
        "Winter G., Et al., How best to use photons, Acta Cryst, D75, pp. 242-261, (2019)",
        ("D75", None),
    ),
    (
        "Peters F.R., Peters R.F., Et al., Introduction, Heritage Conservation and Social Engagement, pp. 1-5, (2020)",
        (None, None),
    ),
]


test_author_data = [
    (
        "Chan L, Cuplinskas D, Eisen M, Friend F, Genova Y, Guedon J-C, Et al., Budapest open access initiative, (2002)",
        "Chan L, Cuplinskas D, Eisen M, Friend F, Genova Y, Guedon J-C",
    ),
    (
        "Ajzen I., From intentions to actions: A theory of planned behavior., Action control, pp. 11-39, (1985)",
        "Ajzen I.",
    ),
    (
        "Breznau N., Does sociology need open science?, Societies, 11, 1, (2021)",
        "Breznau N.",
    ),
    (
        'Chang A.C., Li P., Is economics research replicable? Sixty published papers from thirteen journals say "usually not., Finance and Economics Discussion Series, 2015, 83, pp. 1-26, (2015)',
        "Chang A.C., Li P.",
    ),
    (
        "Lee S., Ditko S., Amazing Fantasy #15: Spider-Man!, (1962)",
        "Lee S., Ditko S.",
    ),
    (
        "Marcoulides, Saunders, Editor's comments: PLS: A silver bullet?, MIS Quarterly, 30, 2, (2006)",
        "Marcoulides, Saunders",
    ),
    ("Walters, 2.2 Research designs in psychology, Pychology-1st Canadian edition, (2020)", "Walters"),
]

test_parse_data = [
    (
        "(2021)",
        None,
    ),
    (
        "CRediT (Contributor Roles Taxonomy) CRT Adopters",
        None,
    ),
    (
        "4, 1, (2020)",
        None,
    ),
    (
        "Rethinking Education. Towards a Global Common Good? UNESCO. Retrieved October 28, 2015, (2015)",
        None,
    ),
    (
        "Caldwell A.R., Vigotsky A.D., Tenan M.S., Radel R., Mellor D.T., Kreutzer A., Lahart I.M., Mills J.P., Boisgontier M.P., Moving sport and exercise science forward: A call for the adoption of more transparent research practices, Sports Medicine (Auckland, N.Z.), 50, 3, pp. 449-459, (2020)",
        None,
    ),
    (
        "Lazer D., Et al., Nature, 595, pp. 189-196, (2021)",
        {
            "author": "Lazer D.",
            "title": None,
            "source": "Nature",
            "volume": "595",
            "issue": None,
            "page": "189-196",
            "year": "2021",
        },
    ),
]

test_general_data = [
    (
        "Ranking, (2015)",
        {
            "author": None,
            "title": "Ranking",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2015",
        },
    ),
    (
        "Country and Lending Groups., (2021)",
        {
            "author": None,
            "title": "Country and Lending Groups.",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2021",
        },
    ),
    (
        "Bishop K., (2011)",
        {
            "author": "Bishop K.",
            "title": None,
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2011",
        },
    ),
    (
        "Boyce D.E., Giddins G., (2022)",
        {
            "author": "Boyce D.E., Giddins G.",
            "title": None,
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2022",
        },
    ),
    (
        "Leiner D. J., SoSci Survey [Computer software], (2022)",
        {
            "author": "Leiner D. J.",
            "title": "SoSci Survey [Computer software]",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2022",
        },
    ),
    (
        "RDF Database Systems, pp. 9-40, (2015)",
        {
            "author": None,
            "title": "RDF Database Systems",
            "source": None,
            "volume": None,
            "issue": None,
            "page": "9-40",
            "year": "2015",
        },
    ),
    (
        "Chambers C.D., 49, pp. 609-610, (2013)",
        {
            "author": "Chambers C.D.",
            "title": None,
            "source": None,
            "volume": "49",
            "issue": None,
            "page": "609-610",
            "year": "2013",
        },
    ),
    (
        "IIC, the Keck Awards, (2012)",
        {
            "author": None,
            "title": "IIC, the Keck Awards",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2012",
        },
    ),
    (
        "Irreproducible biology research costs put at $28 billion per year, Nature, (2015)",
        {
            "author": None,
            "title": "Irreproducible biology research costs put at $28 billion per year",
            "source": "Nature",
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2015",
        },
    ),
    (
        "Bjork B.C., Growth of hybrid open access, 2009-2016, PeerJ, 5, (2017)",
        {
            "author": "Bjork B.C.",
            "title": "Growth of hybrid open access, 2009-2016",
            "source": "PeerJ",
            "volume": "5",
            "issue": None,
            "page": None,
            "year": "2017",
        },
    ),
    (
        "Scheub H., A review of African oral traditions and literature, Afr Stud Rev, 28, 2-3, pp. 1-72, (1985)",
        {
            "author": "Scheub H.",
            "title": "A review of African oral traditions and literature",
            "source": "Afr Stud Rev",
            "volume": "28",
            "issue": "2-3",
            "page": "1-72",
            "year": "1985",
        },
    ),
    (
        "Balland P.-A., Boschma R., Frenken K., Proximity and Innovation: From Statics to Dynamics, Regional Studies, 49, 6, pp. 907-920, (2015)",
        {
            "author": "Balland P.-A., Boschma R., Frenken K.",
            "title": "Proximity and Innovation: From Statics to Dynamics",
            "source": "Regional Studies",
            "volume": "49",
            "issue": "6",
            "page": "907-920",
            "year": "2015",
        },
    ),
    (
        "Dorch B.F., Open, transparent and honest–the way we practice research, J Nordic Perspectives on Open Science, pp. 25-30, (2015)",
        {
            "author": "Dorch B.F.",
            "title": "Open, transparent and honest–the way we practice research",
            "source": "J Nordic Perspectives on Open Science",
            "volume": None,
            "issue": None,
            "page": "25-30",
            "year": "2015",
        },
    ),
    (
        "Comer E.A., Smith C., Public involvement in the preservation and conservation of archaeology, Encyclopedia of Global Archaeology, (2020)",
        {
            "author": "Comer E.A., Smith C.",
            "title": "Public involvement in the preservation and conservation of archaeology",
            "source": "Encyclopedia of Global Archaeology",
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2020",
        },
    ),
    (
        "COVID-19 or Asymptomatic SARS-CoV-2 Infection: Results of the Phase 2a Part, Antimicrob. Agents Chemother, 66, (2022)",
        {
            "author": None,
            "title": "COVID-19 or Asymptomatic SARS-CoV-2 Infection: Results of the Phase 2a Part",
            "source": "Antimicrob. Agents Chemother",
            "volume": "66",
            "issue": None,
            "page": None,
            "year": "2022",
        },
    ),
    (
        "Bruns A., Inf. Commun. Soc., 22, pp. 1544-1566, (2019)",
        {
            "author": "Bruns A.",
            "title": None,
            "source": "Inf. Commun. Soc.",
            "volume": "22",
            "issue": None,
            "page": "1544-1566",
            "year": "2019",
        },
    ),
]


@pytest.mark.parametrize("input, expected", test_clean_data)
def test_clean(input, expected):
    assert ParseScopus.clean(input) == expected


@pytest.mark.parametrize("input, expected", test_year_data)
def test_extract_year(input, expected):
    assert ParseScopus(input).extract_year() == expected


@pytest.mark.parametrize("input, expected", test_page_data)
def test_extract_page(input, expected):
    assert ParseScopus(input).extract_page() == expected


@pytest.mark.parametrize("input, expected", test_volume_issue_data)
def test_extract_volume_issue(input, expected):
    assert ParseScopus(input).extract_volume_issue() == expected


@pytest.mark.parametrize("input, expected", test_author_data)
def test_extract_author(input, expected):
    assert ParseScopus(input).extract_author() == expected


@pytest.mark.parametrize("input, expected", test_parse_data)
def test_parse(input, expected):
    assert ParseScopus(input).parse() == expected


@pytest.mark.parametrize("input, expected", test_general_data)
def test_parse_general(input, expected):
    assert ParseScopus(input).parse_general() == expected
