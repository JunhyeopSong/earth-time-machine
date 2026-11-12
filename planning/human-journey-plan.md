# 인류의 여정 — 기획서 (초안)

> 작성: 2026-11-11 · 상태: 리서치/기획 단계 (코드 없음) · 대상 저장소: 신규 (가칭 `human-journey`)
> 기존 제품: 지구 대륙 타임머신 — https://junhyeopsong.github.io/earth-time-machine/ (`docs/index.html`)

---

## English summary

**What.** A sister product to the Continental Time Machine: the same glass-UI 3D globe, timeline with period bands, playback with wheeling stars, events with map effects, city tracking, mean-temperature card and 10 languages — but telling the story of human evolution and of people spreading across the world.

**MVP.** The last ~300 kyr: the origin of *Homo sapiens* in Africa, the archaic humans who lived at the same time (Neanderthals, Denisovans, *H. floresiensis*, *H. luzonensis*, *H. naledi*, late *H. erectus*), interbreeding, the main Out-of-Africa dispersal (~60–45 ka), and arrival in Sahul, Europe, the Americas and the remote Pacific. Deeper hominin history (~7 Ma → 300 ka) comes in phase 2. The timeline is built for that from day one.

**Timeline.** One fixed, full-width timeline without zoom, because the owner already rejected zoom. Time is mapped with a *shifted logarithm*, x ∝ log(age + c), with c ≈ 5–10 kyr. This gives the crowded last 70 kyr roughly 40–65 % of the width, depending on range and c. Geological stages are shown as period bands and glacial cycles (MIS) as a thin stripe.

**Map.** Present-day relief (ETOPO 2022, CC0) is flooded to a sea-level curve (Spratt & Lisiecki 2016, CC0 on NOAA). For 26 ka → 0 it is refined with ICE-6G_C paleotopography and ice. Older ice sheets come from published reconstructions. This makes Beringia, Sunda, Sahul and Doggerland appear and disappear. Plate motion is **not** needed for ≤ 1 Ma. For the 7 Ma extension it is optional and could reuse PALEOMAP from the existing app.

**Data.** Sites come from ROAD (CC BY-SA 4.0) and the Paleobiology Database (CC BY 4.0), plus a hand-curated event list with per-event citations. Ancient-DNA sample metadata comes from AADR (Harvard Dataverse; licence must be checked, so use only a curated subset with paper citations). Climate comes from Krapp et al. 2021 (800 kyr), Beyer et al. 2020 (120 kyr, CC BY 4.0) and CHELSA-TraCE21k (21 kyr, 1 km). Global temperature comes from Osman 2021, Tierney 2020 and Snyder 2016. Species ranges are drawn as hulls of dated sites and/or Timmermann et al. 2022 habitat models.

**Shared design.** We recommend a third repo, `time-machine-ui`, served from GitHub Pages at versioned paths (`/time-machine-ui/v1/…`, plus immutable `/v1.2.0/`). It holds the tokens CSS, vanilla ES-module components (timeline, chips, settings sheet, toggles, play button, icons, city search, globe shell) and `products.json`. No build step is needed, matching the current single-file style. A screenshot smoke test runs in the UI repo.

