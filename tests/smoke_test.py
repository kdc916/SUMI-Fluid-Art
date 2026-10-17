#!/usr/bin/env python3
"""Visual regression smoke checks on local index.html. Requires Playwright."""
from pathlib import Path
from playwright.sync_api import sync_playwright
from io import BytesIO
import base64
import os, shutil

ROOT=Path(__file__).resolve().parents[1]

def pigment_metric(page):
    return page.evaluate("""() => {
      const c=document.getElementById('fluid');
      const copy=document.createElement('canvas');
      copy.width=160;copy.height=160;
      const ctx=copy.getContext('2d',{willReadFrequently:true});
      ctx.drawImage(c,0,0,c.width,c.height,0,0,160,160);
      const a=ctx.getImageData(0,0,160,160).data;
      let amount=0;
      for(let y=35;y<125;y++)for(let x=20;x<142;x++){
        const j=(y*160+x)*4;
        amount+=Math.max(0, 210 - (a[j]+a[j+1]+a[j+2])/3);
      }
      return amount;
    }""")

def draw(page, points, pressure=.7, pid=41):
    for i,(x,y) in enumerate(points):
        typ='pointerdown' if i==0 else 'pointermove'
        page.evaluate("""({type,x,y,pressure,pid})=>{
           document.getElementById('fluid').dispatchEvent(new PointerEvent(type,{
             bubbles:true,cancelable:true,pointerId:pid,pointerType:'pen',
             clientX:x*innerWidth,clientY:y*innerHeight,pressure:pressure
           }));
        }""",{'type':typ,'x':x,'y':y,'pressure':pressure,'pid':pid})
        page.wait_for_timeout(22)
    page.evaluate("id=>document.dispatchEvent(new PointerEvent('pointerup',{pointerId:id,bubbles:true}))",pid)

with sync_playwright() as p:
    browser=p.chromium.launch(headless=True,executable_path=(os.environ.get('SUMI_CHROMIUM_PATH') or shutil.which('chromium') or shutil.which('google-chrome')),args=['--disable-gpu'])
    ctx=browser.new_context(viewport={'width':420,'height':900},is_mobile=True,has_touch=True)
    page=ctx.new_page()
    errors=[]
    page.on('pageerror',lambda error:errors.append(str(error)))
    page.set_content((ROOT/'index.html').read_text(encoding='utf-8'),wait_until='load')
    page.wait_for_timeout(350)
    assert page.evaluate('SUMI_DIAGNOSTICS().version')=='0.3.0'
    assert page.evaluate('SUMI_DIAGNOSTICS().engine')=='Canvas2D'
    before=pigment_metric(page)
    draw(page,[(.27+i*.047,.44+i*.018) for i in range(8)])
    after=pigment_metric(page)
    assert after>before+50,('Ink painting failed',before,after)
    page.locator('.swatch.water').click()
    assert page.evaluate('SUMI_DIAGNOSTICS().tool')=='water'
    draw(page,[(.39+i*.028,.48+i*.013) for i in range(7)],pid=45)
    page.wait_for_timeout(200)
    watered=pigment_metric(page)
    assert watered<after,('Water did not dilute pigment',after,watered)
    page.locator('.swatch[data-color="#d45046"]').click()
    assert page.evaluate('SUMI_DIAGNOSTICS().tool')=='pigment'
    draw(page,[(.60,.30),(.61,.34)],pid=46)
    page.locator('#clear').click()
    page.wait_for_timeout(180)
    cleared=pigment_metric(page)
    assert cleared<watered*.1,('Clear failed',watered,cleared)
    page.set_viewport_size({'width':390,'height':820})
    page.wait_for_timeout(300)
    assert not errors,errors
    print('PASS: fallback drawing, water dilution, color selection, clear, resize')
    browser.close()
