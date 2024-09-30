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
                ipa_dict[key] = [v.strip().strip('"') for v in value.split(',')]
            except ValueError:
                continue
    return ipa_dict

def ipa_to_pinyin(ipa):
    ipa_to_pinyin_dict = {
    
        # Consonants
        'p': 'b', 'pʰ': 'p', 'm': 'm', 'f': 'f',
        't': 'd', 'tʰ': 't', 'n': 'n', 'l': 'l',
        'k': 'g', 'kʰ': 'k', 'x': 'h', 'h': 'h', 'ɣ': 'e', 'χ': 'h', 'ʁ': 'ʁ', 'ħ': 'haʰoʰ', 'ʕ': 'haʰo', 'ɦ': 'aʰ',
        'tɕ': 'j', 'tɕʰ': 'q', 'ɕ': 'x', 't͡ɕ': 'j', 't͡ɕʰ': 'q',
        'tʂ': 'zh', 'tʂʰ': 'ch', 'ʂ': 'sh', 'ɻ': 'r', 'ʐ': 'r', 't͡s': 'z', 't͡sʰ': 'c', 'ʈ͡ʂ': 'zh', 'ʈ͡ʂʰ': 'ch',
        'ts': 'z', 'tsʰ': 'c', 's': 's',
        'ŋ': 'ng',
        'ʔ': 'ʔ',
        'ɉ': 'i',
        'w': 'u', 'ɥ': 'ü',
        'j': 'i',


        # Syllabic Consonants
        'm̩': 'm', 'm̥': 'hm',
        'n̩': 'n', 'ŋ̍': 'ng', 'ŋ̊': 'hng',
        'ɹ̩': 'i', 'ɻ̩': 'ri',


        # Vowels
        'i': 'i', 'u': 'u', 'y': 'ü', 'u˞': 'ur',
        'ai': 'a', 'ä': 'a', 'ɑ': 'ao', 'e̞': 'ie', 'ə': 'en',
        'o': 'o', 'ɔ': 'ao', 'o̞': 'o', 'o̞˞': 'or',
        'ɤ': 'e', 'ɛ': 'i', 'e': 'ie', 'œ': 'ue',
        'ɵ': 'ou', 'ʊ': 'ong', 'ʊ̃˞': 'ongr', 'ɤ˞': 'e', 'ɤ̞˞': 'eng', 'ɤ˞˞': 'er',
        'ɚ': 'r', 'ɐ': 'i', 'ɚ̃': 'ngr',


        # Diphthongs and Triphthongs
        'ja': 'ia', 'wa': 'ua',
        'jo': 'io', 'wo': 'uo',
        'jɛ': 'ie', 'ɥɛ': 'üe',
        'aɪ': 'ai', 'waɪ': 'uai', 'ai̯': 'ai',
        'eɪ': 'ei', 'weɪ': 'ui', 'ei̯': 'ei',
        'ɑʊ': 'ao', 'jɑʊ': 'iao', 'ɑu̯': 'ao', 'ɑu̯˞': 'aor',
        'oʊ': 'ou', 'joʊ': 'iu', 'ou̯': 'iu', 'ou̯˞': 'our',

        # R-colored vowels and combinations
        'äɚ̯': 'r', 'ä̃ɚ̯̃': 'angr', 'ɐɚ̯': 'yanr',

        'an': 'an', 'jɛn': 'ian', 'wan': 'uan', 'ɥæn': 'üan',
        'ən': 'en', 'in': 'in', 'wən': 'un', 'yn': 'ün',
        'ɑŋ': 'ang', 'jɑŋ': 'iang', 'wɑŋ': 'uang',
        'ɤŋ': 'eng', 'iŋ': 'ing', 'wɤŋ': 'ueng',
        'ʊŋ': 'ong', 'jʊŋ': 'iong',
        'ɚ̃': 'a',

        # Tones
        '˥˥': '55', '˧˥': '35', '˨˩˦': '214', '˨˩˩': '211',
        '˩˦': '14', '˥˩': '51', '˥˧': '53',
        '˨˩': '21', '˧˩': '31', '˦˩': '41', '˩˩': '11', '˨˥': '25',
        '˧': '33', '˩˧': '13', '˨˧': '23', '˨': '22',

        # Neutral Tone
        'k˥': '5', 'k˧': '3', 'k˨': '2', '˥': '55',

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

def process_text(text, ipa_dict, output_type, select_once):
    result = []
    i = 0
    char_choices = {}
    while i < len(text):
        char = text[i]
        if char.isspace():
            result.append(char)
            i += 1
        elif char in '，。！？；：""''（）《》【】—…':
            result.append(char)
            i += 1
        else:
            ipas = ipa_dict.get(char, [char])
            if len(ipas) > 1 and (not select_once or char not in char_choices):
                # 获取上下文
                context_start = max(0, i - 10)
                context_end = min(len(text), i + 11)
                context = text[context_start:context_end]
                
                print(f"\n在以下上下文中选择 '{char}' 的发音：")
                print(context)
                for idx, ipa in enumerate(ipas, 1):
                    print(f"{idx}. {ipa}")
                choice = int(input("请选择发音编号: ")) - 1
                char_choices[char] = choice
            elif char in char_choices:
                choice = char_choices[char]
            else:
                choice = 0

            ipa = ipas[choice]
            
            if output_type == 'ipa':
                result.append(f'\\anno{{{char}}}{{{ipa}}}')
            else:
                pinyin = ipa_to_pinyin(ipa)
                result.append(f'\\anno{{{char}}}{{{pinyin}}}')
            i += 1
    return ''.join(result)

# 加载IPA数据
ipa_dict = load_ipa_data('ipa_data.txt')
print(f"成功加载了 {len(ipa_dict)} 个IPA转换规则")

# 获取用户选择
output_type = input("请选择输出类型 (ipa/pinyin): ").lower()
while output_type not in ['ipa', 'pinyin']:
    output_type = input("无效的选择，请输入 'ipa' 或 'pinyin': ").lower()

# 询问用户是否只选择一次
select_once = input("是否对每个多音字只选择一次？(y/n): ").lower() == 'y'

# 读取输入文件
with open('input.txt', 'r', encoding='utf-8') as f:
    input_text = f.read()

# 处理文本
output_text = process_text(input_text, ipa_dict, output_type, select_once)

# 替换换行符
output_text = output_text.replace('\n', ' \\\\\n')

# 写入输出文件
with open('output.txt', 'w', encoding='utf-8') as f:
    f.write(output_text)

print("处理完成，结果已写入 output.txt 文件。")