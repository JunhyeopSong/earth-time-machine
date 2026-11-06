# 지구 대륙 타임머신 · Continental Time Machine

2억 5천만 년 전 판게아부터 1억 년 뒤까지, 실제 판 이동·고지형 데이터로 대륙의 움직임을 3D 지구본에서 돌려보는 웹 시뮬레이터입니다.

A browser-based 3D globe that shows how the continents moved from Pangaea (250 million years ago) to 100 million years in the future, using published plate-tectonic and paleo-elevation data.

**▶ https://junhyeopsong.github.io/earth-time-machine/**

## 기능 · Features
- 시간 슬라이더, 재생(느리게·보통·빠르게), 지질시대 바로가기, 키보드 단축키 (Space, ←→, 1·2·3)
- 0.25° 고해상도 고지형(PaleoDEM), 당시 해안선과 해수면
- 지구·지질 역사 주요 사건 주석과 지도 효과 (칙술루브 충돌, 대규모 화산 등)
- 도시 1,266곳 검색·추적, 지구 평균 기온(°C/°F)
- 판 조각 경계, 현재 해안선 윤곽, 위경도선
- 10개 언어: 한국어, English, 日本語, 简体中文, 繁體中文, Español, Français, Deutsch, Português, Русский

## 데이터 출처 · Data sources
| 자료 | 출처 | 라이선스 |
|---|---|---|
| 과거 지형·해안선 | Scotese & Wright (2018) PALEOMAP PaleoDEMs — [Zenodo 5460860](https://zenodo.org/records/5460860) | CC BY 4.0 |
| 판 회전·판 다각형 | PALEOMAP PaleoAtlas for GPlates (Scotese) — [doi:10.5281/zenodo.10596609](https://doi.org/10.5281/zenodo.10596609), via [GPlates Web Service](https://gws.gplates.org) | CC BY 4.0 |
| 지구 평균 기온 | PhanDA, Judd et al. (2024), *Science* — [doi:10.1126/science.adk3705](https://doi.org/10.1126/science.adk3705), [GitHub](https://github.com/EJJudd/PhanDA) | 논문 결과 인용 |
| 도시 | [Natural Earth](https://www.naturalearthdata.com) populated places | Public domain |
| 3D 렌더링 | [three.js](https://threejs.org) r128 | MIT |

미래 구간(1억 년 후까지)은 Scotese의 판 운동 예측을 따르며, 충돌·섭입에 따른 지형 변화(산맥, 침식, 분지, 해구)는 단순한 규칙으로 계산한 추정입니다. 사건 설명과 번역은 일반적인 지질학 지식을 바탕으로 작성되었습니다.

The future section follows Scotese's forecast plate motions; terrain changes from collisions and subduction are a simple rule-based estimate.

## 로컬 실행 · Run locally
```bash
cd docs && python3 -m http.server 8000
```
→ http://localhost:8000
