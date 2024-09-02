# 아파트너 : 차량, 관리비 노티
![HACS][hacs-shield]

아파트너 HA Custom_component입니다.
https://cafe.naver.com/stsmarthome/91334
참조하여, 특정 기능만 Component로 만들었습니다.


## 사용자 구성요소를 HA에 설치하는 방법
### HACS
- HACS > Integrations > 우측상단 메뉴 > `Custom repositories` 선택
- `Add custom repository URL`에 `https://github.com/chongjae/aptner` 입력
- Category 는 `Integration` 선택 후 `ADD` 클릭
- HACS > Integrations 에서 `아파트너` 찾아서 설치
- HomeAssistant 재시작

### 수동설치
- `https://github.com/chongjae/aptner` 에서 `코드 -> 소스 코드 다운로드(zip)` 을 눌러 파일을 다운로드, 내부의 `aptner` 폴더 확인
- HomeAssistant 설정폴더 `/config` 내부에 `custom_components` 폴더를 생성(이미 있으면 다음 단계)<br/>설정폴더는 `configuration.yaml` 파일이 있는 폴더를 의미합니다.
- `/config/custom_components`에 위에서 다운받은 `aptner` 폴더를 넣기
- HomeAssistant 재시작

## 아파트너를 통합구성요소로 설치하는 방법
### 통합구성요소
- HomeAssistant 사이드패널 > 설정 > 기기 및 서비스 > 통합 구성요소 추가
- 검색창에서 `아파트너` 입력 후 선택
- 아이디 비밀번호 입력

<img src="https://github.com/chongjae/aptner/blob/master/images/config_flow.png?raw=true" title="ConfigFlow" alt="ConfigFlow" />
<img src="https://github.com/chongjae/aptner/blob/master/images/reservation.png?raw=true" title="Reservation" alt="Reservation" />