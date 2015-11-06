作業研究專題 StarCraft：brood war AI 
======================================

- [Intro](#intro)
- [Usage](#usage)
    - [Main Modules](#main-modules)
    - [Sub Modules](#sub-modules)
- [Mathematical Model](#mathematical-model)
- [Modules](#modules)
    - [KaisevenAI](#kaisevenai)
    - [FunctionTestAI](#functiontestai)
    - [ErrorTestAI](#errortestai)
    - [KaisevenOptimizeSC](#kaisevenoptimizesc)
    - [KaisevenControlSC](#kaisevencontrolsc)
    - [StarCraftAIBasicTool](#starcraftaibasictool)
    - [StarCraftAIDevelopTool](#starcraftaideveloptool)

Intro
-----
此 Project 目標為設計一個 StarCraft 的 AI，依據遊戲中不同的狀況，建立數學模型與演算法來最佳化遊戲結果。
在 DemoVideo 目錄中，放置了 AI 運行的影片。  

#### Demo  
##### Sample 1
沒有 AI Support 之下的 Battle  
[![img_DemoVideo_NoneAI01](http://i.imgur.com/ZLRHnsG.jpg)](https://www.youtube.com/watch?v=8b8EMxdssdw&feature=youtu.be "StarCraft_AI_Demo_01_None_AI_Suport")

有 AI Support 之下的 Battle
[![img_DemoVideo_AI01](http://i.imgur.com/1aEaNIJ.jpg)](https://www.youtube.com/watch?v=rHyXD_33gp0&feature=youtu.be "StarCraft_AI_Demo_01_AI_Suport")

##### Sample 2 2 
沒有 AI Support 之下的 Battle  
[![img_DemoVideo_NoneAI02](http://i.imgur.com/qj0FBLf.jpg)](https://www.youtube.com/watch?v=lTdkjR-rCoE&feature=youtu.be "StarCraft_AI_Demo_022_None_AI_Suport")

有 AI Support 之下的 Battle
[![img_DemoVideo_AI02](http://i.imgur.com/KSrM6JA.jpg)](https://www.youtube.com/watch?v=uta1Sczek5E&feature=youtu.be "StarCraft_AI_Demo_02_AI_Suport")

Usage
-----
    
#### Main Modules
制定 AI 演算法的模組。屬於 Main Modules 的有下列模組 :

- KaisevenAI
- FunctionTestAI
- ErrorTestAI

Main Modules 下會制定各種 AI 的 class。

    class SomeAI(object):
        def __init__(self):
            pybw.consoleManager.locals.update({'k': self})

        def onConnect(self):
            self.game = getGame() 

        def onMatchStart(self):
            if self.game.isReplay:
                return
            do something ...

        def onMatchFrame(self):
            do something ...

若是想使用某 Main Modules 下的 某個 AI class，只需要修改 `pybw.py` 中的部分內容即可。  
例如：想要啟用 SomeMainModule_2 下的 SomeAI_1 的話，只需要將 `pybw.py` 下的 `import SomeMainModule_2` 與 `event ... ( SomeMainModule_2.SomeAI_1() )` 的註解取消掉即可。

![amend_pybw_example](http://i.imgur.com/n8IY84t.gif)

> ##### Note：
> 1.    在 import Main Modules 時，只能 import 其中一個 module，若同時 import 多種 Main Modules 將導致 AI 無法正常運作。
> 
> 2.    FunctionTestAI 與 ErrorTestAI 通常需要在特定的 map 下才能正常運作，尤其是 ErrorTestAI。特定的 map 名稱與該測試 AI 名稱相同，且會放在 FunctionTestMaps 或 ErrorTestMaps 目錄中。例如：ErrorTestAI 下的 AI, TestSome, 對應的 map 名稱為 TestSome.scm 或 TestSome.scx。

#### Sub Modules
輔助 Main Module 的模組。屬於 Sub Modules 的有下列模組 :

- KaisevenOptimizeSC
- KaisevenControlSC
- StarCraftAIBasicTool
- StarCraftAIDevelopTool

Mathematical Model
-------------------

Modules
-------

#### KaisevenAI ( 待修改 ... )
主導整個遊戲策略與流程的 AI。  
目前只有 zerg_FastBreakAI 可以運行。  

- zerg_FastBreakAI : 簡易蟲族快攻

#### FunctionTestAI
用以測試部分 function 運作狀況的 AI

#### ErrorTestAI
用以測試意料之外 function 的 AI

#### KaisevenOptimizeSC
計算遊戲策略的工具，撰寫決策方法或最佳化演算法，與其附屬 function。

- Major function
    - opt_wta
    - quick_wta
- Subsidiary function
    - build_damage_table
    - build_hitpoints_table
    - build_injury_table
    - build_max_injury_table
    - build_move_cost_table

#### KaisevenControlSC
控制遊戲行為的工具，撰寫控制遊戲單位動作的演算法，與其附屬 function。

- Major function
    - start_attack
- Subsidiary function
    - moving_fire_case_escape_neardeath
    - moving_fire_case_escape_dangerous
    - moving_fire_case_escape_energetic
    - moving_fire_case_assault_neardeath
    - moving_fire_case_assault_dangerous
    - moving_fire_case_assault_energetic
    - moving_fire_case_attack_neardeath
    - moving_fire_case_attack_dangerous
    - moving_fire_case_attack_energetic

#### StarCraftAIBasicTool
基本 AI 工具，撰寫大部份 AI 都可以使用或者經常使用到的簡單演算法，與其附屬 function。

- Major function
    - set_basic_information
    - initial_units_scan
    - clear_up_death_unit
    - get_specify_unittype
    - get_distance_of ( 待修改 ... )
    - get_group_center_of
    - is_near_cooldown ( 待修改 ... )
    - weapon_range_diff ( 待修改 ... )
- Subsidiary function
    - build_unittype_dictionary

#### StarCraftAIDevelopTool
開發 AI 工具，撰寫方便用來 Debug function。

- Output to game
    - draw_circle_on
    - draw_range_circle_on
    - draw_line_between
    - draw_box_on
    - draw_text_on
    - show_hitpoints_of
    - show_cooldown_of
    - show_unit_status
- Output to file ( 待修改 ... )
    - write_2D_table_in_file
    - write_1D_table_in_file
    - write_data_in_pickle_file
    - write_dataset_in_pickle_file
