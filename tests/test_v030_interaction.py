#!/usr/bin/env python3
"""S Pen pressure, finger speed, flow settling, water and clear regression checks."""
from pathlib import Path
from playwright.sync_api import sync_playwright
ROOT=Path(__file__).resolve().parents[1]
HTML=(ROOT/'index.html').read_text()

def call(page,typ,x,y,pressure=.5,ptype='touch',pid=42):
    page.evaluate("""([typ,x,y,pressure,ptype,pid])=>{
      const c=document.querySelector('#fluid');
      c.dispatchEvent(new PointerEvent(typ,{pointerId:pid,pointerType:ptype,buttons:typ==='pointerup'?0:1,
       bubbles:true,cancelable:true,clientX:x*innerWidth,clientY:y*innerHeight,pressure}));
    }""",[typ,x,y,pressure,ptype,pid])

def canvas_darkness(page):
    return page.evaluate("""()=>{
      let c=document.getElementById('fluid'),d=document.createElement('canvas');d.width=100;d.height=160;
      let ctx=d.getContext('2d',{willReadFrequently:true});ctx.drawImage(c,0,0,100,160);
      let pixels=ctx.getImageData(0,0,100,160).data,sum=0;
      for(let y=25;y<115;y++)for(let x=10;x<85;x++){
        let k=(y*100+x)*4;sum+=Math.max(0,220-(pixels[k]+pixels[k+1]+pixels[k+2])/3);
      }
      return sum;
    }""")

def check(mode,flags,headless):
    with sync_playwright() as p:
        b=p.chromium.launch(executable_path='/usr/bin/chromium',headless=headless,args=flags)
        ctx=b.new_context(viewport={'width':420,'height':900},is_mobile=True,has_touch=True)
        page=ctx.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
        page.set_content(HTML,wait_until='load');page.wait_for_timeout(450)
        assert page.evaluate('SUMI_DIAGNOSTICS().engine')==mode
        baseline=canvas_darkness(page)
        # pressure on pen stationary touch
        call(page,'pointerdown',.31,.30,.12,'pen',91);page.wait_for_timeout(35)
        low=page.evaluate('SUMI_DIAGNOSTICS().stroke')
        call(page,'pointerup',.31,.30,0,'pen',91)
        call(page,'pointerdown',.52,.30,.93,'pen',92);page.wait_for_timeout(30)
        high=page.evaluate('SUMI_DIAGNOSTICS().stroke')
        call(page,'pointerup',.52,.30,0,'pen',92)
        if mode=='WebGL2':
            assert high['radiusPx']>low['radiusPx']*1.45,(low,high)
        # fresh canvas for fingers
        page.locator('#clear').click()
        call(page,'pointerdown',.26,.45,.5,'touch',31)
        page.wait_for_timeout(110)
        call(page,'pointermove',.28,.46,.5,'touch',31);page.wait_for_timeout(40)
        slow=page.evaluate('SUMI_DIAGNOSTICS().stroke')
        page.wait_for_timeout(15)
        call(page,'pointermove',.70,.47,.5,'touch',31);page.wait_for_timeout(30)
        fast=page.evaluate('SUMI_DIAGNOSTICS().stroke')
        call(page,'pointerup',.70,.47,0,'touch',31)
        assert page.evaluate('SUMI_DIAGNOSTICS().brush.length')==0
        if mode=='WebGL2':
            assert fast['radiusPx']<slow['radiusPx']*.91,(slow,fast)
        after=canvas_darkness(page)
        assert after>baseline+80,(baseline,after)
        # motion decays when not touching
        page.wait_for_timeout(1900)
        assert page.evaluate('SUMI_DIAGNOSTICS().activity')<.08
        page.locator('.swatch.water').click()
        assert page.evaluate('SUMI_DIAGNOSTICS().tool')=='water'
        call(page,'pointerdown',.51,.46,.5,'touch',32)
        for i in range(5):
            page.wait_for_timeout(17)
            call(page,'pointermove',.52+.035*i,.46,.5,'touch',32)
        call(page,'pointerup',.66,.46,0,'touch',32)
        page.locator('.swatch[data-color="#d45046"]').click()
        call(page,'pointerdown',.52,.36,.5,'touch',33);call(page,'pointerup',.52,.36,0,'touch',33)
        assert page.evaluate('SUMI_DIAGNOSTICS().tool')=='pigment'
        page.locator('#clear').click();page.wait_for_timeout(100)
        assert canvas_darkness(page) < baseline+15
        assert not errors,errors
        print('PASS',mode,'S Pen',low,high,'finger',slow,fast)
        b.close()

if __name__=='__main__':
    import os
    if os.environ.get('SUMI_TEST_GPU')=='1':
        check('WebGL2',['--use-gl=angle','--use-angle=gl','--enable-webgl','--ignore-gpu-blocklist','--disable-gpu-sandbox'],False)
    else:
        check('Canvas2D',['--disable-gpu'],True)
