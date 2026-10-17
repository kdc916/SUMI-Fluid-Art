from pathlib import Path
from playwright.sync_api import sync_playwright

HTML=(Path(__file__).resolve().parents[1]/"index.html").read_text()
with sync_playwright() as p:
    browser=p.chromium.launch(headless=True, args=["--disable-gpu"])
    page=browser.new_page(viewport={"width":420,"height":890},has_touch=True,is_mobile=True)
    errors=[]
    page.on("pageerror",lambda e:errors.append(str(e)))
    page.set_content(HTML,wait_until="load")
    assert page.evaluate("SUMI_DIAGNOSTICS().style")=="fluid"
    page.locator('button[data-ink-style="sumi"]').click()
    assert page.evaluate("SUMI_DIAGNOSTICS().style")=="sumi"
    page.mouse.move(175,350)
    page.mouse.down()
    page.wait_for_timeout(350)
    assert page.evaluate("SUMI_DIAGNOSTICS().hadInput")
    page.mouse.up()
    page.locator('button.swatch.water').click()
    assert page.evaluate("SUMI_DIAGNOSTICS().tool")=="water"
    page.locator('button[data-ink-style="fluid"]').click()
    page.locator('#clear').click()
    assert not errors, errors
    browser.close()
print("PASS")
