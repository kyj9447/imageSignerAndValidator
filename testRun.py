import sys
from pathlib import Path

# pip 패키지 디렉터리를 sys.path에 추가하여 로컬 테스트에서 import 가능하도록 설정
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / "pip_package"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))

from Pixseal import signImage, validateImage

# main

choice = input("작업을 선택하세요\n1. Sign Image\n2. Validate Image\n")

if choice == "1":

    image = "original.png"
    string = input("주입할 문자열을 입력하세요: ")

    if string == "":
        print("입력이 없습니다. 기본값으로 설정합니다. (!Validation:kyj9447@mailmail.com)")
        string = "!Validation:kyj9447@mailmail.com"

    signedImage = signImage(image, string) # string 끝에 줄바꿈 추가
    signedImage.save("signed_"+image)
    print("signed_"+image+ " 파일이 작성되었습니다.")

elif choice == "2":

    image = "signed_original.png"

    # validate 결과 (String)
    validation = validateImage(image)
    report = validation["validationReport"]

    # # 줄바꿈 기준으로 split한 배열
    # validationarr = validation.split("\n")

    # # 중복 제거
    # deduplicated = []
    # for i in range(len(validationarr)):
    #     if i == 0 or validationarr[i] != validationarr[i-1]:
    #         deduplicated.append(validationarr[i])

    # # 중복 제거된 결과
    # validation = "\n".join(deduplicated)

    # 파일로 저장
    with open("validation_result.txt", "w") as file:
        file.write(validation["deduplicatedText"])
    print("validation_result.txt 파일이 작성되었습니다.")
    print("검증 결과:", report["verdict"])
    # print(validation)
    
else:
    print("잘못된 입력입니다.")
