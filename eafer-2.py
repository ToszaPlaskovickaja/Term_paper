import os
import xml.etree.ElementTree as ET

command = 'H1 FingerSelection:3-rd + H1 Bent:straight + H1 Facing: + H1 Focus:ulnar'
command = 'H1 FingerSelection:3-rd + H1 FingerSelection:1-rd'
command = 'Dynamic Orientation:* + H1 Aperture:open-closed'
command = 'Dynamic Orientation:* + Manner:repeated'
command = 'Dynamic Orientation:* + Settings:'
command = 'H1 Aperture:open + H1 Bent:bent + H1 Curve:straight'
command = 'H1 Aperture:open + H1 Bent:straight + H1 Curve:curved'
command = 'H1 Aperture:open + H1 Bent:straight + H1 Curve:straight'
command = 'H1 Aperture:open + H1 Bent:bent + H1 Curve:curved'
command = 'H1 Aperture: + H1 Bent:bent + H1 Curve:straight'
command = 'H1 Aperture: + H1 Bent:bent + H1 Curve:curved'
command = 'H1 Aperture: + H1 Bent:straight + H1 Curve:curved'
command = 'H1 FingerSelection:-thumb + H1 Aperture: + H1 Bent:straight + H1 Curve:curved'
command = 'Location:hand-narrow + Manner:symmetrical'
command = 'Manner:crossed'
command = 'H1 Width:pointed-wide'
command = 'Manner:symmetrical + Location: space'
command = 'Manner:alternating'
command = 'Plane:* + Manner:-symmetrical'
command = 'H1 Curve:straight-curved + H1 Aperture:'
command = 'H1 Width:pointed-wide + H1 Aperture:'
command = 'Manner:alternating'

path_to_eaf = 'data'
files = os.listdir(path_to_eaf)

# Информация о команде (ключ - значение)
info = {}
parts = command.split('+')
for element in parts:
    key, value = element.split(':')
    info[key.strip(' ')] = value.strip(' ')

# Список подходящих файлов
list_valid_files = []
for file in files:
    f = open(path_to_eaf + '/' + file, "r", encoding='utf8')
    text = f.read()

    root = ET.fromstring(text)

    for key, value in info.items():
        is_valid = False
        elements = root.findall('.//TIER[@TIER_ID="' + key + '"]')

        # Если звездочка, тогда любое с аннотацией
        if value == '*':
            is_valid = root.findall('.//TIER[@TIER_ID="' + key + '"]//ANNOTATION').__len__() > 0
        # Если пустота, тогда только пустые
        elif value == '':
            elements_count = root.findall('.//TIER[@TIER_ID="' + key + '"]').__len__()
            elements_with_annotation = root.findall('.//TIER[@TIER_ID="' + key + '"]//ANNOTATION').__len__()
            is_valid = elements_count - elements_with_annotation > 0
        # Если у правила есть значение, то проверить и его
        else:
            for element in elements:
                values = element.findall('.//ANNOTATION_VALUE')
                for val in values:
                    if val.text == value:
                        is_valid = True
                # Если -значение, то без него
                    if value[0] == '-':
                        if val.text == value[1:]:
                            is_valid = False
                            break
                        else:
                            is_valid = True

        if not is_valid:
            break
    if is_valid:
        list_valid_files.append(file)

print("Count:", list_valid_files.__len__())
print("\n".join(list_valid_files))
