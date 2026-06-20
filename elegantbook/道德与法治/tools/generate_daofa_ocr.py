from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
from dataclasses import dataclass
from pathlib import Path
from statistics import median


ROOT = Path(__file__).resolve().parents[1]
PDF_PATH = ROOT / "道法.pdf"
TMP_ROOT = ROOT / "tmp" / "pdfs" / "daofa_ocr"
PAGES_DIR = TMP_ROOT / "pages"
RAW_DIR = TMP_ROOT / "raw"
TXT_DIR = TMP_ROOT / "txt"
OUT_TEX = ROOT / "ocr.tex"

LATEX_SPECIALS = {
    "\\": r"\textbackslash{}",
    "%": r"\%",
    "#": r"\#",
    "&": r"\&",
    "_": r"\_",
    "{": r"\{",
    "}": r"\}",
    "$": r"\$",
    "^": r"\textasciicircum{}",
    "~": r"\textasciitilde{}",
}
CIRCLED_DIGITS = set("①②③④⑤⑥⑦⑧⑨⑩⑪⑫⑬⑭⑮⑯⑰⑱⑲⑳")
SYMBOL_CHARS = CIRCLED_DIGITS | set("★☆")
SYMBOL_MACROS = {
    "‧": "·",
    "△": r"\ensuremath{\triangle}",
}

GLOBAL_REPLACEMENTS: list[tuple[str, str]] = [
    ("自已", "自己"),
    ("为代么", "为什么"),
    ("捏卫", "捍卫"),
    ("完法", "宪法"),
]

PAGE_EXACT_REPLACEMENTS: dict[int, dict[str, str]] = {
    40: {
        "①中国新民主主义革命的胜利和社会主义事业成就，是中国共产党领导中国各族人民，战胜许多艰难险": "①中国新民主主义革命的胜利和社会主义事业成就，是中国共产党领导中国各族人民，战胜许多艰难险阻",
        "国共产党领导是中国特色社会主义最本质的特征。": "中国共产党领导是中国特色社会主义最本质的特征。",
        "民服务是党的根本宗旨，党的最高理想和最终且标是实现共产主义。": "人民服务是党的根本宗旨，党的最高理想和最终目标是实现共产主义。",
        "※3.国冕法的基本原则：我国是人民民主专政的社会主义国家国家的一切权力": "※3.我国宪法的基本原则：我国是人民民主专政的社会主义国家，国家的一切权力",
        "于大民（非常非常重要）只要考试考到为什么重视人民、人权、做一些对人民": "属于人民（非常非常重要）只要考试考到为什么重视人民、人权、做一些对人民",
    },
    59: {
        "（1）性质：我国宪法规定：“中华人民共和国人民法院是国家的审判机关）": "（1）性质：我国宪法规定：“中华人民共和国人民法院是国家的审判机关。”",
        "（5）人民检察院在司法活动中的要求(=人民检察院应该如何依法行使职权？）": "（5）人民法院在司法活动中的要求(=人民法院应该如何行使职权？）",
        "函（1）性质我国宪法规定：“中华人民共和国人民检察院是国家法律监督机关。": "※（1）性质：我国宪法规定：“中华人民共和国人民检察院是国家法律监督机关。”",
        "※(4)人民法院在司法活动中的要求（=人民法院应该如何行使职权？）": "※(4)人民检察院在司法活动中的要求（=人民检察院应该如何依法行使职权？）",
    },
}

GRADE_RE = re.compile(r"^[七八九][上下]$")
UNIT_RE = re.compile(r"^第[一二三四五六七八九十0-9]+单元")
LESSON_RE = re.compile(r"^第[一二三四五六七八九十0-9]+课")

HANDWRITTEN_NOTES = {
    1: "页面顶部有手写批注，疑似补充核心素养或法治观念相关内容；（此处有手写笔记但无法识别）。",
    15: "页面右侧和正文周围有多处手写批注；（此处有手写笔记但无法识别）。",
    30: "页面顶部有手写批注；（此处有手写笔记但无法识别）。",
    31: "页面右侧有手写批注，可辨识片段：打造清朗的网络空间；其余（此处有手写笔记但无法识别）。",
    45: "页面中部有手写批注；（此处有手写笔记但无法识别）。",
    90: "页面中下部有大段手写整理；（此处有手写笔记但无法识别）。",
}

