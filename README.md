# pmIME GUI

로마자로 **한글(현대·옛한글)**, **일본어 가나·한자**, **한자 자형 변환**, **확장 라틴 문자**를 입력하는 작은 데스크탑 입력 보조 도구입니다. 위 창에 로마자를 치면 아래 창에 변환 결과가 실시간으로 나타나고, Enter를 누르면 결과가 클립보드로 넘어갑니다. 같은 변환 엔진을 명령행에서도 쓸 수 있습니다.

- 버전: 0.13.1
- 저자: Nova de Hi
- 라이선스: GPLv3

> **ndhmdWriter와의 관계**
> 이 프로그램의 기능은 저술 앱 **ndhmdWriter**에 "한중일 pm 입력기"로 통합되었습니다(변환 코어는 `pmime_core.py`로 분리). ndhmdWriter 안에서 쓰려면 따로 설치할 필요가 없습니다.
> 이 저장소는 그와 별개로 **독립 실행 앱**으로서의 pmIME GUI를 유지·보관합니다. 다른 편집기와 함께 쓰거나 명령행 변환기로 쓸 때는 이쪽을 사용하십시오.

## 구성 파일

| 파일 | 내용 |
|---|---|
| `pmimegui.py` | 프로그램 본체 (GUI + CLI + 변환 엔진) |
| `shinjitai.json` | 정자 → 일본 신자체 표 |
| `kyujitai.json` | 신자체 표 보충 항목 (`han` 역변환에도 사용) |
| `simplified.json` | 정자(번체) → 중국 간체 표 |
| `customkanji.json` | 일본어 한자 사용자 사전 (`{h:읽기}` → 한자) |

## 요구 사항과 실행

