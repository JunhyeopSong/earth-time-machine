# Mark Creer 이벤트 차트 → 업데이트 후보

원본: `Paleo geo event chart.pdf` (A3 한 장, "Chronostratigraphic chart 2026 · Chart by Mark Creer 2026", 지도는 "GPlates – Scotese").
구성: 왼쪽 = 생물 첫 등장(첫 출현), 가운데 = ICS식 시대 표, 오른쪽 = 지질·기후 사건(초록 = 지각, 파랑 = 기후, 빨강 = 멸종), 맨 오른쪽 = 10장의 고지리 지도.
차트 하단에 "All dates and placements are estimates and subject to revision"라고 적혀 있습니다. 날짜는 대부분 눈금 위치로 읽은 값이라 ±2–5 Myr 정도 오차가 있습니다.

비교 대상 앱 코드(`docs/index.html`): `PERIODS`(144행), `EVENTS` 이야기 카드(193행~), `PRESETS` 칩(228행), `FX` 지도 효과(258행~), `GEO_EVENTS` 위치 핀(274행~), 출처 `foot`(93행, 번역은 137행 i18n JSON의 `ui.foot`).
참고로 앱에는 브리프에 적힌 것보다 많은 내용이 이미 있습니다. 드레이크 해협(30), PETM(56), 인도-마다가스카르 분리(88), 파나마 지협(3), 남극 빙상(34), 오르도비스기 말 빙하(445), 틱타알릭(375), 버제스 셰일(508), 시조새(150) 등입니다.

---

## 1. PDF와 앱이 이미 일치하는 것 (할 일 없음)

| PDF | 앱 | 비고 |
|---|---|---|
| Isthmus of Panama closure (~3) | 파나마 지협 형성 3 Ma 핀 | 일치 |
| Antarctic glaciation (~34) | 남극 빙상의 탄생 34 Ma + 빙상 효과 | 일치 |
| Himalayan orogeny (~50) | 인도-아시아 충돌 50 Ma + 충돌 효과 + 칩 | 일치 |
| K-Pg (Chicxulub / Deccan) 66 | 칙술루브 + 데칸 트랩 효과 + 칩 | 일치 (퍼센트 기준은 아래 2절) |
| Extinction 47% (CAMP?) / Pangaea starts breakup ~201 | CAMP 효과 201 + 칩 + 이야기 카드 200 | 일치 |
| Gondwana / Laurasia (~180) | 이야기 카드 175 | 일치 |
| Start of Gondwana breakup (~138) | 이야기 카드 140 | 일치 |
| PT extinction 56% (Siberian Traps) 252 | 시베리아 트랩 효과 + 칩 | 일치 |
| Pangaea formation (~290) | 판게아 탄생 칩 300 + 중앙 판게아 산맥 핀 | 범위 안 |
| Extinction 40% (Kellwasser) ~372 | 후기 데본기 대멸종 칩 372 | 일치 |
| Extinction 57% ~445, Gondwana over south pole → cooling | 오르도비스기 말 칩 + 빙상 효과 | 일치 |
| Tiktaalik, Burgess shale, Archaeopteryx, Tyrannosaurus/Velociraptor, Australopithecus | 각각 화석 핀 있음 | 일치 |

---

## 2. 날짜·이름·숫자가 다른 것

