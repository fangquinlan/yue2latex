import json

def load_japanese_data(file_path):
    with open(file_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def japanese_to_ipa(text, ja_dict):
    result = []
    i = 0
    while i < len(text):
        found = False
        for j in range(len(text), i, -1):
            substr = text[i:j]
            if substr in ja_dict:
                pronunciations = ja_dict[substr].strip('/').split('/, /')
                result.append(pronunciations[0])  # 使用第一个IPA发音
                i = j
                found = True
                break
        if not found:
            result.append(text[i])
            i += 1
    return ' '.join(result)

def ipa_to_pinyin(ipa):
    ipa_to_pinyin_dict = {
        # 辅音
        'p': 'b', 'pʰ': 'p', 'm': 'm', 'f': 'f', 't': 'd', 'tʰ': 't', 'n': 'n', 'l': 'l',
        'k': 'g', 'kʰ': 'k', 'x': 'h', 'tɕ': 'j', 'tɕʰ': 'q', 'ɕ': 'x', 'tʂ': 'zh', 'tʂʰ': 'ch',
        'ʂ': 'sh', 'ɻ': 'r', 'ts': 'z', 'tsʰ': 'c', 's': 's', 'h': 'h',
        # 元音
        'i': 'i', 'u': 'u', 'y': 'ü', 'a': 'a', 'ja': 'ia', 'wa': 'ua', 'o': 'o', 'jo': 'io',
        'wo': 'uo', 'ɤ': 'e', 'ɛ': 'ê', 'jɛ': 'ie', 'ɥɛ': 'üe', 'aɪ': 'ai', 'waɪ': 'uai',
        'eɪ': 'ei', 'weɪ': 'ui', 'ɑʊ': 'ao', 'jɑʊ': 'iao', 'oʊ': 'ou', 'joʊ': 'iu', 'an': 'an',
        'jɛn': 'ian', 'wan': 'uan', 'ɥæn': 'üan', 'ən': 'en', 'in': 'in', 'wən': 'un', 'yn': 'ün',
        'ɑŋ': 'ang', 'jɑŋ': 'iang', 'wɑŋ': 'uang', 'ɤŋ': 'eng', 'iŋ': 'ing', 'wɤŋ': 'ueng',
        'ʊŋ': 'ong', 'jʊŋ': 'iong',
        'œ': 'ue',
        'e': 'ie', 'ɔ': 'ao',
        'ɵ': 'ou',
        'ɯ': 'u',
        # 保留原有的一些映射
        'ŋ': 'ng', 'ʐ': 'r', 'ʔ': 'ʔ', 'ɉ': 'sʰ', 'w': 'w', 'ɥ': 'j', 'm̩': 'm', 'm̥': 'hm',
        'n̩': 'n', 'ŋ̍': 'ng', 'ŋ̊': 'hng', 'ɹ̩': 'c', 'ɻ̩': 'ch', 'ä': 'a', 'ɚ': 'r', 'ɚ̃': 'a',
        'ɐ': 'i', 'ai̯': 'ai', 'äɚ̯': 'r', 'ä̃ɚ̯̃': 'angr', 'ɐɚ̯': 'yanr', 'ɑu̯': 'ao', 'ɑu̯˞': 'aor',
        'ei̯': 'ei', 'ou̯': 'iu', 'ou̯˞': 'our',
        
        ':': ':', '/': '/', '[': '[', ']': ']', '(': '(', ')': ')', '（': '（', '）': '）', ' ': ' ', ',': ',', '.': '.',
        
        '˥˥': '55', '˧˥': '35', '˨˩˦': '214', '˨˩˩': '211', '˩˦': '14', '˥˩': '51', '˥˧': '53', '˨˩': '21', '˧˩': '31', '˦˩': '41', '˩˩': '11',
        '˨˥': '25',  '˧': '33', '˩˧': '13', '˨˧': '23', '˨': '22', 'k˥': '5', 'k˧': '3', 'k˨': '2',
        '˥': '55',
    }
    
    result = []
    i = 0
    while i < len(ipa):
        found = False
        for j in range(len(ipa), i, -1):
            substr = ipa[i:j]
            if substr in ipa_to_pinyin_dict:
                result.append(ipa_to_pinyin_dict[substr])
                i = j
                found = True
                break
        if not found:
            result.append(ipa[i])
            i += 1
    
    return ''.join(result)

# 加载日语数据
try:
    ja_dict = load_japanese_data('ja.json')
    print(f"成功加载了 {len(ja_dict)} 个日语转换规则")
except Exception as e:
    print(f"加载日语数据时出错: {e}")
    exit(1)

# 获取用户输入
input_text = input("请输入日语文本: ")

# 转换为IPA
ipa_output = japanese_to_ipa(input_text, ja_dict)
print("对应的IPA: ", ipa_output)

# 转换为拼音
pinyin_output = ipa_to_pinyin(ipa_output)
print("对应的拼音: ", pinyin_output)