PAGE_REPLACEMENTS: dict[int, list[tuple[str, str]]] = {
    1: [
        ("七上然务 认同，法说见贵低意识", "七上"),
        ("（梦想的作用？（青少年为什么要有梦想？）（p9）", "1.梦想的作用？（青少年为什么要有梦想？）（p9）"),
        ("人生且标", "人生目标"),
        ("自己已的梦想", "自己的梦想"),
    ],
    4: [
        ("福社", "福祉"),
        ("反谊", "友谊"),
    ],
    5: [
        ("散开心雇", "敞开心扉"),
        ("直我保护意识", "自我保护意识"),
    ],
    8: [
        ("赠养扶助", "赡养扶助"),
        ("《民法典义#规定", "《民法典》规定"),
    ],
    11: [
        ("3.为什么要敬畏生命\\}怎样理解生命至上？", "4.为什么要敬畏生命？怎样理解生命至上？"),
        ("自己已的身体", "自己的身体"),
        ("为纤么", "为什么"),
        ("生愈同样重要", "生命同样重要"),
    ],
    12: [
        ("挫拆", "挫折"),
        ("，禾和自己", "，和自己"),
    ],
    13: [
        ("阅压", "阅历"),
        ("色彩与力", "色彩与活力"),
        ("自己已发现", "自己发现"),
        ("1如何传递生命的温暖？", "14.如何传递生命的温暖？"),
        ("15/怎树在平凡中创造伟大？", "15.怎样在平凡中创造伟大？"),
        ("自己已是", "自己是"),
    ],
    15: [
        ("有的先长高。丽计青后期生理受化", "有的先长高。"),
        ("见①反抗与依赖②闭锁与开放勇敢与祛儒。", "：①反抗与依赖②闭锁与开放③勇敢与怯懦。"),
        ("但也为我们的成长提供子契机", "但也为我们的成长提供了契机"),
        ("6.怎样调节童春期的矛盾心理？", "6.怎样调节青春期的矛盾心理？"),
        ("还可以学匀自我调节", "还可以学习自我调节"),
        ("7.怎样正确认识思维的独立（思维的独立要求我们如何做）？  创特", "7.怎样正确认识思维的独立（思维的独立要求我们如何做）？"),
        ("人云亦去", "人云亦云"),
        ("接纳他父合理", "接纳他人合理"),
    ],
    16: [
        ("为什么公一一", "为什么一一"),
        ("勇性成女性角色特征", "男性或女性角色特征"),
    ],
    22: [
        ("人和集体的需要不同", "个人和集体的需要不同"),
        ("当个人利益集体利益发生冲突时", "当个人利益与集体利益发生冲突时"),
        ("4，怎样能让集体的和声更美（更和谐）", "43.怎样才能让集体的和声更美（更和谐）"),
        ("有损集体利", "有损集体利益"),
    ],
    28: [
        ("我国还颁布了未成年人保护法、预", "我国还颁布了未成年人保护法、预防"),
        ("行职责，对未成年人实施专门保护", "依法履行职责，对未成年人实施专门保护"),
        ("同时要尊重", "同时要尊重和"),
    ],
    29: [
        ("76作为象未来的建设者", "76.作为国家未来的建设者"),
        ("辩别是非", "辨别是非"),
    ],
    30: [
        ("效育均衔发展", "教育均衡发展"),
        ("观看新间", "观看新闻"),
        ("个人与种会的关系", "个人与社会的关系"),
        ("发居", "发展"),
        ("老师的教和社会", "老师的教诲和社会"),
    ],
    31: [
        ("1.。 网络的影响", "1. 网络的影响"),
        ("网络是一把双刃有利有弊", "网络是一把双刃剑，有利有弊"),
        ("网络信息良莠不齐", "网络信息良莠不齐"),
        ("要提高媒介养、", "要提高媒介素养，"),
        ("社会主义核必价值观", "社会主义核心价值观"),
        ("如何建立安垒(健康、充满正能量的网络空间？", "如何建立安全、健康、充满正能量的网络空间？"),
        ("有关万联网", "有关互联网"),
        ("完善白我", "完善自我"),
        ("恶怖等不良信息", "恐怖等不良信息"),
        ("自觉避守道德和法律", "自觉遵守道德和法律"),
        ("网络谣言的危害？  绝身国家安全", "网络谣言的危害？"),
        ("Q扰乱人们的思想和行起", "①扰乱人们的思想和行为"),
        ("法律筹", "法律等"),
    ],
    32: [
        ("自由卢规则", "自由与规则"),
        ("外化于心", "外化于行"),
        ("人避守规则", "人遵守规则"),
        ("社会主义核心研值观", "社会主义核心价值观"),
    ],
    45: [
        ("实行宪法宣普制度的意义", "实行宪法宣誓制度的意义"),
        ("对完法的了解", "对宪法的了解"),
        ("一全国人大常委会", "全国人大常委会"),
        ("谁保证本行政区内宪法的实施——地方各级人方", "谁保证本行政区内宪法的实施——地方各级人大"),
    ],
    60: [
        ("法治与自的关系", "法治与自由的关系"),
        ("非法于涉", "非法干涉"),
        ("法治是自山的保障", "法治是自由的保障"),
    ],
    61: [
        ("卫当权利", "正当权利"),
        ("必颁依法行使权利", "必须依法行使权利"),
        ("如何践行平等2", "如何践行平等？"),
    ],
    33: [
        ("艰难快择", "艰难抉择"),
        ("建立健至租关法律法规，拥人执法力度", "建立健全相关法律法规，加大执法力度"),
        ("段打他人", "殴打他人"),
    ],
    34: [
        ("合义：犯罪", "含义：犯罪"),
        ("法律标划", "法律标志"),
        ("有期徒型", "有期徒刑"),
        ("附加形", "附加刑"),
        ("珍美好生活", "珍惜美好生活"),
        ("法治观怒", "法治观念"),
        ("预采成年人犯罪", "预防未成年人犯罪"),
        ("不良行内", "不良行为"),
        ("尊重i", "尊重他人"),
    ],
    55: [
        ("中华人民共行政", "中华人民共和国主席、行政"),
        ("和国主席", ""),
        ("最高人民检蔡院", "最高人民检察院"),
        ("最高中判机关", "最高审判机关"),
        ("中央人民政片", "中央人民政府"),
        ("名部、委员会", "各部、委员会"),
    ],
    56: [
        ("全国人民伐表大会", "全国人民代表大会"),
        ("代装中华人民共和国", "代表中华人民共和国"),
        ("外事权①授工荣举权", "外事权、授予荣誉权"),
    ],
    59: [
        ("6.5国家司法机关一一人民法院和人民检察院", "6.5国家司法机关——人民法院和人民检察院"),
        ("2.△民检察院", "2.人民检察院"),
        ("&（3）职权：", "※（3）职权："),
        ("王涉", "干涉"),
        ("于涉", "干涉"),
        ("涉。各级人民检察院", "干涉。各级人民检察院"),
        ("干干涉", "干涉"),
        ("捏卫", "捍卫"),
        ("3、如何做到公正法？", "3、如何做到公正司法？"),
    ],
    68: [
        ("最居用民主", "最管用民主"),
        ("防治滥用权力", "防止滥用权力"),
        ("6、民4、公民参与民主生活需要具备哪些能力", "4.公民参与民主生活需要具备哪些能力"),
        ("维人民制差", ""),
        ("需具以理性", "②要以理性"),
        ("备能立场正确", "③立场正确"),
        ("力逐步提高依法有序参与民主生活的能力。", "④逐步提高依法有序参与民主生活的能力。"),
    ],
    75: [
        ("证确行使", "正确行使"),
        ("色出行", "绿色出行"),
        ("栖牲环境", "牺牲环境"),
        ("山银山", "金山银山"),
        ("如强和巩固", "加强和巩固"),
        ("加强利巩以民族团线", "加强和巩固民族团结"),
        ("交在中孕育刁闭结友爱的宝贯传统", "交往中孕育了团结友爱的宝贵传统"),
        ("管、人才", "管理、人才"),
        ("化获得", "文化获得"),
        ("备少年", "青少年"),
        ("宜传", "宣传"),
    ],
    78: [
        ("中国特色社会王义文化", "中国特色社会主义文化"),
        ("凝心娶力", "凝心聚力"),
        ("既胸怀理想风求真务实", "既胸怀理想又求真务实"),
        ("③既是梦想家", "⑤既是梦想家"),
    ],
    88: [
        ("弄溯儿", "弄潮儿"),
        ("懂自、能自强", "懂自尊、能自强"),
        ("忧惠意识", "忧患意识"),
        ("闸发中国精神", "阐发中国精神"),
        ("自已", "自己"),
        ("完普自我", "完善自我"),
        ("巡到越来越多的困感", "遇到越来越多的困惑"),
        ("自标轴方向", "目标和方向"),
        ("者春飞扬", "青春飞扬"),
        ("行已有耻", "行己有耻"),
    ],
    89: [
        ("回与(谊问题)", "与同学：友谊问题"),
        ("馬老师", "与老师"),
        ("B与家人", "与家人"),
        ("壶拟社会", "虚拟社会"),
        ("L会交往", "社会交往"),
        ("尊重他夕", "尊重他人"),
        ("科精的怀祖", "奉献精神"),
        ("①做守法公民", "④做守法公民"),
        ("0法治精神", "⑦法治精神"),
    ],
    17: [
        ("15.青春的探索为什么需要自（自信的作用有哪些）？", "15.青春的探索为什么需要自信（自信的作用有哪些）？"),
    ],
    18: [
        ("七个人行事", "行己有耻"),
        ("息人的一种精神境界", "是人的一种精神境界"),
        ("良已", "良好"),
        ("做趣", "做起"),
        ("在理周期", "生理周期"),
        ("观念种行动", "观念和行动"),
    ],
    19: [
        ("情络", "情绪"),
        ("情结", "情绪"),
        ("为任么", "为什么"),
        ("青期", "青春期"),
    ],
    20: [
        ("【3)", "(3)"),
        ("面感受", "负面感受"),
        ("更力饱满", "更加饱满"),
    ],
    24: [
        ("杀盾", "矛盾"),
        ("论为", "沦为"),
        ("辨折题", "辨析题"),
        ("讠过", "通过"),
        ("集体）的动力", "集体的动力"),
    ],
    27: [
        ("作房", "作用"),
        ("为代么", "为什么"),
        ("通德", "道德"),
        ("65。", "65."),
        ("66·", "66."),
        ("67·", "67."),
    ],
    39: [
        ("匹夫有贵", "匹夫有责"),
        ("实于精神", "实干精神"),
        ("就蜕业业", "兢兢业业"),
        ("奉献名", "奉献者"),
        ("实干创造未枣", "实干创造未来"),
        ("娶努力", "要努力"),
    ],
    40: [
        ("最终且标", "最终目标"),
        ("宪法患党的主张和人民意志的统一", "宪法是党的主张和人民意志的统一"),
    ],
    41: [
        ("社会主义经滋制度", "社会主义经济制度"),
        ("国家权利属于人民", "国家权力属于人民"),
        ("人民行使国家权利", "人民行使国家权力"),
        ("生产资料的社会主义有制", "生产资料的社会主义公有制"),
        ("&何坚持党的领导？知以", "8.如何坚持党的领导？"),
        ("党中央权成", "党中央权威"),
        ("为仕么要尊重和保障人权", "为什么要尊重和保障人权"),
    ],
    43: [
        ("避循", "遵循"),
        ("权力是把爽句", "权力是把双刃剑"),
        ("不得懈怠、推诱", "不得懈怠、推诿"),
    ],
    44: [
        ("捏卫宪法尊严", "捍卫宪法尊严"),
        ("完法", "宪法"),
        ("长治安", "长治久安"),
    ],
    57: [
        ("人民政 ", "人民政府 "),
        ("衍政机关", "行政机关"),
        ("从丛行政机关身来说", "从行政机关自身来说"),
        ("阳光型政庭", "阳光型政府"),
    ],
    58: [
        ("监察范闺", "监察范围"),
        ("于涉", "干涉"),
        ("Q监督-监察委员会首要职赁。", "①监督：监察委员会首要职责。"),
        ("腐败行", "腐败行为"),
        ("为的发生", "的发生"),
        ("③处置一对违法", "③处置：对违法"),
        ("大员进行问责", "人员进行问责"),
    ],
    64: [
        ("互联网十养老", "互联网+养老"),
    ],
    69: [
        ("共同原量", "共同准则"),
        ("观代化", "现代化"),
        ("维户稳定", "维护稳定"),
        ("违法可让", "违法可耻"),
        ("合去权益", "合法权益"),
    ],
    74: [
        ("荠筑钱家", "共筑生命家园"),
        ("西部木开发战略", "西部大开发战略"),
    ],
    84: [
        ("衰现", "表现"),
        ("挚重文化多样性", "尊重文化多样性"),
        ("媲紫嫣红", "姹紫嫣红"),
        ("文咀", "文明"),
        ("合作共离", "合作共赢"),
    ],
    86: [
        ("自已", "自己"),
        ("国际关系民化", "国际关系民主化"),
        ("汲营养", "汲取营养"),
    ],
}

