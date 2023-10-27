# 📈 Raman Spectra 도식화
인턴십 당시 제작한 Raman Spectra 분석에 용이한 프로그램

<br />

## 프로그램 개요
Raman Spectra를 시각화하여 간편하게 분석하고, Raman Peak Table 검색이 가능한 프로그램

<br />

## 개발 기간
> 2023.07.19 - 2023.07.25

<br />

## 개발 환경
- 언어 : Python
- UI 제작 : Qt Designer
- 라이브러리
    - PyQt5
    - pyqtgraph
    - Scipy
    - Numpy
    - Pandas
    - BaselineRemoval
<br />

## 팀 구성 및 구현 기능
- 권나경
    - UI 제작
    - UI 반응형으로 수정
    - CSV 파일 불러와 그래프 출력
    - 그래프 베이스라인 보정
    - 2개의 CSV 파일 불러와 하나의 그래프 위젯 내 출력
    - 그래프 x값별 y값 차이 데이터프레임 출력
    - 그래프 색상 변경 및 범례 추가
    - 그래프 peak 점 표시
    - 비밀번호 기능 (한 번 입력 시 계속 검색 가능)
- 윤승현
    - UI 제작
    - x값별 peak table 구간 검색
    - 데이터 프레임 검색
    - 그래프 마우스 오버
    - 파일 중복 오류 처리
    - 비밀번호 기능 (창 생성 / 검색할 때마다 입력)

<br />
