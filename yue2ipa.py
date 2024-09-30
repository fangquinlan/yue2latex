import json

def load_ipa_data(file_path):
    ipa_dict = {}
    with open(file_path, 'r', encoding='utf-8') as f:
        for line_number, line in enumerate(f, 1):
            line = line.strip()
            if not line or line.startswith('{') or line.endswith('}'):
                continue  # 跳过空行和 JSON 的开始/结束括号
            try:
                key, value = line.split(':', 1)
                key = key.strip().strip('"')
                value = value.strip().strip('"').rstrip(',')  # 移除尾部的逗号
                # 如果有多个发音,只取第一个，并去除所有引号
                ipa_dict[key] = value.split(',')[0].strip().replace('"', '')
            except ValueError:
                print(f"警告: 第 {line_number} 行格式不正确: {line}")
    
    if not ipa_dict:
        raise ValueError("无法从文件中解析出任何有效的IPA数据")
    
    return ipa_dict

def cantonese_to_ipa(text, ipa_dict):
    result = []
    for char in text:
        if char in ipa_dict:
            result.append(ipa_dict[char])
        else:
            result.append(char)  # 如果字符不在字典中,保持原样
    return ' '.join(result)

# 加载IPA数据
try:
    ipa_dict = load_ipa_data('ipa_data.txt')
    print(f"成功加载了 {len(ipa_dict)} 个IPA转换规则")
except Exception as e:
    print(f"加载IPA数据时出错: {e}")
    exit(1)

# 获取用户输入
input_text = input("请输入粤语文本: ")

# 转换并输出结果
output_ipa = cantonese_to_ipa(input_text, ipa_dict)
print("对应的IPA: ", output_ipa)