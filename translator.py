from deep_translator import GoogleTranslator
import os

async def translate_subtitle(file_path, target_lang):
    with open(file_path, "r", encoding="utf-8") as f:
        lines = f.readlines()

    translated_lines = []
    for line in lines:
        if "-->" in line or line.strip().isdigit() or line.strip() == "":
            translated_lines.append(line)
        else:
            try:
                translated = GoogleTranslator(target=target_lang).translate(line.strip())
                translated_lines.append(translated + "\n")
            except:
                translated_lines.append(line)

    new_file = file_path.replace(".", f"_{target_lang}.")
    with open(new_file, "w", encoding="utf-8") as f:
        f.writelines(translated_lines)
    return new_file
