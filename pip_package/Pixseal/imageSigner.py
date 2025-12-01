from simpleImage import SimpleImage

class BinaryProvider:

    # 생성자
    def __init__(self, hiddenString):
        self.hiddenBinary = self.strToBinary(hiddenString)
        self.hiddenBinaryIndex = 0
        self.hiddenBinaryIndexMax = len(self.hiddenBinary)

        # 시작 문자열
        self.startString = "START-VALIDATION\n"
        self.startBinary = self.strToBinary(self.startString)
        self.startBinaryIndex = 0
        self.startBinaryIndexMax = len(self.startBinary)

        # 종료 문자열
        self.endString = "\nEND-VALIDATION"
        self.endBinary = self.strToBinary(self.endString)
        # 종료 문자열은 마지막 비트부터 역순으로 입력
        self.endBinaryIndex = len(self.endBinary)-1
        self.endBinaryIndexMin = 0

    # String -> Binary[]
    def strToBinary(self, string):
        # 빈 리스트 생성
        binaries = []
        
        # String 내 각 char에 대한 반복
        for char in string:
            # 각 char를 8비트로 변환하여 리스트에 추가
            binaries.append(bin(ord(char))[2:].zfill(8))
            
        # 리스트를 하나의 문자열로 결합
        return ''.join(binaries)

    # 다음 비트를 가져오는 함수
    # startBinary의 비트 입력 완료 후 hiddenBinary의 비트를 가져옴
    def nextBit(self):

        # startBinary의 인덱스가 최대값에 도달하면 hiddenBinary의 비트를 가져옴
        if self.startBinaryIndex == self.startBinaryIndexMax:    
            # hiddenBinary의 인덱스가 최대값에 도달하면 0으로 초기화
            if self.hiddenBinaryIndex >= self.hiddenBinaryIndexMax:
                self.hiddenBinaryIndex = 0

            # hiddenBinary의 해당 인덱스의 비트를 가져옴
            bit = self.hiddenBinary[self.hiddenBinaryIndex]

            # hiddenBinary의 인덱스 증가
            self.hiddenBinaryIndex += 1

        # startBinary의 인덱스가 최대값에 도달하지 않으면 startBinary의 비트를 가져옴
        else:
            # startBinary의 해당 인덱스의 비트를 가져옴
            bit = self.startBinary[self.startBinaryIndex]

            # startBinary의 인덱스 증가
            self.startBinaryIndex += 1

        return int(bit)
    
    # 다음 비트를 가져오는 함수 2
    # endBinary의 비트를 역순으로 가져옴
    def nextEnd(self):
        # endBinary의 인덱스가 최소값에 도달하면 None을 반환하여 종료 알림
        if self.endBinaryIndex == self.endBinaryIndexMin:
            return None

        # endBinary의 해당 인덱스의 비트를 가져옴
        bit = self.endBinary[self.endBinaryIndex]

        # endBinary의 인덱스 감소
        self.endBinaryIndex -= 1

        return int(bit)

def addHiddenBit(imagePath, hiddenBinary):
    # 이미지 열기
    img = SimpleImage.open(imagePath)

    # 이미지의 너비와 높이 가져오기
    width, height = img.size

    # 이미지의 각 픽셀에 접근하여 1비트 추가
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

            # 가장 먼 색상의 실제 값 읽기
            if maxDiff == diffR: 
                targetColorValue = r
            elif maxDiff == diffG:
                targetColorValue = g
            else:
                targetColorValue = b 
            
            # 가장 먼 색상이 127이상이면 감소방향, 127 미만이면 증가방향
            addDirection = 1 if targetColorValue < 127 else -1

            # 해당 index의 hiddenBinary값
            bit = hiddenBinary.nextBit()
            #print(bit)

            # 해당 픽셀의 RGB 값을 수정
            # nextBit()으로 가져온 비트가 0이면 해당 색상을 짝수로, 1이면 홀수로 만들어줌
            if maxDiff == diffR:
                # 실제 색상 값의 짝수, 홀수여부가 nextBit()의 값과 다르면
                if r % 2 != bit:
                    # 색상값을 증가 또는 감소시켜 nextBit()와 일치시킴
                    r += addDirection
            if maxDiff == diffG:
                if g % 2 != bit:
                    g += addDirection
            if maxDiff == diffB:
                if b % 2 != bit:
                    b += addDirection

            # 이미지의 해당 픽셀에 수정된 RGB 값을 설정
            img.putPixel((x,y), (r, g, b))

    # 이미지 마지막에 endBinary 추가
    for y in reversed(range(height)):
        for x in reversed(range(width)):
            # 현재 픽셀의 RGB 값을 가져옴
            r, g, b = img.getPixel((x, y))

            # 127과의 차이 계산
            diffR = abs(r - 127)
            diffG = abs(g - 127)
            diffB = abs(b - 127)

            # 가장 먼 색상 찾기
            maxDiff = max(diffR, diffG, diffB)

            # 가장 먼 색상의 실제 값 읽기
            if maxDiff == diffR: 
                targetColorValue = r
            elif maxDiff == diffG:
                targetColorValue = g
            else:
                targetColorValue = b 
            
            # 가장 먼 색상이 127이상이면 감소방향, 127 미만이면 증가방향
            addDirection = 1 if targetColorValue < 127 else -1

            # 해당 index의 hiddenBinary값
            bit = hiddenBinary.nextEnd()
            if bit is None:
                break
            #print(bit)

            # 해당 픽셀의 RGB 값을 수정
            # nextBit()으로 가져온 비트가 0이면 해당 색상을 짝수로, 1이면 홀수로 만들어줌
            if maxDiff == diffR:
                # 실제 색상 값의 짝수, 홀수여부가 nextBit()의 값과 다르면
                if r % 2 != bit:
                    # 색상값을 증가 또는 감소시켜 nextBit()와 일치시킴
                    r += addDirection
            if maxDiff == diffG:
                if g % 2 != bit:
                    g += addDirection
            if maxDiff == diffB:
                if b % 2 != bit:
                    b += addDirection

            # 이미지의 해당 픽셀에 수정된 RGB 값을 설정
            img.putPixel((x,y), (r, g, b))

        if bit is None:
            break

    # 수정된 이미지를 return
    return img

# main
# 이미지 경로 + 주입할 String => String 주입된 Image
def signImage(imagePath, hiddenString) :
    hiddenBinary = BinaryProvider(hiddenString+"\n")
    signedImage = addHiddenBit(imagePath, hiddenBinary)
    return signedImage