- Python 3
- GUI: [PyQt6](https://pypi.org/project/PyQt6/) — 없으면 CLI 변환만 동작합니다.
- Windows에서 "직전 창 전송"을 쓰려면 `pyautogui`가 추가로 필요합니다.
- macOS에서 "직전 창 전송"을 쓰려면 손쉬운 사용(Accessibility) 권한이 필요합니다.

```sh
pip install PyQt6
python pmimegui.py            # 인자 없이 실행하면 GUI
```

JSON 사전 파일은 아래 순서로 찾아 처음 발견한 것을 씁니다.

| 순서 | Windows | macOS / Linux |
|---|---|---|
| 1 | 현재 작업 폴더 | 현재 작업 폴더 |
| 2 | 실행 파일(스크립트) 폴더 | `~/.config/pmimegui/` |
| 3 | PyInstaller 내부 폴더 | 실행 파일(스크립트) 폴더 |
| 4 | | (macOS 앱 번들) `Contents/Resources/` |

창 설정(입력 메서드, 한자 필터, 정규화, 폰트, 체크박스)은 `QSettings("ktug.org", "pmIMEgui")`에 저장됩니다.

## 입력 메서드

| 메서드 | 줄머리 태그 | CLI `--mode` | 특징 | 예 |
|---|---|---|---|---|
| pm | `%pm` | `pm` | 음절을 `/`로 직접 구분. 옛한글 자모 전체 지원 | `han/gvr` → 한글 |
| frkim | `%frk` | `frk` | 음절 자동 분리, 필요하면 `'`로 구분 | `hangyr` → 한글 |
| mix | `%mix` | `mix` | pm 자모 표기 + 음절 자동 분리 | `hangvr` → 한글 |
| rrk-ex | `%rrk` | `rrk` | 국어의 로마자 표기법 계열(전자법), `-`로 음절 구분 | `han-geul` → 한글 |
| Kana | `%jp` | `jp` | 로마자 → 가나. 대문자로 쓰면 가타카나 | `nihongo KATAKANA` → にほんご カタカナ |
| transparent | `%clean` | `clean` | 변환 없음 (LaTeX 확장 입력만 적용) | |

pm 방식의 기본 규칙 몇 가지:

- 초성 ㅇ은 생략하거나 `q`, 받침 ㅇ은 `q` — `sa/raq` → 사랑
- ㅡ는 `v`, ㅓ는 `e`, ㅐ는 `ay`(또는 `ai`) — `dai/han/min/gug` → 대한민국
- 아래아는 `@` — `h@n/gvr` → ᄒᆞᆫ글
- 방점: 음절 끝에 `;`(거성), `:`(상성) — `na/rad;mar:ssam/i` → 나랃〮말〯쌈이
- 대문자는 호환 자모(낱자) — `GANADA` → ㄱㅏㄴㅏㄷㅏ

자모별 로마자 대응 전체는 `pmimegui.py` 앞부분의 `pm_map`, `frk_map`, `rrk_map`, `romaji_to_kana` 표를 참조하십시오.

### 줄머리 태그

입력창의 각 줄 맨 앞에 태그를 붙이면 그 줄만 다른 메서드로 변환합니다. 태그에 바로 붙여 대괄호로 한자 필터를 지정할 수 있습니다.

```
%pm han/gvr
%jp nihongo
%mix[shin] ...
%clean \'e \v{s}
```

한자 필터 옵션: `[shin]` 신자체, `[kyu]`, `[sim]` 간체, `[han]` 신자체 → 정자 역변환, `[none]` 필터 끔. 생략하면 위쪽 콤보 상자의 설정을 따릅니다. `[han]`에서 후보가 여럿이면 `{辨|辯|辦|瓣}`처럼 모두 표시합니다.

### 괄호와 문장 부호

| 입력 | 결과 | 입력 | 결과 |
|---|---|---|---|
| `0[` `0]` | 「 」 | `1[` `1]` | 『 』 |
| `2[` `2]` | 〈 〉 | `3[` `3]` | 《 》 |
| `4[` `4]` | 〔 〕 | `5[` `5]` | 【 】 |
| `#3[` `#3]` | （ ） | `#5[` `#5]` | “ ” |
| `^.` `^,` | 。 、 | `^*` `^-` | … ― |
| `^~` `^<` | ～ ・ | `^^` | ^ |

Kana 모드에서는 `.` `,`가 자동으로 `。` `、`가 되고(숫자 사이는 그대로), `` ` `` … `'`는 「 」, ` `` ` … `''`는 『 』가 됩니다.

### LaTeX 문서와 함께 쓰기

- `\textbf{...}` 같은 LaTeX 명령 이름과 `\begin{...}`, `\end{...}`는 변환하지 않고 보존합니다(인자 내용은 변환).
- 로마자를 그대로 두려면 `\`와 `\␣`(백슬래시+공백)로 감쌉니다: `\Apple\ han` → `Apple한`

### LaTeX 확장 입력 (모든 메서드 공통)

"LaTeX 확장 입력"을 켜면(CLI는 기본으로 켜짐, `--no-latex`로 끔) 다음 표기가 실제 문자가 됩니다.

| 입력 | 결과 |
|---|---|
| `\'e` `` \`e `` `\^e` `\"o` `\~n` | é è ê ö ñ |
| `\v{s}` `\c{c}` `\u{g}` `\H{o}` `\k{a}` | š ç ğ ő ą |
| `\ss` `\ae` `\oe` `\o` `\l` `\th` | ß æ œ ø ł þ |
| `\textemdash` `\texteuro` `\%` | — € % |
| `\xAC00` `\x{AC00}` `가` `\char"AC00` | 가 |
| `\x{1112 1161 11AB}` | 한 (코드포인트 나열) |
| `\x{1F600}` `\U0001F600` | 😀 |

잘못된 코드포인트는 원문 그대로 남고, `\\'e`처럼 백슬래시를 겹쳐 쓰면 확장하지 않습니다.

### 정규화

한글 출력은 NFD(첫가끝 조합형) 또는 NFC(완성형)를 고를 수 있습니다. NFD에서도 라틴 확장 문자는 분해하지 않고 한글만 분해합니다. 옛한글은 NFD로 출력해야 조합이 유지됩니다.

## 일본어 한자 입력 보조창

F10으로 여는 작은 창에서 사용자 사전(`customkanji.json`)을 검색해 한자를 고릅니다. 고른 항목은 `{h:ai}` 같은 키로 입력창에 들어가고, Kana 모드에서 `愛`로 변환됩니다.

- 검색은 읽기(로마자)와 한자 양쪽으로 합니다. 정자로 검색해도 신자체 항목을 찾습니다.
- 목록의 앞 10개는 숫자 키 0–9로 바로 고릅니다. ↓로 목록 이동, Enter/더블클릭으로 선택.
- "새 단어 등록"으로 사전에 항목을 추가합니다. 키가 겹치면 뒤에 번호가 붙습니다.

## 단축키

| 키 | 동작 |
|---|---|
| Enter | 변환 결과를 클립보드로 전송 ("전송 후 초기화"가 켜져 있으면 창을 비움) |
| Shift+Enter | 줄바꿈 |
| Alt+Z | 직전에 전송·삭제한 입력 복구 |
| Esc | 입력·출력 지우기 |
| F1 | 도움말 |
| F10 | 일본어 한자 보조창 열기/닫기 |
| Ctrl+F | 보조창 검색란으로 이동 |

"직전 창 전송"을 켜면 전송 후 바로 앞에 쓰던 창으로 전환해 붙여넣기까지 합니다(macOS, Windows).

## 명령행 사용

문자열 인자, `-i` 파일, 또는 파이프 입력이 있으면 GUI 없이 변환만 하고 끝납니다.

```sh
python pmimegui.py -n "han/gvr"                    # 한글
python pmimegui.py -n --mode rrk "han-geul"        # 한글
python pmimegui.py --mode jp "nihongo"             # にほんご
python pmimegui.py -n --hanja shin "眞 國 學"       # 真 国 学
python pmimegui.py --mode clean "\'e \v{s}"        # é š
```

| 옵션 | 뜻 |
|---|---|
| `--mode {pm,frk,mix,rrk,jp,clean}` | 입력 메서드 (기본 `pm`) |
| `--hanja {none,shin,kyu,sim,han}` | 한자 필터 (기본 `none`) |
| `-n`, `--nfc` | 한글을 NFC로 출력 (기본은 NFD) |
| `-i FILE`, `-o FILE` | 입력·출력 파일 (UTF-8) |
| `-r`, `--raw` | 파일·파이프 입력 전체를 변환 |
| `--macro NAME` | 파일·파이프 입력에서 `\NAME{...}` 안쪽만 변환 (기본 `jamoword`) |
| `--env NAME` | `\begin{NAME}...\end{NAME}` 안쪽만 변환 |
| `--keep` | 변환 후에도 매크로·환경 껍데기를 남김 |
| `--no-latex` | LaTeX 확장 입력 끔 |
| `--latex-all` | `--macro`/`--env` 사용 시에도 문서 전체에 LaTeX 확장 입력 적용 |
| `-c`, `--clip` | 결과를 클립보드로도 복사 |
| `-v`, `--version` | 버전 표시 |

파일·파이프 입력은 `-r`을 주지 않으면 **지정한 매크로/환경 안쪽만** 변환합니다.

```sh
echo 'A \jamoword{han/gvr} B' | python pmimegui.py -n          # A 한글 B
echo 'A \jamoword{han/gvr} B' | python pmimegui.py -n --keep   # A \jamoword{한글} B
python pmimegui.py -n --env jamo -i in.tex -o out.tex
```

입력에 `<kr>...</kr>`(pm), `<kr:frk>...</kr:frk>`(frkim), `<jp>...</jp>`(가나) 태그가 있으면 태그 안쪽만 변환합니다.

## 알려진 제한

- 사전 파일을 현재 작업 폴더에서 가장 먼저 찾으므로, 실행 위치에 따라 다른 사전이 읽힐 수 있습니다.
- 표준 입력이 파이프나 파일로 연결된 채 실행하면 GUI가 뜨지 않고 CLI로 동작합니다.
- "직전 창 전송"은 Linux에서 지원하지 않습니다.
- Linux에서 `--clip`은 프로그램이 끝난 뒤 클립보드 내용이 남지 않을 수 있습니다.

## 라이선스

GNU General Public License v3.0 (GPLv3). © 2026 Nova de Hi
