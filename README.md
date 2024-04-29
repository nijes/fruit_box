# Fruit Box
## 이미지 라벨링 게임
> 여러 과일이 포함된 이미지에 바운딩 박스를 빠르게 라벨링하는 간단한 게임.
> 사용자는 순차적으로 나타나는 과일 이미지에 대해 각각 라벨에 맞는 바운딩 박스를 그려야 합니다. Python Streamlit과 Fabric.js 기반 라이브러리를 이용하여 구현하였습니다.
* http://223.130.131.30:8501/
* 2024.04.27 ~ 

<br>

## 주요 기능
* 이미지 시퀀스: 사용자는 연속적으로 제공되는 다양한 과일 이미지에 라벨을 적용합니다.
* 바운딩 박스: 사용자는 Fabric.js 기반의 도구를 사용하여 이미지 위에 바운딩 박스를 그립니다.
* 점수 시스템: 정확하게 라벨링된 박스에는 점수가 부여되며, 속도와 정확성이 점수에 영향을 미칩니다.
* 사용자 인터페이스: 간단하고 직관적인 UI를 통해 사용자가 쉽게 게임을 진행할 수 있습니다.
* *모든 이미지는 DALLE-3를 이용하여 생성하였습니다.*

<br>

## 실행 방법
이 게임을 로컬에서 실행하기 위해 필요한 단계는 다음과 같습니다:
```bash
# 레포지토리 클론
git clone https://github.com/nijes/fruit_box.git

# 가상환경 생성 후 필요한 라이브러리 설치
python3 -m venv . --copies
pip install -r requirements.txt

# sqlite db 생성
cd app
python3 utils/db.py

# streamlit 실행
bash start.sh
```