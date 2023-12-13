 

from assets.PageName import PageName
from assets.ButtonName import ButtonName
from assets.PopupName import PopupName

from modules.AllPage.Page import Page
from modules.AllTask.SubTask.RaidQuest import RaidQuest
from modules.AllTask.Task import Task

from modules.utils import click, swipe, match, page_pic, button_pic, popup_pic, sleep, ocr_area

import numpy as np
import logging

from modules.utils.GlobalState import raidstate

class RunExchangeFight(Task):
    def __init__(self, levelnum, runtimes, name="RunExchangeFight") -> None:
        """
        after enter the location, start to raid
        
        levelnum start from 0
        """
        super().__init__(name)
        self.levelnum = levelnum
        self.runtimes = runtimes

     
    def pre_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)
    
     
    def on_run(self) -> None:
        # 找到目标关卡点击，不用滚动
        clickind = self.levelnum
        points = np.linspace(209, 605, 5)
        logging.info("click level {}".format(self.levelnum+1))
        seepopup = self.run_until(
            lambda: click((1118, points[clickind])),
            lambda: match(popup_pic(PopupName.POPUP_TASK_INFO)))
        if not seepopup:
            logging.warn("没有成功点击到关卡，任务结束")
            return
        # 扫荡
        RaidQuest(raidstate.Exchange, self.runtimes).run()
        # 关闭弹窗，回到EXCHANGE_SUB页面
        self.run_until(
            lambda: click(Page.MAGICPOINT),
            lambda: Page.is_page(PageName.PAGE_EXCHANGE_SUB)
        )
        
        
        
    
     
    def post_condition(self) -> bool:
        return Page.is_page(PageName.PAGE_EXCHANGE_SUB)