PAGE_INSERT_BEFORE: dict[int, list[tuple[str, list[str]]]] = {
    12: [
        (
            "消极影响：面对挫折",
            [
                "【题头小修：第8题挫折的影响】",
                "8.挫折的影响（如何正确认识挫折？）P107",
            ],
        ),
    ],
}

STRUCTURE_SUPPLEMENTS: dict[int, list[str]] = {
    17: [
        "【漏识补录：第13题异性交往做法】",
        "怎么做：异性之间的友谊，可能让人敏感、遭到质疑，但只要我们内心坦荡、言谈得当、举止得体，这份友谊就会成为我们青春美好的见证。",
    ],
    18: [
        "【漏识补录：第17题题头】",
        "17.什么叫“行己有耻”？我们该怎样做到“行己有耻”？",
    ],
    19: [
        "【漏识补录：第25题调节情绪的方法】",
        "25.为什么要调节情绪？调节情绪的方法有哪些？",
        "调节情绪的方法：①改变认知评价；②转移注意；③合理宣泄；④放松训练。",
    ],
    20: [
        "【漏识补录：第33题联结度理解】",
        "（2）联结度理解：①集体的联结度越高，个人感知到的集体温暖就越多。",
        "②集体的联结度通常与以下因素密切相关：成员间相互关联的程度，集体对成员的重要性，成员间相互交流的频率，成员对共同目标的共识程度，成员间的默契程度，集体存在的时间长短。",
    ],
    24: [
        "【漏识补录：第51题美好集体的作用】",
        "在美好集体中，每个人都能在其中获得丰富的精神养料，拥有充实的精神生活，感受集体的关爱和吸引，凝聚拼搏向上的力量，坚定自己的生活信念。",
    ],
    27: [
        "【漏识补录：第65题法律普遍约束力】",
        "（1）在法治社会里，公民在法律面前一律平等，任何人都没有超越法律的特权。",
        "（2）每个公民都平等地受到法律的保护，平等地享有权利和履行义务。",
    ],
    39: [
        "【漏识补录：第5题劳动素养第（1）点】",
        "（1）树立正确劳动观念，尊重劳动，牢固树立劳动最光荣、劳动最崇高、劳动最伟大、劳动最美丽的思想观念。",
    ],
    43: [
        "【漏识补录：民主集中制第（1）点】",
        "（1）在国家机构与人民的关系方面，国家权力来自人民，由人民选举产生国家权力机关，国家权力机关在国家机构中居于主导地位。",
    ],
    44: [
        "【漏识补录：第5题宪法是国家根本法】",
        "5.为什么说宪法是国家的根本法？（宪法和其他法律的区别）",
        "①宪法所规定的内容是国家生活中带有全局性、根本性的问题，而其他法律所规定的内容通常只是国家生活中的一般性问题。",
    ],
    33: [
        "【结构整理：违法行为的分类及异同点表】",
        "表头：类别｜违反的法律｜对社会危害程度｜承担的责任｜举例",
        "民事违法行为｜民事法律规范（如《民法典》）｜较轻｜民事责任（如停止侵害、返还财产、恢复原状、赔偿损失等）｜欠债不还、违反合同、侵犯肖像权、著作权、隐私权等。",
        "行政违法行为｜行政法律规范（如《行政处罚法》《治安管理处罚法》《义务教育法》等）｜较轻｜行政制裁，包括行政处分和行政处罚（警告、罚款、没收违法所得、行政拘留等）｜扰乱社会治安、谎报险情、破坏铁路封闭网、殴打他人等。",
        "说明：民事违法行为和行政违法行为都属于一般违法行为。",
    ],
    34: [
        "【结构整理：违法行为的分类表续】",
        "刑事违法行为（犯罪）｜刑事法律规范（如《刑法》）｜严重｜刑罚处罚｜故意杀人、抢劫、贩毒、醉驾等。",
        "【结构整理：一般违法行为与刑事违法行为的异同点】",
        "相同点：①都有社会危害性；②都是违法行为；③都要承担法律责任。",
        "不同点：一般违法行为包括民事违法行为和行政违法行为，它们对社会的危害相对轻微；刑事违法行为是违法行为中最严重的一种，就是我们常说的犯罪，社会危害性大，情节严重。",
    ],
    55: [
        "【结构整理：我国国家机构】",
        "国家机构包括：国家权力机关、中华人民共和国主席、行政机关、监察机关、司法机关等，是一个严密的组织体系。",
        "【结构整理：中央国家机构组织系统简表】",
        "全国人民代表大会居于最高地位；国家主席、全国人大常委会、国务院、中央军事委员会、国家监察委员会、最高人民法院、最高人民检察院等由其产生或与其相连。",
        "国务院是最高行政机关（中央人民政府）；中央军事委员会是最高军事机关；国家监察委员会是最高监察机关；最高人民法院是最高审判机关；最高人民检察院是最高检察机关。",
        "其他中央国家机关由全国人民代表大会产生，对它负责，受它监督。",
        "【结构整理：我国人民如何行使国家权力】",
        "人民通过民主选举人大代表，组成人民代表大会；人民代表大会作为国家权力机关统一行使国家权力；由人民代表大会产生行政机关、监察机关、审判机关、检察机关等国家机关，具体管理国家和社会事务。",
    ],
    56: [
        "【结构整理：人民代表大会和人大代表的职权】",
        "人民代表大会的职权：立法权、决定权、任免权、监督权。",
        "人大代表的职权：审议权、表决权、提案权、质询权。",
        "不要混淆：全国人大及其常委会依法行使最高立法权、最高决定权、最高任免权、最高监督权；人大代表个人行使审议权、表决权、提案权、质询权。",
        "3.中华人民共和国主席、副主席的任职条件：①有选举权和被选举权；②年满四十五周岁；③中华人民共和国公民。",
        "国家主席的职权：①公布法律、发布命令；②任免权；③外事权；④授予荣誉权。",
    ],
    57: [
        "【漏识补录：第2题行政机关外部监督要求】",
        "为了防止工作人员出现履职不力、监管缺失、失职渎职、徇私枉法等问题，必须加强对行政权的监督和制约。",
    ],
    64: [
        "【漏识补录：公平正义辨析题题干】",
        "小明说：“真正的公平和正义是不存在的，我们没有必要去追求公平正义。”请你运用所学知识，对小明的观点进行评析。",
    ],
    68: [
        "【结构整理：社会主义民主的属性】",
        "产生：新中国成立后，随着各级人民民主政权的建立和社会主义改造的完成，社会主义民主在中国大地上得以真正确立；它从中国社会土壤中长出来，在实践中不断得到验证，是有生命力的。",
        "本质：人民当家作主。",
        "特点：我国社会主义民主是维护人民根本利益的最广泛、最真实、最管用的民主。",
        "作用：有助于推动经济社会持续健康发展，实现人民安居乐业、社会和谐稳定、国家繁荣富强。",
        "真谛：有事好商量，众人的事情由众人商量。",
        "形式：选举民主和协商民主；协商民主是我国社会主义民主政治的特有形式和独特优势。",
        "目的：保障最广大人民的利益。",
        "制度保障：根本政治制度是人民代表大会制度；基本政治制度包括中国共产党领导的多党合作和政治协商制度、民族区域自治制度、基层群众自治制度。",
        "【结构整理：公民参与民主生活的途径】",
        "民主选举：人民实现民主权利的一种重要形式；形式包括直接选举和间接选举、等额选举和差额选举；要遵循公开、公平和公正的原则，公民要积极、主动、理性地参与。",
        "民主决策：形式包括社情民意反映制度、专家咨询制度、重大事项社会公示制度、社会听证制度；意义在于保障人民利益充分实现，促进决策科学化、民主化。",
        "民主监督：是公民参与民主生活、行使公民监督权的具体体现；有利于国家机关和国家工作人员改进工作、防止滥用权力、预防腐败，也有助于增强公民参与意识。",
    ],
    69: [
        "【漏识补录：第5题增强民主意识续句】",
        "增强民主意识是社会主义民主的要求，也是社会主义制度永葆生命力的重要保证。",
    ],
    74: [
        "【漏识补录：第6题关爱和保护环境第①点】",
        "①环境恶化加剧自然灾害的发生，严重破坏生态平衡，威胁着人民的生命安全和身体健康。",
    ],
    75: [
        "【结构整理：民族相关概念表】",
        "民族分布特点：大散居、小聚居、交错杂居。",
        "处理民族关系的基本原则：民族平等、民族团结和各民族共同繁荣。",
        "基本政治制度：民族区域自治制度。",
        "社会主义新型民族关系：平等、团结、互助、和谐。",
    ],
    78: [
        "【结构整理：三步走战略和两个百年目标】",
        "三步走：第一步（1980-1990）解决温饱；第二步（1990-2000）达到总体小康；第三步（2000-21世纪中叶）基本实现社会主义现代化，进而实现中华民族伟大复兴。",
        "第一个百年目标（建党100年，2021）：全面建成小康社会。",
        "第二个百年目标（建国100年，2049）：全面建成社会主义现代化强国。",
        "第二个百年目标分两个阶段：2020-2035年基本实现社会主义现代化；2035年到本世纪中叶，把我国建设成富强民主文明和谐美丽的社会主义现代化强国。",
    ],
    81: [
        "【漏识补录：民生框架第④⑤点】",
        "④有利于发展成果更多更公平惠及全体人民，促进社会公平正义。",
        "⑤有利于巩固全面小康成果，构建社会主义和谐社会。",
    ],
    84: [
        "【漏识补录：第7题文明交流互鉴第（4）点】",
        "（4）学习和借鉴人类文明的一切优秀成果，不能只满足于欣赏物件的精美，更应该领略其中蕴含的人文精神。",
    ],
    86: [
        "【漏识补录：第2题第（5）点开头】",
        "（5）中国在推动国际秩序朝着更加公正合理的方向发展，更好维护我国和广大发展中国家共同利益的同时，坚持以经济建设为中心。",
    ],
    88: [
        "【结构整理：四大模块之心理模块】",
        "青春：青春生理变化；认识自我；接纳欣赏自我（做更好的自己）；青春心理矛盾（三种表现：反抗与依赖、闭锁与开放、勇敢与怯懦）；青春情绪情感；青春的三种思维；青春飞扬（自信、自强）；青春有格（行己有耻、止于至善）。",
        "梦想：梦想的作用；少年与梦；如何实现梦想。",
        "学习：学习的特点、学习的重要性、如何学习。（七上）",
    ],
    89: [
        "【结构整理：心理模块续】",
        "生命问题。",
        "【结构整理：道德模块】",
        "人际交往中的道德品质：与同学（友谊问题、异性交往、网络交友）；与老师（师生交往）；与家人（孝亲敬长、和谐家庭）；与集体（与集体共成长、建设美好集体等）。",
        "与社会：现实社会（亲社会行为、个人与社会）；虚拟社会（网络）。",
        "社会交往需要具备的道德：文明有礼、诚实守信、尊重他人、做负责任的人、不言代价与回报、关爱他人、服务社会、奉献精神等。",
        "【结构整理：法律模块】",
        "①规则与秩序；②法律的特征和作用；③对未成年人的法律保护、六大保护、依法办事；④做守法公民（违法行为、犯罪、善用法律）；⑤宪法；⑥权利与义务；⑦法治精神（自由、平等、公平、正义）；⑧民主与法治。",
    ],
}

