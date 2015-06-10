# 作業研究專題：StarCraft： brood war AI #

未來會考慮將不同作者撰寫的 module 分開編成各自的 package，
然後 Tool 類的 module，會自成一個 package。

### StarCraftAIBasicTool.py ###
基本的 AI 程式工具，
大部份 AI 都可以使用或者經常使用到的簡單程式。

### StarCraftAIDevelopTool.py ###
開發 AI 可以使用的 Debug 工具。

### kai7ai.py ###
這份 module 會被 `pybw.py` import 進來。  
其中包含了：  
1.  zerg_FastBreakAI , 簡易蟲族快攻 AI  
2.  TestAI, 單純做測試用

### KaisevenOptimizeSC.py ###
用來做最佳化的工具，也是本專題的主要角色。  
method XXX_wta(weapon_units, target_units) 是用來做最佳化武器分配的主要程式。  
1.  opt_wta ，尚未完成，還有許多地方需要進行測試 (趕工中...)  
2.  quick_wta ，一個非常簡單的演算法實作分配武器目標，  
    想法：各個單位在周圍一定距離的範圍內，尋找剩餘血量最少的目標攻擊。  
    雖然目前尚存在一些 bug，但基本上還是可以 work 得不錯的。  
