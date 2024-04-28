import pytest

from refparse.scopus import ParseScopus

test_clean_data = [
    (
        "Scimago Journal & Country Rank,, (2022)",
        "Scimago Journal & Country Rank, (2022)",
    ),
    (
        "Making Open Science a Reality, OECD Science, Technology, and Industry Policy Papers, No. 25, (2015)",
        "Making Open Science a Reality, OECD Science, Technology, and Industry Policy Papers, (2015)",
    ),
    (
        "Automotive radar dataset for deep learning based 3d object detection. In: 2019 16th european radar conference (EuRAD), Pp. 129–132, (2019)",
        "Automotive radar dataset for deep learning based 3d object detection. In: 2019 16th european radar conference (EuRAD), pp. 129–132, (2019)",
    ),
    (
        "Hamada I., Yoshida H.K., Physica, 376-377, (2006)",
        "Hamada I., Yoshida H.K., Physica, pp. 376-377, (2006)",
    ),
    (
        "Mubin O., Stevens C.J., Shahid S., Al Mahmud A., Dong J.J., A review of the applicability of robots in education, Journal of Technology in Education and Learning, 1, 209-15, (2013)",
        "Mubin O., Stevens C.J., Shahid S., Al Mahmud A., Dong J.J., A review of the applicability of robots in education, Journal of Technology in Education and Learning, 1, pp. 209-15, (2013)",
    ),
    (
        "Marcellin P., Hepatitis C: The clinical spectrum of the disease, J Hepatol, 31, SUPPL. 1, pp. 9-16, (1999)",
        "Marcellin P., Hepatitis C: The clinical spectrum of the disease, J Hepatol, 31, 1, pp. 9-16, (1999)",
    ),
    (
        "Goodfellow I., Bengio Y., Courville A., Bengio Y., Deep Learning, vol. 1, (2016)",
        "Goodfellow I., Bengio Y., Courville A., Bengio Y., Deep Learning, 1, (2016)",
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

test_issue_data = [
    (
        "Lodwick L., Sowing the seeds of future research: Data sharing, citation and reuse in archaeobotany, Open Quaternary, 5, 1, (2019)",
        "1",
    ),
]

test_volume_data = [
    (
        "Foster ED, Deardorff A., Open science framework (OSF), J Med Lib Assoc, 105, (2017)",
        "105",
    ),
    (
        "Marcellin P., Hepatitis C: The clinical spectrum of the disease, J Hepatol, 31, pp. 9-16, (1999)",
        "31",
    ),
]

test_author_data = [
    (
        "Chan L, Cuplinskas D, Eisen M, Friend F, Genova Y, Guedon J-C, Et al., Budapest open access initiative, (2002)",
        "Chan L, Cuplinskas D, Eisen M, Friend F, Genova Y, Guedon J-C",
    ),
    (
        "Breznau N., Does sociology need open science?, Societies, 11, 1, (2021)",
        "Breznau N.",
    ),
    (
        "Ajzen I., From intentions to actions: A theory of planned behavior., Action control, pp. 11-39, (1985)",
        "Ajzen I.",
    ),
    (
        "Lee S., Ditko S., Amazing Fantasy #15: Spider-Man!, (1962)",
        "Lee S., Ditko S.",
    ),
    (
        "Marcoulides, Saunders, Editor's comments: PLS: A silver bullet?, MIS Quarterly, 30, 2, (2006)",
        "Marcoulides, Saunders",
    ),
    (
        "Walters, 2.2 Research designs in psychology, Pychology-1st Canadian edition, (2020)",
        "Walters",
    ),
    (
        "Minasny B., Hopmans J.W., Harter T., Eching S.O., Tuli A., Denton M.A., Neural networks prediction of soil hydraulic functions for alluvial soils using multistep outflow data, Soil Sci. Soc. Am. J., 68, 2, pp. 417-429, (2004)",
        "Minasny B., Hopmans J.W., Harter T., Eching S.O., Tuli A., Denton M.A.",
    ),
]

test_drop_data = [
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
        "Kaan K., Ying L., Machine Vision Technology for Shelf Inventory Management, Patent No. US20150262116A1, (2014)",
        None,
    ),
    (
        "Lowerre B.T., The HARPY speech recognition system. Ph.D. thesis, Carnegie Mellon University, (1976)",
        None,
    ),
    (
        "Durkota K., Lisy V., Computing optimal policies for attack graphs with action failures and costs, 7th European Starting AI Researcher Symposium (STAIRS, 14, (2014)",
        None,
    ),
    (
        "Hamada I., Yoshida H.K., Physica, 376-377, (2006)",
        "Hamada I., Yoshida H.K., Physica, 376-377, (2006)",
    ),
]

test_parse_data = [
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

test_missing_data = [
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
        "COMEST, Preliminary study on the ethics of Artificial Intelligence, (2019)",
        {
            "author": "COMEST",
            "title": "Preliminary study on the ethics of Artificial Intelligence",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2019",
        },
    ),
    (
        "ACM Policy Council, Statement on algorithmic transparency and accountability, (2017)",
        {
            "author": "ACM Policy Council",
            "title": "Statement on algorithmic transparency and accountability",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2017",
        },
    ),
    (
        "MIT Media Lab, Moral Machine, (2016)",
        {
            "author": "MIT Media Lab",
            "title": "Moral Machine",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2016",
        },
    ),
    (
        "DroneHunter: Net Gun Drone Capture: Products, Fortem Technologies, (2021)",
        {
            "author": None,
            "title": "DroneHunter: Net Gun Drone Capture: Products",
            "source": "Fortem Technologies",
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2021",
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
        "Ahn H., pp. 709-715, (2006)",
        {
            "author": "Ahn H.",
            "title": None,
            "source": None,
            "volume": None,
            "issue": None,
            "page": "709-715",
            "year": "2006",
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
]

test_general_data = [
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
    (
        "Burns K., The History and Development of Algorithms in Music Composition, 1957-1993, (1994)",
        {
            "author": "Burns K.",
            "title": "The History and Development of Algorithms in Music Composition, 1957-1993",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "1994",
        },
    ),
    (
        "Komer B., Bergstra J., Eliasmith C., Hyperopt-sklearn: automatic hyperparameter configuration for scikit-learn, Proceedings of the 13th Python in Science Conference, pp. 32-7, (2014)",
        {
            "author": "Komer B., Bergstra J., Eliasmith C.",
            "title": "Hyperopt-sklearn: automatic hyperparameter configuration for scikit-learn",
            "source": "Proceedings of the 13th Python in Science Conference",
            "volume": None,
            "issue": None,
            "page": "32-7",
            "year": "2014",
        },
    ),
    (
        "Caldwell A.R., Vigotsky A.D., Tenan M.S., Radel R., Mellor D.T., Kreutzer A., Lahart I.M., Mills J.P., Boisgontier M.P., Moving sport and exercise science forward: A call for the adoption of more transparent research practices, Sports Medicine (Auckland, N.Z.), 50, 3, pp. 449-459, (2020)",
        {
            "author": "Caldwell A.R., Vigotsky A.D., Tenan M.S., Radel R., Mellor D.T., Kreutzer A., Lahart I.M., Mills J.P., Boisgontier M.P.",
            "title": "Moving sport and exercise science forward: A call for the adoption of more transparent research practices",
            "source": "Sports Medicine (Auckland, N.Z.)",
            "volume": "50",
            "issue": "3",
            "page": "449-459",
            "year": "2020",
        },
    ),
    (
        "Islam N., Ray B., Pasandideh F., pp. 270-276, (2020)",
        {
            "author": "Islam N., Ray B., Pasandideh F.",
            "title": None,
            "source": None,
            "volume": None,
            "issue": None,
            "page": "270-276",
            "year": "2020",
        },
    ),
    (
        "Lei C., Wu Y., Sankaranarayanan A.C., Chang S.M., Guo B., Sasaki N., Kobayashi H., Sun C.W., Ozeki Y., Goda K., IEEE Photonics J., 9, (2017)",
        {
            "author": "Lei C., Wu Y., Sankaranarayanan A.C., Chang S.M., Guo B., Sasaki N., Kobayashi H., Sun C.W., Ozeki Y., Goda K.",
            "title": None,
            "source": "IEEE Photonics J.",
            "volume": "9",
            "issue": None,
            "page": None,
            "year": "2017",
        },
    ),
    (
        "Krizhevsky A., Sutskever I., Hinton G.E., ImageNet classification with deep convolutional neural networks, Proc. Adv. Neural Inf. Process. Syst. (NIPS), pp. 1097-1105, (2012)",
        {
            "author": "Krizhevsky A., Sutskever I., Hinton G.E.",
            "title": "ImageNet classification with deep convolutional neural networks",
            "source": "Proc. Adv. Neural Inf. Process. Syst. (NIPS)",
            "volume": None,
            "issue": None,
            "page": "1097-1105",
            "year": "2012",
        },
    ),
    (
        "Amodei D., Olah C., Steinhardt J., Christiano P., Schulman J., Mane D., Concrete Problems in Ai Safety., (2016)",
        {
            "author": "Amodei D., Olah C., Steinhardt J., Christiano P., Schulman J., Mane D.",
            "title": "Concrete Problems in Ai Safety.",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2016",
        },
    ),
    (
        "Kallianos K., Mongan J., Antani S., Henry T., Taylor A., Abuya J., Kohli M., How far have we come? Artificial intelligence for chest radiograph interpretation, Clin. Radiol., 74, 5, pp. 338-345, (2019)",
        {
            "author": "Kallianos K., Mongan J., Antani S., Henry T., Taylor A., Abuya J., Kohli M.",
            "title": "How far have we come? Artificial intelligence for chest radiograph interpretation",
            "source": "Clin. Radiol.",
            "volume": "74",
            "issue": "5",
            "page": "338-345",
            "year": "2019",
        },
    ),
    (
        "Patne G.D., Et al., Review of CT and PET Image Fusion Using Hybrid Algorithm I2C2, pp. 1-5, (2017)",
        {
            "author": "Patne G.D.",
            "title": "Review of CT and PET Image Fusion Using Hybrid Algorithm I2C2",
            "source": None,
            "volume": None,
            "issue": None,
            "page": "1-5",
            "year": "2017",
        },
    ),
    (
        "Different ‘intelligibility’ for different folks, Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society, pp. 194-199, (2020)",
        {
            "author": None,
            "title": "Different ‘intelligibility’ for different folks",
            "source": "Proceedings of the AAAI/ACM Conference on AI, Ethics, and Society",
            "volume": None,
            "issue": None,
            "page": "194-199",
            "year": "2020",
        },
    ),
    (
        "Common core state standards for English language arts and literacy in history/social studies, science, and technical subjects, (2010)",
        {
            "author": None,
            "title": "Common core state standards for English language arts and literacy in history/social studies, science, and technical subjects",
            "source": None,
            "volume": None,
            "issue": None,
            "page": None,
            "year": "2010",
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


@pytest.mark.parametrize("input, expected", test_issue_data)
def test_extract_issue(input, expected):
    assert ParseScopus(input).extract_issue() == expected


@pytest.mark.parametrize("input, expected", test_volume_data)
def test_extract_volume(input, expected):
    assert ParseScopus(input).extract_volume() == expected


@pytest.mark.parametrize("input, expected", test_author_data)
def test_extract_author(input, expected):
    assert ParseScopus(input).extract_author() == expected


@pytest.mark.parametrize("input, expected", test_drop_data)
def test_drop(input, expected):
    assert ParseScopus.drop(input) == expected


@pytest.mark.parametrize("input, expected", test_parse_data)
def test_parse(input, expected):
    assert ParseScopus(input).parse() == expected


@pytest.mark.parametrize("input, expected", test_missing_data)
def test_parse_missing(input, expected):
    assert ParseScopus(input).parse_missing() == expected


@pytest.mark.parametrize("input, expected", test_general_data)
def test_parse_general(input, expected):
    assert ParseScopus(input).parse_general() == expected
