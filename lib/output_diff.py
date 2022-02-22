from difflib import SequenceMatcher


def output_def_for_line(from_text:str,to_text:str):
    """ mark diff from_text to to_text """
    s = SequenceMatcher(None, from_text, to_text)
    output=[]
    for tag, i1, i2, j1, j2 in s.get_opcodes():
        if tag=="delete":
            output.append(f"(削除:{from_text[i1:i2]})")
        elif tag=="replace":
            output.append(f"(置換:{from_text[i1:i2]}→{to_text[j1:j2]})")
        elif tag=="insert":
            output.append(f"(挿入:{to_text[j1:j2]})")
        elif tag=="equal":
            output.append(f"{from_text[i1:i2]}")
    return "".join(output)

def main():
    """ for test"""
    text1 = "患者の漠然とした不安を受け止め、不安を軽減するためにわかりやすい言葉で説明できる。"
    text2 = "家族の不安を軽減するためにわかりやすい言葉で説明や対話ができる。"
    print(output_def_for_line(text1,text2))

if __name__ == "__main__":
    main()
