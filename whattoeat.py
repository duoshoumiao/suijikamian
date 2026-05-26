import hoshino, random, os, re, filetype
from hoshino import Service, R, priv, aiorequests
from hoshino.config import RES_DIR
from hoshino.typing import CQEvent
from hoshino.util import DailyNumberLimiter

sv_help = '''
[随机卡面] 随机PCR卡面
'''.strip()

sv = Service(
    name = '随机卡面',  #功能名
    use_priv = priv.NORMAL, #使用权限   
    manage_priv = priv.ADMIN, #管理权限
    visible = True, #可见性
    enable_on_default = False, #默认启用
    bundle = '娱乐', #分组归类
    help_ = sv_help #帮助说明
    )

_lmt = DailyNumberLimiter(99)
imgpath = os.path.join(os.path.expanduser(RES_DIR), 'img', 'benzi')

@sv.on_rex(r'^(随机)卡(面)')    
async def net_ease_cloud_word(bot,ev:CQEvent):    
    uid = ev.user_id    
    if not _lmt.check(uid):    
        await bot.finish(ev, '你今天抽的已经够多的了！', at_sender=True)    
    match = ev['match']    
    time = match.group(1).strip()    
      
    await bot.send(ev, '好的，正在给您随机下载一张pcr卡面', at_sender=True)  
        
    max_retries = 10    
    for attempt in range(max_retries):    
        # Generate random card ID (4 digits)    
        card_id = f"{random.randint(1000, 9999):04d}"    
          
        # Try both suffixes for this card ID  
        for suffix in ['31', '61']:  
            url = f'https://redive.estertion.win/card/full/{card_id}{suffix}.webp'  
                
            try:    
                resp = await aiorequests.head(url, timeout=5)    
                if resp.status_code == 200:    
                    to_eat = f'{time}到的卡面是\n[CQ:image,file={url}]'    
                    await bot.send(ev, to_eat, at_sender=True)    
                    _lmt.increase(uid)    
                    return    
            except Exception as e:    
                hoshino.logger.warning(f'URL验证失败: {url}, 错误: {e}')  
                continue  
        
    await bot.send(ev, '卡面获取失败，请稍后再试~', at_sender=True)