MANUAL_PAGE_LINES: dict[int, list[str]] = {
    90: [
        "【结构整理：四大模块之国情模块】",
        "国情模块（经济、政治、文化、社会、生态、国际）。",
        "①经济：富强与创新（改革开放、共享发展成果、创新）；经济制度；关心国家发展（我国的成就、劳动成就今天，实干创造未来）。（八上）",
        "②政治：政治制度；国家机构。",
        "③文化：守望精神家园（中华文化、传统美德、社会主义核心价值观、中国精神）。",
        "④社会：和谐与梦想（国家统一、民族团结、中国特色社会主义新时代、中国梦）。",
        "⑤生态：美丽中国；人口、环境、资源。",
        "⑥世界：维护国家利益（安全）；构建人类命运共同体；中国担当、中国智慧、中国方案；机遇与挑战；走向未来的少。",
    ],
}

DROP_LINE_EXACT_BY_PAGE: dict[int, set[str]] = {
    15: {"空理现务", "瑕璃心"},
    30: {"更质敏"},
    45: {"。 )足(2甲克身比库("},
    90: {"无上", "么做"},
}

DROP_LINE_CONTAINS_BY_PAGE: dict[int, list[str]] = {
    31: ["打造清网务", "深汽/权剂"],
    90: ["?顾通势"],
}


