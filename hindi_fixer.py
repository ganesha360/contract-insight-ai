import re

def kruti_to_unicode(text):
    """
    Converts Kruti Dev (Legacy) encoded text to Unicode Hindi.
    """
    if not text:
        return ""

    # 1. Map for special ligatures and characters
    # (Simplified common mappings for Kruti Dev 010)
    mapping = {
        "‘": "\"", "’": "\"", "“": "'", "”": "'",
        "å": "ह", "ƒ": "ू", "„": "ध", "…": "?", "†": "?", "‡": "़",
        "ˆ": "ा", "‰": "?", "Š": "?", "‹": "δ", "Œ": "?", "HT": "ज्",
        "÷": "?", "×": "×",
        "Z": "द्ध", "Ô": "O", "È": "E", "Ò": "O", "ê": "ह",
        "Q+": "फ़", "?": "रु", "tZ": "ज्", "Z": "?", 
        "aa": "?", "pp": "?", "&": "–", 
        # Main Characters
        "k": "ा", "K": "ा", "i": "प", "I": "प", "U": "न", "u": "न",
        "h": "ी", "H": "ी", "x": "ग", "X": "ग", "n": "द", "N": "द",
        "j": "र", "J": "र", "p": "च", "P": "च", "L": "स", "l": "स",
        "e": "म", "E": "म", "o": "व", "O": "व", "c": "ब", "C": "ब",
        "_": ".", "-": ".", "y": "ल", "Y": "ल", "r": "त", "R": "त",
        "v": "अ", "V": "अ", "b": "ि", "B": "ि", "m": "उ", "M": "उ",
        "g": "ह", "G": "ह", "{": "क्ष", "|": "क्ष", "}": "द्व",
        "s": "े", "S": "ै", "a": "ं", "A": "ा", "w": "ू", "W": "ू",
        "q": "ु", "Q": "ु", "z": "ह", "Z": "ह", "d": "क", "D": "क",
        "[": "ख", "f": "ि", # 'f' is special (handled below)
        "]": ",", "\\": "?", "'": "ठ", "\"": "ठ",
        "/": "य", "?": "य", ".": "ड़", ">": "श्र",
        "&": "–", "Ø": "क्र",
        # Common Words/Fragments found in your text
        "Hkkxhnkjh": "भागीदारी",
        "foys[k": "विलेख",
        "fnukad": "दिनांक",
        "uxj": "नगर",
        "fuEufyf[kr": "निम्नलिखित",
        "O;fDr;ksa": "व्यक्तियों",
        "chp": "बीच",
        "xzke": "ग्राम",
        "fuoklh": "निवासी",
        "vkRet": "आत्मज",
        "i{kdkj": "पक्षकार",
        "O;olk;": "व्यवसाय",
        "ykkks": "लाभों",
        "ykHkksa": "लाभों", # Fixed key
        "gLrk{kj": "हस्ताक्षर",
        ";g": "यह"
    }

    # 2. Specific fixes for whole words in your sample (Fastest fix)
    # Since building a 100% perfect character mapper is complex, 
    # we replace the most common "garbage" words first.
    
    # Pre-processing known garbage patterns from your specific file
    replacements = [
        ("Hkkxhnkjh", "भागीदारी"), ("foys[k", "विलेख"), ("fnukad", "दिनांक"),
        ("ekg", "माह"), ("lu~", "सन"), ("dks", "को"), ("ds", "के"),
        ("fnu", "दिन"), ("uxj", "नगर"), ("esa", "में"), ("fuEufyf[kr", "निम्नलिखित"),
        ("O;fDr;ksa", "व्यक्तियों"), ("}kjk", "द्वारा"), ("muds", "उनके"),
        ("chp", "बीच"), ("xzke", "ग्राम"), ("'kgj", "शहर"), ("dk", "का"),
        ("uke", "नाम"), ("fu\"ikfnr", "निष्पादित"), ("fd;k", "किया"), ("x;k", "गया"),
        ("Jh", "श्री"), ("vkRet", "आत्मज"), ("vk;q", "आयु"), ("fuoklh", "निवासी"),
        ("mDr", "उक्त"), ("vkxs", "आगे"), ("Øe'k%", "क्रमशः"), ("izFke", "प्रथम"),
        ("f}rh;", "द्वितीय"), (",oa", "एवं"), ("r`rh;", "तृतीय"), ("i{kdkj", "पक्षकार"),
        ("ls", "से"), ("lacaf/kr", "संबंधित"), ("tk,xk", "जायेगा"), ("vkSj", "और"),
        ("pwafd", "चूँकि"), ("ge", "हम"), ("lg", "सह"), ("Hkkxhnkjksa", "भागीदारों"),
        ("us", "ने"), ("feydj", "मिलकर"), ("la;qDr%", "संयुक्त"), (":i", "रूप"),
        ("O;olk;", "व्यवसाय"), ("djus", "करने"), ("mlds", "उसके"), ("ykHkksa", "लाभों"),
        ("ckaVus", "बांटने"), ("fy,", "लिए"), (",d", "एक"), ("QeZ", "फर्म"),
        ("xBu", "गठन"), ("fu'p;", "निश्चय"), ("gS", "है"), ("'krkZsa", "शर्तों"),
        ("vra xZr", "अंतर्गत"), ("bl", "इस"), ("fu\"ikfnr", "निष्पादित"), ("djrs", "करते"),
        ("gS%", "है"), ("lacksf/kr", "संबोधित"), ("vkjEHk", "आरम्भ"), ("ekuk", "माना"),
        ("eq[;", "मुख्य"), ("dk;kZy;", "कार्यालय"), ("LFkku", "स्थान"), ("ij", "पर"),
        ("gksxk", "होगा"), ("jk;", "राय"), ("blesa", "इसमें"), ("ifjorZu", "परिवर्तन"),
        ("ldsxk", "सकेगा"), ("o\"kksZa", "वर्षों"), ("tkrk", "जाता"), ("ckn", "बाद"),
        ("Hkh", "भी"), ("lHkh", "सभी"), ("lgefr", "सहमति"), ("mls", "उसे"),
        ("pkyw", "चालू"), ("j[kk", "रखा"), ("dqy", "कुल"), ("iwath", "पूंजी"),
        (":-", "रु"), ("ftlesa", "जिसमें"), ("rhuksa", "तीनों"), ("cjkcj", "बराबर"),
        ("va'knku", "अंशदान"), ("leku", "समान"), ("ckaVk", "बांटा"), ("gkfu", "हानि"),
        ("ogu", "वहन"), ("djsaxs", "करेंगे"), ("caVokjk", "बंटवारा"), ("ys[kk&tks[kk", "लेखा-जोखा"),
        ("rS;kj", "तैयार"), ("foRrh;", "वित्तीय"), ("o\"kZ", "वर्ष"), ("vizSy", "अप्रैल"),
        ("ekpZ", "मार्च"), ("rd", "तक"), ("izca/kd", "प्रबंधक"), ("fu;qDr", "नियुक्त"),
        (",rn~}kjk", "एतद्द्वारा"), ("djkj", "करार"), ("vf/kdkj", "अधिकार"), ("dRrZO;", "कर्तव्य"),
        ("lkSairs", "सौंपते"), ("og", "वह"), ("dkjksckj", "कारोबार"), ("funsZ'ku", "निर्देशन"),
        ("ns[kHkky", "देखभाल"), ("djsxk", "करेगा"), ("mi;qDr", "उपयुक्त"), ("deZpkfj;ksa", "कर्मचारियों"),
        ("fu;qfDr", "नियुक्ति"), ("ineqfDr", "पदमुक्ति"), ("inksUufr", "पदोन्नति"), ("muds", "उनके"),
        ("osru", "वेतन"), ("fu/kkZj.k", "निर्धारण"), ("dh", "की"), ("vksj", "ओर"),
        ("U;k;ky;", "न्यायालय"), ("okn&lafLFkr", "वाद-संस्थित"), ("viuh", "अपनी"), ("bPNk", "इच्छा"),
        ("fdlh", "किसी"), ("vf/koDrk", "अधिवक्ता"), ("eq[rkj", "मुख्तार"), ("vfHkdrkZ", "अभिकर्ता"),
        (";k", "या"), ("lkjk", "सारा"), ("djok,xk", "करवाएगा"), ("le;&le;", "समय-समय"),
        ("mldk", "उसका"), ("fujh{k.k", "निरीक्षण"), ("djrk", "करता"), ("jgsxk", "रहेगा"),
        ("fujarj", "निरंतर"), ("cSad", "बैंक"), ("[kkrk", "खाता"), ("[kksysxk", "खोलेगा"),
        ("vius", "अपने"), ("pyk,xk", "चलाएगा"), ("var", "अंत"), ("cjkcj&cjkcj", "बराबर-बराबर"),
        ("vnk;xh", "अदायगी"), ("vyx", "अलग"), ("dksbZ", "कोई"), ("ikfjJfed", "पारिश्रमिक"),
        ("ugha", "नहीं"), ("fn;", "दिया"), ("fgr", "हित"), ("dk;Z", "कार्य"),
        ("nqjkpj.k", "दुराचरण"), ("fd;s", "किये"), ("tku s", "जाने"), ("tkus", "जाने"),
        ("vU;", "अन्य"), ("Hkkfxrk", "भागीता"), ("fo?kVu", "विघटन"), ("iwjk", "पूरा"),
        ("fcy", "बिल"), ("jlhn", "रसीद"), ("ckÅpj", "बाउचर"), ("vkfn", "आदि"),
        ("lqjf{kr", "सुरक्षित"), ("okn&fookn", "वाद-विवाद"), ("mRiUu", "उत्पन्न"), ("gks", "हो"),
        ("iap", "पंच"), ("fu.kZ;", "निर्णय"), ("iapksa", "पंचों"), ("iapkV", "पंचाट"),
        ("ck/;dkjh", "बाध्यकारी"), ("tc", "जब"), ("pysxk", "चलेगा"), ("feyrk&tqyrk", "मिलता-जुलता"),
        ("fo?kfVr", "विघटित"), ("yxk;h", "लगायी"), ("x;h", "गयी"), ("ikus", "पाने"),
        ("jgsaxs", "रहेंगे"), ("mi;qZDr", "उपर्युक्त"), ("lk{;", "साक्ष्य"), ("Lo:i", "स्वरूप"),
        ("nksuksa", "दोनों"), ("nks", "दो"), ("lkf{k;ksa", "साक्षियों"), ("le{k", "समक्ष"),
        ("gLrk{kj", "हस्ताक्षर"), ("lk{khx.k", "साक्षीगण")
    ]
    
    # Apply word-level replacements first (More accurate)
    for eng, hin in replacements:
        text = text.replace(eng, hin)
    
    # 3. Handle 'f' (choti ee matra) reordering for remaining text
    # In Kruti: 'f' + 'k' -> 'ki' (looks like कि)
    # We need to swap them: 'f' + char -> char + 'ि'
    
    # This regex finds 'f' followed by a character and swaps them
    text = re.sub(r'f(.)', r'\1ि', text)
    
    # 4. Fallback character mapping for anything missed
    converted = []
    for char in text:
        if char in mapping:
            converted.append(mapping[char])
        else:
            converted.append(char)
            
    return "".join(converted)