| 항목 | PDF | 앱 | 판단 |
|---|---|---|---|
| **멸종 퍼센트** | K-Pg 40%, PT 56%, End-Ordovician 57%, End-Triassic 47%, Kellwasser 40% | 종(species) 기준: K-Pg 약 75%, 오르도비스기 약 85%, 페름기 약 90% | **둘 다 맞지만 단위가 다릅니다.** PDF 숫자는 Wikipedia "Extinction event"에 나오는 **해양 생물 속(genus) 손실률**(Sepkoski / Rohde & Muller 곡선)과 일치합니다. 앱의 종 기준 숫자는 바꾸지 않는 게 좋습니다. 속 기준 숫자를 쓰면 "해양 속의 40%"처럼 단위를 꼭 적어야 합니다. |
| Drake Passage opening | ~41 Ma | 30 Ma | 연구마다 갈립니다(얕은 통로 ~41 Ma, 깊은 해류 통로 ~34–30 Ma). 앱 날짜는 그대로 두고 설명에 "4100만~3000만 년 전 사이에 단계적으로"를 덧붙이면 둘 다 반영됩니다. |
| Start of Atlantic ocean opening | ~165 Ma | 중앙 대서양 175 Ma (+ 이야기 카드 200 "벌어지기 시작") | 중앙 대서양의 해저 확장은 보통 ~190–175 Ma로 봅니다. **앱 쪽이 더 표준에 가깝습니다.** 변경하지 않습니다. |
| Dinosaurs (첫 등장) | ~240 Ma (중기 트라이아스기) | 최초의 공룡 231 Ma (이스치구알라스토) | 확실한 공룡 화석은 ~233–231 Ma입니다. ~243 Ma 니아사사우루스는 공룡인지 논쟁 중입니다. **앱이 보수적이고 맞습니다.** |
| Tethys Ocean closure | ~76 Ma | 없음 | **의심스러운 값입니다.** 네오테티스는 백악기 말부터 마이오세(아라비아-유라시아 충돌 ~20–15 Ma)까지 단계적으로 닫혔습니다. 한 시점으로 넣지 않는 게 좋습니다. |
| "End Atlantic Ocean opening" | ~58 Ma | 없음 | **표현이 모호합니다.** 대서양은 지금도 넓어지고 있습니다. 북대서양(그린란드-유럽)이 마지막으로 열린 시점(~56–55 Ma, PETM과 북대서양 화산 지대)을 가리키는 것으로 보입니다. 앱의 PETM 핀 설명에 "그린란드와 유럽 사이가 열리며"를 넣는 정도면 충분합니다. |
| Popigai asteroid → Extinction 11% | ~36 Ma, 물음표 | 없음 | Popigai 충돌(~35.7 Ma, 시베리아, 지름 약 100 km)은 실제로 있었습니다. 다만 에오세-올리고세 멸종(33.9 Ma)의 주 원인은 남극 빙하화에 따른 냉각으로 봅니다. PDF도 물음표를 달았습니다. **원인으로 표시하지 말 것.** |
| 시대 경계 숫자 | 201.3, 485.4, 443.8, 419.2, ~145.0 | `PERIODS`: 201.4, 485.4, 443.8, 419.2, 145.0 | 두 쪽 모두 2023년 이전 ICS 값입니다. ICS는 2024/12판에서 고생대 경계 여러 개를 수정했습니다. 바꾸기 전에 [ICS 2024/12 차트](https://stratigraphy.org/ICSchart/ChronostratChart2024-12.pdf)로 직접 확인해야 합니다(이번에 숫자까지는 확인하지 못했습니다). PDF의 201.3은 2013–2020판 값이고, 앱의 201.4가 더 최근 값입니다. |

---

## 3. 앱에 없는 사건: 우선순위별

### 높음: 기존 효과 타입을 그대로 쓸 수 있고, 지구본에서 바로 보이는 것

1. **Late Paleozoic Ice Age (~340–260 Ma, PDF 막대는 ~360–255)**
   - 앱에는 이야기 카드 300의 "남쪽 곤드와나는 긴 빙하기"라는 한 문장만 있습니다. 빙상 효과(`FX` type 3)가 오르도비스기와 남극에만 있습니다.
   - 제안: `GEO_EVENTS`에 climate 핀(남아프리카·남아메리카 남부 곤드와나, 예: pid 701)과 `FX` type 3 빙상을 추가합니다. 300 Ma 근처에서 span을 크게(약 30) 줍니다.
   - 이유: 현생누대에서 가장 오래 지속된 빙하기입니다. 지구본에서 판게아 남쪽이 얼음으로 덮이는 모습이 바로 보입니다. 기온 표시(PhanDA)가 이 구간에서 내려가는 것과도 맞아떨어집니다.

2. **Capitanian extinction + Emeishan Traps (~260 Ma)**
   - PDF: "Extinction 48% (Capitanian)". 일반적으로 원인은 중국 남서부 어메이산(峨眉山) 현무암 분출로 봅니다(PDF에는 화산 이름이 없습니다).
   - 제안: `GEO_EVENTS` volcano 핀(쓰촨·윈난, 남중국 판)과 `FX` type 2 홍수 현무암 효과를 추가합니다. 칩은 "5대 대멸종" 구성을 유지하려면 넣지 않는 것을 권합니다.
   - 이유: 홍수 현무암 효과 코드를 그대로 재사용할 수 있습니다. 시베리아 트랩 8 Myr 전에 일어난 "작은 형님" 사건으로 이야기가 이어집니다.

3. **Iapetus suture: Laurentia–Avalonia 충돌 (~425–420 Ma, 칼레도니아 조산운동)**
   - PDF: "Iapetus suture complete (Laurentia / Avalonia collide)". 캄브리아기·오르도비스기 지도에 Iapetus Ocean, Avalonia, Baltica도 표시돼 있습니다.
   - 제안: tectonic 핀(스코틀랜드-잉글랜드 경계, 이아페투스 봉합선이 지나는 솔웨이 지역)과 `FX` type 5 충돌 효과를 추가합니다. 설명은 "잉글랜드와 스코틀랜드가 이때 처음 한 땅이 되었다"는 식으로 씁니다.
   - 이유: 앱에 실루리아기 지각 사건이 하나도 없습니다. 영국 사용자(그리고 Mark)에게 특히 와닿는 장면입니다.

4. **Carnian Pluvial Event (~234–232 Ma)**
   - 제안: climate 핀을 추가하고, 선택적으로 Wrangellia 홍수 현무암(캐나다 BC~알래스카) `FX` type 2를 붙입니다. 설명은 "200만 년 가까이 이어진 습한 기후 뒤에 공룡이 퍼졌다"로 씁니다. 기존 "최초의 공룡들"(231) 핀과 바로 이어집니다.
   - 이유: 공룡 등장 이야기의 원인을 보여줍니다. 최근 연구가 많고 표준 사건으로 자리 잡았습니다.

### 중간: 핀이나 설명 문구로 추가

5. **Hangenberg event (~359 Ma, 데본기-석탄기 경계)**: 후기 데본기 칩/이야기 카드 설명에 "두 차례(Kellwasser ~372, Hangenberg ~359)"를 덧붙입니다. 새 칩은 필요 없습니다.
6. **Variscan orogeny (~380–280 Ma, PDF ~320)**: 유럽 쪽 tectonic 핀(예: 독일·프랑스 중부)을 추가하거나, "중앙 판게아 산맥" 핀 설명에 "유럽에서는 바리스칸 조산운동"을 넣습니다. 영국 남서부(콘월) 화강암도 이때 생겼습니다.
7. **Alpine orogeny (~65 Ma~현재, PDF ~55)**: 알프스 tectonic 핀을 추가합니다(약 35 Ma 전후, 넓은 span). 미래 구간의 "지중해가 닫힘"(−50)과 이야기가 이어집니다.
8. **Iceland formation (~16 Ma, 가장 오래된 암석 기준)**: 북대서양 volcano 핀을 추가합니다. 작은 type 2 효과를 붙여도 됩니다(제주도처럼).
9. **Cenomanian–Turonian anoxic event, OAE 2 (~94 Ma)**: PDF "Extinction 25% (anoxic)". 바다 전체 사건이라 특정 위치가 없습니다. climate 핀으로 하거나 이야기 카드에 한 줄 넣는 정도가 적당합니다. 이름은 "Cenomanian–Turonian extinction (OAE 2)"를 권합니다.
10. **Toarcian event (~183 Ma)**: PDF "Extinction 20%". 앱의 카루-페라 핀 설명에 이미 "쥐라기 초 해양 무산소 사건"이 있습니다. 이름(Toarcian)만 넣으면 됩니다.
11. **Popigai impact (~35.7 Ma)**: 충돌 효과(type 1, 작게)로 넣을 수 있습니다. 다만 2절대로 멸종 원인으로 쓰지 않고 "같은 시기의 큰 충돌, 멸종과의 관련은 불확실"로 씁니다.
12. **Early Paleozoic Ice Age (~470–420 Ma)**: 기존 오르도비스기 말 빙상 효과의 span을 늘리거나, 설명에 "빙하기는 수천만 년 이어졌고 445 Ma가 정점"을 넣습니다.

### 낮음: 근거가 약하거나, 앱 범위 밖이거나, 별도 기능에 맞는 것

13. **Olson's extinction (~272 Ma)**: 실재 여부 자체가 논쟁 중입니다. 넣지 않는 것을 권합니다.
14. **Extinction 31% (~330 Ma, Serpukhovian으로 추정)**, **Extinction 20% (~145 Ma, 쥐라기-백악기 경계)**: 규모와 시점이 불확실한 소규모 사건입니다.
15. **캄브리아기 멸종 3회 (~517, ~502, ~488 Ma)**: Botomian / Dresbachian / End-Cambrian입니다. 이름이 없고 540 Ma 근처라 지도 효과로 보여주기 어렵습니다.
16. **Pyrenean orogeny (PDF ~30, 주요 단계는 에오세 ~55–35 Ma)**, **Greenland rifting from North America (~120)**: 작은 지역 사건입니다. 넣는다면 핀 정도로 충분합니다.
17. **540 Ma 이전 사건**: Marinoan / Sturtian glaciation, Rodinia, Columbia, Huronian snowball Earth, Great Oxygenation Event, plate tectonics 시작, Pongola glaciation. 지도 데이터가 540 Ma에서 끝나므로 지구본에는 보여줄 수 없습니다. 나중에 "지도 이전 이야기" 같은 텍스트 패널을 만든다면 이 목록을 그대로 쓸 수 있습니다.
18. **왼쪽 열 생물 첫 등장 (~70개)**: 꽃식물(~130), 풀, 포유류(~225), 새, 박쥐, 고래류 등입니다. 판 이동 앱의 핵심은 아니지만 `planning/human-journey-plan.md` 같은 "생명/인류" 레이어를 만들 때 좋은 체크리스트입니다. 지금 당장은 꽃식물 하나 정도를 이야기 카드에 넣는 것을 고려할 만합니다.

---

## 4. 표시 방식 요약

| 방식 | 해당 항목 |
|---|---|
| 새 칩 (`PRESETS`) | 넣지 않는 것을 권합니다. 지금 칩은 "5대 대멸종 + 랜드마크"로 구성이 깔끔합니다. 하나만 추가한다면 **Late Paleozoic Ice Age**(~300)나 **Capitanian/Emeishan**(260)입니다. |
| 지도 효과 (`FX`) | LPIA 빙상(type 3), Emeishan(type 2), Iapetus/Caledonian 충돌(type 5), Wrangellia(type 2, 선택), Popigai(type 1, 선택), Iceland(type 2 소형, 선택) |
| 위치 핀 (`GEO_EVENTS`) | 위 항목 전부 + Variscan, Alpine, OAE 2 |
| 설명 문구만 수정 | 드레이크 해협 시기 범위, PETM에 북대서양 개통, 후기 데본기 두 차례, 카루-페라에 Toarcian, 오르도비스기 빙하 기간 |
| 타임라인 마커 | 빙하기 두 개(EPIA, LPIA)는 점이 아니라 **기간**이라서, `TMUI.timeline`에 기간 막대를 그릴 수 있다면 PDF의 점선 막대처럼 보여주기 좋습니다(별도 설계 필요). |

새 항목은 모두 10개 언어 번역(`i18n` JSON의 `events`/`fx`)이 필요합니다. 작업량은 대부분 번역입니다.

---

## 5. 크레딧 문구 제안

Mark는 크레딧이 필요 없다고 했지만 출처에 이름을 넣습니다. 이메일 같은 연락처는 넣지 않습니다.

**문구**
- EN: `Event chart reference: Mark Creer (Dorking, UK), "Chronostratigraphic chart 2026".`
- KO: `사건 연표 참고: Mark Creer(영국 도킹)의 "Chronostratigraphic chart 2026".`
- 지역명(Dorking)을 공개해도 되는지는 Mark에게 한 번 확인하는 게 안전합니다. 아니면 "(UK)"까지만 씁니다.

**넣을 위치**
1. `docs/index.html` 93행 `<div class="foot" id="foot">`: 한국어 기본 문구 끝, "도시: Natural Earth(퍼블릭 도메인)." 바로 뒤에 넣습니다.
2. `docs/index.html` 137행 i18n JSON의 각 언어 `ui.foot`: 화면에 실제로 보이는 문구는 1333행 `$('foot').innerHTML = esc(t('foot'))…`가 이 값으로 덮어씁니다. 그래서 **10개 언어 `ui.foot` 모두**의 "Cities: {ne} (public domain)." 뒤에 추가해야 합니다. 링크가 없으니 `{…}` 자리표시자는 필요 없습니다(인물 이름이라 번역 없이 원문 그대로 둬도 됩니다).
3. `README.md` 영어 "Data sources" 표(34–41행)에 행을 추가합니다.
   `| Event timeline cross-check | Chronostratigraphic event chart by Mark Creer (Dorking, UK), shared with the project | Used with permission |`
   한국어 "데이터 출처" 표(79–86행)에도 같은 행을 추가합니다.
   `| 사건 연표 검토 | Mark Creer(영국 도킹)가 보내준 지질 사건 연표 | 허락받아 참고 |`
   또는 43행/88행 **Notes** 문단의 "corrections are welcome" 앞에 "Event timeline cross-checked against a chart by Mark Creer (UK)."를 넣습니다. 표 쪽을 권합니다.

---

## 6. 요약

- PDF의 큰 사건(5대 대멸종, 판게아 형성·분열, 곤드와나, 인도 충돌, 남극 빙하, 파나마)은 앱에 **이미 다 있습니다**. 날짜도 대체로 앱이 같거나 더 최신입니다.
- PDF의 멸종 %는 **해양 속(genus) 기준**이라 앱의 종 기준 %와 다릅니다. 앱 숫자는 그대로 두는 게 맞습니다.
- 추가할 가치가 큰 것은 4가지입니다. **후기 고생대 빙하기**, **카피타니안 멸종 + 어메이산 트랩**, **이아페투스 봉합(로렌시아-아발로니아 충돌)**, **카르니아절 다우 사건**. 모두 기존 지도 효과를 재사용할 수 있습니다.
- 의심스러운 항목은 넣지 않는 것을 권합니다. 테티스해 닫힘 76 Ma, "End Atlantic Ocean opening", 포피가이를 멸종 원인으로 보는 것, Olson 멸종이 해당됩니다.
- 별도 확인 필요: 앱과 PDF 모두 2023년 이전 ICS 경계값을 씁니다. ICS 2024/12판과 대조해 봐야 합니다.

---

## 7. 출처 확인 후 "확실한 것만" 목록 (2026-11-12 웹 검색으로 확인)

원칙: 연대와 사실이 여러 자료에서 일치하는 부분만 씁니다. 원인이나 퍼센트처럼 논쟁 중인 부분은 문구에서 빼거나 "유력"으로 낮춰 씁니다.

| # | 사건 | 확실하게 쓸 수 있는 것 | 빼야 할 것 | 출처 |
|---|---|---|---|---|
| 1 | Hangenberg event | 358.9 Ma(데본기-석탄기 경계). 후기 데본기의 두 번째 큰 멸종(Kellwasser ~372 다음) | 원인(무산소·화산·초신성 모두 논쟁 중), 31% | [Wikipedia](https://en.wikipedia.org/wiki/Hangenberg_event) |
| 2 | Emeishan Traps | 중국 남서부 홍수 현무암, 약 262–259 Ma. 카피타니안 멸종과 같은 시기 | 48%. 멸종 원인이라는 단정(유력하지만 논쟁 중) | [Wikipedia](https://en.wikipedia.org/wiki/Emeishan_Traps), [UC 2023](https://www.uc.edu/news/articles/2023/04/geology-experts-find-evidence-of-dual-mass-extinctions-260-million-years-ago.html) |
| 3 | Carnian Pluvial Event | 약 234–232 Ma의 습한 기후 시기 | Wrangellia 화산이 원인이라는 단정(유력하지만 결정적이지 않음). "공룡이 퍼진 원인"(아직 미해결) | [Science News](https://www.sciencenews.org/article/volcano-eruptions-rainy-period-earth-climate-dinosaur-friendly), [Utah](https://attheu.utah.edu/facultystaff/insights-into-climate-change-during-origin-of-dinosaurs) |
| 4 | Iapetus Ocean closure (Laurentia–Avalonia) | 실루리아기 중·후기, 약 430–420 Ma. 봉합선이 대략 잉글랜드-스코틀랜드 경계를 지남 | "솔웨이 선"이라는 정확한 위치(논쟁 있음). 단일 연도 | [BGS Earthwise](https://earthwise.bgs.ac.uk/index.php/Iapetus_Suture,_South_of_Scotland) |
| 5 | Late Paleozoic Ice Age | 현생누대에서 가장 긴 빙하기(약 6천만 년 이상). 남쪽 곤드와나에 빙상. 석탄기-페름기 경계(~300 Ma) 무렵이 정점 | 정확한 시작·끝 연도. 계속 이어진 하나의 빙상이었는지(연속인지 여러 번이었는지 논쟁 중) | [USGS](https://pubs.usgs.gov/publication/70265927), [EGU23](https://meetingorganizer.copernicus.org/EGU23/EGU23-6958.html) |
| 6 | Cenomanian–Turonian event (OAE 2) | 93.9 Ma. 전 지구 해양 산소 부족 사건, 해양 생물 멸종 | 25%. "전 세계가 무산소"(지역마다 다름). 원인 단정 | [Wikipedia](https://en.wikipedia.org/wiki/Cenomanian-Turonian_boundary_event) |
| 7 | Toarcian event (이름만 추가) | 앱의 카루-페라 설명에 이미 있는 "쥐라기 초 해양 무산소 사건"에 이름을 붙임 | 20% | (일반 지식, 추가 확인 권장) |

**추가 확인 (2026-11-12):**
- **Toarcian Oceanic Anoxic Event:** 약 1억 8300만 년 전으로 확인했습니다. 해양 무산소와 멸종이 있었습니다. 대부분의 연구가 카루-페라 화산과 연결하지만, 시기만 가깝고 인과관계는 없다는 2019년 연구도 있습니다. → 카루-페라 핀 설명의 "연결됩니다"를 "같은 시기이며 원인으로 많이 거론됩니다"로 낮추고, 사건 이름 "토아르시안 해양 무산소 사건"을 넣는 것을 권합니다. 출처: [Wikipedia](https://en.wikipedia.org/wiki/Toarcian_Oceanic_Anoxic_Event), [Nature Comms 2023](https://link.springer.com/10.1038/s41467-023-36516-x)
- **Iceland:** "16 Ma"는 대중 자료의 대략적인 값입니다. 2023년 연구는 가장 오래된 화산 중심(서부 피오르, Hrafnsfjörður)을 약 1400만 년 전으로 봅니다. 그 아래 지각은 2000만 년보다 오래됐습니다. → 넣는다면 "서부 피오르에 드러난 가장 오래된 화산암은 약 1400만~1600만 년 전"처럼 범위로 쓰고, "아이슬란드가 생긴 해"처럼 한 시점으로 쓰지 않습니다. 출처: [JGR 2023 (Westfjords)](https://www.aminer.org/pub/64a392ecd68f896efa25d25a/petrogenesis-and-geodynamic-evolution-in-the-northern-westfjords-iceland-elucidated-by-iceland), [Wikipedia Iceland hotspot](https://en.wikipedia.com/wiki/Iceland_plume)

**이번 반영에서 제외:** 모든 멸종 퍼센트, Tethys closure 76 Ma, "End Atlantic Ocean opening", Popigai를 멸종 원인으로 보는 것, Olson extinction, ~330 Ma·~145 Ma 소규모 멸종, 이름 없는 캄브리아기 멸종 3회, PDF의 시대 경계 숫자, Drake Passage 날짜 변경, Pyrenean 30 Ma, Greenland 120 Ma.
**사실이지만 이번에 확인하지 않아 보류:** Iceland ~16 Ma, Popigai 충돌 자체(35.7 Ma), Variscan·Alpine 조산운동(긴 과정이라 핀 하나의 날짜로 표현하기 어려움).

**어떤 항목을 구현할까요?** 예: (a) 높음 1–4 + 크레딧, (b) 크레딧 + 설명 문구 수정만, (c) 높음+중간 전부.
