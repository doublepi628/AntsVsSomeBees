# AntsVsSomeBees
# 游戏概述
## 创意来源
本游戏为经典游戏《植物大战僵尸》的复刻版本，为了突出两者的相似性，我选择了与Plants Vs Zombies类似的名称为这个新游戏命名。为了区别于传统的植物大战僵尸，我简化了游戏中“收集阳光”的过程，加大了敌人（即蜜蜂）的数量，使得游戏节奏更快。此外，我还加入了一些全新设计的蚂蚁，使得游戏更有新意。
## 故事背景
蜜蜂和蚂蚁自古以来就是死对头，两个种族需要争抢食物，强大的一方获得生存下去的权利。最近，蜜蜂正在策划一场阴谋，它们想潜入蚁穴，杀掉蚁后，进而歼灭整个蚂蚁种族。蚂蚁们当然不能坐以待毙，他们需要布置防守保卫蚁后，反抗来自蜜蜂的侵略。大战一触即发！
## 游戏规则
你需要操控蚂蚁，消耗相应的食物在前往蚁后的屋子的必经之路上部署不同种类的蚂蚁，抵御蜜蜂的攻击。如果你成功击杀所有的蜜蜂，你便获得了这场战争的胜利，但如果有蜜蜂成功找到蚁后，那么你便输掉了。
## 运行环境
本游戏目前仅支持Windows系统运行
# 功能设计
## 游戏界面设计
<div style="text-align: center;"><a href="https://sm.ms/image/nq6YFRhm4ispuG7" target="_blank"><img src="https://s2.loli.net/2023/09/01/nq6YFRhm4ispuG7.png" ></a></div>
本游戏主要分为四个界面：开始界面、游玩界面、帮助界面、结算界面。上图为本游戏的界面逻辑图，展示了不同界面之间的跳转逻辑。

### 开始界面
每个游戏都有一个启动页，开始界面发挥的就是这个作用。通过点击**TAB**键，我们可以跳转到帮助界面；通过点击**SPACE**键，我们可以开始一场游戏；通过点击**ENTER**键，我们可以调整游戏的难度。
### 游戏界面
顾名思义，这就是玩游戏的地方。当你获得游戏的胜利或失败的时候，就会从该界面跳转到对应的结算界面。如果你在最高难度的情况下获得了游戏的胜利，你还可以发现一个彩蛋。
### 结算界面
正如游戏界面所言，结算界面里会显示出游戏的胜利和失败（以及上文提到的小彩蛋）。通过点击**SPACE**键，我们会再次回到开始界面。
### 帮助界面
通过帮助界面，玩家可以对这个游戏有基本的了解。帮助界面一共有两页，通过点击**TAB**可以在不同页面中跳转切换。
## 游戏元素设计
### 蚂蚁
本游戏里一共有**11种蚂蚁**，有些蚂蚁的创意来源于植物大战僵尸里面的植物，有些则是全新创造的。



| 种类 | 照片 |  介绍   |
|----------|----------|--------------------|
| 农夫 | <a href="https://sm.ms/image/JIuZGhdblQ8Tj7c" target="_blank"><img src="https://s2.loli.net/2023/08/31/JIuZGhdblQ8Tj7c.gif" width = 70 height = 70 ></a>  | 制作食物 |
| 树叶射手 |<a href="https://sm.ms/image/kNt9BKOEsqmo3FD" target="_blank"><img src="https://s2.loli.net/2023/08/31/kNt9BKOEsqmo3FD.gif" width = 70 height = 70 ></a>| 冲蜜蜂扔树叶 |
| 蚂蚁外壳 |<a href="https://sm.ms/image/IVBt7mb139EvRsW" target="_blank"><img src="https://s2.loli.net/2023/08/31/IVBt7mb139EvRsW.gif" width = 70 height = 70 ></a>| 保护身处其中的蚂蚁 |
| 坦克 | <a href="https://sm.ms/image/yeGuq9MrYmTvHhI" target="_blank"><img src="https://s2.loli.net/2023/08/31/yeGuq9MrYmTvHhI.gif" width = 70 height = 70></a>| 保护身处其中的蚂蚁、攻击附近的蜜蜂|
| 火焰蜂 |  <a href="https://sm.ms/image/FnKGCbR3hft9YvD" target="_blank"><img src="https://s2.loli.net/2023/08/31/FnKGCbR3hft9YvD.gif" width = 70 height = 70 ></a> | 灼烧附近的蜜蜂、在死亡时爆炸 |
| 贪吃蜂 | <a href="https://sm.ms/image/KetGOfrZEmYMaUl" target="_blank"><img src="https://s2.loli.net/2023/08/31/KetGOfrZEmYMaUl.gif" width = 70 height = 70></a> | 一口吃掉附近的蜜蜂 |
| 保卫者 | <a href="https://sm.ms/image/hTiSCHDVtc3rEYA" target="_blank"><img src="https://s2.loli.net/2023/08/31/hTiSCHDVtc3rEYA.gif" width = 70 height = 70></a> | 没有攻击能力，但血量很高 |
| 忍者蜂 | <a href="https://sm.ms/image/kidlfe3ThLjKIRO" target="_blank"><img src="https://s2.loli.net/2023/08/31/kidlfe3ThLjKIRO.gif" ></a> | 不会被蜜蜂伤害，也不会阻拦路过的蜜蜂，但会伤害路过的蜜蜂 |
| 女王蜂 | <a href="https://sm.ms/image/SVCzTnWPd5gAHuD" target="_blank"><img src="https://s2.loli.net/2023/08/31/SVCzTnWPd5gAHuD.gif" width = 70 height = 70></a>| 为身后的蜜蜂提供双倍伤害，但如果女王死掉了，游戏就输了|
| 寒冰树叶射手 | <a href="https://sm.ms/image/ZzDaUc9v5xremEb" target="_blank"><img src="https://s2.loli.net/2023/08/31/ZzDaUc9v5xremEb.gif" width = 70 height = 70></a> | 发射具有减速能力的树叶攻击蜜蜂 |
| 镭射蜂 | <a href="https://sm.ms/image/FqTWYhOZG6P1vJV" target="_blank"><img src="https://s2.loli.net/2023/08/31/FqTWYhOZG6P1vJV.gif" width = 70 height = 70></a> | 发出可以穿透蜜蜂的激光，但也会误伤友军|