@dataclass
class OcrEntry:
    text: str
    score: float
    x_min: float
    y_min: float
    x_max: float
    y_max: float

    @property
    def x_center(self) -> float:
        return (self.x_min + self.x_max) / 2

    @property
    def y_center(self) -> float:
        return (self.y_min + self.y_max) / 2

    @property
    def height(self) -> float:
        return max(1.0, self.y_max - self.y_min)

    def to_json(self) -> dict:
        return {
            "text": self.text,
            "score": self.score,
            "bbox": [self.x_min, self.y_min, self.x_max, self.y_max],
        }


def run(cmd: list[str]) -> None:
    print("+ " + " ".join(cmd), flush=True)
    subprocess.run(cmd, cwd=ROOT, check=True)


def ensure_tools() -> None:
    missing = [tool for tool in ("pdftoppm",) if shutil.which(tool) is None]
    if missing:
        raise SystemExit(f"Missing required tool(s): {', '.join(missing)}")
    try:
        from rapidocr_onnxruntime import RapidOCR  # noqa: F401
    except Exception as exc:  # pragma: no cover - environment check
        raise SystemExit(f"rapidocr_onnxruntime is not available: {exc}") from exc


def page_number_from_image(path: Path) -> int:
    match = re.search(r"-(\d+)\.png$", path.name)
    if not match:
        raise ValueError(f"Cannot parse page number from {path.name}")
    return int(match.group(1))


