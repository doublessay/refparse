import pytest

from refparse.cssci import ParseCssci

test_clean_data = [
    (
        "7..中华人民共和国公共图书馆法.2021",
        ".中华人民共和国公共图书馆法.2021",
    ),
    (
        "1.段美珍.智慧图书馆的内涵特点及其认知模型研究.图书情报工作.",
        "段美珍.智慧图书馆的内涵特点及其认知模型研究.图书情报工作",
    ),
    (
        "3.郑晋鸣.南京城东五高校建图书馆联合体.光明日报.04.24(7)",
        "郑晋鸣.南京城东五高校建图书馆联合体.光明日报",
    ),
]

test_drop_data = [
    (
        "1.17 U. S. C. § 107",
        None,
    ),
    (
        "1..",
        None,
    ),
    (
        "2..Campbell v. Acuff-Rose Music, Inc., 510 U. S. 569 (1994),1994",
        None,
    ),
    (
        "26.图书上下架机器人.CN102152293A",
        None,
    ),
    (
        "9.一种基于RFID技术的自动式图书智能盘点机器人:201620075212.0.2016-01-25",
        None,
    ),
    (
        "19.皮亚杰.儿童心理学.北京:商务印书馆",
        "19.皮亚杰.儿童心理学.北京:商务印书馆",
    ),
]

test_author_data = [
    (
        "25.Remy,M..Information Literacy: The Information Commons Connection.California,2004",
        "Remy,M.",
    ),
    (
        "1..2021年度江苏省公共图书馆大数据统计报告",
        None,
    ),
    (
        "14.陈大庆.FOLIO在深圳大学,2018",
        "陈大庆",
    ),
]

test_parse_data = [
    (
        "5.北京市第一中级人民法院民事判决书(2011)一中民初字第1321号",
        {
            "author": None,
            "title": "北京市第一中级人民法院民事判决书(2011)一中民初字第1321号",
            "source": None,
            "year": None,
            "volume": None,
            "issue": None,
        },
    ),
    (
        "10..GB/T 35273-2020，信息安全技术个人信息安全规范",
        {
            "author": None,
            "title": "GB/T 35273-2020，信息安全技术个人信息安全规范",
            "source": None,
            "year": None,
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "6..习近平在第二届世界互联网大会开幕式上的讲话.人民日报.12.17(2)",
        {
            "author": None,
            "title": "习近平在第二届世界互联网大会开幕式上的讲话",
            "source": "人民日报",
            "year": None,
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "21.郑怿昕.智慧图书馆环境下馆员核心能力研究:学位论文.南京:南京农业大学,2015:27-31",
        {
            "author": "郑怿昕",
            "title": "智慧图书馆环境下馆员核心能力研究:学位论文",
            "source": "南京:南京农业大学",
            "year": "2015",
            "volume": None,
            "issue": None,
            "page": "27-31",
        },
    ),
    (
        "9..CNNIC:微博用户达2.5亿，近半数网民使用.2012",
        {
            "author": None,
            "title": "CNNIC:微博用户达2.5亿，近半数网民使用",
            "source": None,
            "year": "2012",
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "4..Society 5.0——科学技术政策——内阁府.2020",
        {
            "author": None,
            "title": "Society 5.0——科学技术政策——内阁府",
            "source": None,
            "year": "2020",
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "5.杨新涯.2.0的图书馆.广州:中山大学出版社",
        {
            "author": "杨新涯",
            "title": "2.0的图书馆",
            "source": "广州:中山大学出版社",
            "year": None,
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "9.全国人民代表大会常务委员会.中华人民共和国个人信息保护法,2021",
        {
            "author": "全国人民代表大会常务委员会",
            "title": "中华人民共和国个人信息保护法",
            "source": None,
            "year": "2021",
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "1.马费成.图书情报学与元宇宙:共识共创共进",
        {
            "author": "马费成",
            "title": "图书情报学与元宇宙:共识共创共进",
            "source": None,
            "year": None,
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "39.刘炜.5G与智慧图书馆建设.中国图书馆学报.2019.45(5)",
        {
            "author": "刘炜",
            "title": "5G与智慧图书馆建设",
            "source": "中国图书馆学报",
            "year": "2019",
            "volume": "45",
            "issue": "5",
            "page": None,
        },
    ),
    (
        "7.Vaz,P C.Improving a hybrid literary book recommendation system through author ranking.New York:Association for Computing Machinery,2012:387-388",
        {
            "author": "Vaz,P C",
            "title": "Improving a hybrid literary book recommendation system through author ranking",
            "source": "New York:Association for Computing Machinery",
            "year": "2012",
            "volume": None,
            "issue": None,
            "page": "387-388",
        },
    ),
    (
        "22.IFLA.IFLA STRATEGY 2019-2024.2019",
        {
            "author": "IFLA",
            "title": "IFLA STRATEGY 2019-2024",
            "source": None,
            "year": "2019",
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
    (
        "1.Lu,Y..Digital Twin-driven smart manufacturing: Connotation, reference model, applications and research issues.Robotics and Computer-Integrated Manufacturing.2020.61",
        {
            "author": "Lu,Y.",
            "title": "Digital Twin-driven smart manufacturing: Connotation, reference model, applications and research issues",
            "source": "Robotics and Computer-Integrated Manufacturing",
            "year": "2020",
            "volume": "61",
            "issue": None,
            "page": None,
        },
    ),
    (
        "14.Hufflen,J M.Languages for Bibliography Styles.TUGB",
        {
            "author": "Hufflen,J M",
            "title": "Languages for Bibliography Styles",
            "source": "TUGB",
            "year": None,
            "volume": None,
            "issue": None,
            "page": None,
        },
    ),
]


@pytest.mark.parametrize("input, expected", test_clean_data)
def test_clean(input, expected):
    assert ParseCssci.clean(input) == expected


@pytest.mark.parametrize("input, expected", test_drop_data)
def test_drop(input, expected):
    assert ParseCssci.drop(input) == expected


@pytest.mark.parametrize("input, expected", test_author_data)
def test_extract_author(input, expected):
    ref = ParseCssci.clean(input)
    assert ParseCssci(ref).extract_author() == expected


@pytest.mark.parametrize("input, expected", test_parse_data)
def test_parse_parse(input, expected):
    assert ParseCssci(input).parse() == expected
