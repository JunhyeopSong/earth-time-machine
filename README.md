# Continental Time Machine · 지구 대륙 타임머신

**▶ Live: https://junhyeopsong.github.io/earth-time-machine/**

[English](#english) · [한국어](#한국어)

![Continental Time Machine](docs/og.png)

---

## English

An interactive 3D globe that shows how Earth's continents moved — from the Cambrian 540 million years ago, through the supercontinent Pangaea, to 100 million years in the future — built on published plate-tectonic and paleo-elevation data.

### Features
- **Travel through time** — drag the timeline, play at three speeds, or jump straight to landmark moments such as the big five mass extinctions. Hover a period band to see its name.
- **Real paleogeography** — 0.25° paleo-elevation maps (PaleoDEM) every 5 million years, with the coastlines and sea level of each age.
- **Plate motions** — every landmass moves with its plate in the PALEOMAP model; optional plate-boundary and present-day-coastline overlays.
- **Major events on the map** — the Chicxulub impact, the Siberian and Deccan Traps, the first dinosaurs, India hitting Asia and more, many with animated map effects.
- **The future** — Scotese's forecast plate motions to +100 million years, with a simple model of new mountains, basins, erosion and trenches where plates collide.
- **Track any place** — search 1,266 cities, or start from the city nearest to you (from your device location, or roughly from your time zone).
- **Terrain or environment** — show the land by height, or by its Köppen climate zones (rainforest, savanna, desert, steppe, temperate, cold, tundra, ice cap): Pangaea's great deserts, the warm poles of the Cretaceous, Antarctica icing over 34 million years ago. A sketch from a climate model every 20 million years, its temperatures matched to the mean temperature shown; today is the observed map.
- **Global mean temperature** for each age, in °C or °F.
- **Other time machines** — the grid button beside settings switches to [Human Journey](https://junhyeopsong.github.io/human-journey/), which follows people across the world over the last 3.3 million years, keeping your language.
- **5 languages** — English, 한국어, 日本語, 繁體中文, Español. Follows your device language, and the language you pick carries over to Human Journey.

### Controls
| Action | Mouse / touch | Keyboard |
|---|---|---|
| Rotate the globe | Drag | Shift + ← → ↑ ↓ |
| Zoom | Scroll / pinch, double-click a spot | + / − |
| Play / pause | ▶ button | Space |
| Step 1 million years (stops at events) | ◀ ▶ buttons | ← → |
| Playback speed | Slow · Normal · Fast | 1 · 2 · 3 |

### Data sources
| Data | Source | License |
|---|---|---|
| Past terrain & coastlines | Scotese & Wright (2018), PALEOMAP PaleoDEMs — [Zenodo 5460860](https://zenodo.org/records/5460860) | CC BY 4.0 |
| Plate rotations & plate polygons | PALEOMAP PaleoAtlas for GPlates (Scotese) — [doi:10.5281/zenodo.10596609](https://doi.org/10.5281/zenodo.10596609), via [GPlates Web Service](https://gws.gplates.org) | CC BY 4.0 |
| Global mean temperature | PhanDA, Judd et al. (2024), *Science* — [doi:10.1126/science.adk3705](https://doi.org/10.1126/science.adk3705) ([GitHub](https://github.com/EJJudd/PhanDA)) | Cited research result |
| Climate zones (environment map style) | Pohl et al. (2022), *Data in Brief* — [doi:10.1016/j.dib.2022.108424](https://doi.org/10.1016/j.dib.2022.108424), FOAM climate model on the Scotese & Wright paleogeography, Köppen–Geiger classes every 20 Myr from 540 Ma ([Zenodo 6620748](https://doi.org/10.5281/zenodo.6620748)), recomputed after matching the model's temperatures to the PhanDA mean temperature (more warming toward the poles and in winter); today: Beck et al. (2023), *Sci. Data* — [doi:10.1038/s41597-023-02549-6](https://doi.org/10.1038/s41597-023-02549-6), observed 1991–2020, 0.5° ([figshare 21789074](https://doi.org/10.6084/m9.figshare.21789074)); grouped into 8 by `tools/build_climate_zones.py` | CC BY 4.0 |
| Cities | [Natural Earth](https://www.naturalearthdata.com) populated places | Public domain |
| Event timeline reference | Geological event chart by Mark (UK), shared with the project; events were checked against published sources before adding | Used with permission |
| 3D rendering | [three.js](https://threejs.org) r128 | MIT |

**Notes.** The future section follows Scotese's forecast; terrain changes from collisions and subduction are a rule-based estimate, not a physical simulation. Event descriptions and translations were written from general geology references — corrections are welcome.

### Feedback
Found a mistake, have an idea, or want an event added? Email **sapu0000@gmail.com** or [open an issue](https://github.com/JunhyeopSong/earth-time-machine/issues).

### Run locally
```bash
cd docs && python3 -m http.server 8000
```
Then open http://localhost:8000.

---

## 한국어

5억 4천만 년 전 캄브리아기부터 초대륙 판게아를 거쳐 1억 년 뒤 미래까지, 대륙이 어떻게 움직여 왔고 움직일지를 3D 지구본에서 돌려보는 웹 시뮬레이터입니다. 실제 연구에 쓰이는 판 운동·고지형 데이터를 바탕으로 만들었습니다.

### 기능
- **시간 여행** — 타임라인을 끌거나, 세 가지 속도로 재생하거나, 5대 대멸종 같은 주요 사건으로 바로 이동할 수 있습니다. 시대 색 띠에 마우스를 올리면 시대 이름이 보입니다.
- **실제 고지리** — 500만 년 간격의 0.25° 고지형 지도(PaleoDEM)로 그 시대의 해안선과 해수면을 보여줍니다.
- **판 이동** — 모든 땅이 PALEOMAP 판 모델에 따라 자기 판과 함께 움직입니다. 판 조각 경계와 현재 해안선 윤곽을 겹쳐 볼 수 있습니다.
- **지도 위 주요 사건** — 칙술루브 소행성 충돌, 시베리아·데칸 트랩, 최초의 공룡, 인도-아시아 충돌 등. 상당수는 지도 위 애니메이션 효과가 있습니다.
- **미래 예측** — 1억 년 뒤까지 Scotese의 판 운동 예측을 따르고, 대륙이 부딪히는 곳의 산맥·분지·침식·해구를 단순한 모델로 계산했습니다.
- **위치 추적** — 1,266개 도시를 검색하거나, 기기 위치(또는 시간대)를 바탕으로 가장 가까운 도시에서 시작합니다.
- **지형 또는 환경** — 땅을 높낮이로, 또는 쾨펜 기후대(열대 우림·사바나·사막·스텝·온대·냉대·툰드라·빙설)로 칠합니다. 판게아의 거대한 사막, 극지방까지 따뜻했던 백악기, 3,400만 년 전 얼어붙는 남극이 보입니다. 2천만 년 간격의 기후 모델 개략도로, 기온은 화면의 평균 기온에 맞춰 보정했고, 현재는 관측 지도입니다.
- **지구 평균 기온** — 시대별 평균 기온을 °C 또는 °F로 보여줍니다.
- **다른 타임머신** — 설정 옆 격자 버튼으로 330만 년 동안 인류가 세계로 퍼져 나간 길을 따라가는 [인류의 여정](https://junhyeopsong.github.io/human-journey/)으로 옮겨 갈 수 있고, 언어 설정은 그대로 이어집니다.
- **5개 언어** — 한국어, English, 日本語, 繁體中文, Español. 기기 언어를 따르며, 고른 언어는 인류의 여정에도 이어집니다.

### 조작법
| 동작 | 마우스 / 터치 | 키보드 |
|---|---|---|
| 지구 돌리기 | 드래그 | Shift + ← → ↑ ↓ |
| 확대·축소 | 휠 / 핀치, 원하는 곳 더블클릭 | + / − |
| 재생 / 정지 | ▶ 버튼 | Space |
| 100만 년씩 이동 (사건이 있으면 멈춤) | ◀ ▶ 버튼 | ← → |
| 재생 속도 | 느리게 · 보통 · 빠르게 | 1 · 2 · 3 |

### 데이터 출처
| 자료 | 출처 | 라이선스 |
|---|---|---|
| 과거 지형·해안선 | Scotese & Wright (2018), PALEOMAP PaleoDEMs — [Zenodo 5460860](https://zenodo.org/records/5460860) | CC BY 4.0 |
| 판 회전·판 다각형 | PALEOMAP PaleoAtlas for GPlates (Scotese) — [doi:10.5281/zenodo.10596609](https://doi.org/10.5281/zenodo.10596609), [GPlates Web Service](https://gws.gplates.org) 이용 | CC BY 4.0 |
| 지구 평균 기온 | PhanDA, Judd et al. (2024), *Science* — [doi:10.1126/science.adk3705](https://doi.org/10.1126/science.adk3705) ([GitHub](https://github.com/EJJudd/PhanDA)) | 논문 결과 인용 |
| 기후대 (지도 표현: 환경) | Pohl 외 (2022), *Data in Brief* — [doi:10.1016/j.dib.2022.108424](https://doi.org/10.1016/j.dib.2022.108424), Scotese & Wright 고지리 위 FOAM 기후 모델, 5억 4천만 년 전부터 2천만 년 간격의 쾨펜–가이거 기후대([Zenodo 6620748](https://doi.org/10.5281/zenodo.6620748)), 모델 기온을 PhanDA 평균 기온에 맞춰 보정한 뒤(극지방·겨울에 더 많이) 다시 계산; 현재는 Beck 외 (2023), *Sci. Data* — [doi:10.1038/s41597-023-02549-6](https://doi.org/10.1038/s41597-023-02549-6), 1991–2020 관측, 0.5°([figshare 21789074](https://doi.org/10.6084/m9.figshare.21789074)); `tools/build_climate_zones.py`로 8개로 묶음 | CC BY 4.0 |
| 도시 | [Natural Earth](https://www.naturalearthdata.com) populated places | 퍼블릭 도메인 |
| 사건 연표 참고 | Mark(영국)가 보내준 지질 사건 연표. 추가한 사건은 공개된 자료로 다시 확인함 | 허락받아 참고 |
| 3D 렌더링 | [three.js](https://threejs.org) r128 | MIT |

**참고.** 미래 구간은 Scotese의 예측을 따르며, 충돌·섭입에 따른 지형 변화는 물리 시뮬레이션이 아니라 규칙에 따른 추정입니다. 사건 설명과 번역은 일반적인 지질학 자료를 바탕으로 작성했습니다. 틀린 부분을 알려주시면 고치겠습니다.

### 피드백
틀린 내용, 아이디어, 추가하고 싶은 사건이 있다면 **sapu0000@gmail.com** 으로 메일을 보내주시거나 [이슈](https://github.com/JunhyeopSong/earth-time-machine/issues)를 남겨주세요.

### 로컬에서 실행
```bash
cd docs && python3 -m http.server 8000
```
브라우저에서 http://localhost:8000 을 엽니다.