def existing_images(page_count: int) -> list[Path]:
    images = sorted(PAGES_DIR.glob("page-*.png"), key=page_number_from_image)
    expected = set(range(1, page_count + 1))
    found = {page_number_from_image(path) for path in images}
    if expected.issubset(found):
        return [path for path in images if page_number_from_image(path) in expected]
    return []


def render_pages(page_count: int, dpi: int, force: bool) -> list[Path]:
    PAGES_DIR.mkdir(parents=True, exist_ok=True)
    if force:
        for image in PAGES_DIR.glob("page-*.png"):
            image.unlink()

    images = existing_images(page_count)
    if not images:
        run(
            [
                "pdftoppm",
                "-f",
                "1",
                "-l",
                str(page_count),
                "-png",
                "-r",
                str(dpi),
                str(PDF_PATH),
                str(PAGES_DIR / "page"),
            ]
        )
        images = existing_images(page_count)

    if len(images) != page_count:
        raise RuntimeError(f"Expected {page_count} rendered pages, got {len(images)}.")
    return images


def normalize_result_item(item) -> OcrEntry | None:
    if not item or len(item) < 3:
        return None
    box, text, score = item[0], str(item[1]).strip(), float(item[2])
    if not text:
        return None
    xs = [float(point[0]) for point in box]
    ys = [float(point[1]) for point in box]
    return OcrEntry(
        text=text,
        score=score,
        x_min=min(xs),
        y_min=min(ys),
        x_max=max(xs),
        y_max=max(ys),
    )


def group_entries(entries: list[OcrEntry]) -> list[dict]:
    if not entries:
        return []

    heights = [entry.height for entry in entries]
    line_tol = max(8.0, median(heights) * 0.55)
    groups: list[list[OcrEntry]] = []

    for entry in sorted(entries, key=lambda item: (item.y_center, item.x_center)):
        for group in groups:
            group_y = median([item.y_center for item in group])
            if abs(entry.y_center - group_y) <= max(line_tol, entry.height * 0.45):
                group.append(entry)
                break
        else:
            groups.append([entry])

    lines = []
    for group in groups:
        ordered = sorted(group, key=lambda item: item.x_min)
        pieces: list[str] = []
        prev: OcrEntry | None = None
        for entry in ordered:
            if prev is not None:
                gap = entry.x_min - prev.x_max
                if gap > max(prev.height, entry.height) * 1.4:
                    pieces.append("  ")
            pieces.append(entry.text)
            prev = entry
        text = "".join(pieces).strip()
        if text:
            lines.append(
                {
                    "text": text,
                    "score": min(item.score for item in ordered),
                    "avg_score": sum(item.score for item in ordered) / len(ordered),
                    "bbox": [
                        min(item.x_min for item in ordered),
                        min(item.y_min for item in ordered),
                        max(item.x_max for item in ordered),
                        max(item.y_max for item in ordered),
                    ],
                }
            )

    return sorted(lines, key=lambda item: (item["bbox"][1], item["bbox"][0]))


