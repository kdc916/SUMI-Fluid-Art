# GitHub 업로드 방법 — SUMI Fluid Art

## 1. GitHub 저장소 생성
1. GitHub의 **New repository** 버튼 선택.
2. Repository name: **`SUMI-Fluid-Art`**.
3. Public 또는 Private 선택. 다른 사람에게 웹에서 보여주려면 Public 권장.
4. **Add a README file** 옵션을 끄고, `.gitignore`/License도 GitHub에서 자동 생성하지 않습니다(패키지에 포함된 파일과 중복 방지).
5. **Create repository** 클릭.

## 2-A. Git으로 업로드 (가장 안정적인 방법)

ZIP을 푼 다음 **`SUMI-Fluid-Art` 폴더 안에서** Git Bash 또는 PowerShell을 엽니다.

```bash
git init
git add .
git commit -m "Initial release: SUMI Fluid Art v0.3.0"
git branch -M main
git remote add origin https://github.com/<GITHUB_USERNAME>/SUMI-Fluid-Art.git
git push -u origin main
```

`<GITHUB_USERNAME>`은 본인의 GitHub 사용자명으로 바꿔야 합니다. GitHub 로그인/인증이 필요할 수 있습니다.

## 2-B. GitHub 웹에서 업로드
- **Add file → Upload files** 메뉴를 이용합니다.
- ZIP 파일 한 개를 그대로 올리는 것이 아니라 **압축을 풀고 안의 파일과 폴더**를 업로드해야 합니다.
- 특히 `.github/workflows`와 `index.html`이 정상 업로드되었는지 확인하세요. 숨김 파일은 일부 파일 관리자에서 보이지 않을 수 있습니다.

## 3. GitHub Pages 공개
`Settings → Pages → Build and deployment → Deploy from a branch`
- Branch: `main`
- Folder: `/(root)`
- Save

활성화 후 주소는 보통 다음과 같습니다.

`https://<GITHUB_USERNAME>.github.io/SUMI-Fluid-Art/`

**참고:** GitHub Pages 주소는 실제로 배포가 완료되어야 접근 가능합니다. 저장소를 업로드하기 전에는 작동하지 않습니다.

## 4. APK
- 수동 설치용: `releases/SUMI-Suminagashi-v0.3.0.apk`
- GitHub Actions: `Actions → Android APK build → Run workflow` 후 생성된 실행의 **Artifacts**에서 디버그 APK를 받습니다.
- GitHub Actions 생성본과 동봉 APK는 서명키가 달라 기존 버전에 덮어쓰기 설치가 실패할 수 있습니다.
- **서명키는 절대 GitHub에 공개하지 않습니다.**

## 5. 첫 업로드 확인
- `index.html`이 저장소 루트에 있는지
- README가 표시되는지
- Pages 주소에서 물(투명), 드로잉, 색상 기능이 작동하는지
- Actions 빌드가 성공하는지 (빌드 검증은 업로드 후 확인)

버전 기준: **v0.3.0 / GitHub 배포 정리 패키지**, 기능 변경 없음.
