class Radical():
    def __init__(self, char: str, variants: list[str], meanings: list[str], num: int):
        self.char = char
        self.variants = variants
        self.meanings = meanings
        self.num = num

    def __repr__(self):
        return f"{self.char}; variants: {self.variants}; meanings: {self.meanings}; num: {self.num}"

# (index + 1) corresponds to the official radical number.
KANGXI_RADICALS = [
    Radical("一", [], ["one"], 1),
    Radical("丨", [], ["line"], 2),
    Radical("丶", [], ["dot"], 3),
    Radical("丿", ["乀", "⺄"], ["slash"], 4),
    Radical("乙", ["乚", "乛"], ["second"], 5),
    Radical("亅", [], ["hook"], 6),
    Radical("二", [], ["two"], 7),
    Radical("亠", [], ["lid"], 8),
    Radical("人", ["亻"], ["man"], 9),
    Radical("儿", [], ["son", "legs"], 10),
    Radical("入", [], ["enter"], 11),
    Radical("八", ["丷"], ["eight"], 12),
    Radical("冂", [], ["wide"], 13),
    Radical("冖", [], ["cloth cover"], 14),
    Radical("冫", [], ["ice"], 15),
    Radical("几", [], ["table"], 16),
    Radical("凵", [], ["receptacle"], 17),
    Radical("刀", ["刂", "⺈"], ["knife"], 18),
    Radical("力", [], ["power"], 19),
    Radical("勹", [], ["wrap"], 20),
    Radical("匕", [], ["spoon"], 21),
    Radical("匚", [], ["box"], 22),
    Radical("匸", [], ["hiding enclosure"], 23),
    Radical("十", [], ["ten"], 24),
    Radical("卜", [], ["divination"], 25),
    Radical("卩", ["㔾"], ["seal (device)"], 26),
    Radical("厂", [], ["cliff"], 27),
    Radical("厶", [], ["private"], 28),
    Radical("又", [], ["again"], 29),
    Radical("口", [], ["mouth"], 30),
    Radical("囗", [], ["enclosure"], 31),
    Radical("土", [], ["earth"], 32),
    Radical("士", [], ["scholar"], 33),
    Radical("夂", [], ["go"], 34),
    Radical("夊", [], ["go slowly"], 35),
    Radical("夕", [], ["evening"], 36),
    Radical("大", [], ["big"], 37),
    Radical("女", [], ["woman"], 38),
    Radical("子", [], ["child"], 39),
    Radical("宀", [], ["roof"], 40),
    Radical("寸", [], ["inch"], 41),
    Radical("小", ["⺌", "⺍"], ["small"], 42),
    Radical("尢", ["尣"], ["lame"], 43),
    Radical("尸", [], ["corpse"], 44),
    Radical("屮", [], ["sprout"], 45),
    Radical("山", [], ["mountain"], 46),
    Radical("巛", ["川"], ["river"], 47),
    Radical("工", [], ["work"], 48),
    Radical("己", [], ["oneself"], 49),
    Radical("巾", [], ["turban"], 50),
    Radical("干", [], ["dry"], 51),
    Radical("幺", ["么"], ["short thread"], 52),
    Radical("广", [], ["dotted cliff"], 53),
    Radical("廴", [], ["long stride"], 54),
    Radical("廾", [], ["arch"], 55),
    Radical("弋", [], ["shoot"], 56),
    Radical("弓", [], ["bow"], 57),
    Radical("彐", ["彑"], ["snout"], 58),
    Radical("彡", [], ["bristle"], 59),
    Radical("彳", [], ["step"], 60),
    Radical("心", ["忄", "⺗"], ["heart"], 61),
    Radical("戈", [], ["halberd"], 62),
    Radical("戶", ["户", "戸"], ["door"], 63),
    Radical("手", ["扌", "龵"], ["hand"], 64),
    Radical("支", [], ["branch"], 65),
    Radical("攴", ["攵"], ["rap", "tap"], 66),
    Radical("文", [], ["script"], 67),
    Radical("斗", [], ["dipper"], 68),
    Radical("斤", [], ["axe"], 69),
    Radical("方", [], ["square"], 70),
    Radical("无", ["旡"], ["not"], 71),
    Radical("日", [], ["sun"], 72),
    Radical("曰", [], ["say"], 73),
    Radical("月", [], ["moon"], 74),
    Radical("木", [], ["tree"], 75),
    Radical("欠", [], ["lack"], 76),
    Radical("止", [], ["stop"], 77),
    Radical("歹", ["歺"], ["death"], 78),
    Radical("殳", [], ["weapon"], 79),
    Radical("毋", ["母"], ["do not"], 80),
    Radical("比", [], ["compare"], 81),
    Radical("毛", [], ["fur"], 82),
    Radical("氏", [], ["clan"], 83),
    Radical("气", [], ["steam"], 84),
    Radical("水", ["氵", "氺"], ["water"], 85),
    Radical("火", ["灬"], ["fire"], 86),
    Radical("爪", ["爫"], ["claw"], 87),
    Radical("父", [], ["father"], 88),
    Radical("爻", [], ["trigrams"], 89),
    Radical("爿", ["丬"], ["split wood"], 90),
    Radical("片", [], ["slice"], 91),
    Radical("牙", [], ["fang"], 92),
    Radical("牛", ["牜", "⺧"], ["cow"], 93),
    Radical("犬", ["犭"], ["dog"], 94),
    Radical("玄", [], ["profound"], 95),
    Radical("玉", ["王", "玊"], ["jade"], 96),
    Radical("瓜", [], ["melon"], 97),
    Radical("瓦", [], ["tile"], 98),
    Radical("甘", [], ["sweet"], 99),
    Radical("生", [], ["life"], 100),
    Radical("用", [], ["use"], 101),
    Radical("田", [], ["field"], 102),
    Radical("疋", ["⺪"], ["bolt of cloth"], 103),
    Radical("疒", [], ["sickness"], 104),
    Radical("癶", [], ["footsteps"], 105),
    Radical("白", [], ["white"], 106),
    Radical("皮", [], ["skin"], 107),
    Radical("皿", [], ["dish"], 108),
    Radical("目", ["⺫"], ["eye"], 109),
    Radical("矛", [], ["spear"], 110),
    Radical("矢", [], ["arrow"], 111),
    Radical("石", [], ["stone"], 112),
    Radical("示", ["礻"], ["spirit"], 113),
    Radical("禸", [], ["track"], 114),
    Radical("禾", [], ["grain"], 115),
    Radical("穴", [], ["cave"], 116),
    Radical("立", [], ["stand"], 117),
    Radical("竹", ["⺮"], ["bamboo"], 118),
    Radical("米", [], ["rice"], 119),
    Radical("糸", ["糹"], ["silk"], 120),
    Radical("缶", [], ["jar"], 121),
    Radical("网", ["⺲", "罓", "⺳"], ["net"], 122),
    Radical("羊", ["⺶", "⺷"], ["sheep"], 123),
    Radical("羽", [], ["feather"], 124),
    Radical("老", ["耂"], ["old"], 125),
    Radical("而", [], ["and"], 126),
    Radical("耒", [], ["plow"], 127),
    Radical("耳", [], ["ear"], 128),
    Radical("聿", ["⺺", "⺻"], ["brush"], 129),
    Radical("肉", ["⺼"], ["meat"], 130),
    Radical("臣", [], ["minister"], 131),
    Radical("自", [], ["self"], 132),
    Radical("至", [], ["arrive"], 133),
    Radical("臼", [], ["mortar"], 134),
    Radical("舌", [], ["tongue"], 135),
    Radical("舛", [], ["oppose"], 136),
    Radical("舟", [], ["boat"], 137),
    Radical("艮", [], ["stopping"], 138),
    Radical("色", [], ["color"], 139),
    Radical("艸", ["⺿"], ["grass"], 140),
    Radical("虍", [], ["tiger"], 141),
    Radical("虫", [], ["insect"], 142),
    Radical("血", [], ["blood"], 143),
    Radical("行", [], ["walk enclosure"], 144),
    Radical("衣", ["⻂"], ["clothes"], 145),
    Radical("襾", ["西", "覀"], ["cover"], 146),
    Radical("見", [], ["see"], 147),
    Radical("角", ["⻇"], ["horn (of an animal)"], 148),
    Radical("言", ["訁"], ["speech"], 149),
    Radical("谷", [], ["valley"], 150),
    Radical("豆", [], ["bean"], 151),
    Radical("豕", [], ["pig"], 152),
    Radical("豸", [], ["badger"], 153),
    Radical("貝", [], ["shell"], 154),
    Radical("赤", [], ["red"], 155),
    Radical("走", [], ["run"], 156),
    Radical("足", ["⻊"], ["foot"], 157),
    Radical("身", [], ["body"], 158),
    Radical("車", [], ["cart"], 159),
    Radical("辛", [], ["bitter"], 160),
    Radical("辰", [], ["morning"], 161),
    Radical("辵", ["⻌", "⻍", "⻎"], ["walk"], 162),
    Radical("邑", ["⻏"], ["city"], 163),
    Radical("酉", [], ["wine"], 164),
    Radical("釆", [], ["distinguish"], 165),
    Radical("里", [], ["village"], 166),
    Radical("金", ["釒"], ["gold"], 167),
    Radical("長", ["镸"], ["long"], 168),
    Radical("門", [], ["gate"], 169),
    Radical("阜", ["⻖"], ["mound"], 170),
    Radical("隶", [], ["slave"], 171),
    Radical("隹", [], ["short-tailed bird"], 172),
    Radical("雨", [], ["rain"], 173),
    Radical("靑", ["青"], ["blue"], 174),
    Radical("非", [], ["wrong"], 175),
    Radical("面", ["靣"], ["face"], 176),
    Radical("革", [], ["leather"], 177),
    Radical("韋", [], ["tanned leather"], 178),
    Radical("韭", [], ["leek"], 179),
    Radical("音", [], ["sound"], 180),
    Radical("頁", [], ["leaf"], 181),
    Radical("風", [], ["wind"], 182),
    Radical("飛", [], ["fly"], 183),
    Radical("食", ["飠"], ["eat"], 184),
    Radical("首", [], ["head"], 185),
    Radical("香", [], ["fragrant"], 186),
    Radical("馬", [], ["horse"], 187),
    Radical("骨", [], ["bone"], 188),
    Radical("高", ["髙"], ["tall"], 189),
    Radical("髟", [], ["hair"], 190),
    Radical("鬥", [], ["fight"], 191),
    Radical("鬯", [], ["sacrificial wine"], 192),
    Radical("鬲", [], ["cauldron"], 193),
    Radical("鬼", [], ["ghost"], 194),
    Radical("魚", [], ["fish"], 195),
    Radical("鳥", [], ["bird"], 196),
    Radical("鹵", [], ["salt"], 197),
    Radical("鹿", [], ["deer"], 198),
    Radical("麥", [], ["wheat"], 199),
    Radical("麻", [], ["hemp"], 200),
    Radical("黃", [], ["yellow"], 201),
    Radical("黍", [], ["millet"], 202),
    Radical("黑", [], ["black"], 203),
    Radical("黹", [], ["embroidery"], 204),
    Radical("黽", [], ["frog"], 205),
    Radical("鼎", [], ["tripod"], 206),
    Radical("鼓", [], ["drum"], 207),
    Radical("鼠", [], ["rat"], 208),
    Radical("鼻", [], ["nose"], 209),
    Radical("齊", ["斉"], ["even"], 210),
    Radical("齒", [], ["tooth"], 211),
    Radical("龍", [], ["dragon"], 212),
    Radical("龜", [], ["turtle"], 213),
    Radical("龠", [], ["flute"], 214),
]
