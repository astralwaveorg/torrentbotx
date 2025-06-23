from enum import Enum

class MtCategoryType(Enum):
    # 自定义 __init__ 方法，允许每个枚举成员有两个值：ID 和 显示名称
    def __init__(self, category_id: str, display_name: str):
        self.id = category_id         # 对应原始字典的键，如 "100"
        self.display_name = display_name # 对应原始字典的值，如 "电影"

    # 以下是 MTeam 各种分类的枚举成员定义
    # 格式：枚举成员名 = (ID, 中文显示名称)

    # 电影类
    MOVIE = ("100", "电影")
    MOVIE_SD = ("401", "电影-SD")
    MOVIE_HD = ("419", "电影-HD")
    MOVIE_DVDISO = ("420", "电影-DVDiSo")
    MOVIE_BLU_RAY = ("421", "电影-Blu-Ray")
    MOVIE_REMUX = ("439", "电影-Remux")

    # 影剧-综艺类
    TV_SHOW = ("105", "影剧-综艺")
    TV_SHOW_SD = ("403", "影剧-综艺-SD")
    TV_SHOW_HD = ("402", "影剧-综艺-HD")
    TV_SHOW_DVDISO = ("435", "影剧-综艺-DVDiSo")
    TV_SHOW_BD = ("438", "影剧-综艺-BD")

    # 纪录片类
    DOCUMENTARY = ("404", "纪录")
    DOCUMENTARY_ALT = ("444", "紀錄") # 注意：原始数据中“纪录”和“紀錄”有不同的ID

    # 动画/动漫类
    ANIMATION = ("405", "动画")
    ANIME = ("449", "動漫") # 注意：原始数据中“动画”和“動漫”有不同的ID

    # 音乐类
    MUSIC = ("110", "Music")
    MUSIC_LOSSLESS = ("434", "Music(无损)")

    # 游戏类
    PC_GAME = ("423", "PC游戏")
    TV_GAME = ("448", "TV遊戲")
    GAME = ("447", "遊戲") # 注意：原始数据中“PC游戏”、“TV遊戲”、“遊戲”有不同的ID

    # 书籍类
    EBOOK = ("427", "电子書")
    AUDIOBOOK = ("442", "有聲書")

    # 成人内容 (AV, IV, H-ACG, H-Game, H-Anime, H-Manga, Gay AV)
    AV_CENSORED = ("115", "AV(有码)")
    AV_UNCENSORED = ("120", "AV(无码)")
    AV_CENSORED_HD = ("410", "AV(有码)-HD Censored")
    AV_UNCENSORED_HD = ("429", "AV(无码)-HD Uncensored")
    AV_CENSORED_SD = ("424", "AV(有码)-SD Censored")
    AV_UNCENSORED_SD = ("430", "AV(无码)-SD Uncensored")
    AV_UNCENSORED_DVDISO = ("426", "AV(无码)-DVDiSo Uncensored")
    AV_CENSORED_DVDISO = ("437", "AV(有码)-DVDiSo Censored")
    AV_CENSORED_BLU_RAY = ("431", "AV(有码)-Blu-Ray Censored")
    AV_UNCENSORED_BLU_RAY = ("432", "AV(无码)-Blu-Ray Uncensored")
    AV_WEBSITE_0DAY = ("436", "AV(网站)-0Day")
    IV_PHOTO_ALBUM = ("425", "IV(写真影集)")
    IV_PHOTO_SET = ("433", "IV(写真图集)")
    H_GAME = ("411", "H-游戏")
    H_ANIME = ("412", "H-动漫")
    H_MANGA = ("413", "H-漫画")
    H_ACG = ("446", "H-ACG")
    AV_GAY_HD = ("440", "AV(Gay)-HD")

    # 其他/杂项
    CONCERT = ("406", "演唱")
    SPORT = ("407", "运动")
    SOFTWARE = ("422", "软件")
    MISC = ("409", "Misc(其他)")
    EDUCATION_VIDEO = ("451", "教育影片")
    OTHER = ("450", "其他") # 注意：原始数据中“Misc(其他)”和“其他”有不同的ID

    @classmethod
    def get_by_id(cls, category_id: str):
        """根据 ID 获取 MtCategoryType 枚举成员。"""
        for member in cls:
            if member.id == category_id:
                return member
        raise ValueError(f"没有找到 ID 为 '{category_id}' 的 MtCategoryType 分类。")

    @classmethod
    def get_display_name_by_id(cls, category_id: str):
        """根据 ID 获取对应的中文显示名称。"""
        try:
            return cls.get_by_id(category_id).display_name
        except ValueError:
            return "未知分类"

### **使用示例**
if __name__ == "__main__":
    print("--- 所有 MTeam 分类 (包含 ID 和中文名称) ---")
    for category in MtCategoryType:
        print(f"枚举名: {category.name}, ID: {category.id}, 中文名: {category.display_name}")

    print("\n--- 根据 ID 获取分类对象和信息 ---")
    try:
        # 获取 ID 为 "100" 的电影分类
        movie_category = MtCategoryType.get_by_id("100")
        print(f"ID '100' 对应的枚举成员是: {movie_category.name}")
        print(f"ID '100' 对应的中文名是: {movie_category.display_name}")
    except ValueError as e:
        print(e)

    print("\n--- 根据 ID 直接获取中文显示名称 ---")
    print(f"ID '427' 对应的中文名是: {MtCategoryType.get_display_name_by_id('427')}")
    print(f"ID '449' 对应的中文名是: {MtCategoryType.get_display_name_by_id('449')}")
    print(f"ID '999' 对应的中文名是: {MtCategoryType.get_display_name_by_id('999')}") # 测试不存在的ID

    print("\n--- 直接使用枚举成员的属性 ---")
    print(f"电子书分类的 ID: {MtCategoryType.EBOOK.id}")
    print(f"电子书分类的中文名: {MtCategoryType.EBOOK.display_name}")

    # 枚举成员的 ID 可以直接用于比较
    if MtCategoryType.MOVIE.id == "100":
        print("MtCategoryType.MOVIE 的 ID 确实是 '100'。")