## imageSigner
#### signImage("이미지 경로/이름", "주입할 문자열") => 문자열이 주입된 Image return

이미지파일의 RGB값(0~255) 중 중간값(127)에서 가장 먼 색상의 값의 홀,짝을 주입할 문자열의 binary값(0,1)에 맞춤

=> 육안으로 인식이 어려운 수준의 노이즈로 문자열을 이미지에 주입함

```python
from imageSigner import signImage
string = "주입할 문자열"
image = "주입대상 이미지 경로"

signedImage = signImage(image, string)
```

## imageValidator
#### validateImage("이미지 경로/이름") => 이미지에 주입된 문자열을 return
이미지파일의 RGB값(0~255) 중 중간값(127)에서 가장 먼 색상의 값의 홀,짝을 문자열의 binary로 인식

=> imageSigner로 주입한 문자열을 추출가능

```python
from imageValidator import validateImage
image = "추출대상 이미지 경로"

validation = validateImage(image)
```

## example
### 원본 (문자열 주입 전)
<img src="https://github.com/kyj9447/imageNoiserAndValidator/blob/main/original.png" width=600px>

### 주입 후 (문자열 `!Validation:kyj9447@mailmail.com` 주입됨)
<img src="https://github.com/kyj9447/imageNoiserAndValidator/blob/main/signed_original.png" width=600px>

### Validation 결과
START-VALIDATION

문자열

문자열 (일부 잘림)

END-VALIDATION

<img src="https://github.com/kyj9447/imageSignerAndValidator/assets/122734245/48da75e9-df58-4326-9b42-965cc3e7d6a2" width=600px>

---

## main.py 

기능 테스트 시연용 스크립트.

### 1. signImage

프로젝트 루트의 original.png 파일을 읽고 입력한 문자열을 주입한 후 signed_original.png로 저장한다.

<sup>(주입할 문자열을 입력하지 않을경우 기본값으로 설정합니다. (`!Validation:kyj9447@mailmail.com`) )</sup>

### 2. validateImage

프로젝트 루트의 signed_original.png 파일을 읽고 추출한 문자열을 validation_result.txt로 저장한다.

## etc.

이미지에 암호화 문자열 주입하는 카메라 어플 / 문자열 추출 후 복호화하는 서버 프로젝트

https://github.com/kyj9447/imageSignerCamera
