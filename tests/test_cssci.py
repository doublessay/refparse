import pytest

from refparse.cssci import ParseCssci

test_clean_data = [
    (
        "1.康德.纯粹理性批判.北京:人民出版社",
        "康德.纯粹理性批判.北京:人民出版社",
    ),
    (
        "7..中华人民共和国公共图书馆法.2021",
        ".中华人民共和国公共图书馆法.2021",
    ),
]

test_web_data = [
    (
        "8.Google.Analytics.js.2021",
        {
            "type": "web",
            "author": "Google",
            "title": "Analytics.js",
            "year": "2021",
        },
    ),
    (
        "9..CNNIC:微博用户达2.5亿，近半数网民使用.2012",
        {
            "type": "web",
            "author": None,
            "title": "CNNIC:微博用户达25亿，近半数网民使用2012",
            "year": "2012",
        },
    ),
    (
        "22.IFLA.IFLA STRATEGY 2019-2024.2019",
        {
            "type": "web",
            "author": "IFLA",
            "title": "IFLA STRATEGY 2019-2024",
            "year": "2019",
        },
    ),
]

test_standard_data = [
    (
        "8..GB/T37043-2018，智慧城市术语.北京:中国标准出版社",
        {
            "type": "standard",
            "author": None,
            "title": "智慧城市术语",
            "source": "北京:中国标准出版社",
            "year": None,
            "identifier": "GB/T37043-2018",
        },
    ),
    (
        "17.全国信息技术标准化技术委员会教育技术分会.GB/T 36342-2018,智慧校园总体框架,2018",
        {
            "type": "standard",
            "author": "全国信息技术标准化技术委员会教育技术分会",
            "title": "智慧校园总体框架",
            "source": None,
            "year": "2018",
            "identifier": "GB/T 36342-2018",
        },
    ),
    (
        "30.全国信息技术标准化技术委员会.智慧城市，数据融合，第5部分:市政基础设施数据元素:GB/T 36625.5-2019.北京:中国标准出版社",
        {
            "type": "standard",
            "author": "全国信息技术标准化技术委员会",
            "title": "智慧城市，数据融合，第5部分:市政基础设施数据元素",
            "source": "北京:中国标准出版社",
            "year": None,
            "identifier": "GB/T 36625.5-2019",
        },
    ),
]

test_book_data = [
    (
        "14.吴建中.21世纪图书馆新论.上海:上海科学技术文献出版社",
        {
            "type": "book",
            "author": "吴建中",
            "title": "21世纪图书馆新论",
            "source": "上海:上海科学技术文献出版社",
        },
    ),
    (
        "3.金元浦.中国文化概论.北京:首都师范大学出版社",
        {
            "type": "book",
            "author": "金元浦",
            "title": "中国文化概论",
            "source": "北京:首都师范大学出版社",
        },
    ),
]

test_thesis_data = [
    (
        "21.郑怿昕.智慧图书馆环境下馆员核心能力研究:学位论文.南京:南京农业大学,2015:27-31",
        {
            "type": "thesis",
            "author": "郑怿昕",
            "title": "智慧图书馆环境下馆员核心能力研究",
            "source": "南京:南京农业大学",
            "year": "2015",
        },
    ),
    (
        "17.段美珍.智慧图书馆建设评价模型与应用研究:学位论文.北京:中国科学院大学,2020",
        {
            "type": "thesis",
            "author": "段美珍",
            "title": "智慧图书馆建设评价模型与应用研究",
            "source": "北京:中国科学院大学",
            "year": "2020",
        },
    ),
]

test_newspaper_data = [
    (
        "6..习近平在第二届世界互联网大会开幕式上的讲话.人民日报.12.17(2)",
        {
            "type": "newspaper",
            "author": None,
            "title": "习近平在第二届世界互联网大会开幕式上的讲话",
            "source": "人民日报",
            "date": "12.17",
        },
    ),
    (
        "25.曹磊.大数据:数字世界的智慧基因.文汇报.11.8(12)",
        {
            "type": "newspaper",
            "author": "曹磊",
            "title": "大数据:数字世界的智慧基因",
            "source": "文汇报",
            "date": "11.8",
        },
    ),
    (
        "65..图书馆来了机器人管理员.宁波日报.1.8",
        {
            "type": "newspaper",
            "author": None,
            "title": "图书馆来了机器人管理员",
            "source": "宁波日报",
            "date": "1.8",
        },
    ),
]

