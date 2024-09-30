import json

def load_ipa_data(file_path):
    ipa_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if not line or line.startswith('{') or line.endswith('}'):
                continue
            try:
                key, value = line.split(':', 1)
                key = key.strip().strip('"')
                value = value.strip().strip('"').rstrip(',')
                ipa_dict[key] = [v.strip() for v in value.split(',')]
            except ValueError:
                continue
    return ipa_dict

def cantonese_to_ipa(char, ipa_dict):
    return ipa_dict.get(char, [char])[0]

def ipa_to_pinyin(ipa):
    ipa_to_pinyin_dict = {
        'p': 'b', 'pʰ': 'p', 'm': 'm', 'f': 'f', 't': 'd', 'tʰ': 't', 'n': 'n', 'l': 'l',
        'k': 'g', 'kʰ': 'k', 'x': 'h', 'tɕ': 'j', 'tɕʰ': 'q', 'ɕ': 'x', 'tʂ': 'zh', 'tʂʰ': 'ch',
        'ʂ': 'sh', 'ɻ': 'r', 'ts': 'z', 'tsʰ': 'c', 's': 's', 'h': 'h',
        'i': 'i', 'u': 'u', 'y': 'ü', 'a': 'a', 'ja': 'ia', 'wa': 'ua', 'o': 'o', 'jo': 'io',
        'wo': 'uo', 'ɤ': 'e', 'ɛ': 'ê', 'jɛ': 'ie', 'ɥɛ': 'üe', 'aɪ': 'ai', 'waɪ': 'uai',
        'eɪ': 'ei', 'weɪ': 'ui', 'ɑʊ': 'ao', 'jɑʊ': 'iao', 'oʊ': 'ou', 'joʊ': 'iu', 'an': 'an',
        'jɛn': 'ian', 'wan': 'uan', 'ɥæn': 'üan', 'ən': 'en', 'in': 'in', 'wən': 'un', 'yn': 'ün',
        'ɑŋ': 'ang', 'jɑŋ': 'iang', 'wɑŋ': 'uang', 'ɤŋ': 'eng', 'iŋ': 'ing', 'wɤŋ': 'ueng',
        'ʊŋ': 'ong', 'jʊŋ': 'iong', 'œ': 'ue', 'e': 'ie', 'ɔ': 'ao', 'ɵ': 'ou',
        'ŋ': 'ng', 'ʐ': 'r', 'ʔ': 'ʔ', 'ɉ': 'sʰ', 'w': 'w', 'ɥ': 'j', 'm̩': 'm', 'm̥': 'hm',
        'n̩': 'n', 'ŋ̍': 'ng', 'ŋ̊': 'hng', 'ɹ̩': 'c', 'ɻ̩': 'ch', 'ä': 'a', 'ɚ': 'r', 'ɚ̃': 'a',
        'ɐ': 'i', 'ai̯': 'ai', 'äɚ̯': 'r', 'ä̃ɚ̯̃': 'angr', 'ɐɚ̯': 'yanr', 'ɑu̯': 'ao', 'ɑu̯˞': 'aor',
        'ei̯': 'ei', 'ou̯': 'iu', 'ou̯˞': 'our',
        '˥˥': '55', '˧˥': '35', '˨˩˦': '214', '˨˩˩': '211', '˩˦': '14', '˥˩': '51', '˥˧': '53',
        '˨˩': '21', '˧˩': '31', '˦˩': '41', '˩˩': '11', '˨˥': '25',  '˧': '33', '˩˧': '13',
        '˨˧': '23', '˨': '22', 'k˥': '5', 'k˧': '3', 'k˨': '2', '˥': '55',
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

def process_text(text, ipa_dict, output_type):
    result = []
    multi_pronunciations = {}
    for char in text:
        if char.isspace():
            result.append(char)
        elif char in '，。！？；：""''（）《》【】—…':
            result.append(char)
        else:
            ipas = ipa_dict.get(char, [char])
            if len(ipas) > 1:
                multi_pronunciations[char] = ipas[1:]
            ipa = ipas[0]
            if output_type == 'ipa':
                result.append(f'\\anno{{{char}}}{{{ipa}}}')
            else:
                pinyin = ipa_to_pinyin(ipa)
                result.append(f'\\anno{{{char}}}{{{pinyin}}}')
    return ''.join(result), multi_pronunciations

# 加载IPA数据
ipa_dict = load_ipa_data('ipa_data.txt')
print(f"成功加载了 {len(ipa_dict)} 个IPA转换规则")

# 获取用户选择
output_type = input("请选择输出类型 (ipa/pinyin): ").lower()
while output_type not in ['ipa', 'pinyin']:
    output_type = input("无效的选择，请输入 'ipa' 或 'pinyin': ").lower()

# 读取输入文件
with open('input.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()

# 处理文本
output_text, multi_pronunciations = process_text(input_text, ipa_dict, output_type)

# 替换换行符
output_text = output_text.replace('\n', ' \\\\\n')

# 写入输出文件
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(output_text)

# 写入多音字信息
with open('multi_pronunciations.txt', 'w', encoding='utf-8') as f:
    f.write("多音字信息：\n\n")
    for char, pronunciations in multi_pronunciations.items():
        f.write(f"{char}:\n")
        for p in pronunciations:
            if output_type == 'ipa':
                f.write(f"  IPA: {p}\n")
            else:
                pinyin = ipa_to_pinyin(p)
                f.write(f"  拼音: {pinyin}\n")
        f.write("\n")

print("处理完成，结果已写入 output.txt 文件，多音字信息已写入 multi_pronunciations.txt 文件。")