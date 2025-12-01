from simpleImage import SimpleImage

def binaryToString(binaryCode):
    string = ""
    for i in range(0, len(binaryCode), 8):
        byte = binaryCode[i:i+8]
        decimal = int(byte, 2)
        character = chr(decimal)
        string += character
    return string

def readHiddenBit(imagePath):
    # 비트 저장용 문자열
    hiddenBinary = ""

    # 이미지 열기
    img = SimpleImage.open(imagePath)

    # 이미지의 너비와 높이 가져오기
    width, height = img.size

    # 이미지의 각 픽셀에 접근하여 값 확인
    for y in range(height):
        for x in range(width):
            # 현재 픽셀의 RGB 값을 가져옴
            r, g, b = img.getPixel((x, y))

            # 127과의 차이 계산
            diffR = abs(r - 127)
            diffG = abs(g - 127)
            diffB = abs(b - 127)

            # 가장 먼 색상 찾기
            maxDiff = max(diffR, diffG, diffB)

            # 가장 먼 색상의 값이 짝수면 hiddenBinary에 1 추가, 홀수면 0 추가
            if maxDiff % 2 == 0:
                hiddenBinary += "1"
            else:
                hiddenBinary += "0"
    
    return hiddenBinary

def deduplicate(arr):
    deduplicated = []
    for i in range(len(arr)):
        if i == 0 or arr[i] != arr[i-1]:
            deduplicated.append(arr[i])
    return deduplicated

def buildValidationReport(decrypted, deduplicated):
    # 복호화된 배열 길이 (중복제거 기준)
    arrayLength = len(deduplicated)

    # 1. 중복제거, 복호화 완료된 배열의 길이를 확인하여 성공/실패 여부 판단
    lengthCheck = True if arrayLength == 3 or arrayLength == 4 else False

    # 2. 시작,끝 부분 검사
    startCheck = decrypted[0] == "START-VALIDATION" if decrypted else False
    endCheck = decrypted[-1] == "END-VALIDATION" if decrypted else False

    # 3. 시작, 끝 부분이 암호화 -> 복호화 되지 않은경우
    # 복호화 하지 않은 START-VALIDATION, END-VALIDATION이 deduplicated에 있으면 false
    if deduplicated:
        startIsCrypted = False if deduplicated[0] == "START-VALIDATION" else True
        endIsCrypted = False if deduplicated[-1] == "END-VALIDATION" else True
    else:
        startIsCrypted = False
        endIsCrypted = False

    # 4. 두번째 요소 복호화 여부 확인 (==로 끝나면 암호화된 문자열임)
    decryptedPayload = decrypted[1] if len(decrypted) > 1 else ""
    isDecrypted = bool(decryptedPayload) and not decryptedPayload.endswith("==")

    # 최종 결과
    # 모두 true일 경우 Success, 하나라도 false일 경우 Fail
    verdict = all([lengthCheck, startCheck, endCheck, isDecrypted, startIsCrypted, endIsCrypted])

    return {
        "arrayLength": arrayLength,
        "lengthCheck": lengthCheck,
        "startCheck": startCheck,
        "endCheck": endCheck,
        "startIsCrypted": startIsCrypted,
        "endIsCrypted": endIsCrypted,
        "isDecrypted": isDecrypted,
        "verdict": verdict
    }

# main
def validateImage(imagePath):
    resultBinary = readHiddenBit(imagePath)
    resultString = binaryToString(resultBinary)
    decrypted = resultString.split("\n")
    deduplicated = deduplicate(decrypted)
    report = buildValidationReport(decrypted, deduplicated)
    return {
        "decrypted": decrypted,
        "deduplicated": deduplicated,
        "decryptedText": "\n".join(decrypted),
        "deduplicatedText": "\n".join(deduplicated),
        "validationReport": report
    }