test_patent1_data = [
    (
        "26.图书上下架机器人.CN102152293A",
        {
            "type": "patent",
            "title": "图书上下架机器人",
            "identifier": "CN102152293A",
        },
    )
]
test_patent2_data = [
    (
        "9.一种基于RFID技术的自动式图书智能盘点机器人:201620075212.0.2016-01-25",
        {
            "type": "patent",
            "title": "一种基于RFID技术的自动式图书智能盘点机器人",
            "identifier": "201620075212.0",
        },
    ),
    (
        "39.一种基于区块链的金融安全存证平台系统及方法:中国，201910838935. X(2019-09-05)",
        {
            "type": "patent",
            "title": "一种基于区块链的金融安全存证平台系统及方法",
            "identifier": "201910838935",
        },
    ),
]


test_paper_data = [
    (
        "2.严栋.基于物联网的智慧图书馆.图书馆学刊.2010.32(7)",
        {
            "type": "paper",
            "author": "严栋",
            "title": "基于物联网的智慧图书馆",
            "source": "图书馆学刊",
            "year": "2010",
            "volume": "32",
            "issue": "7",
        },
    ),
    (
        "39.刘炜.5G与智慧图书馆建设.中国图书馆学报.2019.45(5)",
        {
            "type": "paper",
            "author": "刘炜",
            "title": "5G与智慧图书馆建设",
            "source": "中国图书馆学报",
            "year": "2019",
            "volume": "45",
            "issue": "5",
        },
    ),
]

test_english_data = [
    (
        "20.Alexei,P..Rite of passage.USA:Galaxy Publishing Co",
        {
            "type": "english-book",
            "author": "Alexei,P.",
            "title": "Rite of passage",
            "source": "USA:Galaxy Publishing Co",
            "year": None,
            "page": None,
        },
    ),
    (
        "8.Sohail,S S.Book recommendation system using opinion mining technique:IEEE,2013:1609-1614",
        {
            "type": "english-book",
            "author": "Sohail,S S",
            "title": "Book recommendation system using opinion mining technique",
            "source": "IEEE",
            "year": "2013",
            "page": "1609-1614",
        },
    ),
    (
        "7.Vaz,P C.Improving a hybrid literary book recommendation system through author ranking.New York:Association for Computing Machinery,2012:387-388",
        {
            "type": "english-book",
            "author": "Vaz,P C",
            "title": "Improving a hybrid literary book recommendation system through author ranking",
            "source": "New York:Association for Computing Machinery",
            "year": "2012",
            "page": "387-388",
        },
    ),
    (
        "7.Hunzaker,M.B. Fallin.Mapping Cultural Schemas: From Theory to Method.American Sociological Review.2019.84(5)",
        {
            "type": "english-paper",
            "author": "Hunzaker,M.B. Fallin",
            "title": "Mapping Cultural Schemas: From Theory to Method",
            "source": "American Sociological Review",
            "year": "2019",
            "volume": "84",
            "issue": "5",
        },
    ),
    (
        "1.Aittola,M..Smart Library: Location-Aware Mobile Library Service.International Symposium on Human Computer Interaction with Mobile Devices and Services.2003.(5)",
        {
            "type": "english-paper",
            "author": "Aittola,M.",
            "title": "Smart Library: Location-Aware Mobile Library Service",
            "source": "International Symposium on Human Computer Interaction with Mobile Devices and Services",
            "year": "2003",
            "volume": None,
            "issue": "5",
        },
    ),
]

