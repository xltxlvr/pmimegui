# pmIME-Multilingual Engine
#
# (C) 2026 Nova de Hi
# GPLv3
#
# version 0.13.2 (2026-11-12), bug fixes
# version 0.13.1 (2026-10-03), add "TYI" and "DYI" to japanese rules
# version 0.13.0 (2026-08-14), global LaTeX Latin-char & \x{...} codepoint input
# version 0.12.4 (2026-07-03), LaTeX Commands/Envs 
# version 0.12.3 (2026-07-02), add RRK methhod
# version 0.12.1 (2026-06-30), clear after send
# version 0.12.0 (2026-06-24), send_to_editor & clipboard
# version 0.11.1 (2026-06-24), reversed shinjitai = han
# version 0.10.7 (2026-06-23), find_file 
# version 0.10.6 (2026-06-21), save_new_word in kanja_assistant
# version 0.10.5 (2026-06-21), improve kanja_assistant actions
# version 0.10.4 (2026-06-20), bug fix in kana-map
# version 0.10.3 (2026-06-20), hanja assistant
#
import sys
import os
import platform
import unicodedata
import re
import json

__version__ = "0.13.2"

GUI_AVAILABLE = False
try:
    from PyQt6.QtWidgets import (QApplication, QWidget, QVBoxLayout, QHBoxLayout,
                                 QTextEdit, QLabel, QSplitter, QPushButton, QComboBox,
                                 QDialog, QTextBrowser, QStatusBar, QLineEdit, QListWidget, 
                                 QListWidgetItem,
                                 QFormLayout, QDialogButtonBox, QCheckBox, QMessageBox)
    from PyQt6.QtGui import QFont, QIcon, QShortcut, QKeySequence, QKeyEvent
    from PyQt6.QtCore import Qt, QSettings, pyqtSignal, QEvent
    import time 
    import subprocess
    GUI_AVAILABLE = True
except ImportError:
    pass

def resource_path(relative_path):
    try:
        base_path = sys._MEIPASS
    except AttributeError:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)


# ==============================================================================
# pm map
# ==============================================================================
pm_map = {
  "cho": {
    "ᄀ": "g", "ᄁ": "gg", "ᄂ": "n", "ᄃ": "d", "ᄄ": "dd", "ᄅ": "r", "ᄆ": "m", "ᄇ": "b", "ᄈ": "bb", "ᄉ": "s",
    "ᄊ": "ss", "ᄋ": "q", "ᄌ": "j", "ᄍ": "jj", "ᄎ": "c", "ᄏ": "k", "ᄐ": "t", "ᄑ": "p", "ᄒ": "h", 
    "ᄓ": "ng", "ᄔ": "nn", "ᄕ": "nd", "ᄖ": "nb", "ᄗ": "dg", "ᄘ": "rn", "ᄙ": "rr", "ᄚ": "rh", "ᄛ": "rq",
    "ᄜ": "mb", "ᄝ": "mq", "ᄞ": "bg", "ᄟ": "bn", "ᄠ": "bd", "ᄡ": "bs", "ᄢ": "bsg", "ᄣ": "bsd", "ᄤ": "bsb",
    "ᄥ": "bss", "ᄦ": "bsj", "ᄧ": "bj", "ᄨ": "bc", "ᄩ": "bt", "ᄪ": "bp", "ᄫ": "bq", "ᄬ": "bbq", "ᄭ": "sg",
    "ᄮ": "sn", "ᄯ": "sd", "ᄰ": "sr", "ᄱ": "sm", "ᄲ": "sb", "ᄳ": "sbg", "ᄴ": "sss", "ᄵ": "sf", "ᄶ": "sj",
    "ᄷ": "sc", "ᄸ": "sk", "ᄹ": "st", "ᄺ": "sp", "ᄻ": "sh", "ᄼ": "sl", "ᄽ": "ssl", "ᄾ": "slr", "ᄿ": "sslr",
    "ᅀ": "z", "ᅁ": "qg", "ᅂ": "qd", "ᅃ": "qm", "ᅄ": "qb", "ᅅ": "qs", "ᅆ": "qz", "ᅇ": "qq", "ᅈ": "qj",
    "ᅉ": "qc", "ᅊ": "qt", "ᅋ": "qp", "ᅌ": "f", "ᅍ": "jq", "ᅎ": "jl", "ᅏ": "jjl", "ᅐ": "jlr", "ᅑ": "jjlr",
    "ᅒ": "ck", "ᅓ": "ch", "ᅔ": "cl", "ᅕ": "clr", "ᅖ": "pb", "ᅗ": "pq", "ᅘ": "hh", "ᅙ": "x",
    "ᅚ": "gd", "ᅛ": "ns", "ᅜ": "nj", "ᅝ": "nh", "ᅞ": "dr",
    "ꥠ": "dm", "ꥡ": "db", "ꥢ": "ds", "ꥣ": "dj", "ꥤ": "rg", "ꥥ": "rgg", "ꥦ": "rd", "ꥧ": "rdd", "ꥨ": "rm",
    "ꥩ": "rb", "ꥪ": "rbb", "ꥫ": "rbq", "ꥬ": "rs", "ꥭ": "rj", "ꥮ": "rk", "ꥯ": "mg", "ꥰ": "md", "ꥱ": "ms",
    "ꥲ": "bst", "ꥳ": "bk", "ꥴ": "bh", "ꥵ": "ssb", "ꥶ": "qr", "ꥷ": "qh", "ꥸ": "jjh", "ꥹ": "tt", "ꥺ": "ph",
    "ꥻ": "hs", "ꥼ": "xx", "\u115F": "w"
  },
  "jung": {
    "ᅡ": "a", "ᅢ": "ay", "ᅣ": "ya", "ᅤ": "yay", "ᅥ": "e", "ᅦ": "ey", "ᅧ": "ye", "ᅨ": "yey",
    "ᅩ": "o", "ᅪ": "oa", "ᅫ": "oay", "ᅬ": "oy", "ᅭ": "yo", "ᅮ": "u", "ᅯ": "ue", "ᅰ": "uey",
    "ᅱ": "uy", "ᅲ": "yu", "ᅳ": "v", "ᅴ": "vy", "ᅵ": "i",
    "ᅶ": "ao", "ᅷ": "au", "ᅸ": "yao", "ᅹ": "yayo", "ᅺ": "eo", "ᅻ": "eu", "ᅼ": "ev", "ᅽ": "yeo",
    "ᅾ": "yeu", "ᅿ": "oe", "ᆀ": "oey", "ᆁ": "oyey", "ᆂ": "oo", "ᆃ": "ou", "ᆄ": "yoya", "ᆅ": "yoyay",
    "ᆆ": "yoye", "ᆇ": "yoo", "ᆈ": "yoi", "ᆉ": "ua", "ᆊ": "uay", "ᆋ": "uev", "ᆌ": "uyey", "ᆍ": "uu",
    "ᆎ": "yua", "ᆏ": "yue", "ᆐ": "yuey", "ᆑ": "yuye", "ᆒ": "yuyey", "ᆓ": "yuu", "ᆔ": "yui", "ᆕ": "vu",
    "ᆖ": "vv", "ᆗ": "viu", "ᆘ": "ia", "ᆙ": "iya", "ᆚ": "io", "ᆛ": "iu", "ᆜ": "iv", "ᆝ": "i@",
    "ᆞ": "@", "ᆟ": "@e", "ᆠ": "@u", "ᆡ": "@i", "ᆢ": "@@", "ᆣ": "av", "ᆤ": "yau", "ᆥ": "yeya",
    "ᆦ": "oya", "ᆧ": "oyay",
    "ힰ": "oye", "ힱ": "ooi", "ힲ": "yoa", "ힳ": "yoay", "ힴ": "yoe", "ힵ": "uye", "ힶ": "uii", "ힷ": "yuay",
    "ힸ": "yuo", "ힹ": "va", "ힺ": "ve", "ힻ": "vey", "ힼ": "vo", "ힽ": "iyao", "ힾ": "iyay", "ힿ": "iye",
    "ퟀ": "iyey", "ퟁ": "ioi", "ퟂ": "iyo", "ퟃ": "iyu", "ퟄ": "ii", "ퟅ": "@a", "ퟆ": "@ey",
    "\u1160": "*"
  },
  "jong": {
    "ᆨ": "g", "ᆩ": "gg", "ᆪ": "gs", "ᆫ": "n", "ᆬ": "nj", "ᆭ": "nh", "ᆮ": "d",
    "ᆯ": "r", "ᆰ": "rg", "ᆱ": "rm", "ᆲ": "rb", "ᆳ": "rs", "ᆴ": "rt", "ᆵ": "rp",
    "ᆶ": "rh", "ᆷ": "m", "ᆸ": "b", "ᆹ": "bs", "ᆺ": "s", "ᆻ": "ss", "ᆼ": "q",
    "ᆽ": "j", "ᆾ": "c", "ᆿ": "k", "ᇀ": "t", "ᇁ": "p", "ᇂ": "h", "ᇃ": "gr",
    "ᇄ": "gsg", "ᇅ": "ng", "ᇆ": "nd", "ᇇ": "ns", "ᇈ": "nz", "ᇉ": "nt", "ᇊ": "dg",
    "ᇋ": "dr", "ᇌ": "rgs", "ᇍ": "rn", "ᇎ": "rd", "ᇏ": "rdh", "ᇐ": "rr", "ᇑ": "rmg",
    "ᇒ": "rms", "ᇓ": "rbs", "ᇔ": "rbh", "ᇕ": "rbq", "ᇖ": "rss", "ᇗ": "rz", "ᇘ": "rk",
    "ᇙ": "rx", "ᇚ": "mg", "ᇛ": "mr", "ᇜ": "mb", "ᇝ": "ms", "ᇞ": "mss", "ᇟ": "mz",
    "ᇠ": "mc", "ᇡ": "mh", "ᇢ": "mq", "ᇣ": "br", "ᇤ": "bp", "ᇥ": "bh", "ᇦ": "bq",
    "ᇧ": "sg", "ᇨ": "sd", "ᇩ": "sr", "ᇪ": "sb", "ᇫ": "z", "ᇬ": "fg", "ᇭ": "fgg",
    "ᇮ": "ff", "ᇯ": "fk", "ᇰ": "f", "ᇱ": "fs", "ᇲ": "fz", "ᇳ": "pb", "ᇴ": "pq",
    "ᇵ": "hn", "ᇶ": "hr", "ᇷ": "hm", "ᇸ": "hb", "ᇹ": "x", "ᇺ": "gn", "ᇻ": "gb",
    "ᇼ": "gc", "ᇽ": "gk", "ᇾ": "gh", "ᇿ": "nn", "ퟋ": "nr", "ퟌ": "nc", "ퟍ": "dd",
    "ퟎ": "ddb", "ퟏ": "db", "ퟐ": "ds", "ퟑ": "dsg", "ퟒ": "dj", "ퟓ": "dc", "ퟔ": "dt",
    "ퟕ": "rgg", "ퟖ": "rgh", "ퟗ": "rrz", "ퟘ": "rmh", "ퟙ": "rbd", "ퟚ": "rbp",
    "ퟛ": "rf", "ퟜ": "rfh", "ퟝ": "rq", "ퟞ": "mn", "ퟟ": "mnn", "ퟠ": "mm", "ퟡ": "mbs",
    "ퟢ": "mj", "ퟣ": "bd", "ퟤ": "brp", "ퟥ": "bm", "ퟦ": "bb", "ퟧ": "bsd", "ퟨ": "bj",
    "ퟩ": "bc", "ퟪ": "sm", "ퟫ": "sbq", "ퟬ": "ssg", "ퟭ": "ssd", "ퟮ": "sz", "ퟯ": "sj",
    "ퟰ": "sc", "ퟱ": "st", "ퟲ": "sh", "ퟳ": "zb", "ퟴ": "zbq", "ퟵ": "fm", "ퟶ": "fh",
    "ퟷ": "jb", "ퟸ": "jbb", "ퟹ": "jj", "ퟺ": "ps", "ퟻ": "pt"
  },
  "generic": {
    "ㄱ": "G", "ㄲ": "GG", "ㄴ": "N", "ㄷ": "D", "ㄸ": "DD", "ㄹ": "R", "ㅁ": "M", "ㅂ": "B", "ㅃ": "BB", "ㅅ": "S", "ㅆ": "SS", "ㅇ": "Q", "ㅈ": "J", "ㅊ": "C", "ㅋ": "K", "ㅌ": "T", "ㅍ": "P", "ㅎ": "H",
    "ㄳ": "GS", "ㄵ": "NJ", "ㄶ": "NH", "ㄺ": "RG", "ㄻ": "RM", "ㄼ": "RB", "ㄽ": "RS", "ㄾ": "RT", "ㄿ": "RP", "ㅀ": "RH", "ㅄ": "BS", 
    "ㆁ": "F", "ㅿ": "Z", "ㆆ": "X", "ㅸ": "BQ",
    "ㅏ": "A", "ㅐ": "AY", "ㅑ": "YA", "ㅒ": "YAY", "ㅓ": "E", "ㅔ": "EY", "ㅕ": "YE", "ㅖ": "YEY", "ㅗ": "O", "ㅘ": "OA", "ㅙ": "OAY", "ㅚ": "OY", "ㅛ": "YO", "ㅜ": "U", "ㅝ": "UE", "ㅞ": "UEY", "ㅟ": "UY", "ㅠ": "YU", "ㅡ": "V", "ㅢ": "VY", "ㅣ": "I", "ㆍ": "AA"
  }
}

