# SUMI Fluid Art — Cumulative Handoff v0.3.0

Official repo: https://github.com/kdc916/SUMI-Fluid-Art

## v0.3.0 (2026-10-17)

### User changes
1. Galaxy Ultra S Pen pressure sensitivity and hover exclusion.
2. Finger drawing speed-responsive width; normalized across sampling rates.
3. Natural fluid momentum on pen/finger release without artificial perpetual stirring.
4. Add missing GitHub project files: README, Android Studio Gradle project, workflow, smoke tests, documentation.

### Engineering
- pointerType=pen uses PointerEvent.pressure; finger pressure defaults to 0.5.
- Exponential velocity/pressure low-pass filter with elapsed-time-aware smoothing.
- GPU Navier-Stokes style advection/projection remain, wake is directional and decays under viscosity.
- On release, one velocity-only splat carries the end-of-stroke momentum without depositing dye.
- CPU Canvas2D fallback mirrors brush sizing and release momentum.
- Source of truth: repo root index.html; Android Gradle syncWebAssets copies it into APK.
- Never commit signing keys; Actions debug APK is not same signing identity as separately provided legacy-signed APK.

### Testing
- Node syntax check, CPU and software WebGL2 browser input/pixel tests, APK signature verification.
- Galaxy Ultra S Pen physical pressure range/latency still requires real-device test.

## Earlier versions

# SUMI Fluid Art — 누적 인수인계 v0.2.6 (GitHub 배포 정리본)

## 1. 프로젝트
- 앱 이름: SUMI Fluid Art — 墨流し
- 저장소 폴더: `SUMI-Fluid-Art`
- Android package name: `com.maxvfx.suminagashi`
- 기능 기준: v0.2.6 (사용자 확인 받은 물(투명) 도구 포함)
- 배포: GitHub Pages `index.html`, Android APK, Android Studio 소스

## 2. 핵심 기능 누적
- v0.1.1: 터치 입력 안정화 및 Canvas2D 대체 엔진.
- v0.2.0: WebGL2 fragment shader 기반 반 라그랑주 이류, 와도 보정, Jacobi 압력 계산, 필압·속도 브러시.
- v0.2.1: dye + stain 레이어, 중심부 농담·번짐 강화.
- v0.2.2–0.2.5: 수면 감쇠/소멸 조정 및 JavaScript 중복 코드 회귀 오류 수정.
- v0.2.6: MIZU 물(투명) 도구 추가. 안료를 추가하지 않고 터치 영역의 색소를 희석·확산함. GPU/CPU 양쪽 반영.

## 3. 코드 구조
- `index.html`: HTML/CSS/JS 단독 웹 앱, CDN 없음. GitHub Pages 배포용 유일한 웹 소스.
- `android/`: Android Studio Gradle 프로젝트. `syncWebAssets` Gradle 작업으로 루트 HTML을 자동 복사하여 앱에 포함.
- `releases/*.apk`: 기존 v0.2.6 서명된 APK 배포본(새로 컴파일한 결과가 아님).
- `.github/workflows/android-build.yml`: 저장소 수정 또는 수동 실행 시 디버그 APK 빌드.
- `tests/smoke_test.py`: 브라우저 기본 UI/픽셀 테스트.
- `scripts/verify_package.py`: 파일/버전/구조 검사.

## 4. 패치 시 중요 주의사항
- `index.html`의 스크립트 IIFE가 **1개**만 있는지 확인. v0.2.4에서는 JS 이중 삽입 때문에 터치가 작동하지 않았음.
- Water tool: `data-tool="water"`와 `currentTool`, `WATER_TOKEN`이 이어져야 함. 검정색 대체로 처리하지 말 것.
- WebGL2에서 float framebuffer 미지원이면 Canvas2D로 안전하게 전환해야 함.
- 초기 터치 후 브라우저 resize 이벤트로 기존 색소를 초기화하지 않도록 유지.
- `fade=100`에서도 소멸 루프를 끊지 말 것; 물 흐름(activity) 감쇠와 별도 유지.
- CPU/GPU 각각 터치와 물 희석 테스트를 별도로 수행.

## 5. 서명 보안·배포
- 이전 빌드의 Android 서명 키는 **배포 저장소에 넣지 않음**.
- 제공된 기존 v0.2.6 서명 APK는 기존 서명과 호환되는 사용본으로 보관.
- GitHub Actions 기본 디버그 APK는 다른 키로 서명돼 기존 앱에 직접 업데이트되지 않을 수 있음.
- 정식 배포용 keystore는 저장소 밖에서 안전하게 관리하고 서명 단계 분리.

## 6. 남은 검증 / 향후 개발
- Android 실기기 GPU 드라이버에서 유체 및 투명 물 동작 테스트.
- WebGL2 장기 안정성, 메모리 회복 및 Context Lost 처리.
- 물 희석 강도와 flow decay / dye fade / stain fade 세부 슬라이더 분리.
- 성능 옵션과 FPS/품질 표시.
- 공개 라이선스 사용자 결정 필요.

## 7. GitHub 재패키징 검증
- 최신 HTML과 APK 내 index.html SHA256 일치 확인.
- 브라우저 자동 검증: CPU 안전 모드에서 먹 그리기/물 희석/색 변경/초기화/리사이즈 통과.
- Android Studio Gradle 및 GitHub Actions 실제 빌드는 이 환경에서 실행하지 못함. 업로드 후 Actions 빌드 성공 여부 확인 필요.
- 웹앱 버전 유지 0.2.6; GitHub 폴더 배치와 워크플로/문서만 변경.
