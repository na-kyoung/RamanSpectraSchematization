# 📈 Raman Spectra Schematization : 라만 스펙트럼 도식화
인턴십 당시 제작한 Raman Spectra 분석에 용이한 프로그램

<br />

## 프로그램 개요
Raman Spectra를 시각화하여 간편하게 분석하고, 논문을 토대로 제작된 Raman Peak Table 검색이 가능한 프로그램

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
    - PyInstaller
<br />

## 팀 구성 및 구현 기능
### **권나경**
- UI 제작
- UI 반응형 수정 <br />
- Tab 1
    - 파일을 불러오면 베이스라인 보정 전후 그래프 출력 <br />
- Tab 2
    - 파일 2개를 불러오면 베이스라인 보정 후 그래프 출력
    - 파일 2개의 x값별 y값 차이 데이터프레임 출력
    - 그래프 색상 변경 및 범례 추가
    - 그래프 Peak 점 표시
- Tab 3
    - 비밀번호 기능 수정 (미리 입력 후 검색 가능)

### **윤승현**
- UI 제작
- Tab 2
    - 파일 중복 처리
    - 그래프 마우스 오버시 x좌표 정수형으로 출력
    - 데이터프레임 검색
- Tab 3
    - Peak Table 검색
    - 버튼 링크 연결
    - 비밀번호 기능 추가 (검색할 때마다 창 생성하여 입력)

<br />