frk_map = {
    "cho": {
        "ᄀ": "g", "ᄁ": "G", "ᄂ": "n", "ᄃ": "d", "ᄄ": "D", "ᄅ": "r", "ᄆ": "m", "ᄇ": "b", "ᄈ": "B",
        "ᄉ": "s", "ᄊ": "S", "ᄋ": "x", "ᄌ": "j", "ᄍ": "J", "ᄎ": "c", "ᄏ": "k", "ᄐ": "t", "ᄑ": "p", "ᄒ": "h",
        "ᅀ": "z", "ᅌ": "Q", "ᅙ": "X", "ᄫ": "v",
        "ᄡ": "bs", "ᄠ": "bd", "ᄢ": "bsg", "ᄣ": "bsd", "ᄦ": "bsj",
        "ᄭ": "sg", "ᄯ": "sd", "ᄰ": "sr", "ᄲ": "sb", "ᄶ": "sj", "ᄷ": "sc", "ᄸ": "sk", "ᄹ": "st", "ᄺ": "sp",
        "\u115F": "w"
    },
    "jung": {
        "ᅡ": "a", "ᅢ": "ai", "ᅣ": "ia", "ᅤ": "iai", "ᅥ": "e", "ᅦ": "ei", "ᅧ": "ie", "ᅨ": "iei",
        "ᅩ": "o", "ᅪ": "oa", "ᅫ": "oai", "ᅬ": "oi", "ᅭ": "io", "ᅮ": "u", "ᅯ": "ue", "ᅰ": "uei",
        "ᅱ": "ui", "ᅲ": "iu", "ᅳ": "y", "ᅴ": "yi", "ᅵ": "i", "ᆞ": "@", "ᆡ": "@i", "ᆢ": "@@",
        "\u1160": "*"
    },
    "jong": {
        "ᆨ": "g", "ᆩ": "G", "ᆪ": "gs", "ᆫ": "n", "ᆬ": "nj", "ᆭ": "nh", "ᆮ": "d",
        "ᆯ": "r", "ᆰ": "rg", "ᆱ": "rm", "ᆲ": "rb", "ᆳ": "rs", "ᆴ": "rt", "ᆵ": "rp",
        "ᆶ": "rh", "ᆷ": "m", "ᆸ": "b", "ᆹ": "bs", "ᆺ": "s", "ᆻ": "S", "ᆼ": "q",
        "ᆽ": "j", "ᆾ": "c", "ᆿ": "k", "ᇀ": "t", "ᇁ": "p", "ᇂ": "h",
        "ᇰ": "Q", 
        "ᇦ": "v", 
        "ᇙ": "rX", 
        "ᇹ": "X", 
        "ᇚ": "mg", 
        "ᇧ": "sg", 
        "ᇨ": "sd", 
        "ᇩ": "sr", 
        "ᇪ": "sb"
    }
}

rrk_map = {
    "cho": {
        "ᄀ": "g", "ᄁ": "kk", "ᄂ": "n", "ᄃ": "d", "ᄄ": "tt", "ᄅ": "l", "ᄆ": "m", "ᄇ": "b", "ᄈ": "pp",
        "ᄉ": "s", "ᄊ": "ss", "ᄋ": "", "ᄌ": "j", "ᄍ": "jj", "ᄎ": "ch", "ᄏ": "k", "ᄐ": "t", "ᄑ": "p", "ᄒ": "h",
        "ᄭ": "sg", "ᄯ": "sd", "ᄰ": "sl", "ᄲ": "sb", "ᄶ": "sj", "ᄷ": "sch", "ᄸ": "sk", "ᄹ": "st", "ᄺ": "sp",
    },
    "jung": {
        "ᅡ": "a", "ᅢ": "ae", "ᅣ": "ya", "ᅤ": "yae", "ᅥ": "eo", "ᅦ": "e", "ᅧ": "yeo", "ᅨ": "ye",
        "ᅩ": "o", "ᅪ": "wa", "ᅫ": "wae", "ᅬ": "oe", "ᅭ": "yo", "ᅮ": "u", "ᅯ": "wo", "ᅰ": "we",
        "ᅱ": "wi", "ᅲ": "yu", "ᅳ": "eu", "ᅴ": "ui", "ᅵ": "i", "ᆞ": "@", "ᆡ": "@i"
    },
    "jong": {
        "ᆨ": "g", "ᆩ": "kk", "ᆪ": "gs", "ᆫ": "n", "ᆬ": "nj", "ᆭ": "nh", "ᆮ": "d",
        "ᆯ": "l", "ᆰ": "lg", "ᆱ": "lm", "ᆲ": "lb", "ᆳ": "ls", "ᆴ": "lt", "ᆵ": "lp",
        "ᆶ": "lh", "ᆷ": "m", "ᆸ": "b", "ᆹ": "bs", "ᆺ": "s", "ᆻ": "ss", "ᆼ": "ng",
        "ᆽ": "j", "ᆾ": "ch", "ᆿ": "k", "ᇀ": "t", "ᇁ": "p", "ᇂ": "h",
        "ᇚ": "mg", 
        "ᇧ": "sg", 
        "ᇨ": "sd", 
        "ᇩ": "sl", 
        "ᇪ": "sb"
    }
}

rrk_cho_map = {v: k for k, v in rrk_map["cho"].items()}
rrk_jung_map = {v: k for k, v in rrk_map["jung"].items()}
rrk_jong_map = {v: k for k, v in rrk_map["jong"].items()}
rrk_cho_map["r"] = "ᄅ"
RRK_VOWEL_PATTERN = re.compile(f"({'|'.join(sorted(rrk_jung_map.keys(), key=len, reverse=True))})")

romaji_to_kana = {
    "a":"あ","i":"い","u":"う","e":"え","o":"お",
    "xa":"ぁ","xi":"ぃ","xu":"ぅ","xe":"ぇ","xo":"ぉ",
    "va":"ゔぁ","vi":"ゔぃ","vu":"ゔ","ve":"ゔぇ","vo":"ゔぉ",
    "ka":"か","ki":"き","ku":"く","ke":"け","ko":"こ",
    "kya": "きゃ", "kyu": "きゅ", "kyo": "きょ",
    "ga":"が","gi":"ぎ","gu":"ぐ","ge":"げ","go":"ご",
    "gya": "ぎゃ", "gyu": "ぎゅ", "gyo": "ぎょ",
    "sa":"さ","si":"し","su":"す","se":"せ","so":"そ",
    "sha":"しゃ","shi":"し","shu":"しゅ","sho":"しょ",
    "sya":"しゃ","syu":"しゅ","syo":"しょ",
    "ja":"じゃ","ji":"じ","ju":"じゅ","jo":"じょ",
    "zya":"じゃ","zyu":"じゅ","zyo":"じょ",
    "jya":"じゃ","jyu":"じゅ","jyo":"じょ",
    "za":"ざ","zi":"じ","zu":"ず","ze":"ぜ","zo":"ぞ",
    "ta":"た","ti":"ち","tu":"つ","te":"て","to":"と",
    "da":"だ","di":"ぢ","du":"づ","de":"で","do":"ど",
    "dxi":"でぃ", "txi": "てぃ",
    "cha":"ちゃ","chi":"ち","tsu":"つ","chu":"ちゅ","cho":"ちょ",
    "tya":"ちゃ","tyu":"ちゅ","tyo":"ちょ",
    "na":"な","ni":"に","nu":"ぬ","ne":"ね","no":"の",
    "nya": "にゃ", "nyu": "にゅ", "nyo": "にょ",
    "ha":"は","hi":"ひ","hu":"ふ","he":"へ","ho":"ほ",
    "hya":"ひゃ","hyu":"ひゅ","hyo":"ひょ",
    "fa":"ふぁ","fi":"ふぃ","fu":"ふ","fe":"ふぇ","fo":"ふぉ",
    "ba":"ば","bi":"び","bu":"ぶ","be":"べ","bo":"ぼ",
    "bya":"びゃ","byu":"びゅ","byo":"びょ",
    "pa":"ぱ","pi":"ぴ","pu":"ぷ","pe":"ぺ","po":"ぽ",
    "pya":"ぴゃ","pyu":"ぴゅ","pyo":"ぴょ",
    "ma":"ま","mi":"み","mu":"む","me":"め","mo":"も",
    "mya": "みゃ", "myu": "みゅ", "myo": "みょ",
    "ya":"や","yu":"ゆ","yo":"よ",
    "xya":"ゃ","xyu":"ゅ","xyo":"ょ",
    "~a":"ゃ","~u":"ゅ","~o":"ょ",
    "ra":"ら","ri":"り","ru":"る","re":"れ","ro":"ろ",
    "rya": "りゃ", "ryu": "りゅ", "ryo": "りょ",
    "wa":"わ","wi":"ゐ","we":"ゑ","wo":"を",
    "n'":"ん", "xt":"っ", "xk":"ヶ",
    "{onaji}":"ゝ", "--":"ー", "{noma}":"\u3005",
    "?a": "は", "?e": "へ", "?i": "ひ", "?u": "ふ", "?o": "ほ",
    "tyi": "てぃ", "dyi": "でぃ"
}

kanji_tables = {"none": {}, "shinjitai": {}, "kyujitai": {}, "simplified": {}}

# 전역 변수 초기화
kanji_tables = {}
sorted_kana_keys = []
reverse_hanja_map = {}

def build_reverse_map(original_dict):
    reverse_map = {}
    for trad_hanja, simp_hanja in original_dict.items():
        if simp_hanja not in reverse_map:
            reverse_map[simp_hanja] = []
        reverse_map[simp_hanja].append(trad_hanja)
    return reverse_map

def get_possible_base_dirs():
    paths = []
    
    # 1. Working Directory (OS 공통)
    working_dir = os.getcwd()
    if working_dir not in paths:
        paths.append(working_dir)

    system = platform.system()
    is_frozen = getattr(sys, 'frozen', False)

    if system == "Windows":
        # Windows 2. exe가 있는 폴더 (또는 스크립트 경로)
        if is_frozen:
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.abspath(__file__))
            
        if exe_dir not in paths:
            paths.append(exe_dir)
            
        # Windows 3. PyInstaller 내부 라이브러리 임시 경로 (_MEIPASS)
        if is_frozen and hasattr(sys, '_MEIPASS'):
            meipass_dir = sys._MEIPASS
            if meipass_dir not in paths:
                paths.append(meipass_dir)

    else:
        # MacOS & Linux 2. ~/.config/pmimegui/ 폴더
        config_dir = os.path.expanduser("~/.config/pmimegui")
        if config_dir not in paths:
            paths.append(config_dir)
            
        # MacOS & Linux 3. 실행파일 (py)이 있는 경로
        if is_frozen:
            exe_dir = os.path.dirname(sys.executable)
        else:
            exe_dir = os.path.dirname(os.path.abspath(__file__))
            
        if exe_dir not in paths:
            paths.append(exe_dir)
            
        # MacOS 4. Mac Bundle의 경우만 ../Resources/ 추가
        # (App Bundle 내부 구조: Contents/MacOS 에 실행파일 존재)
        if system == "Darwin" and is_frozen:
            resource_dir = os.path.abspath(os.path.join(exe_dir, "..", "Resources"))
            if resource_dir not in paths:
                paths.append(resource_dir)

    return paths


def find_file(filename):
    for base in get_possible_base_dirs():
        full_path = os.path.join(base, filename)
        if os.path.exists(full_path):
            return full_path
    return None # 파일을 찾지 못한 경우

def _clean_table(obj, file_path=""):
    """사전 JSON 검증: {문자열: 문자열} 항목만 받아들인다.
    (예전 판이 만든 {"custom_kana": {...}} 중첩 구조는 알맹이를 꺼낸다)"""
    if isinstance(obj, dict) and isinstance(obj.get("custom_kana"), dict):
        obj = obj["custom_kana"]
    if not isinstance(obj, dict):
        raise ValueError("최상위가 JSON 객체가 아님")
    clean = {k: v for k, v in obj.items()
             if isinstance(k, str) and isinstance(v, str) and k and v}
    if len(clean) != len(obj):
        print(f"경고: {file_path}: 문자열이 아닌 항목 {len(obj) - len(clean)}개 무시", file=sys.stderr)
    return clean


def app_dir():
    """실행 파일(또는 스크립트)이 있는 폴더. PyInstaller 임시 폴더(_MEIPASS)가 아니다."""
    if getattr(sys, 'frozen', False):
        return os.path.dirname(sys.executable)
    return os.path.dirname(os.path.abspath(__file__))


def load_kanji_tables():
    global kanji_tables, sorted_kana_keys
    
    filenames = {
        "shinjitai": "shinjitai.json",
        "kyujitai": "kyujitai.json",
        "simplified": "simplified.json",
        "custom_kana": "customkanji.json"
    }
    
    kanji_tables["none"] = {}
    
    for mode, filename in filenames.items():
        file_path = find_file(filename)
        
        if file_path:
            try:
                with open(file_path, "r", encoding="utf-8") as f:
                    kanji_tables[mode] = _clean_table(json.load(f), file_path)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                kanji_tables[mode] = {}
        else:
            print(f"File not found: {filename}")
            kanji_tables[mode] = {}

    if "romaji_to_kana" in globals() and kanji_tables["custom_kana"]:
        target_map = globals()["romaji_to_kana"]
        target_map.update(kanji_tables["custom_kana"])
        sorted_kana_keys = sorted(target_map.keys(), key=lambda x: len(x), reverse=True)

    reverse_hanja_map.clear()
    
    for mode in ["shinjitai", "kyujitai"]:
        if mode in kanji_tables:
            temp_map = build_reverse_map(kanji_tables[mode])
            for simp, trad_list in temp_map.items():
                if simp not in reverse_hanja_map:
                    reverse_hanja_map[simp] = []
                
                # 중복 방지 (예: 신자체와 간체자가 동일한 형태일 경우)
                for t in trad_list:
                    if t not in reverse_hanja_map[simp]:
                        reverse_hanja_map[simp].append(t)