test_parse_data = [
    (
        "3..2021第五届中国未来智慧图书馆发展论坛.2021",
        {
            "type": "web",
            "author": None,
            "title": "2021第五届中国未来智慧图书馆发展论坛",
            "year": "2021",
        },
    ),
    (
        "10..GB/T 35273-2020，信息安全技术个人信息安全规范",
        {
            "type": "standard",
            "author": None,
            "title": "信息安全技术个人信息安全规范",
            "source": None,
            "year": None,
            "identifier": "GB/T 35273-2020",
        },
    ),
    (
        "14.吴慰慈.图书馆学概论.北京:北京图书馆出版社",
        {
            "type": "book",
            "author": "吴慰慈",
            "title": "图书馆学概论",
            "source": "北京:北京图书馆出版社",
        },
    ),
    (
        "37.潘星.智慧图书馆联盟建设策略研究:学位论文.扬州:扬州大学,2021",
        {
            "type": "thesis",
            "author": "潘星",
            "title": "智慧图书馆联盟建设策略研究",
            "source": "扬州:扬州大学",
            "year": "2021",
        },
    ),
    (
        "12.王伟健.一个来了还想再来的图书馆.人民日报.1.7(11)",
        {
            "type": "newspaper",
            "author": "王伟健",
            "title": "一个来了还想再来的图书馆",
            "source": "人民日报",
            "date": "1.7",
        },
    ),
    (
        "25.一种用于图书馆机器人的书本上架装置.CN202880264U",
        {
            "type": "patent",
            "title": "一种用于图书馆机器人的书本上架装置",
            "identifier": "CN202880264U",
        },
    ),
    (
        "10.一种基于RFID标签RSSI信号值的图书排序方法:201610050963.1.2016-01-25",
        {
            "type": "patent",
            "title": "一种基于RFID标签RSSI信号值的图书排序方法",
            "identifier": "201610050963.1",
        },
    ),
    (
        "33.司莉.科学数据的标准规范体系框架研究.图书馆.2016.(5)",
        {
            "type": "paper",
            "author": "司莉",
            "title": "科学数据的标准规范体系框架研究",
            "source": "图书馆",
            "year": "2016",
            "volume": None,
            "issue": "5",
        },
    ),
    (
        "18.Ahirwar,J..Five Laws of Library Science and Information Economics.Informatics Studies.2021.7(1)",
        {
            "type": "english-paper",
            "author": "Ahirwar,J.",
            "title": "Five Laws of Library Science and Information Economics",
            "source": "Informatics Studies",
            "year": "2021",
            "volume": "7",
            "issue": "1",
        },
    ),
]


@pytest.mark.parametrize("input, expected", test_clean_data)
def test_clean(input, expected):
    assert ParseCssci.clean(input) == expected


@pytest.mark.parametrize("input, expected", test_web_data)
def test_parse_web(input, expected):
    assert ParseCssci(input).parse_web() == expected


@pytest.mark.parametrize("input, expected", test_standard_data)
def test_parse_standard(input, expected):
    assert ParseCssci(input).parse_standard() == expected


@pytest.mark.parametrize("input, expected", test_book_data)
def test_parse_book(input, expected):
    assert ParseCssci(input).parse_book() == expected


@pytest.mark.parametrize("input, expected", test_thesis_data)
def test_parse_thesis(input, expected):
    assert ParseCssci(input).parse_thesis() == expected


@pytest.mark.parametrize("input, expected", test_newspaper_data)
def test_parse_newspaper(input, expected):
    assert ParseCssci(input).parse_newspaper() == expected


@pytest.mark.parametrize("input, expected", test_patent1_data)
def test_parse_patent1(input, expected):
    assert ParseCssci(input).parse_patent1() == expected


@pytest.mark.parametrize("input, expected", test_patent2_data)
def test_parse_patent2(input, expected):
    assert ParseCssci(input).parse_patent2() == expected


@pytest.mark.parametrize("input, expected", test_paper_data)
def test_parse_paper(input, expected):
    assert ParseCssci(input).parse_paper() == expected


@pytest.mark.parametrize("input, expected", test_english_data)
def test_parse_english(input, expected):
    assert ParseCssci(input).parse_english() == expected


@pytest.mark.parametrize("input, expected", test_parse_data)
def test_parse_parse(input, expected):
    assert ParseCssci(input).parse() == expected