def run_ocr(
    images: list[Path],
    text_score: float,
    box_thresh: float,
    force: bool,
) -> dict[int, list[dict]]:
    from rapidocr_onnxruntime import RapidOCR

    RAW_DIR.mkdir(parents=True, exist_ok=True)
    TXT_DIR.mkdir(parents=True, exist_ok=True)
    ocr = RapidOCR()
    pages: dict[int, list[dict]] = {}

    for image in images:
        page_no = page_number_from_image(image)
        raw_path = RAW_DIR / f"page-{page_no:02d}.json"
        txt_path = TXT_DIR / f"page-{page_no:02d}.txt"
        if raw_path.exists() and txt_path.exists() and not force:
            with raw_path.open("r", encoding="utf-8") as fh:
                payload = json.load(fh)
            pages[page_no] = payload.get("lines", [])
            print(f"[skip] OCR page {page_no:02d}", flush=True)
            continue

        print(f"[ocr] page {page_no:02d}: {image.name}", flush=True)
        try:
            result, elapsed = ocr(
                str(image),
                text_score=text_score,
                box_thresh=box_thresh,
            )
        except TypeError:
            result, elapsed = ocr(str(image))

        entries = []
        for item in result or []:
            entry = normalize_result_item(item)
            if entry is not None:
                entries.append(entry)

        lines = group_entries(entries)
        payload = {
            "page": page_no,
            "image": str(image.relative_to(ROOT)),
            "elapsed": elapsed,
            "entries": [entry.to_json() for entry in entries],
            "lines": lines,
        }
        with raw_path.open("w", encoding="utf-8") as fh:
            json.dump(payload, fh, ensure_ascii=False, indent=2)
            fh.write("\n")
        with txt_path.open("w", encoding="utf-8") as fh:
            fh.write(f"PDF第{page_no}页\n")
            for line in lines:
                fh.write(line["text"] + "\n")
        pages[page_no] = lines

    return pages


def latex_escape(text: str) -> str:
    pieces: list[str] = []
    for char in text:
        if char in SYMBOL_MACROS:
            pieces.append(SYMBOL_MACROS[char])
        elif char in SYMBOL_CHARS:
            pieces.append(r"\daofasym{" + char + "}")
        else:
            pieces.append(LATEX_SPECIALS.get(char, char))
    return "".join(pieces)


def is_emphasis_line(text: str) -> bool:
    stripped = text.strip()
    if GRADE_RE.match(stripped) or UNIT_RE.match(stripped) or LESSON_RE.match(stripped):
        return True
    if stripped.startswith("关键词"):
        return True
    if len(stripped) <= 36 and re.search(r"[？?]$", stripped):
        return True
    return False


def tex_line_for_text(text: str) -> list[str]:
    stripped = re.sub(r"\s+", " ", text).strip()
    if not stripped:
        return []
    escaped = latex_escape(stripped)
    if GRADE_RE.match(stripped):
        return [
            rf"\subsection*{{{escaped}}}",
            rf"\addcontentsline{{toc}}{{subsection}}{{{escaped}}}",
        ]
    if UNIT_RE.match(stripped) or LESSON_RE.match(stripped):
        return [
            rf"\subsection*{{{escaped}}}",
            rf"\addcontentsline{{toc}}{{subsection}}{{{escaped}}}",
        ]
    if is_emphasis_line(stripped):
        return [rf"\textbf{{{escaped}}}\par"]
    return [escaped + r"\par"]


def normalize_spaces(text: str) -> str:
    return re.sub(r"\s+", " ", text).strip()


def line_is_footer_or_watermark(line: dict, max_y: float) -> bool:
    text = normalize_spaces(line.get("text", ""))
    bbox = line.get("bbox", [0, 0, 0, 0])
    y_min = float(bbox[1]) if len(bbox) > 1 else 0.0
    near_bottom = bool(max_y) and y_min >= max_y * 0.86

    if "扫描全能王" in text:
        return True
    if near_bottom and re.fullmatch(r"页\s*\d+", text):
        return True
    if near_bottom and re.fullmatch(r"\d+\]?", text):
        return True
    return False


def apply_replacements(page_no: int, text: str) -> str:
    text = PAGE_EXACT_REPLACEMENTS.get(page_no, {}).get(text, text)
    for old, new in GLOBAL_REPLACEMENTS:
        text = text.replace(old, new)
    for old, new in PAGE_REPLACEMENTS.get(page_no, []):
        text = text.replace(old, new)
    return text


def should_drop_line(page_no: int, text: str) -> bool:
    stripped = normalize_spaces(text)
    if stripped in DROP_LINE_EXACT_BY_PAGE.get(page_no, set()):
        return True
    return any(token in stripped for token in DROP_LINE_CONTAINS_BY_PAGE.get(page_no, []))


def make_manual_line(text: str) -> dict:
    return {"text": text, "score": 1.0, "avg_score": 1.0, "bbox": [0, 0, 0, 0]}