# load kanji table
load_kanji_tables()

bracket_map = {
    "0": ("「", "」"), "1": ("『", "』"), "2": ("〈", "〉"), "3": ("《", "》"), "4": ("〔", "〕"),
    "5": ("【", "】"), "6": ("〖", "〗"), "7": ("\u3018", "\u3019"), "8": ("\u301A", "\u301B"), "9": ("｟", "｠"),
    "#0": ("\uFE59","\uFE5A"), "#1": ("\uFE5B","\uFE5C"), "#2": ("\uFF3B","\uFF3D"), "#3": ("\uFF08","\uFF09"),
    "#4": ("\u2018","\u2019"), "#5": ("\u201C","\u201D")
}

hat_map = {
    "^~": "\uFF5E", "^.": "\u3002", "^,": "\u3001", "^>": "\u00B7", "^<": "\u30FB",
    "^-": "\u2015", "^*": "\u2026", "^/": "/", "^\\": "\\",
    "^=": "\u3005", "^:": "\uFF1A", "^;": "\uFF1B", "^^": "\u005E"
}

cho_map = {v: k for k, v in pm_map["cho"].items() if v != "q"}
cho_map["q"] = "ᄋ"
if "" not in cho_map: cho_map[""] = "ᄋ"
cho_map["fg"] = "ᅁ"

jung_map = {v: k for k, v in pm_map["jung"].items()}
jong_map = {v: k for k, v in pm_map["jong"].items()}

jung_aliases = {
    "ai": "ᅢ", "yai": "ᅤ", "ei": "ᅦ", "yei": "ᅨ", "oi": "ᅬ", "oai": "ᅫ", "uei": "ᅰ", "ui": "ᅱ", "vi": "ᅴ",
    "oyei": "ᆁ", "yoy": "ᆈ", "yoyai": "ᆅ", "uai": "ᆊ", "uyei": "ᆌ", "yuei": "ᆐ", "yuyei": "ᆒ", "oyai": "ᆧ",
    "oei": "ᆀ"
}
jung_map.update(jung_aliases)

sorted_pm_vowels = sorted(jung_map.keys(), key=lambda x: (len(x), x), reverse=True)
PM_VOWEL_PATTERN_FIXED = r"(" + "|".join(re.escape(v) for v in sorted_pm_vowels) + r")"

frk_jung_map = {v: k for k, v in frk_map["jung"].items()}
sorted_frk_vowels = sorted(frk_jung_map.keys(), key=lambda x: (len(x), x), reverse=True)
FRK_VOWEL_PATTERN = r"(" + "|".join(re.escape(v) for v in sorted_frk_vowels) + r")"

frk_cho_map = {v: k for k, v in frk_map["cho"].items() if v not in ("q", "x")}
frk_cho_map["x"] = "ᄋ"
if "" not in frk_cho_map: frk_cho_map[""] = "ᄋ"

frk_jong_map = {v: k for k, v in frk_map["jong"].items()}

compat_map = {}
for k, v in pm_map["generic"].items():
    roman = v.replace("/", "")
    if roman.isalpha() and roman.isupper():
        compat_map[roman] = k
compat_map.update({k.upper(): v for k, v in jung_aliases.items()})

PM_PSEUDO_SINGLE_CONSONANTS = ["gg", "dd", "bb", "ss", "jj"]


def hira_to_kata(text):
    return "".join(chr(ord(ch) + 0x60) if 0x3041 <= ord(ch) <= 0x3096 else ch for ch in text)


def kata_to_hira(text):
    return "".join(chr(ord(ch) - 0x60) if 0x30A1 <= ord(ch) <= 0x30F6 else ch for ch in text)


def romaji_to_kana_convert(romaji, force_mode=None):
    kana = ""
    i = 0
    max_len = max(len(k) for k in romaji_to_kana.keys())

    # 기호 쌍(앞/뒤) 상태를 추적하기 위한 플래그 변수
    # True: 열린 상태(다음에는 닫아야 함), False: 닫힌 상태(다음에는 열어야 함)
    single_quote_opened = False
    double_quote_opened = False

    while i < len(romaji):
        # 1. 쌍따옴표형 기호 처리 (`` 또는 '') -> 『 』
        if romaji[i:i+2] in ("``", "''"):
            if not double_quote_opened:
                kana += "『"
                double_quote_opened = True
            else:
                kana += "』"
                double_quote_opened = False
            i += 2
            continue

        # 2. 홑따옴표형 기호 처리 (` 또는 ') -> 「 」
        # 단, n' 처리 로직(ん/ッ)이 아래에 따로 있으므로 n' 상태가 아닐 때만 처리
        if romaji[i] in ("`", "'"):
            # 이전 글자가 'n' 또는 'N'인 경우 아래의 n' 로직으로 토스하기 위해 패스
            if i > 0 and romaji[i-1].lower() == 'n':
                pass 
            else:
                if not single_quote_opened:
                    kana += "「"
                    single_quote_opened = True
                else:
                    kana += "」"
                    single_quote_opened = False
                i += 1
                continue

        # ==========================================
        # 마침표, 쉼표 처리 로직
        # ==========================================
        if romaji[i] in ('.', ','):
            prev_is_digit = (i > 0 and romaji[i-1].isdigit())
            next_is_digit = (i + 1 < len(romaji) and romaji[i+1].isdigit())
            if prev_is_digit and next_is_digit:
                kana += romaji[i]
            else:
                kana += "。" if romaji[i] == '.' else "、"
            i += 1
            continue

        # n 및 n' 처리 로직
        if romaji[i].lower() == "n":
            is_upper_n = romaji[i].isupper()
            if i + 1 < len(romaji) and romaji[i + 1] == "'":
                kana += "ッ" if is_upper_n else "ん"
                i += 2
                continue
            elif i + 1 < len(romaji) and romaji[i + 1].lower() in "aeiouyw":
                pass
            else:
                kana += "ン" if is_upper_n else "ん"
                i += 1
                continue

        # 촉음(っ) 처리 로직
        if i + 1 < len(romaji) and romaji[i].isalpha() and romaji[i].lower() == romaji[i+1].lower():
            if romaji[i].lower() not in "aeioun":
                chunk_matched = False
                for l in range(max_len, 0, -1):
                    if romaji[i:i+l].lower() in romaji_to_kana:
                        chunk_matched = True
                        break
                if not chunk_matched:
                    kana += "ッ" if romaji[i].isupper() else "っ"
                    i += 1
                    continue

        # 로마자 -> 카나 매칭 로직
        matched = None
        matched_len = 0
        for length in range(max_len, 0, -1):
            chunk = romaji[i:i + length]
            if chunk.lower() in romaji_to_kana:
                matched = romaji_to_kana[chunk.lower()]
                matched_len = length
                chunk_is_upper = chunk[0].isupper()
                break
                
        if matched:
            if force_mode == "kata" or (force_mode is None and chunk_is_upper):
                kana += hira_to_kata(matched)
            elif force_mode == "hira":
                kana += kata_to_hira(hira_to_kata(matched))
            else:
                kana += matched
            i += matched_len
        else:
            kana += romaji[i]
            i += 1

    return kana

def filter_kanji(text, hanja_mode="none"):
    if hanja_mode == "none":
        return text

    output_text = []
    
    for char in text:
        # 1. 한국식 정자체(hanja)로 역변환
        if hanja_mode == "hanja":
            if char in reverse_hanja_map:
                candidates = reverse_hanja_map[char]
                if len(candidates) > 1:
                    output_text.append(f"{{{'|'.join(candidates)}}}")
                else:
                    output_text.append(candidates[0])
            else:
                output_text.append(char)
                
        # 2. 신자체, 구자체, 간체자로 변환하는 모드
        elif hanja_mode in kanji_tables:
            output_text.append(kanji_tables[hanja_mode].get(char, char))
            
        # 3. 알 수 없는 모드일 경우 원본 유지
        else:
            output_text.append(char)

    return "".join(output_text)

########################## 
def copy_to_clipboard(text):
    if not text:
        return False
        
    current_os = platform.system()
    
    # -----------------------------------------------------------------
    # 1. macOS (Darwin) 및 Linux: PyQt6 QClipboard 활용
    # -----------------------------------------------------------------
    if current_os in ["Darwin", "Linux"]:
        try:
            # 현재 실행 중인 QApplication 인스턴스 획득
            app = QApplication.instance()
            if not app:
                # GUI가 아직 뜨지 않았거나 CLI 테스트 환경일 경우 임시 생성
                app = QApplication(sys.argv)
                
            clipboard = QApplication.clipboard()
            clipboard.setText(text)
            
            # [핵심] macOS 시스템(NSPasteboard)이 데이터를 완전히 긁어갈 때까지 
            # Qt의 이벤트 루프를 강제로 구동하여 프로세스 처리를 완료합니다.
            QApplication.processEvents()
            
            # 시스템 클립보드에 데이터가 비어있지 않고 잘 안착했는지 최종 검증
            if clipboard.text() == text:
                return True
                
        except Exception as e:
            sys.stderr.write(f"PyQt6 클립보드 복사 실패 ({current_os}): {e}\n")
            # 실패 시 아래의 subprocess 폴백 로직으로 진입
            pass

    # -----------------------------------------------------------------
    # 2. Windows: ctypes를 통한 Win32 API 유니코드(CF_UNICODETEXT) 직주입
    # -----------------------------------------------------------------
    try:
        if current_os == "Windows":
            import ctypes
            from ctypes import wintypes
            
            GMEM_MOVEABLE = 0x0002
            CF_UNICODETEXT = 13
            
            # Win32 API 함수 포인터 정의
            OpenClipboard = ctypes.windll.user32.OpenClipboard
            OpenClipboard.argtypes = [wintypes.HWND]
            OpenClipboard.restype = wintypes.BOOL
            
            EmptyClipboard = ctypes.windll.user32.EmptyClipboard
            EmptyClipboard.argtypes = []
            EmptyClipboard.restype = wintypes.BOOL
            
            SetClipboardData = ctypes.windll.user32.SetClipboardData
            SetClipboardData.argtypes = [wintypes.UINT, wintypes.HANDLE]
            SetClipboardData.restype = wintypes.HANDLE
            
            CloseClipboard = ctypes.windll.user32.CloseClipboard
            CloseClipboard.argtypes = []
            CloseClipboard.restype = wintypes.BOOL
            
            GlobalAlloc = ctypes.windll.kernel32.GlobalAlloc
            GlobalAlloc.argtypes = [wintypes.UINT, ctypes.c_size_t]
            GlobalAlloc.restype = wintypes.HGLOBAL
            
            GlobalLock = ctypes.windll.kernel32.GlobalLock
            GlobalLock.argtypes = [wintypes.HGLOBAL]
            GlobalLock.restype = wintypes.LPVOID
            
            GlobalUnlock = ctypes.windll.kernel32.GlobalUnlock
            GlobalUnlock.argtypes = [wintypes.HGLOBAL]
            GlobalUnlock.restype = wintypes.BOOL

            GlobalFree = ctypes.windll.kernel32.GlobalFree
            GlobalFree.argtypes = [wintypes.HGLOBAL]
            GlobalFree.restype = wintypes.HGLOBAL
            
            # UTF-16 LE 인코딩 및 널 문자(\x00\x00) 추가
            unicode_bytes = text.encode('utf-16le') + b'\x00\x00'
            
            if not OpenClipboard(None):
                return False
                
            try:
                EmptyClipboard()
                h_global = GlobalAlloc(GMEM_MOVEABLE, len(unicode_bytes))
                if not h_global:
                    return False
                    
                ptr = GlobalLock(h_global)
                if not ptr:
                    GlobalFree(h_global)
                    return False
                ctypes.memmove(ptr, unicode_bytes, len(unicode_bytes))
                GlobalUnlock(h_global)
                # 성공하면 메모리 소유권이 시스템으로 넘어간다. 실패했을 때만 직접 해제.
                if not SetClipboardData(CF_UNICODETEXT, h_global):
                    GlobalFree(h_global)
                    return False
            finally:
                CloseClipboard()
            return True

        # -----------------------------------------------------------------
        # 3. macOS 폴백 (PyQt6 호출 실패 시 Subprocess 사용)
        # -----------------------------------------------------------------
        elif current_os == "Darwin":
            import subprocess
            # 외부 환경 유실 방지를 위해 pbcopy의 절대 경로 지정
            process = subprocess.Popen(
                ['/usr/bin/pbcopy'], 
                stdin=subprocess.PIPE, 
                text=True, 
                encoding='utf-8', 
                errors='replace'
            )
            process.stdin.write(text)
            process.stdin.close()  # EOF 명시적 전달
            process.wait()         # pbcopy 데몬이 완전히 가져갈 때까지 대기
            return process.returncode == 0

        # -----------------------------------------------------------------
        # 4. Linux 폴백 (PyQt6 호출 실패 시 xclip/xsel 사용)
        # -----------------------------------------------------------------
        elif current_os == "Linux":
            import subprocess
            try:
                process = subprocess.Popen(
                    ['xclip', '-selection', 'clipboard', '-t', 'UTF8_STRING'], 
                    stdin=subprocess.PIPE, text=True, encoding='utf-8', errors='replace'
                )
                process.communicate(input=text)
                return True
            except FileNotFoundError:
                try:
                    process = subprocess.Popen(
                        ['xsel', '--clipboard', '--input'], 
                        stdin=subprocess.PIPE, text=True, encoding='utf-8', errors='replace'
                    )
                    process.communicate(input=text)
                    return True
                except FileNotFoundError:
                    return False
                    
    except Exception as e:
        sys.stderr.write(f"클립보드 전체 복사 프로세스 중 예외 발생: {e}\n")
        return False
        
    return False