### 蜜蜂

<div style="text-align: center;"> <a href="https://sm.ms/image/LZEYeXtfziPUxrb" target="_blank"> <img src="https://s2.loli.net/2023/08/31/LZEYeXtfziPUxrb.gif" alt="图片描述" width = 150 height = 150> </a> </div>
本游戏只有一种蜜蜂，为了有足够的难度区分，游戏主要以释放蜜蜂的频率和数量决定难度。

### 地图
<div style="text-align: center;"><a href="https://sm.ms/image/a1yxA9veYC3QgGX" target="_blank"><img src="https://s2.loli.net/2023/09/01/a1yxA9veYC3QgGX.png" ></a></div>
上图展示了本游戏地图的内在逻辑：蜜蜂从蜂巢出发，经过不同的通道，如果成功抵达蚁穴，那么你就输了。

### 难度设置
因开发时间有限，本游戏并没有设定很多关卡，而是改用四档游戏难度作为区分。四档难度都有一个特点：前期游戏节奏快，只有较为熟练地了解本游戏才可以成功抵御蜜蜂的攻击。四档难度的差异体现在总体的蜜蜂数量与后期的攻击频率，只有采取合适的策略部署蚂蚁才能引导你走向游戏最终的胜利。
### 音效设置
本游戏有两种背景音乐，在开始界面与帮助界面里播放的是《私たちは付き合っている》，在游戏过程和结算时播放的音乐是《Flake》。
### 动画设置
本游戏为大多数蚂蚁设计了攻击动画，均为本人手绘。

| 名称 | 动画 | 介绍 |
|------|----------|--------------------|
| 农夫收集的食物 | <a href="https://sm.ms/image/BC5PTsi78RbfaVD" target="_blank"><img src="https://s2.loli.net/2023/09/01/BC5PTsi78RbfaVD.png" width = 50 height = 50></a>| 也许是一个坚果？ |
| 树叶 | <a href="https://sm.ms/image/IMRqyfBNH1zjl8X" target="_blank"><img src="https://s2.loli.net/2023/09/01/IMRqyfBNH1zjl8X.png" width = 50 height = 50 ></a> | 树叶射手射出来的叶子 |
| 冰镇树叶| <a href="https://sm.ms/image/KQk2OjP6JMSWC8G" target="_blank"><img src="https://s2.loli.net/2023/09/01/KQk2OjP6JMSWC8G.png" width = 50 height = 50></a> | 虽然是冰镇的，但不能吃|
| 黄金叶 | <a href="https://sm.ms/image/6lEuPSyqjrDHFJN" target="_blank"><img src="https://s2.loli.net/2023/09/01/6lEuPSyqjrDHFJN.png" width = 50 height = 50></a>| 至高无上的女王蜂使用的叶子，但攻击力和普通蜜蜂没啥差别 |
| 贪吃蜂的牙 | <a href="https://sm.ms/image/uWvRI1qdQ8iTVte" target="_blank"><img src="https://s2.loli.net/2023/09/01/uWvRI1qdQ8iTVte.png" width = 50 height = 50 ></a> | 很锋利，口嚼蜜蜂不是梦 |
| 火焰蜂的火 | <a href="https://sm.ms/image/WmjF76EZnHqpvGx" target="_blank"><img src="https://s2.loli.net/2023/09/01/WmjF76EZnHqpvGx.png" width = 50 height = 50></a> <a href="https://sm.ms/image/MniJ6rW82LGfxy5" target="_blank"><img src="https://s2.loli.net/2023/09/01/MniJ6rW82LGfxy5.png" width = 50 height = 50></a>| 点燃！点燃！点燃！|
| 爆炸的火焰蜂 | <a href="https://sm.ms/image/xfa1GQ6jSZyRqng" target="_blank"><img src="https://s2.loli.net/2023/09/01/xfa1GQ6jSZyRqng.png" width = 50 height = 50></a>| 鞠躬尽瘁，死而后已 |
# 技术细节
本游戏在Windows平台采用pygame开发，用PyCharm完成代码的编写与调试。游戏部分图片素材来源于**UC Berkely**开设的课程[**CS61A**](https://cs61a.org)，其余的素材均为原创。