**Navigation.** Both apps live on the same origin, `junhyeopsong.github.io`, so preferences can be shared through namespaced localStorage (`tm.lang`, `tm.city`, `tm.unit`). The existing key `lang` is migrated. A product switcher is fed by `products.json`. Time bridges connect the two apps: below ~7 Ma the continent app offers “see the human story” (and the reverse link sits at the human app's oldest end), carrying `?lang=&city=&age=` in the URL.

**Owner decisions** are listed at the end (§9).

---

## 0. 기존 앱에서 가져올 것 / 바꿀 것 한눈에

| 기능 (기존 앱) | 새 제품에서 | 비고 |
|---|---|---|
| three.js r128 지구본, 대기 림, 별 (천구극 회전) | 그대로 재사용 | 별 회전 속도는 시간 척도(로그)에 맞춰 재조정 |
| 유리(glass) UI, 디자인 토큰 | 공유 저장소로 이동 | §6 |
| 선형 타임라인 + 시대 띠 + 호버 툴팁 | **척도만 교체**(shifted log), 컴포넌트는 공유 | §2 |
| 사건 단축 칩(가장자리 페이드/블러) | 공유 | 사건 수가 많아 칩 그룹화 필요 |
| 사건 핀 + 지도 효과 셰이더(충돌·화산·빙상·온난화·충돌 파문) | 셰이더 엔진 재사용, 효과 종류 추가(이동 경로 화살표, 해수면 하강, 화산 겨울 등) | |
| 도시 추적 (Natural Earth 1,266개) | 그대로 | 판 이동이 없어 좌표 변환 불필요 |
| 평균 기온 카드 (PhanDA) | 데이터 교체 (빙하기 곡선) | PhanDA는 해상도가 너무 거칠다 |
| PaleoDEM, 판 회전 모델, 미래 시뮬레이션 | **사용 안 함** (MVP) | 7 Ma 확장 때 선택 |
| 10개 언어 i18n | 같은 구조, 공유 UI 문자열은 공유 저장소로 | |

---

## 1. 범위와 MVP 제안

### 1.1 제안: 단계별 범위

| 단계 | 기간 | 주제 | 왜 이 순서인가 |
|---|---|---|---|
| **MVP** | 약 300 ka → 1 ka (끝에 "현재" 표시) | *H. sapiens*의 기원과 확산, 같은 시기의 옛 인류, 교잡, 대륙별 도착, 마지막 빙기의 육교 | 사건이 가장 많고(70 ka 이후 집중), 유전체·연대 자료가 가장 풍부하다. 지도 효과(해수면·빙상)가 시각적으로 강하다. 기후·해수면 데이터가 이 기간에 가장 좋다. |
| 2단계 | 약 7 Ma → 300 ka | 사헬란트로푸스부터 오스트랄로피테쿠스, 초기 *Homo*, *H. erectus*의 아프리카 밖 확산, 중기 플라이스토세 호미닌 | 화석 지점이 적고 논쟁이 많다. 기후 격자 자료가 거칠다(≤ 800 ka만 0.5°급). |
| 3단계 (선택) | 12 ka → 1 ka 세부 | 농경의 독립적 기원, 태평양 원양 항해, 그린란드 등 | 이 시기는 "확산" 범위를 넘어 문명사로 커질 위험이 있어 별도로 판단한다. |

MVP 끝점은 **약 1 ka**(뉴질랜드 정착 ≈ 1250–1300 CE)이다. 타임라인 오른쪽 끝에 "현재" 라벨을 둔다. 로그 척도에서도 0을 표현할 수 있는 방법은 §2에서 다룬다.

### 1.2 이야기 흐름 (주요 사건과 연대 범위)

표기: **ka** = 천 년 전, **Ma** = 백만 년 전. "논쟁" 표시는 학계에서 연대나 해석이 갈리는 항목이며, 앱에서도 배지로 보여 준다(§5).

#### MVP (≈ 300 ka → 1 ka)

| # | 사건 | 연대 | 위치 | 지도 효과 아이디어 | 근거 |
|---|---|---|---|---|---|
| 1 | 제벨 이르후드의 초기 *H. sapiens* | 약 315 ± 34 ka | 모로코 | 핀 + "아프리카 전역의 기원(범아프리카)" 반투명 영역 | Hublin et al. 2017 *Nature* [doi:10.1038/nature22336](https://doi.org/10.1038/nature22336); Richter et al. 2017 [doi:10.1038/nature22335](https://doi.org/10.1038/nature22335) — 이 화석을 "*sapiens*"로 부를지는 논쟁 |
| 2 | *H. naledi* (라이징 스타 동굴) | 335–236 ka | 남아공 | 핀 | Dirks et al. 2017 *eLife* [doi:10.7554/eLife.24231](https://doi.org/10.7554/eLife.24231); 의도적 매장·각화 주장(Berger et al. 2023, eLife reviewed preprint)은 **논쟁** [eLife 89102](https://elifesciences.org/reviewed-preprints/89102) |
| 3 | 오모 키비시 I | ≥ 233 ka | 에티오피아 | 핀 | Vidal et al. 2022 *Nature* [doi:10.1038/s41586-021-04275-8](https://doi.org/10.1038/s41586-021-04275-8) |
| 4 | 아피디마 1 (유럽의 초기 *sapiens*?) | 약 210 ka | 그리스 | 점선 경로 "초기 확산 – 이후 사라짐" | Harvati et al. 2019 *Nature* [doi:10.1038/s41586-019-1376-z](https://doi.org/10.1038/s41586-019-1376-z) — 동정(同定) **논쟁** |
| 5 | 미슬리야 위턱뼈 | 194–177 ka | 이스라엘 | 점선 경로 | Hershkovitz et al. 2018 *Science* [doi:10.1126/science.aap8369](https://doi.org/10.1126/science.aap8369) |
| 6 | 데니소바인 — 바이시야 동굴(샤허) 아래턱 | ≥ 160 ka | 티베트고원 | 고지대 핀 | Chen et al. 2019 *Nature* [doi:10.1038/s41586-019-1139-x](https://doi.org/10.1038/s41586-019-1139-x) |
| 7 | 하얼빈 두개골 ("용인", *Homo longi*) → 데니소바인으로 동정 | ≥ 146 ka | 중국 헤이룽장 | 핀 + "이름 논쟁" 배지 | Ji et al. 2021 *The Innovation* [doi:10.1016/j.xinn.2021.100132](https://doi.org/10.1016/j.xinn.2021.100132); Fu et al. 2025 단백질(*Science*)·mtDNA(*Cell*) — 요약 [Science News](https://www.sciencenews.org/article/skull-first-denisovan-human-cousin). 오염 가능성 비판이 있어 **논쟁** |
| 8 | 플로레스인 (*H. floresiensis*) | 골격 약 100–60 ka, 석기 약 190–50 ka | 인도네시아 플로레스 | 섬 핀 | Sutikna et al. 2016 *Nature* [doi:10.1038/nature17179](https://doi.org/10.1038/nature17179) |
| 9 | 루손인 (*H. luzonensis*) | ≥ 50 ka (일부 시료 ≥ 67 ka) | 필리핀 칼라오 동굴 | 섬 핀 | Détroit et al. 2019 *Nature* [doi:10.1038/s41586-019-1067-9](https://doi.org/10.1038/s41586-019-1067-9) |
| 10 | 마지막 *H. erectus* (응간동) | 117–108 ka | 자와 | 핀이 서서히 사라짐 | Rizal et al. 2019 *Nature* [doi:10.1038/s41586-019-1863-2](https://doi.org/10.1038/s41586-019-1863-2) |
| 11 | 스훌·카프제 — 레반트의 초기 *sapiens* | 약 130–90 ka | 이스라엘 | 점선 경로 | Grün et al. 2005 *J. Hum. Evol.* [doi:10.1016/j.jhevol.2005.04.006](https://doi.org/10.1016/j.jhevol.2005.04.006) |
| 12 | 블롬보스 동굴 — 황토 판화·상징 행동 | 약 100–73 ka | 남아공 | 핀 | Henshilwood et al. 2018 *Nature* [doi:10.1038/s41586-018-0514-3](https://doi.org/10.1038/s41586-018-0514-3) |
| 13 | 데니(네안데르탈인 × 데니소바인 1세대 혼혈) | 약 90 ka | 알타이 데니소바 동굴 | 두 범위가 겹치는 곳에 반짝임 | Slon et al. 2018 *Nature* [doi:10.1038/s41586-018-0455-x](https://doi.org/10.1038/s41586-018-0455-x) |
| 14 | 토바 초분화 | 약 74 ka | 수마트라 | **화산 효과(기존 셰이더 2 재사용)** + 화산재 범위 | Kappelman et al. 2024 *Nature* [doi:10.1038/s41586-024-07208-3](https://doi.org/10.1038/s41586-024-07208-3) — 인류 "병목" 원인설은 **논쟁**(대체로 부정적) |
| 15 | 주 출(出)아프리카 확산 | 약 60–45 ka | 아프리카 → 유라시아 | 흐르는 경로 화살표(남부 해안 경로 / 북부 경로) | Sümer et al. 2024 *Nature* [doi:10.1038/s41586-024-08420-x](https://doi.org/10.1038/s41586-024-08420-x) (비아프리카인 공통 조상 집단 기준); 경로는 **논쟁** |
| 16 | 네안데르탈인과의 교잡 (단일 주요 사건) | 약 49–45 ka | 서아시아/유럽 | 두 범위가 겹치는 곳에 반짝임 | Sümer et al. 2024 *Nature* (위); Iasi et al. 2024 *Science* [doi:10.1126/science.adq3010](https://doi.org/10.1126/science.adq3010) |
| 17 | 사훌(오스트레일리아·뉴기니) 도착 | 약 65 ka (마제드베베) vs 약 50–47 ka | 아넘랜드 | 바다를 건너는 점선 + 순다·사훌 육교 | Clarkson et al. 2017 *Nature* [doi:10.1038/nature22968](https://doi.org/10.1038/nature22968) vs O'Connell et al. 2018 *PNAS* [doi:10.1073/pnas.1808385115](https://doi.org/10.1073/pnas.1808385115) — **논쟁**: 두 연대를 모두 보여 준다 |
| 18 | 술라웨시 동굴 벽화 | ≥ 51.2 ka | 인도네시아 | 핀 | Oktaviana et al. 2024 *Nature* [doi:10.1038/s41586-024-07541-7](https://doi.org/10.1038/s41586-024-07541-7) |
| 19 | 유럽의 초기 *sapiens* (만드랭 / 바초 키로 / 라니스) | 약 54 ka (논쟁) / 약 46–44 ka / 약 47–45 ka | 프랑스 / 불가리아 / 독일 | 핀 | Slimak et al. 2022 *Sci. Adv.* [doi:10.1126/sciadv.abj9496](https://doi.org/10.1126/sciadv.abj9496); Hublin et al. 2020 *Nature* [doi:10.1038/s41586-020-2259-z](https://doi.org/10.1038/s41586-020-2259-z); Mylopotamitaki et al. 2024 *Nature* [doi:10.1038/s41586-023-06923-7](https://doi.org/10.1038/s41586-023-06923-7) |
| 20 | 우스트이심 — 가장 오래된 고품질 *sapiens* 게놈 중 하나 | 약 45 ka | 서시베리아 | aDNA 핀(별도 아이콘) | Fu et al. 2014 *Nature* [doi:10.1038/nature13810](https://doi.org/10.1038/nature13810) |
| 21 | 네안데르탈인의 사라짐 | 약 41–39 ka (지역차, 지브롤터 늦은 생존설은 논쟁) | 유럽 | 범위가 서서히 옅어짐 | Higham et al. 2014 *Nature* [doi:10.1038/nature13621](https://doi.org/10.1038/nature13621) |
| 22 | 야나 RHS — 북극권 시베리아 | 약 32 ka | 동시베리아 | 핀 | Sikora et al. 2019 *Nature* [doi:10.1038/s41586-019-1279-z](https://doi.org/10.1038/s41586-019-1279-z) |
| 23 | 최종 빙기 최성기(LGM) | 약 26–19 ka | 전 지구 | **빙상 효과(기존 셰이더 3)** + 해수면 −120 m 내외 → 베링기아·순다·사훌·도거랜드 | Clark et al. 2009 *Science* [doi:10.1126/science.1172873](https://doi.org/10.1126/science.1172873) |
| 24 | 아메리카 도착 — 화이트샌즈 발자국 | 약 23–21 ka | 미국 뉴멕시코 | 베링기아 → 남쪽 점선 | Bennett et al. 2021 *Science* [doi:10.1126/science.abg7586](https://doi.org/10.1126/science.abg7586); Pigati et al. 2023 [doi:10.1126/science.adh5007](https://doi.org/10.1126/science.adh5007) — **논쟁**(연대 시료) |
| 25 | 몬테베르데 | 약 14.5 ka | 칠레 | 핀 | Dillehay et al. 2015 *PLOS ONE* [doi:10.1371/journal.pone.0141923](https://doi.org/10.1371/journal.pone.0141923) |
| 26 | 해수면 상승, 도거랜드·베링 육교 침수 | 약 14–8 ka | 북해·베링해 | 해수면 애니메이션 | Spratt & Lisiecki 2016 (§3); Lambeck et al. 2014 *PNAS* [doi:10.1073/pnas.1411762111](https://doi.org/10.1073/pnas.1411762111) |
| 27 | 비옥한 초승달 지대의 농경 시작 (선택) | 약 11.5–10 ka | 서아시아 | 핀 | Zeder 2011 *Curr. Anthropol.* [doi:10.1086/659307](https://doi.org/10.1086/659307) |
| 28 | 라피타 — 원격 오세아니아 진입 | 약 3.0–2.8 ka | 바누아투·통가 | 바다 위 점선 | Burley, Weisler & Zhao 2012 *PLOS ONE* [doi:10.1371/journal.pone.0048769](https://doi.org/10.1371/journal.pone.0048769) (통가 첫 정착 U/Th 연대) |
| 29 | 동폴리네시아 정착 → 뉴질랜드 | 약 1025–1120 CE → 약 1250–1300 CE | 소시에테 제도 → 아오테아로아 | 마지막 화살표, 타임라인 끝 | Wilmshurst et al. 2011 *PNAS* [doi:10.1073/pnas.1015876108](https://doi.org/10.1073/pnas.1015876108) |

#### 2단계 (≈ 7 Ma → 300 ka) — 미리 정해 둘 후보

| 사건 | 연대 | 근거 / 논쟁 |
|---|---|---|
| 사헬란트로푸스 차덴시스 | 약 7 Ma | Brunet et al. 2002 *Nature* [doi:10.1038/nature00879](https://doi.org/10.1038/nature00879); 두 발 걷기 여부는 **논쟁**: Daver et al. 2022 *Nature* [doi:10.1038/s41586-022-04901-z](https://doi.org/10.1038/s41586-022-04901-z) vs Macchiarelli et al. 2020 *J. Hum. Evol.* [doi:10.1016/j.jhevol.2020.102898](https://doi.org/10.1016/j.jhevol.2020.102898) |
| 메시나 염분 위기 (지중해 마름) — **대륙 앱과 겹치는 다리 사건** | 5.97–5.33 Ma | Krijgsman et al. 1999 *Nature* [doi:10.1038/23231](https://doi.org/10.1038/23231) |
| 아르디피테쿠스 라미두스 | 약 4.4 Ma | White et al. 2009 *Science* [doi:10.1126/science.1175802](https://doi.org/10.1126/science.1175802) |
| 라에톨리 발자국 | 약 3.66 Ma | Leakey & Hay 1979 *Nature* [doi:10.1038/278317a0](https://doi.org/10.1038/278317a0) |
| "루시" *Australopithecus afarensis* | 약 3.2 Ma | Johanson & White 1979 *Science* [doi:10.1126/science.104384](https://doi.org/10.1126/science.104384) |
| 로메크위 3 석기 | 약 3.3 Ma | Harmand et al. 2015 *Nature* [doi:10.1038/nature14464](https://doi.org/10.1038/nature14464) — 의도적 제작 여부는 **논쟁** |
| 가장 이른 *Homo* (LD 350-1) | 약 2.8 Ma | Villmoare et al. 2015 *Science* [doi:10.1126/science.aaa1343](https://doi.org/10.1126/science.aaa1343) |
| *H. habilis* | 약 2.3–1.6 Ma | Spoor et al. 2015 *Nature* [doi:10.1038/nature14224](https://doi.org/10.1038/nature14224) |
| 상천(上陈) 석기 — 아프리카 밖 가장 이른 흔적 | 약 2.1 Ma | Zhu et al. 2018 *Nature* [doi:10.1038/s41586-018-0299-4](https://doi.org/10.1038/s41586-018-0299-4) |
| 드리몰렌 *H. erectus* | 약 2.04 Ma | Herries et al. 2020 *Science* [doi:10.1126/science.aaw7293](https://doi.org/10.1126/science.aaw7293) |
| 드마니시 | 약 1.85–1.77 Ma | Ferring et al. 2011 *PNAS* [doi:10.1073/pnas.1106638108](https://doi.org/10.1073/pnas.1106638108) |
| 아슐리안 주먹도끼 | 약 1.76 Ma | Lepre et al. 2011 *Nature* [doi:10.1038/nature10372](https://doi.org/10.1038/nature10372) |
| 원더워크 동굴의 불 사용 흔적 | 약 1 Ma | Berna et al. 2012 *PNAS* [doi:10.1073/pnas.1117620109](https://doi.org/10.1073/pnas.1117620109) |
| 윈셴 2 두개골 → *H. longi* 계통 (깊은 분기) | 약 1 Ma | Feng et al. 2025 *Science* [doi:10.1126/science.ado9202](https://doi.org/10.1126/science.ado9202) — 분기 연대는 **논쟁** |
| 시마 데 로스 우에소스 (초기 네안데르탈 계통) | 약 430 ka | Meyer et al. 2016 *Nature* [doi:10.1038/nature17405](https://doi.org/10.1038/nature17405) |

---

## 2. 타임라인 설계 (≈ 7 Ma → ≈ 1 ka, 사건은 최근 70 kyr에 몰림)

### 2.1 문제

- 선형으로 7 Ma를 그리면 최근 70 kyr은 폭의 **1 %**, 최근 25 kyr은 **0.36 %**밖에 되지 않는다. 휴대폰에서는 1–2 px이다.
- MVP 범위(300 ka)만 선형으로 해도 최근 25 kyr은 폭의 8 %라서, 아메리카·태평양 사건이 한데 몰린다.
- 오너는 기존 앱에서 **타임라인 확대(zoom)를 거절**했다. 따라서 "한 줄짜리 고정 타임라인 한 개, 손가락으로 끌면 바로 그 시점"이라는 기존 상호작용을 지키는 것이 전제다.

### 2.2 선택지

폭 비율은 7 Ma 전체 범위 기준으로 계산했다(c = 5 kyr).

| 안 | 사상 x(age) | 최근 70 kyr 폭 | 장점 | 단점 |
|---|---|---|---|---|
| **A. 순수 로그** | log(age), 1 ka에서 끝 | 7 Ma→1 ka의 3.85 자릿수 중 1.85 → **약 48 %** | 자릿수마다 같은 폭. 과학적으로 익숙하다. | 0(현재)을 표시할 수 없다. 최근 몇 천 년이 지나치게 넓다(1–10 ka가 26 %). 눈금이 직관적이지 않다. |
| **B. 구간별 선형 (segmented)** | 예: 7–1 Ma 20 % · 1 Ma–300 ka 15 % · 300–70 ka 25 % · 70 ka–0 40 % | 40 % (설정값) | 구간 안에서는 선형이라 읽기 쉽다. 구간 경계를 시대 띠처럼 보여 줄 수 있다. | 경계에서 속도가 꺾여 재생이 덜컥거린다. 경계 위치가 자의적으로 보인다. |
| **C. 이동 로그 (shifted log) — 추천** | log(age + c) | c=5 kyr: **37 %**, (최근 25 kyr 25 %, 최근 5 kyr 10 %, 7–1 Ma 27 %) | 연속적이고 부드럽다. **0을 포함한다.** c 하나로 균형을 맞춘다. 재생 속도가 자연스럽게 "최근일수록 천천히" 바뀐다. | 눈금 간격이 불균등하다(시대 띠·눈금 라벨로 보완). c 값 설명이 필요할 수 있다. |
| D. asinh 척도 | asinh(age / c) | C와 거의 같다 | 음수(미래)까지 매끄럽다 | 미래가 필요 없으므로 이점이 없다 |
| E. 개요 + 상세 두 줄 | 위: 전체, 아래: 선택 구간 선형 | — | 선형의 정확함 | 사실상 **확대**다. 오너가 거절한 방식과 같다. 화면을 더 차지한다. |
| F. MVP만 선형 300 ka | 선형 | 23 % | 기존 코드 그대로 | 최근 사건이 몰린다. 2단계(7 Ma)에서 결국 척도를 바꿔야 한다. |

MVP(300 ka → 0)에 C를 쓰면: c=5 kyr일 때 최근 70 kyr 66 %, 최근 25 kyr 44 %이고, c=10 kyr일 때 최근 70 kyr 60 %, 최근 25 kyr 36 %이다. **추천: MVP는 c = 10 kyr로 시작하고 목업에서 조정.** 7 Ma로 넓힐 때는 c = 5 kyr로 바꾼다.

### 2.3 추천안 세부

- **사상:** `x = (ln(age + c) − ln(c)) / (ln(AGE_MAX + c) − ln(c))`. 왼쪽이 과거, 오른쪽이 현재이다(기존 앱과 같은 방향).
- **시대 띠:** ICS 색상의 지질 시대 띠를 쓴다(기존 앱의 period bands와 같은 컴포넌트, 같은 출처). 플라이오세 · 젤라시안 · 칼라브리안 · 치바니안 · 후기 플라이스토세 · 홀로세. 출처: [ICS 국제 연대층서표](https://stratigraphy.org/chart). 로그 척도에서 홀로세(11.7 ka)도 충분히 넓게 보인다.
- **보조 띠 (얇은 줄):** 빙기/간빙기(MIS) 줄무늬. 출처는 LR04 벤틱 δ¹⁸O 스택, Lisiecki & Raymo 2005 [doi:10.1029/2004PA001071](https://doi.org/10.1029/2004PA001071) (NOAA 공개). 고고학 시대(구석기 등)는 지역마다 달라서 전 지구 띠로 쓰지 않는다.
- **눈금:** 1·2·5 계열(1 ka, 2 ka, 5 ka, 10 ka, 20 ka, 50 ka …)을 쓴다. 로그 척도에서는 거의 등간격이라 읽기 쉽다.
- **재생:** 화면 속도를 일정하게 유지한다(= 시간은 과거로 갈수록 빨리 흐름). 사건에 닿으면 기존 "playback tour"처럼 멈추고 돌려 본다. 속도 3단계는 그대로 둔다.
- **◀ ▶ 단계 이동:** "100만 년씩" 대신 **다음 눈금(1·2·5 계열)** 또는 **다음 사건**으로 이동한다. 기존 "가는 길의 사건에서 먼저 멈춤" 규칙을 유지한다.
- **별 회전:** 시간 변화량 대신 **타임라인 위치 변화량(x)**에 비례해 돌린다. 로그 척도에서도 화면상 체감 속도가 일정하다.
- **불확실한 연대:** 사건 점 대신 **구간 막대**(예: 마제드베베 65 ka ↔ 50 ka)로 그린다. §5.

### 2.4 확대 거절과의 관계

C안은 "확대 없이 한 줄"이라는 오너의 결정을 지키면서 최근 사건에 폭을 준다. 사용자가 조작하는 것은 여전히 막대 하나뿐이다. 선택지 E(개요+상세)는 같은 문제를 확대로 푸는 방식이라 추천하지 않는다.

**목업 제안:** C(c=5k / 10k / 20k) 세 가지와 B를 같은 사건 세트로 그려 휴대폰·데스크톱에서 비교한다.

### 2.5 결정 (2026-11-11, 오너)

목업 [`mockup-timeline-scale.png`](mockup-timeline-scale.png)(A 선형 · B 구간별 · C1 이동 로그 c=10 kyr · C2 c=5 kyr)을 보고 정했다.

- **A(선형)와 C1(이동 로그, c = 10 kyr) 두 가지를 모두 제공하고, 설정 창에서 사용자가 고른다. 기본값은 A(선형).**
- 설정 항목(안): "타임라인 눈금" — 분절 컨트롤 `선형 | 로그`. 선택은 공유 설정 키(예: `tm.scale`)에 저장한다. 7 Ma로 넓히는 2단계에서도 같은 두 선택지를 유지한다(C1의 c 값은 그때 다시 목업으로 정한다).
- 확대 없음 원칙은 그대로다. 두 눈금 모두 한 줄, 전체 범위.

구현 시 맞춰야 할 점:
- 타임라인 컴포넌트는 `age ↔ x` 사상 함수를 바꿔 끼울 수 있게 만든다(시대 띠·빙기 줄·눈금·사건 점·막대·손잡이·hover 툴팁이 모두 같은 함수를 쓴다). 공용 UI(`time-machine-ui`)의 타임라인에 `scale` 옵션으로 넣으면 대륙 앱은 선형만 쓰면 된다.
- 눈금 라벨: 선형은 5만 년 간격, 로그는 1·2·5 계열.
- 재생: 선형은 지금 앱처럼 시간 속도 일정. 로그는 화면 속도 일정(과거일수록 시간이 빨리 흐름). 속도 3단계 이름은 같게 둔다.
- 별 회전: 시간 변화량 기준(선형)과 x 변화량 기준(로그) 중 어떤 쪽이 자연스러운지 프로토타입에서 확인한다.
- 기본값이 선형이라 최근 7만 년(폭 23%)에 이동·도착 사건이 몰린다. 겹치는 사건 점은 hover/탭 목록으로 펼치고, 바로가기 칩으로 보완한다. 설정의 로그 눈금을 발견하기 쉽도록 첫 방문 안내(힌트)에 한 줄 넣는 것을 검토한다.

---

## 3. 지도 모델

### 3.1 기본 방식: 현재 지형 + 해수면 곡선 + 빙상

1. **현재 지형/해저 지형:** ETOPO 2022 (15″/30″/60″, GeoTIFF/NetCDF, **CC0-1.0**) — [doi:10.25921/fd45-gt74](https://doi.org/10.25921/fd45-gt74), [NCEI 제품 페이지](https://www.ncei.noaa.gov/products/etopo-global-relief-model). 기존 앱처럼 약 0.1° 텍스처(3600×1800)를 쓰고, 고도를 16비트로 PNG RGB에 담는다. 셰이더에서 `land = elev > SL(t)`로 판정한다("욕조 채우기").
2. **해수면 곡선:** Spratt & Lisiecki 2016, 0–798 ka (PCA 스택, 1 kyr 간격, 표준편차 포함). *Clim. Past* [doi:10.5194/cp-12-1079-2016](https://doi.org/10.5194/cp-12-1079-2016). 데이터는 [NOAA 19982](https://www.ncei.noaa.gov/access/paleo-search/study/19982)에 있다([텍스트 파일](https://www.ncei.noaa.gov/pub/data/paleo/contributions_by_author/spratt2016/spratt2016-noaa.txt), NOAA 메타데이터상 **CC0**). 2025년 개정판 v2가 [PANGAEA doi:10.1594/PANGAEA.979830](https://doi.org/10.1594/PANGAEA.979830)에 있다(라이선스는 PANGAEA 기본 CC BY 4.0으로 보이나 **확인 필요**). 800 ka보다 오래된 구간에는 LR04 기반 해수면 환산(예: Rohling et al. 2014 *Nature* [doi:10.1038/nature13230](https://doi.org/10.1038/nature13230))을 검토한다.
3. **26 ka → 0 보정:** ICE-6G_C (VM5a) 고지형 + 빙상 두께, 1°/10′ 격자, 0.5–1 kyr 간격. [PMIP4 배포 페이지](https://pmip4.lsce.ipsl.fr/doku.php/data:ice_ice6g_c), [Peltier 그룹](https://www.atmosp.physics.utoronto.ca/~peltier/data.php). 논문은 Peltier, Argus & Drummond 2015 *JGR* [doi:10.1002/2014JB011176](https://doi.org/10.1002/2014JB011176). 단순 욕조 방식이 놓치는 **지각 평형(GIA)** 효과를 반영한다(허드슨만·발트해, 빙상 주변 융기/침강). 방법은 `elev(t) = ETOPO + (Topo_ICE6G(t) − Topo_ICE6G(0))`이다.
4. **26 ka보다 오래된 빙상:**
   - Batchelor et al. 2019 *Nat. Commun.* — 제4기 북반구 빙상 경계(MIS별 최소/최적/최대) [doi:10.1038/s41467-019-11601-2](https://doi.org/10.1038/s41467-019-11601-2) (형상 파일 공개, 라이선스 **확인 필요**)
   - Gowan et al. 2021 *Nat. Commun.* PaleoMIST 1.0 (80 ka → 0, 2.5 kyr 간격) [doi:10.1038/s41467-021-21469-w](https://doi.org/10.1038/s41467-021-21469-w) (**확인 필요**)
   - 그 이전 구간: "해수면이 같은 시기 = 비슷한 빙상"이라는 아날로그 방식으로 위 경계를 보간한다(과학적 단순화이므로 정보 패널에 명시).
5. **표시 요소:** 육교(베링기아·순다·사훌·도거랜드)는 이름 라벨로 표시하고, 해수면 값은 기존 앱 "해수면" 표시처럼 미터로 보여 준다. 빙상은 기존 셰이더 효과 3의 하얀 빙상 표현을 재사용한다.

### 3.2 판 운동이 필요한가?

- **≤ 1 Ma: 필요 없다.** 빠른 판(약 5–10 cm/yr)도 1 Myr에 50–100 km, 300 kyr에 15–30 km밖에 움직이지 않는다. 0.1° 텍스처(약 11 km)에서 거의 보이지 않으며, 해수면 효과가 훨씬 크다.
- **7 Ma 확장 시: 선택 사항이다.** 최대 수백 km 이동이 생기고, 파나마 지협 형성(약 3 Ma, O'Dea et al. 2016 *Sci. Adv.* [doi:10.1126/sciadv.1600883](https://doi.org/10.1126/sciadv.1600883))과 메시나 위기 같은 지형 변화가 있다. 이때는 기존 앱의 **PALEOMAP 회전 + PaleoDEM 0/5 Ma 프레임**(CC BY 4.0, [Zenodo 5460860](https://zenodo.org/records/5460860))을 같은 엔진으로 읽어 쓰면 된다. 2단계에서 결정한다.
- **도시 추적:** 판 이동이 없으므로 현재 좌표를 그대로 쓴다(기존 앱의 plate-id 처리가 필요 없다).

### 3.3 알려 둘 한계

욕조 방식은 퇴적·침식(예: 하천 삼각주), 국지적 지각 변동을 반영하지 못한다. 26 ka보다 오래된 구간은 GIA 보정이 없어 해안선 오차가 수십 m 수준이다. 이 점을 정보 패널의 "지도는 어떻게 만들었나요?"에 적는다.

---

## 4. 데이터 목록

| 데이터 | 내용 | 해상도 / 범위 | 형식 | 라이선스 | 공개 정적 사이트 재배포 |
|---|---|---|---|---|---|
| **ETOPO 2022** | 육지·해저 지형 | 15″–60″, 현재 | GeoTIFF, NetCDF | **CC0-1.0** ([NCEI](https://doi.org/10.25921/fd45-gt74)) | ✅ 가능 (가공 텍스처) |
| **Spratt & Lisiecki 2016** 해수면 스택 | 전 지구 평균 해수면 ± σ | 1 kyr, 0–798 ka | TXT | NOAA: **CC0** ([NOAA 19982](https://www.ncei.noaa.gov/access/paleo-search/study/19982)) / v2: PANGAEA (확인 필요) | ✅ |
| **ICE-6G_C (VM5a)** | 고지형, 빙상 두께, 육지/바다 마스크 | 10′·1°, 26 ka → 0 | NetCDF | 명시 라이선스 **없음**, 인용 요구 ([PMIP4](https://pmip4.lsce.ipsl.fr/doku.php/data:ice_ice6g_c)) | ⚠️ 가공된 저해상도 마스크만 배포 + 인용. 원자료 재배포는 피하고, 필요하면 Peltier 그룹에 문의 |
| **Batchelor et al. 2019** 빙상 경계 | MIS별 북반구 빙상 윤곽 | 벡터, 약 2.6 Ma → 0의 주요 빙기 | Shapefile | 논문 CC BY 4.0, 데이터 **확인 필요** ([doi](https://doi.org/10.1038/s41467-019-11601-2)) | ⚠️ 확인 후 |
| **ROAD (ROCEEH Out of Africa Database)** | 3 Ma–20 ka 고고·고인류 지점, 층위, 연대, 석기 문화, 인류 화석 | 지점 수만 건 | 웹 질의, R 패키지 [`roadDB`](https://cran.r-project.org/web/packages/roadDB/readme/README.html) | **CC BY-SA 4.0** (roadDB README 기준, 인용: Kandel et al. 2023 *PLOS ONE* [doi:10.1371/journal.pone.0289513](https://doi.org/10.1371/journal.pone.0289513)) | ✅ 가능. 단, 가공 JSON도 **CC BY-SA 4.0**으로 공개해야 함(코드 라이선스와 분리) |
| **Paleobiology Database (PBDB)** | 호미닌 화석 산출 기록(분류군·좌표·연대) | 전 시대 | CSV/JSON API | **CC BY 4.0** ([PBDB 이용 안내](https://paleobiodb.org/#/faq)) | ✅ |
| **AADR (Allen Ancient DNA Resource)** | 고대 인류 게놈 1만여 개체의 메타데이터(위치·연대·논문) + 유전자형 | 개체 단위, v54+ | `.anno` TSV + EIGENSTRAT | Harvard Dataverse [doi:10.7910/DVN/FFIDCW](https://doi.org/10.7910/DVN/FFIDCW), 라이선스 **확인 필요**, 인용 요구 (Mallick et al. 2024 *Sci. Data* [doi:10.1038/s41597-024-03031-7](https://doi.org/10.1038/s41597-024-03031-7)) | ⚠️ 유전자형은 사용하지 않는다. **선별한 약 100–300개 개체의 메타데이터**(위치·연대·원 논문 DOI)만, 원 논문 인용과 함께 쓴다 |
| **Krapp et al. 2021** 기후 | 월별 기온·강수, 생물기후 변수 | 0.5°, 1 kyr, **800 ka → 0** | NetCDF (R `pastclim`) | **확인 필요** (*Sci. Data* [doi:10.1038/s41597-021-01009-3](https://doi.org/10.1038/s41597-021-01009-3)) | ⚠️ 확인 후. MVP 300 ka 전 구간을 덮는 유일한 0.5° 자료 |
| **Beyer, Krapp & Manica 2020** | 기온·강수·생물기후 17종·NPP·**바이옴** | 0.5°, 1–2 kyr, **120 ka → 0** | NetCDF | **CC BY 4.0** (pastclim 기준) — *Sci. Data* [doi:10.1038/s41597-020-0552-1](https://doi.org/10.1038/s41597-020-0552-1) | ✅ (가공 텍스처) |
| **CHELSA-TraCE21k** | 기온·강수·빙하·생물기후 | 30″ (약 1 km), **100년 간격, 21 ka → 0** | GeoTIFF | 논문 CC BY 4.0, 데이터 **확인 필요** — Karger et al. 2023 *Clim. Past* [doi:10.5194/cp-19-439-2023](https://doi.org/10.5194/cp-19-439-2023), [EnviDat](https://www.envidat.ch/) | ⚠️ 확인 후. 너무 커서 약 0.1–0.25°로 줄여 쓴다 |
| **Timmermann et al. 2022** 인류 종별 서식 적합도 | *H. sapiens*·네안데르탈·하이델베르겐시스·에렉투스 서식 확률 지도 | 약 1°, 2 Ma → 0 | NetCDF | **확인 필요** — *Nature* [doi:10.1038/s41586-022-04600-9](https://doi.org/10.1038/s41586-022-04600-9), [IBS 기후물리연구단 데이터](https://climatedata.ibs.re.kr/) (부산 IBS — 한국 연구단이라 협조 요청이 쉬울 수 있음) | ⚠️ 확인 후. "종 분포"를 모델 기반으로 보여 줄 유일한 자료 |
| **전 지구 평균 기온 (빙하기 곡선)** | GMST 편차 | 아래 참조 | CSV | 각각 확인 | ✅/⚠️ |
| └ Osman et al. 2021 | 24 ka → 0, 자료 동화 | 200년 | | *Nature* [doi:10.1038/s41586-021-03984-4](https://doi.org/10.1038/s41586-021-03984-4) (NOAA 공개) | ✅ |
| └ Tierney et al. 2020 | LGM 냉각 −6.1 °C (−6.5~−5.7) | LGM 한 시점 | | *Nature* [doi:10.1038/s41586-020-2617-x](https://doi.org/10.1038/s41586-020-2617-x) | 숫자만 인용 |
| └ Snyder 2016 | 2 Ma → 0 GAST | 1 kyr | | *Nature* [doi:10.1038/nature19798](https://doi.org/10.1038/nature19798) — 진폭 과대 **비판**: Schmidt 2017 (확인 필요) | ⚠️ 정보 패널에 비판 명시 |
| **LR04 벤틱 스택** | δ¹⁸O (빙기 주기) | 1–5 kyr, 5.3 Ma → 0 | TXT | NOAA 공개 — [doi:10.1029/2004PA001071](https://doi.org/10.1029/2004PA001071) | ✅ (MIS 띠) |
| **Natural Earth** 도시 | 기존 앱과 동일 | | | Public domain | ✅ |
| **Lucide 아이콘** | | | SVG | ISC | ✅ |
| **three.js r128** | | | | MIT | ✅ |

### 4.1 종 분포 범위(species ranges)를 어떻게 그릴까

공인된 "옛 인류 분포 지도" 데이터셋은 없다. 다음 셋 중에서 고른다(목업에서 비교):

1. **지점 기반 외곽선:** 해당 시간창(±σ)에 있는 ROAD/PBDB 지점의 볼록 껍질(convex hull) + 완충 거리 → 흐릿한 경계. 정직하지만 듬성하다.
2. **모델 기반:** Timmermann 2022 서식 적합도(확률이 높을수록 진하게). 매끄럽지만 "모델"임을 명시해야 한다.
3. **손으로 그린 개략도:** 문헌 지도를 참고해 시대별 3–6개 폴리곤만 그린다. 가장 가볍지만 출처 표기가 어렵다.

**추천:** 1(기본) + 2(설정에서 켜기)이다. 3은 쓰지 않는다.

### 4.2 용량 예산 (기존 앱 패턴 유지: 필요할 때 프레임 가져오기)

- 지형 텍스처 1장(0.1°, 16비트 RGB PNG) ≈ 6–10 MB → 휴대폰용 0.25° ≈ 1–2 MB.
- 해수면/기온 곡선: 수십 KB.
- 바이옴/기후 0.5° 프레임(720×360, 8비트 PNG) ≈ 50–150 KB × 약 150 프레임 → 필요할 때 가져온다.
- 지점·사건 JSON: 약 200–500 KB.

---

## 5. 불확실성, 학계 논쟁, 이름 정책, 민감성 가이드

### 5.1 불확실성 표시 원칙

- **연대 = 구간이다.** 모든 사건과 지점에 `age_min`, `age_max`, `age_best?`, `method`(U-series, OSL, ¹⁴C, ESR, 유전체 시계), `source_doi`를 둔다. 타임라인에는 막대로, 지도에는 구간 동안 핀이 서서히 나타나고 사라지게 그린다.
- **논쟁 배지:** 해석이 갈리는 사건에 "논쟁" 칩을 붙이고, 툴팁에 양쪽 주장과 출처 2개 이상을 보여 준다(위 표의 **논쟁** 항목: 제벨 이르후드의 분류, naledi 매장, 아피디마, 하얼빈 이름, 토바 병목, 이동 경로, 마제드베베, 만드랭, 화이트샌즈, 사헬란트로푸스 보행, 로메크위, 윈셴 분기 연대, Snyder 기온 곡선).
- **이동 경로는 점선이다.** "이 길로 갔다"가 아니라 "가능한 경로"임을 시각적으로 구분한다. 화살표 끝은 확인된 가장 이른 지점에서 멈춘다.
- **"가장 이른" 대 "주장된":** 설정에서 "널리 인정된 연대만 / 논쟁 중인 연대도"를 토글로 고르게 하는 안을 제안한다(오너 결정 항목).
- **업데이트 정책:** 새 논문이 자주 나오는 분야다(2024–2025년에만 교잡 연대, 하얼빈, 윈셴 등). `events.json`에 `reviewed: 2026-11` 필드를 두고 정보 패널에 "마지막 검토일"을 표시한다. 정정 요청은 기존 앱처럼 이메일과 GitHub 이슈로 받는다.

### 5.2 이름 정책 (종 vs 아종 vs 집단)

| 대상 | 화면 표기 (한국어 / 영어) | 학명 표기 | 메모 |
|---|---|---|---|
| 네안데르탈인 | 네안데르탈인 / Neanderthals | *Homo neanderthalensis* (종으로 보는 견해가 다수, 일부는 *H. sapiens neanderthalensis*) | 정보 패널에 아종 견해를 한 줄 적는다 |
| 데니소바인 | 데니소바인 / Denisovans | 학명 없음(유전체로 정의된 집단). 하얼빈 연구 이후 *H. longi* 제안 | "데니소바인 (*H. longi*로 부르자는 제안도 있음)" |
| 중기 플라이스토세 호미닌 | 하이델베르크인 계열 / *H. heidelbergensis* s.l. | *H. heidelbergensis*, *H. rhodesiensis*, *H. bodoensis*(Roksandic et al. 2021 [doi:10.1002/evan.21929](https://doi.org/10.1002/evan.21929)) | 가장 혼란스러운 분류다. 넓은 의미(s.l.)라고 명시한다 |
| *H. erectus* | 호모 에렉투스 | *H. erectus* (아시아), *H. ergaster*(아프리카 초기)는 별칭 | |
| 초기 *H. sapiens* | 초기 현생인류 / early *H. sapiens* | 제벨 이르후드 등은 "*sapiens* 계통의 초기 형태" | "해부학적 현생인류" 같은 용어는 피한다 |
| 플로레스인, 루손인, 날레디 | 고유 이름 + 학명 | 종으로 표기 | |

규칙: ① 일상 이름을 크게, 학명은 기울임으로 작게 쓴다. ② 학명이 논쟁 중이면 "논쟁" 배지를 붙인다. ③ 10개 언어 이름은 각 언어 위키백과·교과서 표기를 따른다(번역 시 표기 출처를 기록).

### 5.3 민감성 가이드 (인종 범주를 쓰지 않음)

- **인종 범주를 쓰지 않는다.** 사람 집단은 "어디·언제의 사람들"(예: "약 45 ka 서시베리아의 사람들", "최종 빙기 베링기아의 사람들")이나 유전학 문헌의 집단명(예: Ancient North Eurasians)으로만 부른다. 피부색·두개골 형태로 집단을 분류하거나 칠하지 않는다.
- **위계·진보 서사를 피한다.** "원시적/진화된", "열등/우월", 일렬 행진(march of progress) 이미지를 쓰지 않는다. 계통은 나무가 아니라 **얽힌 그물**(교잡)로 보여 준다.
- **현재 집단과 직접 연결하지 않는다.** "○○인의 조상" 같은 문장보다 "이 사람들의 유전적 흔적은 오늘날 여러 지역 사람들에게 남아 있다"처럼 쓴다. 네안데르탈·데니소바 비율은 지역 평균 범위로만 적고, 국가·민족별 순위는 매기지 않는다.
- **원주민 관점을 존중한다.** 오스트레일리아·아메리카·태평양의 "도착 연대"는 과학적 추정이며, 그 땅의 원주민 공동체가 자신들의 역사에 대해 지닌 관점(예: "언제나 여기 있었다")이 있다는 점을 정보 패널에 적는다. 원주민 데이터 원칙 CARE(Carroll et al. 2020 *Data Sci. J.* [doi:10.5334/dsj-2020-043](https://doi.org/10.5334/dsj-2020-043))를 참고한다.
- **유해 이미지를 쓰지 않는다.** 원주민 조상의 유해 사진을 쓰지 않는다. 화석 사진이 필요하면 공개 라이선스가 확인된 박물관 복제품으로 한정하거나, 아이콘으로 대신한다.
- **지역 이벤트 표현:** 기존 앱의 지역 이벤트(시청자 지역에만 표시) 기능을 쓸 때 "우리 민족의 기원" 같은 민족주의적 서술을 피한다(예: 한반도 구석기 유적은 "이 지역의 사람들" 기준).
- **검수:** 출시 전에 고인류학 연구자 1명 이상에게 사건 문구 검토를 받는 것을 권장한다(오너 결정 항목).

---

## 6. 저장소 간 공유 디자인 시스템

### 6.1 요구 사항

두 제품(앞으로 더 늘 수도 있음)은 **각자 저장소**를 갖는다. 그래도 디자인은 늘 같아야 하며, 기존 앱의 "빌드 없는 단일 HTML" 방식을 가능한 한 유지한다.

### 6.2 선택지 비교

| 안 | 방식 | 장점 | 단점 |
|---|---|---|---|
| **A. 제3 저장소 `time-machine-ui` + Pages 버전 경로 — 추천** | `https://junhyeopsong.github.io/time-machine-ui/v1/tm.css`, `…/v1/timeline.js` 등을 `<link>`/`import`로 직접 불러온다. 고정 버전 `/v1.2.0/`도 함께 배포한다. | 빌드 없음. 한 번 고치면 두 제품에 동시 반영(동기화 요구 충족). 같은 출처라 CORS 문제 없음. 메이저 버전 경로로 깨지는 변경을 격리. | 런타임 의존 — UI 저장소 배포 실수가 두 제품을 동시에 깨뜨릴 수 있다(→ 고정 버전 롤백, 스모크 테스트로 완화). 첫 로드 요청 수 증가(파일 몇 개, 미미함). |
| B. 모노레포 | 한 저장소에 `packages/ui`, `apps/continents`, `apps/human` | 원자적 변경, 테스트 쉬움 | 요구 사항("각자 저장소")과 충돌한다. 기존 저장소를 옮겨야 하고 Pages 경로도 바뀐다. |
| C. 파일 복사 + 자동 업데이트 PR | UI 저장소에 태그를 달면 GitHub Action이 각 제품 저장소에 `vendor/tm-ui/` 갱신 PR을 연다 | 제품이 자기완결적이다(오프라인·고정). 의존이 깨질 위험이 없다. | 동기화가 PR 머지에 달려 있어 어긋나기 쉽다. 액션·토큰(PAT) 관리가 필요하다. 같은 코드가 세 곳에 있다. |
| D. npm 패키지 + 번들러 | `@junhyeopsong/tm-ui` 배포, Vite 빌드 | 업계 표준, 트리 셰이킹 | 빌드 단계가 새로 생긴다. 현재 단일 파일 방식에서 멀어진다. 정적 사이트에는 과하다. |
| E. git submodule | 제품 저장소에 UI 저장소를 서브모듈로 | 버전 고정 | Pages 빌드에서 서브모듈 처리, 기여자 혼란 |

**추천: A안. 다만 C안의 안전장치를 일부 섞는다.**
- 제품은 기본적으로 `/v1/`(움직이는 메이저 경로)을 불러온다. 디자인 동기화가 자동으로 된다.
- UI 저장소의 GitHub Action이 릴리스마다 `/v1.x.y/`(불변)도 만든다. 문제가 생기면 제품에서 한 줄을 바꿔 고정 버전으로 롤백한다.
- UI 저장소에 **스모크 테스트**를 둔다: Playwright로 두 제품의 배포 URL을 `?tmui=next` 프리뷰 경로로 열어 스크린샷을 비교한다. 통과해야 `/v1/`을 갱신한다.
- GitHub Pages의 캐시 헤더(약 10분 `max-age`)를 고려해, 큰 변경은 `/v1/` 안의 파일명 대신 메이저 버전을 올리는 방식으로 처리한다.

### 6.3 `time-machine-ui` 구조 (제안)

```
time-machine-ui/
  docs/                       ← GitHub Pages 루트
    v1/
      tokens.css              ← :root 변수 (색·반경·유리·글꼴)
      base.css                ← 레이아웃 셸, 유리 표면, 버튼, 토글, 세그먼트, 칩, 시트
      icons.js                ← Lucide 인라인 SVG (ISC) — 이름 → <svg> 문자열
      timeline.js             ← 시간축(척도 주입식) + 시대 띠 + 호버 툴팁 + 사건 점 + 핸들
      chips.js                ← 단축 칩 줄 + 가장자리 페이드/블러
      sheet.js                ← 설정 시트 + 위/아래 가장자리 페이드
      transport.js            ← ◀ ▶ 재생(유리 버튼) + 속도 세그먼트 + 키보드 단축키
      citysearch.js           ← 도시 검색 드롭다운 + 위치 추적 + 시간대 추정
      globe.js                ← three.js 셸: 장면, 대기 림, 별(천구극 회전), 끌기/핀치, 핀, 효과 셰이더 틀
      prefs.js                ← tm.* localStorage 읽기/쓰기 + URL 매개변수 + 구 키 이전
      switcher.js             ← products.json 기반 제품 전환기 (설정 옆 버튼 + 카드 메뉴)
      i18n-ui.json            ← 공유 컴포넌트 문자열 (10개 언어)
      products.json
    v1.0.0/ …                 ← 불변 복사본
  demo/index.html             ← 모든 컴포넌트 카탈로그 (목업 검토용)
  tests/                      ← Playwright 스크린샷
```

모든 컴포넌트는 **바닐라 ES 모듈**이다. 프레임워크를 쓰지 않으며 `import { createTimeline } from '/time-machine-ui/v1/timeline.js'` 형태로 불러온다. three.js r128은 각 제품이 cdnjs에서 불러오고 `globe.js`가 전역 `THREE`를 받는다(r128은 ES 모듈 빌드가 불편하므로).

`products.json` 예시:

```json
{
  "version": 1,
  "products": [
    {
      "id": "continents",
      "url": "/earth-time-machine/",
      "name": { "ko": "지구 대륙 타임머신", "en": "Continental Time Machine" },
      "icon": "globe",
      "range": { "from": "540Ma", "to": "-100Ma" },
      "bridges": [ { "to": "human", "when": { "ageBelow": "7Ma" } } ]
    },
    {
      "id": "human",
      "url": "/human-journey/",
      "name": { "ko": "인류의 여정", "en": "Human Journey" },
      "icon": "footprints",
      "range": { "from": "300ka", "to": "0" },
      "bridges": [ { "to": "continents", "when": { "atOldestEnd": true } } ]
    }
  ]
}
```

### 6.4 `docs/index.html`에서 옮길 부분 (줄 번호는 2026-11-11 기준 커밋 `774ccb3`)

| 영역 | 현재 위치 | 공유 저장소로 | 제품에 남김 |
|---|---|---|---|
| `:root` 디자인 토큰 (색·유리·반경·글꼴) | `docs/index.html:27`–`43` | `tokens.css` | — |
| 레이아웃 셸·시대 칩·원형 아이콘 버튼 | `:24`, `:73`, `:83` | `base.css` | 시대 칩 내용 |
| 설정 시트 + 가장자리 페이드, 드롭다운 | `:89`–`139` | `base.css` + `sheet.js` | 시트 안의 제품별 항목 |
| 토글, 세그먼트 컨트롤 | `:140`–`153` | `base.css` | — |
| 지구본 조작 버튼, 타임 독, 재생 클러스터 | `:154`–`213` | `base.css` + `transport.js` | — |
| 칩 가장자리 페이드/블러 | `:214`– | `base.css` + `chips.js` | 칩 목록(사건) |
| 휴대폰 레이아웃 | `:270`–`280`, JS `:1790` | `base.css` / `prefs.js` | — |
| Lucide 아이콘 인라인 SVG | `:314` 등 | `icons.js` | — |
| 지질 시대 정의 (ICS 색) | `:393` | `periods.js`(두 제품 공통 — 인류 제품도 ICS 띠 사용) | — |
| i18n 로딩·`applyLang` | `:409`, `:1922`–`1948` | 틀 + 공유 문자열 | 제품 문자열(`i18n.json`) |
| three.js 장면, 대기 림, 별 | `:1050`–`1134` | `globe.js` | 텍스처 생성(`:662`–`940`) |
| 도시 마커 | `:1135` | `globe.js` | — |
| 사건 효과 셰이더 틀 | `:1136`–`1258` | `globe.js` (효과 종류 등록식) | 제품별 효과 정의 |
| 지구본 끌기·핀치·바라보기 | `:1259`–`1411` | `globe.js` | — |
| 사건 핀, 지역 판정 | `:1412`–`1533` | `globe.js` / `prefs.js` | 판 위 핀 이동(대륙 전용) |
| 타임라인 (선형 사상, 띠, 툴팁) | `:1602`–`1739` | `timeline.js` (**척도 함수 주입**: 대륙 = 선형, 인류 = 이동 로그) | 범위 상수 |
| 도시 검색 | `:1740`–`1789` | `citysearch.js` | `cities.json` 데이터는 공유 저장소에 한 벌 |
| 평균 기온 카드 | `:1805`–`1845` | 카드 틀 | 데이터(PhanDA / 빙하기 곡선) |
| ◀ ▶ 단계 이동, 키보드, 재생 투어 | `:1846`–`1919` | `transport.js` (단계 규칙 주입) | 단계 크기 |
| 위치·시간대 → 가까운 도시 | `:1949`–`2010` | `citysearch.js` | — |
| **남는 것 (대륙 전용)** | PhanDA 표 `:485`, 사건 목록 `:493`, 고도 색 `:565`, 쿼터니언 회전 `:585`, 미래 시뮬 `:620`, PaleoDEM `:659`, 0.25° 프레임 `:712`, 해안선 획 `:941`, 충돌 핀 `:1534` | — | 그대로 |

**진행 상황:** ① 완료 (2026-11-11) — `JunhyeopSong/time-machine-ui` 5e6f2ce(v1 · v1.0.0), 앱 b1b84ba. 모든 요소의 계산된 스타일이 이전과 같음(데스크톱·휴대폰, 설정 창 열림). 아티팩트는 외부 CSS를 못 불러오므로 공용 CSS를 페이지 안에 넣은 사본으로 올린다.
② 완료 (2026-11-11) — time-machine-ui v1.1.0 `ui.js`(0bc65ea): `TMUI.icon/fillIcons`(Lucide), `edgeFade`(칩 줄·설정 창 가장자리), `popover`(설정 창 열고 닫기), `segmented`(단위·속도). 앱 4ae7253. 버튼 HTML·계산된 스타일·동작이 이전과 같음(데스크톱·휴대폰). 도시 검색(`citysearch.js`)은 ④ 지구본 셸과 함께 옮긴다.
③ 완료 (2026-11-11) — time-machine-ui v1.2.0(6916939): `TMUI.scale.linear` / `TMUI.scale.shiftedLog`, `TMUI.timeline`(시대 띠·hover/드래그 툴팁·눈금·슬라이더, `setScale`로 눈금 교체). 앱 4615a80은 선형으로 사용, 이전과 같음. 로그 눈금은 [demo/timeline.html](https://junhyeopsong.github.io/time-machine-ui/demo/timeline.html)에서 확인(최근 7만 년 60.6%). 터치 드래그 툴팁이 한 단계 늦던 문제도 고침.
④ 완료 (2026-11-11) — time-machine-ui v1.3.0(3947ec6): `TMUI.globe`(장면·대기·별·지구본 조작, 별 이동 단위 설정 가능), `TMUI.geo`(가까운 도시·시간대 추정), `TMUI.citySearch`. 앱 dc33adf(약 300줄 감소), 장면·조작 결과·검색·스타일이 이전과 같음. 도시 목록이 설정 창 스크롤을 따라가지 않던 문제도 고침. **이전 완료.** 남은 공용화 후보: 사건 효과 셰이더 틀, 사건 핀·팝업, 평균 기온 카드 틀, `cities.json` 한 벌로 합치기(인류의 여정 착수 때 필요하면).

**이전 순서:** ① 토큰과 CSS만 먼저 옮긴다. 기존 앱은 `<link>` 한 줄로 바꾸고 스크린샷이 같은지 확인한다. ② 아이콘·칩·시트·토글을 옮긴다. ③ 타임라인(척도 주입)을 옮긴다. ④ globe 셸을 옮긴다. 단계마다 기존 앱이 픽셀 단위로 같아야 넘어간다.

---

## 7. 제품 간 이동

### 7.1 같은 출처와 공유 설정

- `junhyeopsong.github.io/earth-time-machine/`와 `junhyeopsong.github.io/human-journey/`는 **같은 출처(origin)**이므로 localStorage를 함께 쓴다. 같은 출처의 다른 프로젝트 페이지와 충돌하지 않도록 **`tm.` 접두어**를 붙인다.
- 주의: 나중에 사용자 지정 도메인을 쓰면 출처가 달라져 공유가 끊긴다. 그때는 URL 매개변수만으로 넘긴다.

| 키 | 값 | 용도 |
|---|---|---|
| `tm.v` | `1` | 스키마 버전 |
| `tm.lang` | `ko`, `en`, … | 언어 |
| `tm.city` | Natural Earth `ne_id` (+ 이름 백업) 또는 `off` | 추적 도시 |
| `tm.unit` | `C` / `F` | 기온 단위 |
| `tm.speed` | `1`/`2`/`3` | 재생 속도 (선택) |
| `tm.layers.<product>.<name>` | `0`/`1` | 제품별 보기 설정 (제품마다 따로) |

### 7.2 제품 전환기

- 설정 시트 맨 위(또는 시대 칩 옆)에 **제품 전환 버튼**을 둔다. `products.json`을 읽어 아이콘 + 이름 + 범위("5억 4천만 년 전 → 1억 년 후")를 목록으로 보여 준다.
- 정보 패널·README 맨 위에 "다른 타임머신" 링크를 둔다.
- `<link rel="alternate">`와 OG 태그를 각 제품에 둔다(공유 시 검색 노출).

### 7.2.1 결정 (2026-11-11, 오너)

목업 [`mockup-product-switcher.png`](mockup-product-switcher.png)(A 왼쪽 위 제품 이름 · B 설정 창 안 · C 설정 옆 버튼 · 시간 다리 칩)을 보고 정했다.

- **C안 채택:** 설정(톱니) 버튼 바로 왼쪽에 같은 크기의 유리 아이콘 버튼(Lucide `layout-grid`)을 둔다. 누르면 제품 카드 메뉴가 열린다.
  - 카드: 제품 아이콘 · 이름 · 시간 범위 · 한 줄 설명. 지금 보는 제품엔 체크(`check`), 다른 제품엔 화살표(`arrow-right`), 새 제품엔 '새로움' 배지.
  - 메뉴 아래 안내: "언어와 추적 중인 도시는 그대로 이어집니다".
  - 휴대폰: 메뉴가 화면 폭(좌우 16px 여백)으로 펼쳐지고, 열린 동안 시대 카드를 덮는다.
  - 목록은 `products.json`에서 읽는다.
- **시간 다리 칩은 쓰지 않는다.** 아래 §7.3의 칩·띠 제안은 폐기. 제품 사이 이동은 전환 메뉴로만 한다.
  - URL 매개변수(`lang`, `city`, `age`)와 `?age=` 딥 링크는 전환 메뉴와 공유 링크에 그대로 쓴다.

### 7.3 시간 다리 (time-based bridges) — **폐기됨 (§7.2.1)**. 칩은 만들지 않고, URL 매개변수·딥 링크 부분만 유지.

- **대륙 앱 → 인류 앱:** 재생 머리가 **7 Ma 이후(0–7 Ma)**에 들어오면, 타임라인의 그 구간 위에 얇은 띠와 칩 "인류의 여정 보기 →"를 띄운다. MVP 단계(300 ka부터)에서는 0–0.3 Ma 구간에서 띄우고 "인류 앱은 30만 년 전부터"라고 알려 준다.
- **인류 앱 → 대륙 앱:** 타임라인 왼쪽 끝(가장 오래된 시점)에 도달하면 "더 먼 과거: 대륙의 이동 보기 ←" 칩을 띄운다.
- **함께 넘기는 URL 매개변수:** `?lang=ko&city=1159151299&age=7Ma`
  - `age`: 단위를 붙인 문자열(`540Ma`, `45ka`, `1200a`, 미래는 `-50Ma`). 양 앱이 같은 파서를 쓴다(`prefs.js`).
  - URL 매개변수 > `tm.*` > 기기 언어/위치 순으로 우선한다. URL로 받은 값은 `tm.*`에도 저장한다(같은 출처라 대부분은 이미 같다).
  - 개인정보: 도시 ID만 넘긴다. 좌표나 기기 위치는 넘기지 않는다.
- **딥 링크:** 두 앱 모두 `?age=`로 시작 시점을 지정할 수 있게 한다(공유·교육 용도로도 유용).

### 7.4 기존 앱에 필요한 이전 작업 (별도 작업, 이 기획서에서는 바꾸지 않음)

1. `localStorage 'lang'` → `tm.lang`: 읽을 때는 `tm.lang`을 먼저 보고, 없으면 `lang`을 본 뒤 `tm.lang`에 옮겨 적는다. 쓸 때는 한동안 두 키에 모두 쓴다(현재 위치 `docs/index.html:422`, `:1955`).
2. 도시 선택을 `tm.city`에 저장한다(현재는 저장하지 않고, 매번 위치/시간대로 추정함).
3. 기온 단위를 `tm.unit`에 저장한다.
4. URL 매개변수 `lang`, `city`, `age`를 읽는다(현재 `URLSearchParams`를 쓰지 않음).
5. 제품 전환기(설정 옆 버튼 + 카드 메뉴)를 넣는다(공유 UI의 `switcher.js`). 시간 다리 칩은 넣지 않는다.
6. §6.4 순서에 따라 공유 UI로 이전한다.

---

## 8. 진행 계획

**진행 상황 (2026-11-11):** 프로토타입 1차 공개 — [junhyeopsong.github.io/human-journey](https://junhyeopsong.github.io/human-journey/) (저장소 `JunhyeopSong/human-journey` e53dac6, 5d27910). 공용 UI v1 위에 지구본·설정 창·타임 독·타임라인(기본 선형, 설정에서 로그)·재생·별, 한국어/영어. 해안선은 ETOPO1(0.25°) + Spratt & Lisiecki 2016 해수면(0–430 ka, 오늘 = 0 m로 맞춤)으로 그려 빙기에 순다·사훌·베링이 드러난다. 언어 선택은 `tm.lang`(없으면 대륙 앱의 `lang`)을, 눈금 선택은 `tm.scale`을 쓴다.
사건·유적 (219e0df): §1.2 표의 29개 + 농경 기원 3곳(중국 기장, 발사스 옥수수, 뉴기니 쿡) = 34개를 `docs/data/events.json`으로. 지구본 핀(연대 범위 동안 표시), 타임라인 점·막대(점선 = 논쟁 주장, 빗금 = 논쟁 부분), 팝업(종류·논쟁 배지·연대·설명·양쪽 주장·출처), 설정 '논쟁 중인 연대도 보기'(기본 켬). 요약문과 추가한 농경 3곳의 출처는 검토 필요(결정 10).
빙상 (a800d46): Batchelor 2019 데이터(OSF)에 라이선스가 없어(논문만 CC BY 4.0) 결정 11에 따라 공개 사이트에는 직접 그린 LGM 개략도(북미·그린란드·유라시아·알프스·파타고니아·아이슬란드 + 남극은 지형으로)를 해수면에 맞춰 가장자리부터 줄고 늘게 함. Batchelor LGM 외곽선은 내 컴퓨터에서만 비교용으로 사용(대체로 일치, 북극 대륙붕·배핀만·산악 빙하 차이). 저자 허락 요청 메일 초안 전달.
빙상 갱신 (9f0bab9, 2026-11-11): 오너 판단 — Batchelor 2019 데이터는 논문의 일부로 출판되어 CC BY 4.0이 적용된다. 이에 따라 12개 시기(LGM, 30·35·40·45 ka, MIS 4, 5a–5d, 6, 8)의 최적 추정 복원을 0.25°로 바꿔(`data/ice_nh.png`, 출처 `data/ice_nh.json`) 공개 사이트에 사용. 시기 사이와 빙기 이후 해빙은 가장 가까운 복원을 해수면에 맞춰 줄이고 늘림. 그린란드·남극 현재 빙상은 지형, 파타고니아는 개략도. 출처는 설정 창과 README에 표기.
이동 경로 (2026-11-11): 9개 경로(`docs/data/routes.json`, 지점마다 연대). 시간이 지점을 지날 때마다 점선이 자라고, 진행 중엔 밝게 + 끝에 이름표, 끝나면 옅게 남음. 이른 레반트 확산은 9만 년 전 이후 사라짐. 남부·북부 경로와 아메리카 진입 시기는 '논쟁'. 이름표를 누르면 팝업(설명·논쟁·출처). 설정 토글.
종 분포 (2026-11-11): 결정 5대로 유적 기반 — 고인류 6종, 유적 30곳(`docs/data/species.json`). 지금 시점에 연대가 맞는 유적마다 약 600 km 원, 2,200 km 안의 유적끼리만 이어 흐린 영역으로(볼록 껍질은 빈 지역까지 덮어 버림). 종 이름표 → 팝업(설명·보이는 유적 수·논쟁·출처). 서식 모델 레이어(Timmermann 2022)는 라이선스 확인 전까지 공개 사이트에 넣지 않음.
현생인류 분포 (2026-11-11, 오너 요청): 종 분포 표현으로 이동 경로를 함께 보여 줌 — 아프리카 초기 유적(제벨 이르후드·오모·헤르토·피너클 포인트·블롬보스) 주변 영역 + 각 경로가 지나온 만큼의 띠. 고인류 영역 아래에 그림. 점선 경로는 위에 유지.
오너 요청 (2026-11-11): 이동 경로 표시 제거(데이터는 현생인류 확산의 뼈대로만 사용). 현생인류는 1° 칸마다 도달 시점을 계산(아프리카 초기 유적·진행 중인 경로에서 천 년에 약 1,000 km)해 그 시점 이후 육지·비빙상이면 면으로 채움. 평균 기온 추가: EPICA Dome C(Jouzel 2007)를 LGM −6.1 °C(Tierney 2020)에 맞춰 14.0 °C 기준으로 환산한 근사치 — Snyder 2016은 공개 데이터 파일을 찾지 못함.
근거 기반 종 분포 (2026-11-11, 오너 요청 — 모로코 단일 기원처럼 보이는 문제): 확산 모델과 `routes.json` 제거. `docs/data/sites.json`(유적 3,707곳, `tools/build_sites.py`) = Timmermann 2022 보충표 1(CC BY 4.0, 30–350 ka, 종 귀속) + ROAD(CC BY-SA 4.0, 30 ka 이후 현생인류) + 출처(DOI) 붙인 목록(아메리카·사훌·오세아니아·섬 종). 세 겹: **확인**(지금 시기 연대 유적 주변 ~450 km, 진하게) · **추정**(앞뒤로 넓힌 연대 창, ~1,600 km, 그 시기 육지·비빙상만, 옅게) · **논쟁**(종 귀속 또는 연대 논쟁 유적, 호박색 빗금, 설정 토글). 현생인류가 50 ka 이후 도달한 곳은 현재까지 추정으로 유지. 공개 데이터 파일은 ROAD 때문에 CC BY-SA 4.0. 결정 5의 '서식 모델 레이어'는 아직 없음.
종 분포 표현 개선 (2026-11-11, 오너 요청): 세 겹 구분을 없애고 종마다 옅은 칠 하나 + 종 색 외곽선, 겹치는 곳은 종 색 줄무늬. 초록·파랑 계열 색을 빼고 분홍(현생인류)·주황(네안데르탈)·보라(데니소바)·빨강(하이델베르겐시스)·흰색(에렉투스) 등으로. 유적마다 가장 오래된 연대에 다가가면 영역이 자라고 가장 젊은 연대 뒤엔 줄어듦(더해 그려 이웃 유적이 매끈하게 이어짐). 논쟁 유적은 '논쟁 중인 연대도 보기'를 켤 때 같은 칠에 포함. 현재에 아메리카·아프리카·오스트레일리아 일부가 비는 문제 → 현생인류는 50 ka 이후 인정된 유적이 있는 땅덩어리(50 ka 이후 가장 낮은 해수면 기준 육교로 이어진 땅) 안에서 천 년에 약 250 km(최대 5,000 km)씩 넓어짐. 다시 그리기 평균 10–23 ms.
육지 경로 도달 모델 (2026-11-11, 오너 요청 — 3만 년 전 남아메리카가 칠해지는 오류: 직선 원이 베링 육교로 이어진 땅덩어리 판정을 통과해 대서양을 건넘): `tools/build_arrival.py` → `docs/data/arrival.png`(0.5°, 칸마다 처음 도달한 시점). 인정된 현생인류 유적(50 ka보다 오래되면 50 ka)에서 8방향으로 천 년에 약 500 km씩, 그 시기 해수면 위 육지만(육교가 열릴 때까지 기다림), 바다와 베링 해협 경도선은 건너지 않음 → 아메리카·사훌·섬은 그곳 유적에서만 시작. 바다로 건너간 곳을 위해 유적 추가(DOI 확인): 아마존 페드라 핀타다, 라파 도 산투, 카리브(Napolitano 2019: 쿠바·푸에르토리코·히스파니올라·자메이카), 마다가스카르(Anderson 2018; Hansford 2018 1만 년 전 주장은 논쟁), 그린란드 사카크, 아이슬란드, 술라웨시, 티모르, 크레타, 뉴칼레도니아·피지·사모아 라피타, 하와이 여러 섬, 뉴질랜드 북섬. 현재 육지의 97.4% 덮임; 남은 곳은 캐나다 북극 섬·스발바르·아주 작은 섬. 빙상은 이동을 막지 않음(한계). 현생인류 파랑·하이델베르겐시스 초록으로 복귀.
200만 년 확장 (2026-11-11, 오너 결정): AGE_MAX 300 → 2,000 ka. 해수면 0–430 ka Spratt short + 430–798 ka long PC1 + 0.8–2 Ma LR04 선형 회귀(r = 0.90), 기온 0–800 ka EPICA + 이후 LR04 회귀(`tools/build_climate.py`). 종: Timmermann 보충표의 30만 년 이전 유적(하빌리스 18, 에르가스테르 45, 에렉투스, 하이델베르겐시스) + 추가(안테세소르, 파란트로푸스, 세디바, 드마니시, 상천, 마타 멩게; DOI 확인) → 13종 3,986곳. 사건 10개 추가(드마니시, 아슐리안, 투르카나 소년, 자바, 중기 플라이스토세 전환, 해피스버그, 안테세소르, 게셔 베노트 야아코브, 마타 멩게, 시마 데 로스 우에소스) → 44개. 시대 띠에 젤라시안·칼라브리안. 유적 앞뒤 여유는 오래된 시기에서 40 ka(자라는 시간 25 ka)로 제한. 재생은 선형에서 전체 약 2분. 빙상은 MIS 8보다 오래된 시기를 가장 가까운 복원을 해수면에 맞춰 씀(한계). 선형 기본값에선 최근 30만 년이 슬라이더의 15% — 기본 눈금 재검토 필요.
타임라인 기본 눈금 변경 (2026-11-11, 오너 결정): 200만 년으로 늘어나 기본값을 로그(C1)로 바꿈. 설정에서 선형을 고른 적이 있으면(`tm.scale` = linear) 그대로 유지. 선형의 한 칸 이동은 10만 년.
재생 속도 조절 (2026-11-12, 오너 요청 — 200만 년 구간에서 숫자가 너무 빨리 바뀜): 재생 최고 속도를 보통 기준 초당 1만 2천 년(느리게 ×0.4, 빠르게 ×3)으로 제한해 4만 1천 년 빙기 주기가 몇 초에 걸쳐 지나가게 함. 재생 중 연도는 초당 약 2번 바뀌는 단위로 반올림(보통: 1만 년 단위), 해수면·기온·문구는 초당 최대 4번 갱신; 멈추면 정밀 값. 전체 재생: 느리게 약 9분, 보통 약 3분 40초, 빠르게 약 1분 10초. 로그 눈금 끝에서 0에 닿지 않던 문제, 50년 미만이 ' 년 전'으로 비던 문제도 고침.
설정 창 스타일 맞춤 (2026-11-12, 오너 요청): 대륙 앱이 자기 페이지에만 두던 규칙(전체 `box-sizing: border-box`, `body { margin: 0 }`, 언어 선택 상자 자체 화살표·150px, 설정 안 분할 버튼 한 줄, 비활성 행 `.item.off`)을 time-machine-ui v1.4.0 공용 base.css로 옮김. 인류의 여정 설정 창 크기가 대륙 앱과 같아짐(행 40px, 묶음 44px). 함께 타임 독(770→745px, 여백 16px)과 시대 카드(369→340px)도 의도한 크기로 돌아옴. 대륙 앱 측정값은 변화 없음.
주요 사건 바로가기 칩 (2026-11-12, 오너 요청): 대륙 앱처럼 타임라인 아래 칩 줄(공용 edgeFade). 11개 — 아프리카 밖 첫 인류(드마니시), 불의 사용, 현생인류의 등장, 출아프리카, 오스트레일리아 도착, 네안데르탈인의 사라짐, 빙하기 절정, 아메리카 도착, 농경의 시작, 마지막 땅 뉴질랜드, 현재. 누르면 사건 팝업과 같이 시점·장소·설명으로 이동, 화면에 보이는 사건 칩 하나만 강조. 휴대폰에선 사건 점과 함께 접힘.
사건 표시 줄 → 접힘/종별 계통도 (2026-11-12, 오너 요청 — 연대 범위 막대가 겹쳐 누르기 어려움): 막대 대신 대표 연대에 점. 접힘(기본): 바로가기 칩의 주요 사건 10개만 한 줄. 펼침('종별로 펼치기' 칩, `hj.tree`에 기억): 기후 + 10개 종 칸(하빌리스, 에르가스테르, 에렉투스, 플로레스인·루손인, 날레디, 안테세소르, 하이델베르겐시스, 네안데르탈인, 데니소바인, 현생인류), 각 칸에 그 종 유적 연대 범위 막대와 사건 점(종 색), 갈라져 나온 칸으로 점선(계통은 논쟁 중 · 대략적 모습). 칸 안에서 닿는 점은 아래 줄로. 종 이름을 누르면 그 종으로 이동. 점 클릭 영역은 점 크기 그대로(넓히면 모인 곳에서 더 어려워서 되돌림).
사건 색 통일 (2026-11-12, 오너 요청): 사건의 색을 종류(고인류·교잡 등) 대신 계통도 칸의 종 색으로 — 지구 위 핀, 팝업, 타임라인 점(접힘·펼침) 모두 같은 색. 팝업 머리글도 종 이름(예: 호모 에렉투스), 기후 칸 사건은 기후 색과 종류 이름(화산, 기후·해수면). 루손인 사건은 같은 칸이라도 루손인 색.
재생 중 따라가기·이전/다음 버튼 (2026-11-12, 오너 요청): 설정에 '재생 중 따라가기'(기본 켬, `hj.follow`) — 대륙 앱과 같이 지나가는 사건을 줄 세워 최소 1.6초 간격으로 그곳으로 돌리고 팝업을 엶, 재생은 계속. ◀ ▶ 버튼·← →: 눈금 단위 대신 막대의 약 4%씩, 그 사이에 사건이 있으면 그 사건에서 멈추고 열기(같은 연대 사건도 하나씩) → 200만 년 전에서 현재까지 53번.
출아프리카 연대 검토 (2026-11-12, 오너 지적 — 만드랭·술라웨시보다 뒤에 나옴): 60–45 ka(대표 50)를 70–50 ka(대표 60)로. 유전학(Sümer·Iasi 2024: 네안데르탈인과의 교잡 약 5만~4만 4천 년 전 뒤 확산)과 고고학(술라웨시 ≥5만 1천, 사훌 4만 7천~6만 5천)의 차이를 논쟁 설명에 넣고, 출처에 Bergström 외 2021 추가.
다음 후보: 재생 중 사건에서 멈추기, 제품 전환 메뉴(두 제품 모두), 10개 언어.

| 단계 | 내용 | 산출물 | 완료 기준 |
|---|---|---|---|
| **0. 리서치** (이 문서) | 범위, 데이터, 라이선스, 설계 선택지 | `planning/human-journey-plan.md` | 오너가 §9 결정 |
| **1. 라이선스 확인** | AADR, Krapp 2021, CHELSA-TraCE21k, ICE-6G_C, Batchelor 2019, Timmermann 2022, Spratt v2 확인. 필요하면 저자에게 문의 | `planning/licenses.md` | 각 자료에 ✅/❌ 판정 |
| **2. 목업** | ① 타임라인 척도 4안(C 5k/10k/20k, B) ② LGM 지구본(육교·빙상) ③ 사건 카드 + 논쟁 배지 ④ 종 범위 표현 2안 ⑤ 제품 전환기·시간 다리 칩 ⑥ 휴대폰 | PNG (기존 `mockup-*.png`처럼) | 오너가 안을 선택 |
| **3. 공유 UI 저장소** | `time-machine-ui` 생성, 토큰·CSS 먼저, `demo/` 카탈로그, Pages `/v1/`, 스모크 테스트 | 저장소 + 데모 URL | 기존 앱이 `<link>`로 바꿔도 스크린샷이 같다 |
| **4. 기존 앱 이전 1차** | 토큰/CSS 연결, `tm.*` 이전, URL 매개변수, 전환기 | 기존 앱 PR | 회귀 없음 |
| **5. 새 저장소 프로토타입** | `human-journey` 생성, globe 셸 + 이동 로그 타임라인 + ETOPO 텍스처 + 해수면 곡선(욕조) + 사건 10개 | Pages 프리뷰 | 300 ka → 0 재생, 육교 출현 |
| **6. 데이터 층** | ICE-6G 보정·빙상, 사건 29개 + 2단계 후보, ROAD/PBDB 지점, aDNA 핀, 종 범위, 기온 곡선, (선택) 바이옴 | `data/*.json`, `tools/*.py` (원자료 → 가공 파이프라인, 기존 `tools/`처럼) | 모든 항목에 출처·라이선스 필드 |
| **7. i18n** | 10개 언어. 공유 문자열은 UI 저장소, 사건 문구는 제품 저장소. 인류 종 이름 표기 출처 기록 | `i18n.json` | 10개 언어 화면 검수 |
| **8. 검수** | 연구자 문구 검토(권장), 민감성 체크리스트, 접근성(키보드·스크린리더 라벨) | 검토 기록 | 지적 사항 반영 |
| **9. 배포** | GitHub Pages, OG 이미지, README(데이터 출처 표 — 기존 앱 형식), 양 앱의 상호 링크 | 공개 URL | 두 앱 사이 왕복 이동, 설정 유지 |
| 10. 2단계 | 7 Ma 확장(c=5k), 선택적으로 PALEOMAP 판 운동 재사용 | | |

---

## 9. 오너가 결정할 사항

1. ~~**제품 이름**~~ → **결정됨 (2026-11-11):** 한국어 "인류의 여정", 영문 "Human Journey", 저장소 `JunhyeopSong/human-journey`, 주소 `junhyeopsong.github.io/human-journey/`. 나머지 8개 언어 이름은 영문을 기준으로 번역해 정한다.
2. ~~**MVP 범위**~~ → **결정됨 (2026-11-11):** 30만 년 전(300 ka)부터 시작. 7 Ma까지 넓히는 것은 2단계.
3. ~~**타임라인 척도**~~ → **결정됨 (§2.5):** 선형 A와 이동 로그 C1(c = 10 kyr)을 설정에서 선택, 기본값 A. 확대 없음 유지.
4. ~~**논쟁 연대 표시**~~ → **결정됨 (2026-11-11):** 기본으로 둘 다 보여 준다. 연대는 범위 막대, 논쟁 사건에 '논쟁' 표시와 양쪽 주장·출처 툴팁(§5.1). 설정에서 '널리 인정된 것만'으로 바꿀 수 있다.
5. ~~**종 분포 표현**~~ → **결정됨 (2026-11-11):** 기본은 유적 지점 외곽선(흐린 경계), 설정에서 서식 적합도 모델 레이어(Timmermann 2022)를 켤 수 있다(§4.1). 손그림 개략도는 쓰지 않는다.
6. ~~**공유 디자인 방식**~~ → **결정됨 (2026-11-11):** 공용 저장소 `time-machine-ui`를 GitHub Pages의 버전 주소(`/time-machine-ui/v1/…`)에서 불러온다(§6).
7. ~~**기존 앱 이전 시점**~~ → **결정됨 (2026-11-11):** 새 제품보다 먼저 기존 앱을 공용 UI로 옮긴다(§6.4 순서 ①→④, 단계마다 화면이 같아야 다음으로).
8. ~~**시간 다리 위치**~~ → **결정됨 (§7.2.1):** 시간 다리 칩은 쓰지 않음. 제품 전환은 설정 옆 버튼(C안)으로만.
9. ~~**농경·문명 사건**~~ → **결정됨 (2026-11-11):** 농경 기원 4~6곳(비옥한 초승달, 중국, 메소아메리카 등)을 사건으로 넣는다. 그 밖의 문명사는 넣지 않는다.
10. **연구자 검토:** 출시 전 외부 검토를 받을지, 받는다면 누구에게(예: Timmermann 2022 데이터의 IBS 기후물리연구단 협조 겸).
11. ~~**라이선스 리스크**~~ → **결정됨 (2026-11-11):** 라이선스가 불명확한 자료(ICE-6G_C, AADR, Timmermann 등)는 내 컴퓨터의 프로토타입에서만 쓴다. 공개 배포 전에 저자 허락을 받거나 확실한 자료로 바꾼다(부록 A).

---

## 부록 A. 확인이 더 필요한 항목

- AADR Dataverse 라이선스 필드 ([doi:10.7910/DVN/FFIDCW](https://doi.org/10.7910/DVN/FFIDCW))
- CHELSA-TraCE21k 데이터 파일 라이선스 ([EnviDat](https://www.envidat.ch/))
- Krapp et al. 2021, Timmermann et al. 2022 데이터 라이선스
- ICE-6G_C 재배포 조건 (Peltier 그룹 문의)
- Batchelor 2019, Gowan 2021 형상 파일 라이선스
- Spratt & Lisiecki v2 (PANGAEA) 라이선스와 v1과의 차이
- Snyder 2016에 대한 비판 문헌의 정확한 서지
- ROAD Zenodo 스냅숏([zenodo.org/record/7669784](https://zenodo.org/record/7669784))의 라이선스가 roadDB와 같은지

## 부록 B. 참고한 2차 자료

- ROAD 데이터 이용: [roadDB README (CRAN)](https://cran.r-project.org/web/packages/roadDB/readme/README.html)
- AADR 배포 이력: [Reich lab curated releases](https://reichdata.hms.harvard.edu/pub/datasets/amh_repo/curated_releases/index.html)
- Beyer 2020 / pastclim: [pastclim Beyer2020 문서](https://rdrr.io/cran/pastclim/man/Beyer2020.html), [Cambridge 소식](https://eeg.zoo.cam.ac.uk/news/high-resolution-terrestrial-climate-bioclimate-and-vegetation-last-120000-years)
- CHELSA-TraCE21k: [Clim. Past 논문](https://cp.copernicus.org/articles/19/439/2023/), [기술 문서 PDF](https://www.envidat.ch/dataset/c88baa58-dbae-452c-8c2c-343e4c9fb885/resource/613fcb27-3649-4b5f-8880-984403cccd62/download/chelsa-trace21k_technical_documentation.pdf)
- 하얼빈 = 데니소바인 보도: [Science News](https://www.sciencenews.org/article/skull-first-denisovan-human-cousin)
- 윈셴 2: [NHM 보도자료](https://www.nhm.ac.uk/press-office/press-releases/analysis-of-reconstructed-ancient-skull-pushes-back-our-origins-.html), [Smithsonian](https://www.smithsonianmag.com/smart-news/scientists-reconstruct-a-million-year-old-skull-and-suggest-it-could-rewrite-our-timeline-of-human-evolution-180987419/)
- 사훌 도착 논쟁: [Cosmos](https://cosmosmagazine.com/history/the-quest-to-understand-when-ancient-migration-to-australia-began)
- ETOPO 2022: [NCEI](https://www.ncei.noaa.gov/products/etopo-global-relief-model)