def parse_syllable_core(roman_str, engine_mode="pm"):
    if not roman_str: return ""
    if engine_mode == "pm" and "/" in roman_str:
        return "".join([parse_syllable_core(s, "pm") for s in roman_str.split("/")])
    
    remaining = roman_str

    if engine_mode == "rrk":
        c_map, v_map, t_map = rrk_cho_map, rrk_jung_map, rrk_jong_map
    elif engine_mode == "frkim":
        c_map, v_map, t_map = frk_cho_map, frk_jung_map, frk_jong_map
    else:
        c_map, v_map, t_map = cho_map, jung_map, jong_map

    cho_char = c_map.get("")
    for i in range(len(remaining), 0, -1):
        if remaining[:i] in c_map:
            cho_char = c_map[remaining[:i]]
            remaining = remaining[i:]
            break
    jung_char = ""
    for i in range(len(remaining), 0, -1):
        if remaining[:i] in v_map:
            jung_char = v_map[remaining[:i]]
            remaining = remaining[i:]
            break
    jong_char = ""
    for i in range(len(remaining), 0, -1):
        if remaining[:i] in t_map:
            jong_char = t_map[remaining[:i]]
            remaining = remaining[i:]
            break
            
    # [방점 처리 루틴]
    bangjeom = ""
    if remaining.startswith(";"):
        bangjeom = "\u302E"  # 거성 (Single Dot)
        remaining = remaining[1:]
    elif remaining.startswith(":"):
        bangjeom = "\u302F"  # 상성 (Double Dot)
        remaining = remaining[1:]
        
    return cho_char + jung_char + jong_char + bangjeom + remaining


def parse_compat(roman_str):
    result = ""
    remaining = roman_str
    while remaining:
        matched = False
        for i in range(len(remaining), 0, -1):
            if remaining[:i] in compat_map:
                result += compat_map[remaining[:i]]
                remaining = remaining[i:]
                matched = True
                break
        if not matched:
            result += remaining[0]; remaining = remaining[1:]
    return result


def split_consonants_pmfrk(lead_cluster):
    if not lead_cluster: return "", ""
    if lead_cluster in PM_PSEUDO_SINGLE_CONSONANTS or len(lead_cluster) == 1: return "", lead_cluster
    if len(lead_cluster) >= 2 and lead_cluster[-2:] in PM_PSEUDO_SINGLE_CONSONANTS: return lead_cluster[:-2], lead_cluster[-2:]
    return lead_cluster[:-1], lead_cluster[-1]


def parse_auto_chunk(chunk, engine_mode="frkim"):
    prev_jong=""
    this_jong=""
    if not chunk: return ""
    
    # =========================================================================
    # [규칙 4] 대시(-) 강제 음절 분리: 
    # 대시를 기준으로 잘라 재귀 호출하면, 뒤에 모음이 올 경우 자연스럽게 
    # 선행 자음이 없으므로 'ㅇ'이 붙고(규칙 1), 자음이 오면 초성이 됩니다(규칙 2).
    # =========================================================================
    if engine_mode == "rrk" and "-" in chunk:
        return "".join([parse_auto_chunk(c, engine_mode="rrk") for c in chunk.split("-")])
        
    # =========================================================================
    # pm 모드: /, ;, : 
    # =========================================================================
    if engine_mode == "pm":
        tokens = re.split(r"(?<=[/;:])", chunk)
        
        result_chunks = []
        for token in tokens:
            if not token: 
                continue
            
            if token.endswith("/"):
                pure_token = token[:-1]
                if pure_token:
                    result_chunks.append(parse_syllable_core(pure_token, engine_mode="pm"))
            else:
                result_chunks.append(parse_syllable_core(token, engine_mode="pm"))
                
        return "".join(result_chunks)

    # =========================================================================
    # mix(pmfrk), frkim, rrk 모드: 자동 음절 분리
    # =========================================================================
    if engine_mode == "pmfrk": vow_pattern = PM_VOWEL_PATTERN_FIXED
    elif engine_mode == "rrk": vow_pattern = RRK_VOWEL_PATTERN
    else: vow_pattern = FRK_VOWEL_PATTERN
    
    vowel_matches = list(re.finditer(vow_pattern, chunk))
    if not vowel_matches: 
        return chunk
        
    syllables = []
    for idx, match in enumerate(vowel_matches):
        v_start = match.start()
        this_jung = match.group(1)
        
        if idx == 0: lead_cluster = chunk[:v_start]
        else: lead_cluster = chunk[vowel_matches[idx-1].end():v_start]
            
        this_cho, this_jong = "", ""
        
        if idx == 0:
            # [규칙 1 & 2] 첫 모음 앞의 자음 처리
            if not lead_cluster: this_cho = ""  # 자음이 없으면 'ㅇ' (맵에서 ""는 "ㅇ"으로 매칭됨)
            elif engine_mode == "rrk": this_cho = lead_cluster
            elif lead_cluster.startswith("-"): this_cho = lead_cluster[1:]
            elif lead_cluster.startswith("'"): this_cho = ""
            elif lead_cluster.startswith("/"): this_cho = lead_cluster[1:]
            else: this_cho = lead_cluster
        else:
            prev_jong = ""
            if engine_mode == "rrk":
                # [규칙 3] 모음과 모음 사이의 자음 분리
                # 오른쪽 끝에서부터 '유효한 초성'을 먼저 찾고, 남은 앞부분이 '유효한 종성'인지 확인하여 분리
                # (예: "ngg" -> prev_jong="ng", this_cho="g")
                for i in range(len(lead_cluster)):
                    head, tail = lead_cluster[:i], lead_cluster[i:]
                    if (tail == "" or tail in rrk_cho_map) and (head == "" or head in rrk_jong_map):
                        prev_jong, this_cho = head, tail
                        break
                else:
                    # 완벽한 분리점을 찾지 못한 경우의 안전망 (왼쪽부터 종성 최대 매칭)
                    for i in range(len(lead_cluster), -1, -1):
                        head, tail = lead_cluster[:i], lead_cluster[i:]
                        if head == "" or head in rrk_jong_map:
                            prev_jong, this_cho = head, tail
                            break
            elif "'" in lead_cluster:
                parts = lead_cluster.split("'", 1)
                prev_jong, this_cho = parts[0], parts[1]
            elif "-" in lead_cluster:
                parts = lead_cluster.split("-", 1)
                prev_jong, this_cho = parts[0], parts[1]
            else:
                if engine_mode == "pmfrk":
                    prev_jong, this_cho = split_consonants_pmfrk(lead_cluster)
                else:
                    m = re.match(r"^(.*?)([a-zA-Z]*)$", lead_cluster)
                    prefix = m.group(1) if m else lead_cluster
                    alpha = m.group(2) if m else ""
                    if alpha and len(alpha) > 1:
                        prev_jong = prefix + alpha[:-1]
                        this_cho = alpha[-1]
                    else:
                        prev_jong = prefix
                        this_cho = alpha
                        
        if prev_jong and syllables: 
            syllables[-1][2] = (syllables[-1][2] or "") + prev_jong
            
        syllables.append([this_cho, this_jung, this_jong])
        
    last_v_end = vowel_matches[-1].end()
    rem_tail = chunk[last_v_end:]
    if rem_tail and syllables: 
        syllables[-1][2] = (syllables[-1][2] or "") + rem_tail

    result_str = ""
    for syl in syllables:
        if syl[1] == "": 
            result_str += syl[0]
        else:
            c_part = syl[0]
            core_mode = "pm" if engine_mode == "pmfrk" else engine_mode
            result_str += parse_syllable_core(c_part + syl[1] + syl[2], engine_mode=core_mode)
            
    return result_str

# ==============================================================================
# LaTeX 입력 확장 (전역)
#   1) 확장 라틴문자   : \'e -> é , \v{s} -> š , \ss -> ß , \ae -> æ ...
#   2) 유니코드 코드포인트 : \xAC00 -> 가 , \x{1F600} -> 😀 , \x{1112 1161 11AB} -> 한
#  * 입력 메서드(pm/frk/mix/rrk/jp/clean)와 무관하게 변환 파이프라인 최전방에서 동작한다.
# ==============================================================================

LATEX_EXPAND_ENABLED = True          # 전역 스위치 (GUI 체크박스 / CLI --no-latex 로 제어)

def set_latex_expand(flag):
    global LATEX_EXPAND_ENABLED
    LATEX_EXPAND_ENABLED = bool(flag)

# 마커용 사용자 영역(PUA) 문자. 본문에 등장할 일이 없으므로 후속 치환 규칙과 충돌하지 않는다.
_LX_OPEN = "\uE000"
_LX_CLOSE = "\uE001"
# LaTeX 명령 보호 / ^ 기호 보호용 마커도 같은 이유로 PUA 문자를 쓴다.
# (예전의 숫자 마커 999NNN / 888NN 은 본문의 숫자, "0[" 괄호 규칙과 충돌했다)
_CMD_OPEN, _CMD_CLOSE = "\uE002", "\uE003"
_HAT_OPEN, _HAT_CLOSE = "\uE004", "\uE005"

# ------------------------------------------------------------------
# 1) 액센트 명령 -> 결합 발음구별기호(combining diacritical mark)
#    결합 후 NFC 정규화하므로 미리 만들어 둔 완성형 표가 필요 없다.
# ------------------------------------------------------------------
LATEX_ACCENT_MAP = {
    "'": "\u0301",   # acute        \'e      -> é
    "`": "\u0300",   # grave        \`e      -> è
    "^": "\u0302",   # circumflex   \^e      -> ê
    '"': "\u0308",   # diaeresis    \"o      -> ö
    "~": "\u0303",   # tilde        \~n      -> ñ
    "=": "\u0304",   # macron       \=a      -> ā
    ".": "\u0307",   # dot above    \.z      -> ż
    "u": "\u0306",   # breve        \u{g}    -> ğ
    "v": "\u030C",   # caron        \v{s}    -> š
    "H": "\u030B",   # double acute \H{o}    -> ő
    "r": "\u030A",   # ring         \r{a}    -> å
    "c": "\u0327",   # cedilla      \c{c}    -> ç
    "k": "\u0328",   # ogonek       \k{a}    -> ą
    "d": "\u0323",   # dot below    \d{s}    -> ṣ
    "b": "\u0331",   # macron below \b{h}    -> ẖ
    "t": "\u0361",   # tie          \t{oo}   -> o͡o
}

# ------------------------------------------------------------------
# 2) 독립 문자/합자 명령 (이름이 영문자인 것)
# ------------------------------------------------------------------
LATEX_SPECIAL_WORD_MAP = {
    # 라틴 확장 문자
    "ss": "ß", "SS": "ẞ", "ae": "æ", "AE": "Æ", "oe": "œ", "OE": "Œ",
    "aa": "å", "AA": "Å", "o": "ø", "O": "Ø", "l": "ł", "L": "Ł",
    "i": "ı", "j": "ȷ", "dh": "ð", "DH": "Ð", "th": "þ", "TH": "Þ",
    "ng": "ŋ", "NG": "Ŋ", "dj": "đ", "DJ": "Đ",
    # 인용/구두점
    "guillemotleft": "«", "guillemotright": "»",
    "guilsinglleft": "‹", "guilsinglright": "›",
    "quotedblbase": "„", "quotesinglbase": "‚",
    "textquotedblleft": "“", "textquotedblright": "”",
    "textquoteleft": "‘", "textquoteright": "’",
    "textendash": "–", "textemdash": "—",
    "textellipsis": "…", "ldots": "…", "dots": "…",
    "textbullet": "•", "textperiodcentered": "·",
    "dag": "†", "ddag": "‡", "S": "§", "P": "¶",
    # 기호
    "pounds": "£", "texteuro": "€", "textyen": "¥", "textcent": "¢",
    "copyright": "©", "textregistered": "®", "texttrademark": "™",
    "textdegree": "°", "textmu": "µ", "textpm": "±",
    "texttimes": "×", "textdiv": "÷",
    "textasciitilde": "~", "textasciicircum": "^",
    "textbackslash": "\\", "textunderscore": "_",
    "textbraceleft": "{", "textbraceright": "}",
    # 자주 쓰는 IPA
    "textschwa": "ə", "textopeno": "ɔ", "textesh": "ʃ", "textyogh": "ʒ",
    "textturnv": "ʌ", "textscripta": "ɑ", "textglotstop": "ʔ", "textbari": "ɨ",
}

# ------------------------------------------------------------------
# 3) 이름이 기호인 명령 (뒤에 오는 공백을 먹지 않는다)
# ------------------------------------------------------------------
LATEX_SPECIAL_SYM_MAP = {
    "%": "%", "&": "&", "#": "#", "$": "$", "_": "_",
}

def _lx_alt(keys):
    return "|".join(re.escape(k) for k in sorted(keys, key=len, reverse=True))

_LX_ACC_ALPHA = _lx_alt([k for k in LATEX_ACCENT_MAP if k.isalpha()])
_LX_ACC_SYM = _lx_alt([k for k in LATEX_ACCENT_MAP if not k.isalpha()])
_LX_SPEC_WORD = _lx_alt(LATEX_SPECIAL_WORD_MAP.keys())
_LX_SPEC_SYM = _lx_alt(LATEX_SPECIAL_SYM_MAP.keys())

