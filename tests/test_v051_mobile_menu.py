from pathlib import Path
from playwright.sync_api import sync_playwright

html=(Path(__file__).resolve().parents[1]/"index.html").read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,args=["--disable-gpu"])
    for width,height in [(393,852),(360,640),(320,640),(412,915)]:
        page=browser.new_page(viewport={"width":width,"height":height},is_mobile=True,has_touch=True)
        page.set_content(html,wait_until="load")
        assert page.evaluate("SUMI_DIAGNOSTICS().panelState")=="mini"
        mini=page.locator("#tool-panel").bounding_box()
        assert mini["height"]<125
        page.locator('.mini-content [data-ink-style="sumi"]').click()
        page.locator(".mini-palette .swatch.water").click()
        assert page.evaluate("SUMI_DIAGNOSTICS().style")=="sumi"
        assert page.evaluate("SUMI_DIAGNOSTICS().tool")=="water"
        page.locator('[data-menu-state="expanded"]').click()
        assert page.locator("#size").is_visible()
        assert page.locator('#palette .swatch.water').get_attribute("aria-pressed")=="true"
        page.locator('[data-menu-state="collapsed"]').click()
        assert page.locator("#tool-panel").bounding_box()["height"]<=56
        page.locator('[data-menu-state="mini"]').click()
        assert page.locator(".mini-content").is_visible()
        page.close()
    page=browser.new_page(viewport={"width":1200,"height":800})
    page.set_content(html,wait_until="load")
    assert page.locator("#size").is_visible()
    assert page.locator(".mobile-menu-switch").evaluate("x=>getComputedStyle(x).display")=="none"
    browser.close()
print("PASS: 3-state mobile panel + desktop regression")
