import sys
from pathlib import Path

# pip 패키지 디렉터리를 sys.path에 추가하여 로컬 테스트에서 import 가능하도록 설정
ROOT_DIR = Path(__file__).resolve().parent
PACKAGE_DIR = ROOT_DIR / "pip_package"
if str(PACKAGE_DIR) not in sys.path:
    sys.path.insert(0, str(PACKAGE_DIR))


# main
from pprint import pprint
from Pixseal import signImage, validateImage

choice = input("작업을 선택하세요\n1. Sign Image\n2. Validate Image\n")

if choice == "1":

    image = "original.png"
    string = input("주입할 문자열을 입력하세요: ")

    if string == "":
        print("입력이 없습니다. 기본값으로 설정합니다. (!Validation:kyj9447@mailmail.com)")
        string = "!Validation:kyj9447@mailmail.com"

    choice2 = input("1.암호 포함\n2.평문")
    if choice2 == "1":
        signedImage = signImage(image, string,publicKeyPath="SSL/public_key.pem") # string 끝에 줄바꿈 추가
    elif choice2 == "2":
        signedImage = signImage(image, string)

    signedImage.save("signed_"+image)
    print("signed_"+image+ " 파일이 작성되었습니다.")

elif choice == "2":

    image = "signed_original.png"

    choice3 = input("1.암호 포함\n2.평문\n")
    if choice3 == "1":
        validation = validateImage(image, privKeyPath="SSL/private_key.pem")
    elif choice3 == "2":
        validation = validateImage(image)
    
    print("검증 결과:")
    pprint(validation)
    
else:
    print("잘못된 입력입니다.")