# 액센트 인자: {...}(1단계 중첩 허용) / \i \j / 단일 문자
_LX_ARG = r"(?:\{(?:[^{}]|\{[^{}]*\})*\}|\\[ij](?![A-Za-z])|[A-Za-z])"

LATEX_INPUT_RE = re.compile(
    rf"""
      (?P<esc>\\\\)                                     # \\ 는 확장하지 않고 그대로 통과(탈출 문자)
    | \\x\{{(?P<cpbrace>[^{{}}]{{0,80}})\}}             # \x{{AC00}} , \x{{1112 1161 11AB}}
    | \\x(?P<cp4>[0-9A-Fa-f]{{4}})                      # \xAC00
    | \\u(?P<cpu4>[0-9A-Fa-f]{{4}})                     # \uAC00
    | \\U(?P<cpU8>[0-9A-Fa-f]{{8}})                     # \U0001F600
    | \\char"(?P<chex>[0-9A-Fa-f]{{1,6}})               # TeX: \char"AC00
    | \\char'(?P<coct>[0-7]{{1,8}})                     # TeX: \char'101
    | \\char(?P<cdec>[0-9]{{1,7}})                      # TeX: \char97
    | \\(?P<specw>{_LX_SPEC_WORD})(?![A-Za-z])(?P<specw_tail>\{{\}}|[ \t])?
    | \\(?P<specs>{_LX_SPEC_SYM})
    | \\(?P<acca>{_LX_ACC_ALPHA})(?![A-Za-z])[ \t]*(?P<arga>{_LX_ARG})
    | \\(?P<accs>{_LX_ACC_SYM})[ \t]*(?P<args>{_LX_ARG})
    """,
    re.VERBOSE,
)


def _lx_codepoint(token):
    """단일 코드포인트 토큰(16진)을 문자로. 실패하면 None."""
    t = token.strip()
    if not t:
        return None
    low = t.lower()
    if low.startswith("u+"):
        t = t[2:]
    elif low.startswith("0x"):
        t = t[2:]
    try:
        cp = int(t, 16)
    except ValueError:
        return None
    if cp < 0 or cp > 0x10FFFF or 0xD800 <= cp <= 0xDFFF:
        return None
    return chr(cp)


def _lx_codepoint_list(body):
    """\\x{...} 내부: 공백/쉼표/+ 로 구분된 여러 코드포인트를 허용."""
    tokens = [t for t in re.split(r"[\s,+]+", body.strip()) if t]
    if not tokens:
        return None
    out = []
    for tok in tokens:
        ch = _lx_codepoint(tok)
        if ch is None:
            return None
        out.append(ch)
    return "".join(out)


def _lx_accent_base(arg):
    """액센트 인자를 실제 밑글자 문자열로 정규화."""
    if arg.startswith("{") and arg.endswith("}"):
        arg = arg[1:-1]
    arg = arg.strip()
    # 액센트 밑글자로 쓰인 \i \j 는 점 없는 i/j 가 아니라 보통의 i/j 로 취급 (\'\i -> í)
    arg = re.sub(r"\\([ij])(?![A-Za-z])", r"\1", arg)
    # 중첩 액센트 지원: \'{\v{s}}
    return expand_latex_input(arg)


def _lx_apply_accent(mark, base):
    if not base:
        return None
    return unicodedata.normalize("NFC", base[0] + mark + base[1:])


def expand_latex_input(text, protect=None):
    """
    LaTeX식 확장 라틴문자/코드포인트 입력을 실제 문자로 렌더링한다.

    protect 가 리스트이면, 확장 결과를 그 리스트에 적재하고 본문에는 PUA 마커만 남긴다.
    (이후 로마자->한글 치환 단계에서 확장 결과가 다시 건드려지는 것을 막기 위한 장치)
    """
    if not text or not LATEX_EXPAND_ENABLED or "\\" not in text:
        return text

    def _repl(m):
        g = m.group
        if g("esc") is not None:
            return m.group(0)

        value = None
        if g("cpbrace") is not None:
            value = _lx_codepoint_list(g("cpbrace"))
        elif g("cp4") is not None:
            value = _lx_codepoint(g("cp4"))
        elif g("cpu4") is not None:
            value = _lx_codepoint(g("cpu4"))
        elif g("cpU8") is not None:
            value = _lx_codepoint(g("cpU8"))
        elif g("chex") is not None:
            value = _lx_codepoint(g("chex"))
        elif g("coct") is not None:
            try:
                value = chr(int(g("coct"), 8))
            except (ValueError, OverflowError):
                value = None
        elif g("cdec") is not None:
            try:
                cp = int(g("cdec"), 10)
                value = chr(cp) if 0 <= cp <= 0x10FFFF and not (0xD800 <= cp <= 0xDFFF) else None
            except (ValueError, OverflowError):
                value = None
        elif g("specw") is not None:
            value = LATEX_SPECIAL_WORD_MAP.get(g("specw"))
            # 제어어 뒤의 {} 나 공백 한 칸은 TeX 규칙대로 흡수, 그 외 공백류는 보존
            tail = g("specw_tail")
            if value is not None and tail and tail not in ("{}", " ", "\t"):
                value = value + tail
        elif g("specs") is not None:
            value = LATEX_SPECIAL_SYM_MAP.get(g("specs"))
        elif g("acca") is not None:
            value = _lx_apply_accent(LATEX_ACCENT_MAP[g("acca")], _lx_accent_base(g("arga")))
        elif g("accs") is not None:
            value = _lx_apply_accent(LATEX_ACCENT_MAP[g("accs")], _lx_accent_base(g("args")))

        if value is None:
            return m.group(0)          # 해석 실패 시 원문 보존
        if protect is None:
            return value
        protect.append(value)
        return f"{_LX_OPEN}{len(protect) - 1}{_LX_CLOSE}"

    return LATEX_INPUT_RE.sub(_repl, text)


def restore_latex_input(text, saved):
    for idx, ch in enumerate(saved):
        text = text.replace(f"{_LX_OPEN}{idx}{_LX_CLOSE}", ch)
    return text


def convert_text(text, engine_mode="pm"):
    if not text: return ""

    # ==========================================
    # 0. LaTeX 입력 확장 (모든 입력 메서드 공통, 최우선 처리)
    #    확장 결과는 PUA 마커로 봉인해 두었다가 마지막에 복원한다.
    # ==========================================
    latex_saved = []
    text = expand_latex_input(text, protect=latex_saved)

    if engine_mode == "transparent":
        return restore_latex_input(text, latex_saved)

    # ==========================================
    # 1. 라틴 문자 보호 구문 및 LaTeX 명령어 보호
    # ==========================================
    # 1) (\\[^\s\\].*?\\[ \t]) : 시작은 '\' + 공백아님, 끝은 '\' + 공백/탭 (\Apple\ )
    # 2) (\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\s*\{?)?) : 일반 LaTeX 명령어 (\Apple 등)
    cmd_pattern = (
        r"(\\[^\s\\].*?\\[ \t])"              # 기존: \Word ... \[space] 리터럴 보호
        r"|(\\(?:begin|end)\{[^}]*\})"        # 신규: \begin{...} / \end{...} 환경 이름 통째 보호
        r"|(\\[a-zA-Z]+(?:\[[^\]]*\])?(?:\s*\{?)?)"  # 기존: 일반 명령어(인자는 변환 대상으로 남김)
    )
    saved_commands = []

    def replacer(match):
        cmd = match.group(0)
        saved_commands.append(cmd)
        return f"{_CMD_OPEN}{len(saved_commands)-1}{_CMD_CLOSE}"

    protected_text = re.sub(cmd_pattern, replacer, text)

    # ==========================================
    # 2. 치환
    # ==========================================
    # 호환자모 처리
    if engine_mode in ("pm", "pmfrk"):
        sorted_generic = sorted(pm_map["generic"].items(), key=lambda x: len(x[1]), reverse=True)
        for kor_char, rom_upper in sorted_generic:
            protected_text = protected_text.replace(rom_upper, kor_char)

    # 숫자+대괄호 치환
    sorted_brackets = sorted(bracket_map.items(), key=lambda x: len(x[0]), reverse=True)
    for key, (open_bracket, close_bracket) in sorted_brackets:
        protected_text = protected_text.replace(f"{key}[", open_bracket)
        protected_text = protected_text.replace(f"{key}]", close_bracket)

    # 방점 보호
    hat_markers = {}
    for i, (k, v) in enumerate(hat_map.items()):
        marker = f"{_HAT_OPEN}{i}{_HAT_CLOSE}"
        hat_markers[marker] = v
        protected_text = protected_text.replace(k, marker)

    # 자음 분리 (rrk, pmfrk)
    if engine_mode in ("pmfrk", "rrk"):        
        # 1. 'ss'로 시작하는 그룹 처리
        protected_text = re.sub(r"ss([sgdbj])", r"ss-\1", protected_text)
        
        # 2. 'ggg' 처리
        protected_text = protected_text.replace("ggg", "g-gg")
        
        # 3. 모음 사이의 sg, sd, sb, sch, sj 분리 
        # 어두나 기분리된 하이픈(-sg)에서는 무시하고 오직 모음(a,e,i,o,u,w,y) 사이에서만 동작
        protected_text = re.sub(r"(?<=[aeiouwyAEIOUWY])s(g|d|b|ch|j)(?=[aeiouwyAEIOUWY])", r"s-\1", protected_text)
        
        # 4. (기존 pmfrk 전용) sss 패턴 추가 처리
        if engine_mode == "pmfrk":
            vowels = "aeiouAEIOU"
            sss_pattern = rf"([{vowels}])sss([{vowels}])"
            protected_text = re.sub(sss_pattern, r"\1ss-s\2", protected_text)

    # 단어 단위 분리 및 변환
    if engine_mode in ("pm", "frkim", "pmfrk", "rrk"):  # "rrk" 추가
        def replacer_chunk(m):
            return parse_auto_chunk(m.group(1), engine_mode)
        
        chunk_pattern = r"([a-zA-Z\@\*\-\/\'\:\;]+)"
        intermediate = re.sub(chunk_pattern, replacer_chunk, protected_text)
    elif engine_mode == "kana":
        intermediate = romaji_to_kana_convert(protected_text) 
    else:
        intermediate = protected_text

    # ==========================================
    # 3. 복원 로직
    # ==========================================
    for idx, orig_cmd in enumerate(saved_commands):
        marker = f"{_CMD_OPEN}{idx}{_CMD_CLOSE}"
        
        # 라틴 문자 보호 구문 (끝이 백슬래시+공백)
        if orig_cmd.endswith('\\ ') or orig_cmd.endswith('\\\t'):
            # 맨 앞의 '\'(1글자)와 맨 뒤의 '\ '(2글자) 완벽 제거
            pure_latex_cmd = orig_cmd[1:-2]
        else:
            # 일반 LaTeX 명령어 복원
            if orig_cmd.startswith("\\\\"):
                pure_latex_cmd = "\\" + orig_cmd[2:]
            else:
                pure_latex_cmd = orig_cmd.replace("\\\\", "\\")
                
        intermediate = intermediate.replace(marker, pure_latex_cmd)

    # 방점 기호 복원
    for marker, char in hat_markers.items():
        intermediate = intermediate.replace(marker, char)

    # LaTeX 확장 문자 복원
    intermediate = restore_latex_input(intermediate, latex_saved)

    return intermediate


# NFD 출력 시 한글만 분해하고 라틴 확장문자는 결합형으로 유지할지 여부
NFD_HANGUL_ONLY = True

def _is_hangul_char(ch):
    code = ord(ch)
    return (0xAC00 <= code <= 0xD7A3 or   # 한글 음절
            0x1100 <= code <= 0x11FF or   # 한글 자모
            0xA960 <= code <= 0xA97F or   # 한글 자모 확장 A
            0xD7B0 <= code <= 0xD7FF)     # 한글 자모 확장 B

def normalize_output(text, norm_mode="NFD", hangul_only=None):
    if not text: return ""
    if hangul_only is None:
        hangul_only = NFD_HANGUL_ONLY
    # NFD를 문자열 전체에 걸면 \'e -> e+U+0301 처럼 라틴 확장문자까지 분해된다.
    # 옛한글 조합에 필요한 것은 한글 분해뿐이므로 한글 문자에만 선택 적용한다.
    if norm_mode == "NFD" and hangul_only:
        return "".join(unicodedata.normalize("NFD", ch) if _is_hangul_char(ch) else ch
                       for ch in text)
    return unicodedata.normalize(norm_mode, text)