def prepare_page_lines(page_no: int, lines: list[dict]) -> list[dict]:
    if page_no in MANUAL_PAGE_LINES:
        return [make_manual_line(text) for text in MANUAL_PAGE_LINES[page_no]]

    max_y = max((float(line.get("bbox", [0, 0, 0, 0])[3]) for line in lines), default=0.0)
    prepared: list[dict] = []
    for line in lines:
        if line_is_footer_or_watermark(line, max_y):
            continue
        text = apply_replacements(page_no, line.get("text", ""))
        if should_drop_line(page_no, text):
            continue
        prepared.append({**line, "text": text})

    if page_no == 31:
        inserted: list[dict] = []
        for line in prepared:
            inserted.append(line)
            if "建立健全网络监管、预警机制" in line.get("text", ""):
                inserted.append(
                    make_manual_line(
                        "（2）网络运营商（企业）：要依法经营，切实加强对网络平台和网络从业人员的监督和管理。"
                    )
                )
        prepared = inserted

    if page_no == 45 and not any("如何加强宪法监督工作" in line.get("text", "") for line in prepared):
        inserted = []
        for line in prepared:
            if line.get("text", "").startswith("①要完善全国人大"):
                inserted.append(make_manual_line("※3. 如何加强宪法监督工作？（=如何健全宪法实施和监督机制？）"))
            inserted.append(line)
        prepared = inserted

    for needle, manual_lines in PAGE_INSERT_BEFORE.get(page_no, []):
        if any(manual_lines[0] in line.get("text", "") for line in prepared):
            continue
        inserted = []
        inserted_once = False
        for line in prepared:
            if not inserted_once and needle in line.get("text", ""):
                inserted.extend(make_manual_line(text) for text in manual_lines)
                inserted_once = True
            inserted.append(line)
        prepared = inserted

    if page_no in STRUCTURE_SUPPLEMENTS:
        prepared = [make_manual_line(text) for text in STRUCTURE_SUPPLEMENTS[page_no]] + prepared

    return prepared


def tex_note_for_page(page_no: int) -> list[str]:
    note = HANDWRITTEN_NOTES.get(page_no)
    if not note:
        return []
    return [
        r"\begin{note}[手写批注]",
        latex_escape(note) + r"\par",
        r"\end{note}",
        "",
    ]


def tex_preamble() -> str:
    return r"""\documentclass[lang=cn,11pt]{elegantbook}

\title{道德与法治}
\subtitle{OCR整理稿}

\author{夏同}
\institute{华南理工大学}
\date{\today}
\version{1.0}
\bioinfo{说明}{由道法.pdf OCR整理}

\extrainfo{OCR初稿，仍需人工校对}

\setcounter{tocdepth}{3}

\logo{logo-blue.png}
\cover{cover.jpg}

\usepackage{array}
\usepackage{mathtools}
\IfFileExists{esint.sty}{
  \usepackage{esint}
}{
  \providecommand{\oiint}{\iint}
}
\ExplSyntaxOn
\tl_gset:Nn \CJKttdefault { ebtt }
\ExplSyntaxOff
\IfFontExistsTF{FangSong}{
  \setCJKmonofont[BoldFont={FangSong},ItalicFont={FangSong},BoldItalicFont={FangSong}]{FangSong}
  \setCJKfamilyfont{ebfs}[BoldFont={FangSong},ItalicFont={FangSong},BoldItalicFont={FangSong}]{FangSong}
  \renewcommand*{\fangsong}{\CJKfamily{ebfs}}
}{}
\IfFontExistsTF{KaiTi}{
  \setCJKfamilyfont{ebkai}[BoldFont={KaiTi},ItalicFont={KaiTi},BoldItalicFont={KaiTi}]{KaiTi}
  \renewcommand*{\kaishu}{\CJKfamily{ebkai}}
}{}
\IfFontExistsTF{Segoe UI Symbol}{
  \newfontfamily\daofasymbolfont{Segoe UI Symbol}
  \newcommand{\daofasym}[1]{{\daofasymbolfont #1}}
}{
  \newcommand{\daofasym}[1]{#1}
}
\newcommand{\ccr}[1]{\makecell{{\color{#1}\rule{1cm}{1cm}}}}
\newenvironment{shortexenum}
  {\par\noindent\setlength{\tabcolsep}{0pt}\renewcommand{\arraystretch}{1.15}%
   \begin{tabular}{@{}>{\raggedright\arraybackslash}p{0.485\linewidth}@{\hspace{0.03\linewidth}}>{\raggedright\arraybackslash}p{0.485\linewidth}@{}}}
  {\end{tabular}\par}
\newcommand{\shortitem}[2]{#1.\enspace #2}

\begin{document}
"""


def generate_tex(pages: dict[int, list[dict]], page_count: int) -> None:
    chunks: list[str] = [tex_preamble()]
    for page_no in range(1, page_count + 1):
        chunks.extend(
            [
                "",
                rf"\section*{{PDF第{page_no}页}}",
                rf"\addcontentsline{{toc}}{{section}}{{PDF第{page_no}页}}",
                "",
            ]
        )
        chunks.extend(tex_note_for_page(page_no))
        lines = prepare_page_lines(page_no, pages.get(page_no, []))
        if not lines:
            chunks.append(r"（本页未识别出文字。）\par")
            continue
        for line in lines:
            chunks.extend(tex_line_for_text(line["text"]))
            chunks.append("")
    chunks.extend(["", r"\end{document}", ""])
    OUT_TEX.write_text("\n".join(chunks), encoding="utf-8")
    print(f"[tex] wrote {OUT_TEX}", flush=True)


def parse_args(argv: list[str]) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Render 道法.pdf, OCR all pages, and build ocr.tex.")
    parser.add_argument("--pages", type=int, default=90, help="Number of PDF pages to process.")
    parser.add_argument("--dpi", type=int, default=200, help="pdftoppm rendering DPI.")
    parser.add_argument("--text-score", type=float, default=0.45, help="RapidOCR text score threshold.")
    parser.add_argument("--box-thresh", type=float, default=0.45, help="RapidOCR detection box threshold.")
    parser.add_argument("--force-render", action="store_true", help="Re-render page PNG files.")
    parser.add_argument("--force-ocr", action="store_true", help="Re-run OCR even if JSON/TXT exists.")
    return parser.parse_args(argv)


def main(argv: list[str]) -> int:
    args = parse_args(argv)
    if not PDF_PATH.exists():
        raise SystemExit(f"Missing PDF: {PDF_PATH}")
    ensure_tools()
    images = render_pages(args.pages, args.dpi, args.force_render)
    pages = run_ocr(images, args.text_score, args.box_thresh, args.force_ocr)
    generate_tex(pages, args.pages)
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
