MarkerClipManager — DaVinci Resolve용 타임라인 및 클립 마커 관리자
==================================================================
Author: Tommaso Feraboli — Film Editor
Version: 1.4.7
MIT License — see the script header

수행할 작업
-----------
Resolve 타임라인의 모든 마커를 보고 관리하는 단일 창: 
루러(타임라인 레벨) 마커와 개별 클립에 배치된 마커, 
모든 비디오 및 오디오 트랙.

각 마커에 대해 표시: 마커 그래픽(Resolve와 동일한 기본 모양),
트랙, TC 시작, TC 종료, 지속 시간, 색상, 이름, 키워드, 노트.

기능
----
- 하나 이상의 마커를 선택해 색상 변경, 트랙 변경("TIMELINE" 눈금자로
  이동하거나 그 반대 포함), 삭제를 할 수 있습니다
- 이름, 키워드, 노트를 표에서 바로 편집할 수 있으며(더블 클릭), 선택한
  여러 마커에 한 번에 적용됩니다
- Delete 키는 삭제 버튼과 같은 역할을 하며, 확인 창은 끌 수 있습니다
- Cmd+Z / Ctrl+Z로 실행 취소와 다시 실행이 가능하고, History 패널에서 이전
  단계를 더블 클릭하면 바로 그 지점으로 돌아갑니다. 현재 세션에만
  해당하며 스크립트를 닫으면 지워집니다
- 색상, 트랙, 작성자/이름, 키워드로 필터링할 수 있습니다
- 마커를 CSV로 내보내고 가져올 수 있습니다
- 행을 클릭하면 타임라인 재생 헤드가 해당 마커로 이동합니다
- 인터페이스는 12개 언어를 지원합니다. 해당하는 언어가 있으면 시스템
  언어로 시작하고 없으면 영어로 시작하며, 창 위쪽 메뉴에서 바꿀 수
  있습니다(스크립트를 다시 시작하면 적용됩니다)

필수 사항
---------
- DaVinci Resolve 19/20 (macOS)
- 시스템에 설치된 Python 3
- PySide6(아래 설정 스크립트에 의해 자동 설치 — 수동 단계 필요 없음)

설치(1회)
---------
1. 사용하는 시스템에 맞는 설치 프로그램을 내려받습니다
2. macOS: .command 파일을 마우스 오른쪽 버튼으로 클릭한 뒤 "열기"를
   선택합니다. 더블 클릭이 아닙니다. 이 파일은 Apple 개발자 인증서로
   서명되어 있지 않아 더블 클릭하면 macOS가 차단합니다
   Windows: .cmd 파일을 더블 클릭합니다. SmartScreen 경고가 나오면 "추가
   정보"를 누른 뒤 "실행"을 선택합니다
3. 설치 프로그램이 파일을 복사한 다음, 스크립트에 필요한 Python 환경을
   준비합니다(이 부분은 인터넷 연결이 필요하며 1분 정도 걸립니다)
4. 두 번째 부분이 실패하더라도(연결이 없거나 Python이 없는 경우) 파일은
   정상적으로 설치되어 있습니다. 설치된 폴더를 열고 가능할 때
   "MarkerClipManager_Setup.command"(macOS) 또는
   "MarkerClipManager_Setup_Windows.cmd"(Windows)를 실행하세요
5. 완료입니다. 업데이트도 같은 방법으로 이전 버전 위에 설치되며, 설정은
   그대로 유지됩니다

사용법
------
DaVinci Resolve에서: Workspace > Scripts > Comp > MarkerClipManager > MarkerClipManager
(스크립트는 Comp 내부의 "MarkerClipManager" 하위 폴더에 있으므로,
메뉴에 같은 이름의 하위 메뉴로 나타남)

알려진 제한사항
---------------
- 테이블의 마커는 스크립트에서 그린 다시 만든 아이콘이며, Resolve의
  공식 아이콘이 아닙니다(API에 노출되지 않음). 색상은 사용자가 제공한
  정확한 16진수 값 — 아이콘 모양만 근사값
- "키워드"는 기본 Resolve 마커 필드가 아닙니다: 내부 마커 필드(customData)에
  저장되며, Resolve의 기본 마커 패널에는 보이지 않음 — 이 스크립트에서만
  읽기/쓰기 가능
- 타임코드는 프로젝트의 활성 타임라인에서 직접 fps 및 Drop Frame/Non-Drop Frame
  모드를 읽음(29.97 및 59.94 DF는 표준 SMPTE 알고리즘으로 올바르게 처리);
  비표준 fps의 경우 계산은 근사값
- EDL 가져오기/내보내기는 이 스크립트에서 처리하지 않음: Resolve의 기본
  기능 사용(Timeline > Markers > Export/Import)
- 마커를 비디오/오디오 트랙으로 이동하려면 해당 위치에 클립이 이미
  존재해야 함

지원
----
버그 보고: 앱의 🐛 버튼 사용(tomfilmeditor.tools@gmail.com으로 사전 작성된
이메일 열기)
개발을 지원하고 싶으면: 앱의 ☕ 버튼 또는
https://paypal.me/acoffeefortom

⚠️  Note on translations: This documentation is available in multiple languages.
These translations were generated automatically. If you find any errors or typos,
please report them to the contact listed in the SUPPORT section above.