if GUI_AVAILABLE:
    class KanjiAssistant(QWidget):
        kanji_selected = pyqtSignal(str)

        def __init__(self, parent=None):
            super().__init__(parent, Qt.WindowType.Tool | Qt.WindowType.WindowStaysOnTopHint)
            self.setWindowTitle("일본어 한자 입력")
            
            self.resize(300, 310)

            kanji_font = QFont("Noto Sans CJK KR", 11)
            self.setFont(kanji_font)
            
            layout = QVBoxLayout(self)
            layout.setContentsMargins(5, 5, 5, 5)
            
            self.search_input = QLineEdit()
            self.search_input.setPlaceholderText("검색어 입력 (Ctrl+F로 포커스)")
            self.search_input.textChanged.connect(self.filter_items)
            layout.addWidget(self.search_input)
            
            self.result_list = QListWidget()
            self.result_list.itemDoubleClicked.connect(self.on_item_double_clicked)
            layout.addWidget(self.result_list)
            
            # -----------------------------------------------------------------
            # "새 단어 등록" 버튼 배치
            # -----------------------------------------------------------------
            self.register_btn = QPushButton("새 단어 등록")
            self.register_btn.clicked.connect(self.show_registration_dialog)
            layout.addWidget(self.register_btn)
            
            self.full_data = kanji_tables.get("custom_kana", {})
            self.shinjitai_data = kanji_tables.get("shinjitai", {})
            
            self.populate_list(self.full_data)

            # 엔터키 연결 유지 (검색창용)
            self.search_input.returnPressed.connect(self.on_enter_pressed)

            # 키보드 이벤트를 직접 통제하기 위해 이벤트 필터 설치
            self.search_input.installEventFilter(self)
            self.result_list.installEventFilter(self)

        # 창이 표시될 때마다 메인 윈도우 우측 하단으로 위치 고정
        def showEvent(self, event):
            super().showEvent(event)
            if self.parent():
                parent_rect = self.parent().geometry()
                margin = 20
                x = parent_rect.right() - self.width() - margin
                y = parent_rect.bottom() - self.height() - margin
                self.move(x, y)

        # 방향키 및 엔터키 흐름
        def eventFilter(self, source, event):
            if event.type() == QEvent.Type.ShortcutOverride:
                if event.key() == Qt.Key.Key_Escape:
                    event.accept()
                    return True

            if event.type() == QEvent.Type.KeyPress:
                if event.key() == Qt.Key.Key_Escape:
                    if self.search_input.text():
                        self.search_input.clear()
                        self.search_input.setFocus()
                    else:
                        self.hide()
                    return True

                if Qt.Key.Key_0 <= event.key() <= Qt.Key.Key_9:
                    index = event.key() - Qt.Key.Key_0
                    if index < self.result_list.count():
                        item = self.result_list.item(index)
                        self._send_item_data(item)
                    return True

                if source == self.search_input and event.key() == Qt.Key.Key_Down:
                    self.result_list.setFocus()
                    if self.result_list.currentRow() < 0 and self.result_list.count() > 0:
                        self.result_list.setCurrentRow(0)
                    return True

                elif source == self.result_list and event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    self.on_enter_pressed()
                    return True

            return super().eventFilter(source, event)

        def populate_list(self, data):
            self.result_list.clear()
            sorted_items = sorted(data.items(), key=lambda item: len(item[0]), reverse=False)
            
            for index, (key, val) in enumerate(sorted_items):
                if index <= 9:
                    display_text = f"[{index}] {val} - {key}"
                else:
                    display_text = f"    {val} - {key}"
                
                list_item = QListWidgetItem(display_text)
                list_item.setData(Qt.ItemDataRole.UserRole, key)
                self.result_list.addItem(list_item)
                
            if self.result_list.count() > 0:
                self.result_list.setCurrentRow(0)

        def filter_items(self, text):
            if not text:
                self.populate_list(self.full_data)
                return
            
            converted_text = "".join([self.shinjitai_data.get(char, char) for char in text])
            text_lower = text.lower()
            converted_lower = converted_text.lower()

            filtered = {}
            for key, val in self.full_data.items():
                if (text_lower in key.lower() or text_lower in val.lower() or
                    converted_lower in key.lower() or converted_lower in val.lower()):
                    filtered[key] = val
                    
            self.populate_list(filtered)

        def _send_item_data(self, item):
            if item:
                kanji_key = item.data(Qt.ItemDataRole.UserRole)
                self.kanji_selected.emit(kanji_key)

        def on_item_double_clicked(self, item):
            self._send_item_data(item)

        def on_enter_pressed(self):
            self._send_item_data(self.result_list.currentItem())
                
        def closeEvent(self, event):
            self.hide()
            event.ignore()

        # -----------------------------------------------------------------
        # 새 단어 등록 다이알로그 및 저장/메모리 동기화
        # -----------------------------------------------------------------
        def show_registration_dialog(self):
            """간단한 입력 폼 다이알로그를 띄워 Key와 Value를 입력받음"""
            dialog = QDialog(self)
            dialog.setWindowTitle("새 단어 등록")
            dialog.setWindowModality(Qt.WindowModality.WindowModal) # 부모 창을 블록함
            
            dial_layout = QFormLayout(dialog)
            
            key_edit = QLineEdit()
            key_edit.setPlaceholderText("예: 단어 뒤 숫자가 붙은 형태 등")
            val_edit = QLineEdit()
            val_edit.setPlaceholderText("예: 漢字")
            
            dial_layout.addRow("검색키 (Key):", key_edit)
            dial_layout.addRow("변환값 (Value):", val_edit)
            
            btn_box = QDialogButtonBox(QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel)
            btn_box.accepted.connect(dialog.accept)
            btn_box.rejected.connect(dialog.reject)
            dial_layout.addRow(btn_box)
            
            # 확인(Ok)을 누른 경우에만 파일 저장 로직 실행
            if dialog.exec() == QDialog.DialogCode.Accepted:
                key = key_edit.text().strip()
                val = val_edit.text().strip()
                
                if key and val:
                    self.save_new_word(key, val)

        def save_new_word(self, key, val):
            """customkanji.json 파일에 단순 딕셔너리 형태로 저장하고 실시간 메모리 동기화"""
            file_path = find_file("customkanji.json")
            data = {}

            # 1. 기존 파일 읽기
            if file_path:
                try:
                    with open(file_path, "r", encoding="utf-8") as f:
                        data = _clean_table(json.load(f), file_path)
                except Exception as e:
                    # 읽지 못한 채로 저장하면 기존 사전 전체가 새 단어 하나로 덮어써진다 -> 중단
                    QMessageBox.warning(self, "새 단어 등록",
                        f"사용자 사전을 읽을 수 없어 저장하지 않았습니다.\n{file_path}\n{e}")
                    return
                # PyInstaller 임시 폴더 안의 사본은 종료하면 사라지므로 실행 파일 옆에 쓴다
                meipass = getattr(sys, '_MEIPASS', None)
                if meipass and os.path.abspath(file_path).startswith(os.path.abspath(meipass) + os.sep):
                    file_path = os.path.join(app_dir(), "customkanji.json")
            else:
                # customkanji.json이 어디에도 없는 최초 실행 상태
                if platform.system() == "Windows":
                    base_dir = app_dir()
                else:
                    base_dir = os.path.expanduser("~/.config/pmimegui")
                file_path = os.path.join(base_dir, "customkanji.json")

            # 2. {h: } 포맷팅 적용 및 중복 키 검사
            base_key = key.strip()
            
            # 사용자가 실수로 {h: }를 직접 입력했을 경우를 대비해 벗겨냄
            if base_key.startswith("{h:") and base_key.endswith("}"):
                base_key = base_key[3:-1]

            final_key = f"{{h:{base_key}}}"
            
            # 중복 검사: 단순 딕셔너리 구조 내에서 즉시 비교
            if final_key in data:
                for i in range(1, 100):
                    new_key = f"{{h:{base_key}{i:02d}}}"
                    if new_key not in data:
                        final_key = new_key
                        break
            
            # 최종 확정된 단순 키 위치에 값 할당
            data[final_key] = val

            # 3. JSON 파일 저장 (임시 파일에 다 쓴 뒤 교체 -> 쓰다 죽어도 원본은 남는다)
            tmp_path = file_path + ".tmp"
            try:
                os.makedirs(os.path.dirname(file_path), exist_ok=True)
                with open(tmp_path, "w", encoding="utf-8") as f:
                    json.dump(data, f, ensure_ascii=False, indent=2)
                    f.flush()
                    os.fsync(f.fileno())
                os.replace(tmp_path, file_path)
            except Exception as e:
                try:
                    os.remove(tmp_path)
                except OSError:
                    pass
                QMessageBox.warning(self, "새 단어 등록",
                    f"사용자 사전을 저장하지 못했습니다.\n{file_path}\n{e}")
                return

            # 4. 실시간 메모리 데이터(kanji_tables 전역 변수 및 내부 캐시) 즉시 동기화
            load_kanji_tables()
            kanji_tables["custom_kana"] = data
            self.full_data = data
            
            # 5. 현재 검색창 텍스트를 기준으로 즉시 리스트 위젯 리프레시
            self.filter_items(self.search_input.text())
            self.search_input.setFocus()
            
    class MainWindow(QWidget):
        def __init__(self):
            super().__init__()
            self.settings = QSettings("ktug.org", "pmIMEgui")

            icon_path = resource_path("pmimegui.png")
            if os.path.exists(icon_path):
                self.setWindowIcon(QIcon(icon_path))
            else:
                print(f"로그: 아이콘 파일을 찾을 수 없습니다 -> {icon_path}")

            self._last_sent_input = ""
            self._is_sending = False
            
            load_kanji_tables()
            self.init_ui()
            
        def init_ui(self):
            self.setWindowTitle(f"pm IME GUI v{__version__}")
            self.resize(400, 580)
            main_layout = QVBoxLayout(self)
            
            # 상단 설정 레이아웃 (콤보박스 라인)
            top_layout = QHBoxLayout()
            self.mode_combo = QComboBox()
            self.mode_combo.addItems(["pm (pm)", "frkim (frk)", "mix (mix)", "rrk-ex (rrk)", "Kana (jp)", "transparent"])
            self.mode_combo.setCurrentIndex(self.settings.value("engine_mode_index", 0, type=int))
            self.mode_combo.currentIndexChanged.connect(self.update_translation)
            self.mode_combo.currentIndexChanged.connect(self.save_settings)
            top_layout.addWidget(QLabel("입력 메서드:"))
            top_layout.addWidget(self.mode_combo)
            
            self.hanja_combo = QComboBox()
            self.hanja_combo.addItems(["없음(none)", "新字体(shin)", "舊字體(kyu)", "简体(sim)"])
            self.hanja_combo.setCurrentIndex(self.settings.value("hanja_mode_index", 0, type=int))
            self.hanja_combo.currentIndexChanged.connect(self.update_translation)
            self.hanja_combo.currentIndexChanged.connect(self.save_settings)
            top_layout.addWidget(QLabel("한자 필터:"))
            top_layout.addWidget(self.hanja_combo)
            
            self.norm_combo = QComboBox()
            self.norm_combo.addItems(["NFD", "NFC"])
            self.norm_combo.setCurrentIndex(self.settings.value("norm_mode_index", 0, type=int))
            self.norm_combo.currentIndexChanged.connect(self.update_translation)
            self.norm_combo.currentIndexChanged.connect(self.save_settings)
            top_layout.addWidget(QLabel("정규화:"))
            top_layout.addWidget(self.norm_combo)
            
            top_layout.addStretch()
            main_layout.addLayout(top_layout)
            
            # 중앙 텍스트 에디터 영역
            splitter = QSplitter(Qt.Orientation.Vertical)
            self.input_edit = QTextEdit()
            self.input_edit.setPlaceholderText("줄머리 %pm, %frk, %mix, %rrk, %jp, %clean. Shift+Enter 개행")
            self.input_edit.textChanged.connect(self.update_translation)
            
            # 운영체제별 입력창 폰트 설정
            current_os = platform.system()
            if current_os == "Windows":
                font = QFont("Consolas", 12)
            elif current_os == "Darwin":
                font = QFont("Menlo", 14)
            else:
                font = QFont("Free Sans", 13)
            self.input_edit.setFont(font)
            splitter.addWidget(self.input_edit)
            
            self.output_edit = QTextEdit()
            self.output_edit.setReadOnly(True)
            
            # ----------------------------------------------------
            # 출력창 폰트 변경
            # ----------------------------------------------------
            # Mac의 Hiragino와 Win의 MS Gothic을 크로스플랫폼 대응용 튜플로 묶음
            self.font_mapping = {
                0: ("Noto Sans CJK KR", "Source Han Sans KR"),
                1: ("Noto Serif CJK KR", "Source Han Serif KR"),
                2: ("HCR Batang LVT", "HCRBatangLVT", "HCR Batang", "HCRBatang"), 
                3: ("Malgun Gothic", "맑은 고딕"),
                4: ("KoPubWorldDotum Medium", "KoPubWorldDotumMedium"),
                5: ("Hiragino Mincho ProN", "MS Mincho", "TakaoMincho", "Harano Aji Mincho")
            }
            
            splitter.addWidget(self.output_edit)
            main_layout.addWidget(splitter)
            
            # 하단 버튼 바로 위에 배치할 폰트 선택 레이아웃
            font_layout = QHBoxLayout()
            font_layout.addWidget(QLabel("출력 폰트:"))
            
            self.font_combo = QComboBox()
            self.font_combo.addItems([
                "Noto Sans CJK KR",
                "Noto Serif CJK KR",
                "함초롬바탕 LVT / 함초롬바탕",
                "Malgun Gothic",
                "KoPubWorldDotum",
                "Hiragino / MS Mincho"
            ])
            self.font_combo.setCurrentIndex(self.settings.value("output_font_index", 0, type=int))
            self.font_combo.currentIndexChanged.connect(self.apply_output_font)
            self.font_combo.currentIndexChanged.connect(self.save_settings)
            
            font_layout.addWidget(self.font_combo)
            
            # 여백을 추가하여 폰트 콤보는 왼쪽에, 체크박스는 오른쪽에 밀착시킴
            font_layout.addStretch()

            # LaTeX 확장 입력 토글 (모든 입력 메서드에 전역 적용)
            self.latex_cb = QCheckBox("LaTeX 확장 입력")
            self.latex_cb.setToolTip(
                "확장 라틴문자와 유니코드 코드포인트를 실제 문자로 렌더링합니다.\n"
                "예) \\'e → é   \\v{s} → š   \\ss → ß   \\xAC00 → 가   \\x{1F600} → 😀"
            )
            self.latex_cb.setChecked(self.settings.value("latex_expand", True, type=bool))
            set_latex_expand(self.latex_cb.isChecked())
            self.latex_cb.stateChanged.connect(self.on_latex_toggle)
            font_layout.addWidget(self.latex_cb)

            self.clear_after_send_cb = QCheckBox("전송 후 초기화")
            # 설정값 복원 (기본값은 True로 설정하여 기존 동작 유지)
            self.clear_after_send_cb.setChecked(self.settings.value("clear_after_send", True, type=bool))
            self.clear_after_send_cb.stateChanged.connect(self.save_settings)
            font_layout.addWidget(self.clear_after_send_cb)
            
            self.send_prev_cb = QCheckBox("직전 창 전송")
            # 설정값 복원 (기본값은 False)
            self.send_prev_cb.setChecked(self.settings.value("send_prev_window", False, type=bool))
            self.send_prev_cb.stateChanged.connect(self.save_settings)
            
            font_layout.addWidget(self.send_prev_cb)
            # -----------------------------------
            
            main_layout.addLayout(font_layout)
            
            # 하단 버튼 컨트롤 타워
            btn_layout = QHBoxLayout()
            
            self.send_btn = QPushButton("클립보드로 전송 (Enter)")
            self.send_btn.clicked.connect(self.send_to_editor)
            btn_layout.addWidget(self.send_btn)
            
            self.undo_btn = QPushButton("직전 전송 복구 (Alt+Z)")
            self.undo_btn.clicked.connect(self.undo_send)
            btn_layout.addWidget(self.undo_btn)
            
            self.clear_btn = QPushButton("지우기 (ESC)")
            self.clear_btn.clicked.connect(self.clear_text)
            btn_layout.addWidget(self.clear_btn)
            
            main_layout.addLayout(btn_layout)
            
            # 상태 표시줄 및 전역 단축키 맵
            self.status_bar = QStatusBar()
            main_layout.addWidget(self.status_bar)
            
            QShortcut(QKeySequence("Escape"), self, self.clear_text)
            QShortcut(QKeySequence("Alt+Z"), self, self.undo_send)
            QShortcut(QKeySequence("F1"), self, self.show_help)
            
            self.input_edit.installEventFilter(self)
            self.input_edit.setFocus()
            
            # 초기 폰트 적용
            self.apply_output_font(self.font_combo.currentIndex())

            # 한자 검색 보조창 초기화
            self.kanji_assistant = KanjiAssistant(self)
            self.kanji_assistant.kanji_selected.connect(self.insert_kanji_to_editor)
            
            # F10: 보조창 토글
            self.shortcut_f10 = QShortcut(QKeySequence("F10"), self)
            self.shortcut_f10.activated.connect(self.toggle_kanji_assistant)
            
            # Ctrl+F: 보조창 검색 필드로 포커스 이동
            self.shortcut_alt_f = QShortcut(QKeySequence("Ctrl+F"), self)
            # QApplication 차원에서 이 단축키를 잡아야 보조창이 활성화되어 있을 때도 먹힙니다.
            self.shortcut_alt_f.setContext(Qt.ShortcutContext.ApplicationShortcut)
            self.shortcut_alt_f.activated.connect(self.focus_kanji_search)

        def apply_output_font(self, index):
            font_families = self.font_mapping.get(index, ("Noto Sans CJK KR",))
            
            font = QFont()
            font.setFamilies(font_families)
            font.setPointSize(20)
            
            self.output_edit.setFont(font)

        def get_hanja_mode_str(self):
            return ["none", "shinjitai", "kyujitai", "simplified"][self.hanja_combo.currentIndex()]

        def update_translation(self):
            if getattr(self, '_is_sending', False):
                return  # 전송 중일 때는 시그널이 발생해도 무조건 즉시 탈출!
    
            input_text = self.input_edit.toPlainText()
            lines = input_text.split('\n')
            final_output_lines = []

            global_modes = ["pm", "frkim", "pmfrk", "rrk", "kana", "transparent"]
            default_mode = global_modes[self.mode_combo.currentIndex()]
            global_h_mode = self.get_hanja_mode_str()

            for line in lines:
                current_mode = default_mode
                current_h_mode = global_h_mode
                clean_line = line

                match = re.match(r"^%(pm|frk|mix|rrk|jp|clean)(?:\[(shin|kyu|sim|none|han)\])?", line)

                if match:
                    mode_tag = match.group(1)
                    hanja_tag = match.group(2)

                    # 1단계: 글자 변환 메서드 매핑
                    if mode_tag == "pm": current_mode = "pm"
                    elif mode_tag == "frk": current_mode = "frkim"
                    elif mode_tag == "mix": current_mode = "pmfrk"
                    elif mode_tag == "rrk": current_mode = "rrk"
                    elif mode_tag == "jp": current_mode = "kana"
                    elif mode_tag == "clean": current_mode = "transparent"

                    # 2단계: 대괄호 내부 한자 옵션 정밀 매핑 (none 분기 신설)
                    if hanja_tag == "shin": current_h_mode = "shinjitai"
                    elif hanja_tag == "kyu": current_h_mode = "kyujitai"
                    elif hanja_tag == "sim": current_h_mode = "simplified"
                    elif hanja_tag == "none": current_h_mode = "none" # 한자 필터 강제 무력화
                    elif hanja_tag == "han": current_h_mode = "hanja"

                    # 3단계: 매칭된 태그 문장 규격만큼 본문 슬라이싱 후 공백 청소
                    raw_text_start = match.end()
                    clean_line = line[raw_text_start:]
                    clean_line = re.sub(r"^\s+", "", clean_line)

                # 핵심 백엔드 변환 및 동적 한자 필터 가동
                intermediate = convert_text(clean_line, engine_mode=current_mode)
                converted_line = filter_kanji(intermediate, hanja_mode=current_h_mode)

                # 옛한글 모드 정규화
                if current_mode != "kana":
                    norm_mode = "NFC" if self.norm_combo.currentIndex() == 1 else "NFD"
                    converted_line = normalize_output(converted_line, norm_mode=norm_mode)

                final_output_lines.append(converted_line)

            self.output_edit.setPlainText("\n".join(final_output_lines))

        def on_latex_toggle(self):
            set_latex_expand(self.latex_cb.isChecked())
            self.save_settings()
            self.update_translation()

        def save_settings(self):
            self.settings.setValue("latex_expand", self.latex_cb.isChecked())
            self.settings.setValue("engine_mode_index", self.mode_combo.currentIndex())
            self.settings.setValue("hanja_mode_index", self.hanja_combo.currentIndex())
            self.settings.setValue("norm_mode_index", self.norm_combo.currentIndex())
            self.settings.setValue("output_font_index", self.font_combo.currentIndex())
            self.settings.setValue("send_prev_window", self.send_prev_cb.isChecked())
            self.settings.setValue("clear_after_send", self.clear_after_send_cb.isChecked())

        def clear_text(self):
            # 청소 시작 전 현재 원문을 안전하게 백업
            current_input = self.input_edit.toPlainText()
            
            if current_input.strip():  # 비어있지 않을 때만 백업 (의미 있는 데이터 보호)
                self._last_sent_input = current_input
                
                # 가드 가동 (clear 과정에서 실시간 번역 이벤트 트리거 방지)
                self._is_sending = True
                
                self.input_edit.clear()
                self.output_edit.clear()
                
                # 가드 해제
                self._is_sending = False
                
                self.status_bar.showMessage("작업 내역 초기화됨 (ESC) - 복구 가능", 2000)
            else:
                # 이미 비어있는 상태라면 그냥 깔끔하게 청소 처리
                self.input_edit.clear()
                self.output_edit.clear()
                self.status_bar.showMessage("작업 내역 초기화됨 (ESC)", 2000)

        def send_to_editor(self):
            txt = self.output_edit.toPlainText() 
            if txt:
                # 1단계: 청소 시작 전 현재 원문을 완벽하게 변수에 고정
                current_input = self.input_edit.toPlainText()
                
                if copy_to_clipboard(txt):
                    self.status_bar.showMessage("클립보드 복사 완료", 2000)
                    
                    # 2단계: 복사 성공 직후 안전하게 백업 전역 변수에 안착
                    self._last_sent_input = current_input
                    
                    # --- 수정된 부분: 전송 후 초기화 여부 체크 ---
                    if self.clear_after_send_cb.isChecked():
                        # 3단계: 가드 성벽 가동 (update_translation의 접근을 원천 봉쇄)
                        self._is_sending = True
                        
                        # 4단계: 안심하고 양쪽 창 청소 수행
                        self.input_edit.clear()
                        self.output_edit.clear()
                        
                        # 5단계: 청소 작전 종료 후 성벽 해제
                        self._is_sending = False
                    else:
                        # 초기화를 하지 않더라도 백업은 이미 완료되었으므로 알림 상태 유지 및 통과
                        pass
                    # --------------------------------------------
                    
                    # 6단계: '직전 창 전송' 체크박스가 켜져 있다면 포커스 이동 및 붙여넣기 실행
                    if self.send_prev_cb.isChecked():
                        import platform
                        import time
                        current_os = platform.system()
                        
                        if current_os == "Darwin":
                            import subprocess
                            script = '''
                            tell application "System Events"
                                keystroke tab using command down
                                delay 0.3
                                keystroke "v" using command down
                            end tell
                            '''
                            try:
                                done = subprocess.run(['/usr/bin/osascript', '-e', script],
                                                      timeout=10, capture_output=True).returncode == 0
                            except (OSError, subprocess.SubprocessError):
                                done = False
                            if done:
                                self.status_bar.showMessage("직전 창으로 전송 및 붙여넣기 완료!", 3000)
                            else:
                                self.status_bar.showMessage("⚠️ 붙여넣기 실패(손쉬운 사용 권한 확인): 클립보드 복사만 수행되었습니다.", 4000)
                            
                        elif current_os == "Windows":
                            try:
                                import pyautogui
                                pyautogui.keyUp('ctrl')
                                pyautogui.hotkey('alt', 'tab')
                                time.sleep(0.3)
                                pyautogui.hotkey('ctrl', 'v')
                                self.status_bar.showMessage("직전 창으로 전송 및 붙여넣기 완료!", 3000)
                            except ImportError:
                                # pyautogui가 설치되어 있지 않은 경우의 안전 장치
                                self.status_bar.showMessage("⚠️ pyautogui 누락: 클립보드 복사만 수행되었습니다.", 3000)
                else:
                    self.status_bar.showMessage("❌ 클립보드 복사 실패! 입력을 유지합니다.", 3000)

        def undo_send(self):
            if self._last_sent_input:
                self.input_edit.setPlainText(self._last_sent_input)
                self._last_sent_input = ""
                self.status_bar.showMessage("이전 입력 복구 완료", 2000)
            else:
                self.status_bar.showMessage("❌ 복구할 내역이 없습니다.", 2000)

        def eventFilter(self, obj, event):
            """입력창 키 필터: Enter는 전송, Shift+Enter는 개행만 순수하게 분리"""
            if obj is self.input_edit and event.type() == event.Type.KeyPress:
                if event.key() in (Qt.Key.Key_Return, Qt.Key.Key_Enter):
                    modifiers = event.modifiers()
                    
                    # 오직 Enter만 단독으로 눌린 경우 -> 클립보드로 전송
                    if not (modifiers & Qt.KeyboardModifier.ShiftModifier):
                        self.send_to_editor()
                        return True
                    
            return super().eventFilter(obj, event)


        def toggle_kanji_assistant(self):
            if self.kanji_assistant.isVisible():
                self.kanji_assistant.hide()
                self.input_edit.setFocus()  # 창을 닫으면 메인 에디터로 포커스 복귀
            else:
                self.kanji_assistant.show()
                self.kanji_assistant.search_input.setFocus()
                self.kanji_assistant.search_input.selectAll()

        def focus_kanji_search(self):
            if self.kanji_assistant.isVisible():
                self.kanji_assistant.activateWindow()
                self.kanji_assistant.search_input.setFocus()
                self.kanji_assistant.search_input.selectAll()

        def insert_kanji_to_editor(self, kanji_text):
            # 1. 텍스트 삽입
            cursor = self.input_edit.textCursor()
            cursor.insertText(kanji_text)
            
            # 2. 보조창 검색창 비우기 (다음 검색을 위해)
            self.kanji_assistant.search_input.clear()
            
            # 3. 메인 윈도우 자체를 활성화한 뒤, 에디터에 포커스 주기
            self.activateWindow()       # OS 레벨에서 메인 창으로 포커스를 가져옴
            self.input_edit.setFocus()  # 그 안의 입력 에디터에 커서를 깜빡이게 함

        def show_help(self):
            help_dialog = QDialog(self)
            help_dialog.setWindowTitle("pmIME 도움말 및 가이드")
            help_dialog.resize(500, 480)
            layout = QVBoxLayout(help_dialog)
            
            browser = QTextBrowser()
            browser.setOpenExternalLinks(True)
            
            help_html = """
            <h3>💡 행별 독립 제어 % 매직 태그 신택스</h3>
            <p>각 행의 <b>맨 첫머리</b>에 아래 태그를 붙이면 해당 줄만 독립 엔진으로 작동합니다.</p>
            <table border="1" cellpadding="5" style="border-collapse:collapse; border-color:#ccc; width:100%;">
                <tr bgcolor="#f2f2f2"><th>매직 태그</th><th>글자 변환 메서드 (엔진 종류)</th></tr>
                <tr><td><b>%pm </b></td><td>pm 방식 (음절 구분자: /)</td></tr>
                <tr><td><b>%frk </b></td><td>frkim 방식 (자동 청크 분리, 음절 구분자: ')</td></tr>
                <tr><td><b>%mix </b></td><td>pmfrk 혼합 방식 (자동 청크 분리)</td></tr>
                <tr><td><b>%jp </b></td><td>일본어 로마자 -> 카나(Kana) 변환 모드</td></tr>
                <tr><td><b>%clean </b></td><td>변환없음</td></tr>
            </table>
            <br>
            <h4>🎯 대괄호 한자 필터 옵션 (메서드 태그에 밀착 지정)</h4>
            <p>태그 뒤에 스페이스 없이 대괄호로 한자 옵션을 주어 행별 자형 필터를 강제합니다.</p>
            <ul>
                <li><b>%pm[shin] </b> : pm 방식 + 일본어 신자체(新字体) 필터</li>
                <li><b>%frk[kyu] </b> : frkim 방식 + 일본어 구자체(旧字体) 필터</li>
                <li><b>%mix[sim] </b> : pmfrk 방식 + 중국어 간체(简体) 필터</li>
                <li><i>※ 옵션 생략 시(예: %pm) 상단 콤보박스의 글로벌 설정을 그대로 추종합니다.</i></li>
            </ul>
            <hr>
            <h3>🔤 LaTeX 확장 라틴문자 (입력 메서드 무관, 전역 적용)</h3>
            <p>하단 <b>[LaTeX 확장 입력]</b> 체크 시, 어떤 엔진 모드에서도 아래 표기가 실제 문자로 렌더링됩니다.
            결과 문자는 한글 변환 대상에서 제외되므로 로마자 사이에 섞어 써도 안전합니다.</p>
            <table border="1" cellpadding="4" style="border-collapse:collapse; border-color:#ccc; width:100%;">
                <tr bgcolor="#f2f2f2"><th>입력</th><th>결과</th><th>입력</th><th>결과</th></tr>
                <tr><td>\\'e \\`e \\^e \\"o \\~n</td><td>é è ê ö ñ</td><td>\\=a \\.z \\u{g} \\v{s}</td><td>ā ż ğ š</td></tr>
                <tr><td>\\H{o} \\r{a} \\c{c} \\k{a}</td><td>ő å ç ą</td><td>\\d{s} \\b{h} \\t{oo}</td><td>ṣ ẖ o͡o</td></tr>
                <tr><td>\\ss \\ae \\oe \\o \\l</td><td>ß æ œ ø ł</td><td>\\i \\j \\th \\dh \\ng</td><td>ı ȷ þ ð ŋ</td></tr>
                <tr><td>\\'{\\i} \\'{\\v{s}}</td><td>í š́ (중첩 가능)</td><td>\\textemdash \\texteuro \\%</td><td>— € %</td></tr>
            </table>
            <p><i>※ 액센트 이름이 영문자인 명령(\\v \\u \\c \\d \\t 등)은 TeX 규칙대로 <b>{ } 또는 공백</b>이 뒤따를 때만
            동작합니다. 따라서 \\textbf, \\begin 같은 일반 명령과 충돌하지 않습니다.</i></p>
            <hr>
            <h3>#️⃣ 유니코드 코드포인트 직접 입력</h3>
            <ul>
                <li><b>\\xAC00</b> → 가 &nbsp;(16진수 4자리 직접 표기)</li>
                <li><b>\\x{AC00}</b>, <b>\\x{1F600}</b> → 가, 😀 &nbsp;(중괄호형: 1~6자리, BMP 밖도 가능)</li>
                <li><b>\\x{1112 1161 11AB}</b> → 한 &nbsp;(공백·쉼표로 여러 코드포인트 나열, 첫가끝 조합에 유용)</li>
                <li><b>\\x{U+AC00}</b>, <b>\\x{0xAC00}</b> → 가 &nbsp;(U+ / 0x 접두사 허용)</li>
                <li><b>\\uAC00</b>, <b>\\U0001F600</b> → 가, 😀 &nbsp;(각각 4자리·8자리 고정)</li>
                <li><b>\\char"AC00</b>, <b>\\char'101</b>, <b>\\char97</b> → 가, A, a &nbsp;(TeX식 16/8/10진수)</li>
                <li>잘못된 코드포인트(범위 밖·서로게이트·비16진수)는 <b>원문 그대로</b> 남습니다.</li>
                <li>확장을 피하려면 백슬래시를 겹쳐 쓰십시오: <b>\\\\'e</b> 는 변환되지 않습니다.</li>
            </ul>
            <p><i>※ NFD 출력 시에도 라틴 확장문자는 결합형(NFC)으로 유지되며, 한글만 분해됩니다.</i></p>
            <hr>
            <h3>⌨️ 시스템 통합 핵심 핫키 (키보드 동작 규칙)</h3>
            <ul>
                <li><b style="color:#d9534f;">Enter</b> : <b>클립보드로 전송</b> (출력 텍스트 복사 후 입력/출력창 모두 자동 청소)</li>
                <li><b style="color:#f0ad4e;">Shift + Enter</b> : <b>행 나누기 (줄바꿈)</b> (멀티레이어 태그 라인 작성용 개행)</li>
                <li><b style="color:#337ab7;">Alt + Z</b> : <b>전송 취소 (Undo)</b> (방금 전송되어 지워진 로마자 원문 복구)</li>
                <li><b>Escape (ESC)</b> : <b>작업 내역 전체 지우기</b> (입력필드 및 출력필드 즉시 초기화)</li>
                <li><b>F1</b> : <b>본 도움말 가이드 팝업</b></li>
                <li><b>F10</b>: <b>일본어 한자 입력 보조창 토글</b></li>
            </ul>
            <br>
            <p style="color:#666; font-size:11px;">※ 상세한 자모 로마자 매핑 테이블 규칙은 외부 동반 명세 문서를 참조하십시오.</p>
            """
            
            browser.setHtml(help_html)
            layout.addWidget(browser)
            help_dialog.exec()

