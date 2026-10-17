#!/usr/bin/env python3
"""SUMI v0.3.1 continuous hold, speed-sensitive width, S Pen, water regression."""
from pathlib import Path
from playwright.sync_api import sync_playwright
HTML=(Path(__file__).resolve().parents[1]/"index.html").read_text()

def pointer(page,kind,x,y,pressure=.5,ptype="touch",pid=11):
    page.evaluate("""(v)=>document.querySelector('#fluid').dispatchEvent(
      new PointerEvent(v[0],{bubbles:true,cancelable:true,pointerId:v[5],
      pointerType:v[4],buttons:v[0]==='pointerup'?0:1,pressure:v[3],
      clientX:v[1]*innerWidth,clientY:v[2]*innerHeight}))""",
      [kind,x,y,pressure,ptype,pid])

def check():
    with sync_playwright() as p:
        browser=p.chromium.launch(executable_path='/usr/bin/chromium',headless=True,args=['--disable-gpu'])
        page=browser.new_page(viewport={'width':420,'height':900},is_mobile=True,has_touch=True)
        errors=[]
        page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(HTML,wait_until='load')
        page.wait_for_timeout(250)
        page.eval_on_selector('#fade',"e=>{e.value='5'}")
        pointer(page,'pointerdown',.47,.44)
        start=page.evaluate('SUMI_DIAGNOSTICS().stroke.radiusPx')
        page.wait_for_timeout(900)
        end=page.evaluate('SUMI_DIAGNOSTICS().stroke.radiusPx')
        assert end>start*1.25,(start,end)
        assert page.evaluate('SUMI_DIAGNOSTICS().brush.length')==1
        pointer(page,'pointerup',.47,.44,0)
        page.click('#clear')
        pointer(page,'pointerdown',.22,.48)
        page.wait_for_timeout(140)
        pointer(page,'pointermove',.225,.48)
        slow=page.evaluate('SUMI_DIAGNOSTICS().stroke.radiusPx')
        pointer(page,'pointermove',.78,.48)
        fast=page.evaluate('SUMI_DIAGNOSTICS().stroke.radiusPx')
        assert fast<slow*.88,(slow,fast)
        pointer(page,'pointerup',.78,.48,0)
        page.click('#clear')
        pointer(page,'pointerdown',.36,.41,.12,'pen',22)
        low=page.evaluate('SUMI_DIAGNOSTICS().stroke.radiusPx')
        pointer(page,'pointerup',.36,.41,0,'pen',22)
        pointer(page,'pointerdown',.59,.41,.95,'pen',23)
        high=page.evaluate('SUMI_DIAGNOSTICS().stroke.radiusPx')
        assert high>low*1.2,(low,high)
        pointer(page,'pointerup',.59,.41,0,'pen',23)
        page.click('.swatch.water')
        assert page.evaluate('SUMI_DIAGNOSTICS().tool')=='water'
        assert not errors,errors
        print('PASS v0.3.1 browser regression')
        browser.close()

if __name__=='__main__':
    check()
