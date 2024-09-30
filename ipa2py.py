import gradio as gr

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
    
    result = ''
    i = 0
    while i < len(ipa):
        if i < len(ipa) - 3 and ipa[i:i+4] in ipa_to_pinyin_dict:
            result += ipa_to_pinyin_dict[ipa[i:i+4]]
            i += 4
        elif i < len(ipa) - 2 and ipa[i:i+3] in ipa_to_pinyin_dict:
            result += ipa_to_pinyin_dict[ipa[i:i+3]]
            i += 3
        elif i < len(ipa) - 1 and ipa[i:i+2] in ipa_to_pinyin_dict:
            result += ipa_to_pinyin_dict[ipa[i:i+2]]
            i += 2
        elif ipa[i] in ipa_to_pinyin_dict:
            result += ipa_to_pinyin_dict[ipa[i]]
            i += 1
        else:
            result += '�'
            i += 1
    return result

def pinyin_to_ipa(pinyin):
    pinyin_to_ipa_dict = {v: k for k, v in ipa_to_pinyin_dict.items()}
    
    result = ''
    i = 0
    while i < len(pinyin):
        if i < len(pinyin) - 3 and pinyin[i:i+4] in pinyin_to_ipa_dict:
            result += pinyin_to_ipa_dict[pinyin[i:i+4]]
            i += 4
        elif i < len(pinyin) - 2 and pinyin[i:i+3] in pinyin_to_ipa_dict:
            result += pinyin_to_ipa_dict[pinyin[i:i+3]]
            i += 3
        elif i < len(pinyin) - 1 and pinyin[i:i+2] in pinyin_to_ipa_dict:
            result += pinyin_to_ipa_dict[pinyin[i:i+2]]
            i += 2
        elif pinyin[i] in pinyin_to_ipa_dict:
            result += pinyin_to_ipa_dict[pinyin[i]]
            i += 1
        else:
            result += '�'
            i += 1
    return result

def convert(ipa_input, pinyin_input):
    if ipa_input:
        return ipa_to_pinyin(ipa_input), ""
    elif pinyin_input:
        return "", pinyin_to_ipa(pinyin_input)
    else:
        return "", ""

iface = gr.Interface(
    fn=convert,
    inputs=[
        gr.Textbox(label="IPA"),
        gr.Textbox(label="拼音")
    ],
    outputs=[
        gr.Textbox(label="拼音"),
        gr.Textbox(label="IPA")
    ],
    title="IPA 和拼音转换器",
    description="在左边输入IPA获得拼音，或在右边输入拼音获得IPA。",
    allow_flagging="never"
)

if __name__ == "__main__":
    iface.launch()