def process_tags_mixed(text):
    def repl_kr_pm(m): return convert_text(m.group(1), engine_mode="pm")
    def repl_kr_frk(m): return convert_text(m.group(1), engine_mode="frkim")
    def repl_jp_mixed(m): return romaji_to_kana_convert(m.group(1))

    text = re.sub(r"<kr>(.*?)</kr>", repl_kr_pm, text, flags=re.DOTALL)
    text = re.sub(r"<kr:frk>(.*?)</kr:frk>", repl_kr_frk, text, flags=re.DOTALL)
    text = re.sub(r"<jp>(.*?)</jp>", repl_jp_mixed, text, flags=re.DOTALL)
    return text


def process_latex_text(text, target_name="jamoword", mode="macro", keep_structure=False, engine_mode="pm"):
    clean_name = target_name.lstrip('\\').replace('begin{', '').replace('}', '')
    result = []
    i = 0
    if mode == "env":
        start_tag = f"\\begin{{{clean_name}}}"
        end_tag = f"\\end{{{clean_name}}}"
        while i < len(text):
            idx = text.find(start_tag, i)
            if idx == -1: result.append(text[i:]); break
            result.append(text[i:idx])
            start_content = idx + len(start_tag)
            end_idx = text.find(end_tag, start_content)
            if end_idx != -1:
                inner_text = text[start_content:end_idx]
                converted = convert_text(inner_text, engine_mode=engine_mode)
                result.append(f"{start_tag}{converted}{end_tag}" if keep_structure else converted)
                i = end_idx + len(end_tag)
            else: result.append(text[idx:start_content]); i = start_content
    else:
        target = f"\\{clean_name}{{"
        while i < len(text):
            idx = text.find(target, i)
            if idx == -1: result.append(text[i:]); break
            result.append(text[i:idx])
            start_content = idx + len(target)
            brace_count = 1
            j = start_content
            while j < len(text) and brace_count > 0:
                if text[j] == '{': brace_count += 1
                elif text[j] == '}': brace_count -= 1
                j += 1
            if brace_count == 0:
                roman_text = text[start_content:j-1]
                converted = convert_text(roman_text, engine_mode=engine_mode)
                result.append(f"\\{clean_name}{{{converted}}}" if keep_structure else converted)
                i = j
            else: result.append(text[idx:start_content]); i = start_content
    return "".join(result)

# ==============================================================================
# CLI 및 전체 런타임 제어 엔트리 포인트
# ==============================================================================
def main():
    import sys
    import os
    import argparse
    import stat

    parser = argparse.ArgumentParser(description="pmIME Case-Sensitive Converter")
    parser.add_argument('-v', '--version', action='version', version=f'%(prog)s {__version__}')
    parser.add_argument('-i', '--input', type=str, help='입력 파일 경로')
    parser.add_argument('-o', '--output', type=str, help='출력 파일 경로')
    parser.add_argument('--macro', type=str, default='jamoword', help='LaTeX 매크로 변환 타겟')
    # parser.add_argument('--macro', type=str, default=None, help='LaTeX 매크로 변환 타겟 (기본적으로 전체 변환, 지정 시 해당 매크로만 변환)')
    parser.add_argument('--env', type=str, help='LaTeX 환경 변환 타겟')
    parser.add_argument('--keep', action='store_true', help='LaTeX 구조 기호 보존')
    
    parser.add_argument('--mode', choices=['pm', 'frk', 'mix', 'rrk', 'jp', 'clean'], default='pm', help='변환 엔진 모드 선택 (기본값: pm)')
    parser.add_argument('--hanja', choices=['none', 'shin', 'kyu', 'sim', 'han'], default='none', help='한자 변환 필터 (기본값: none)')

    parser.add_argument('--no-latex', action='store_true', help='LaTeX 확장 라틴문자/코드포인트 입력 확장을 끔')
    parser.add_argument('--latex-all', action='store_true', help='--macro/--env 문서 모드에서도 문서 전체에 LaTeX 확장 입력 적용')

    parser.add_argument('-n', '--nfc', action='store_true', help='출력 한글을 NFC로 결합 정규화')
    parser.add_argument('-c', '--clip', action='store_true', help='클립보드 전송')
    
    parser.add_argument('-r', '--raw', action='store_true', help='입력 텍스트 전체 변환 (파일 또는 파이프)')
    
    parser.add_argument('text', nargs='?', help='변환할 로마자 문자열')
    
    args = parser.parse_args()

    mode_map = {
        'pm': 'pm', 'frk': 'frkim', 'mix': 'pmfrk', 'rrk': 'rrk',
        'jp': 'kana', 'clean': 'transparent'
    }
    hanja_map = {
        'none': 'none', 'shin': 'shinjitai', 'kyu': 'kyujitai', 
        'sim': 'simplified', 'han': 'hanja'
    }
    
    actual_mode = mode_map[args.mode]
    actual_hanja = hanja_map[args.hanja]

    # LaTeX 확장 입력 전역 스위치
    set_latex_expand(not args.no_latex)
    # --------------------------------------------------------------
    
    has_piped_input = False
    if sys.stdin is not None:
        try: 
            has_piped_input = stat.S_ISFIFO(os.fstat(sys.stdin.fileno()).st_mode) or stat.S_ISREG(os.fstat(sys.stdin.fileno()).st_mode)
        except Exception: 
            pass

    if args.text or args.input or has_piped_input:
        input_text = ""
        if args.text: 
            input_text = args.text
        elif args.input:
            with open(args.input, 'r', encoding='utf-8') as f: 
                input_text = f.read()
        elif has_piped_input:
            input_text = sys.stdin.buffer.read().decode('utf-8', errors='replace') if hasattr(sys.stdin, 'buffer') else sys.stdin.read()
                
        if not input_text.strip(): 
            sys.exit(0)

        if args.raw:
            output_text = convert_text(input_text, engine_mode=actual_mode)
        elif (args.input or has_piped_input) and ("<jp>" in input_text or "<kr>" in input_text):
            output_text = process_tags_mixed(input_text)
        elif args.env or (args.macro and (args.input or has_piped_input)):
            # 환경(env)과 매크로(macro) 둘 다 순차적으로 변환
            output_text = input_text
            
            if args.env:
                output_text = process_latex_text(output_text, target_name=args.env, mode="env", keep_structure=args.keep, engine_mode=actual_mode)
            
            if args.macro and (args.input or has_piped_input):
                output_text = process_latex_text(output_text, target_name=args.macro, mode="macro", keep_structure=args.keep, engine_mode=actual_mode)
        else:
            output_text = convert_text(input_text, engine_mode=actual_mode)
        
        # 문서 모드(--macro/--env)는 기본적으로 변환 대상 구간에서만 확장된다.
        # --latex-all 지정 시 문서 전체에 적용.
        if args.latex_all:
            output_text = expand_latex_input(output_text)

        output_text = filter_kanji(output_text, hanja_mode=actual_hanja)

        if actual_mode not in ["kana", "transparent"]:
            output_text = normalize_output(output_text, norm_mode="NFC" if args.nfc else "NFD")
        
        if args.clip: 
            copy_to_clipboard(output_text)
            
        if args.output:
            with open(args.output, 'w', encoding='utf-8') as f: 
                f.write(output_text)
        else:
            if hasattr(sys.stdout, 'buffer'):
                sys.stdout.buffer.write((output_text + '\n').encode('utf-8'))
            else:
                sys.stdout.write(output_text + '\n')
        sys.exit(0)
    else:
        if not GUI_AVAILABLE:
            print("Error: GUI에 필요한 패키지가 없습니다.", file=sys.stderr)
            sys.exit(1)
        app = QApplication(sys.argv)
        win = MainWindow()
        win.show()
        sys.exit(app.exec())


if __name__ == '__main__':
    main()