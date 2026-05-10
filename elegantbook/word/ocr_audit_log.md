# `ocr.md` 人工核查记录

- 核查日期：2026-05-10
- 真值来源：源 PDF 渲染页图像；`ocr.md` 与 PDF 文本层仅作辅助
- 当前交付状态：已完成前置部分高风险页、目录页、`LECTURE 1-35`、附录开头与附录续页 `PDF 420` 的人工修订；正文下一起点为 `LECTURE 36`；全书尚未完成逐页人工核查

## 已完成批次

### A1：PDF 1-5（封面 / 内容简介 / 版权 CIP / 编委）
- 结构已核：是
- 字段已核：封面书名、副题、作者、出版社；封底简介段落；ISBN；版权页出版社、责编、电话、网址；编委页标题和名单
- 处理说明：
  - 修正了 `NEW ORIENTAL`、`Vocabulary Workshop 2`、`英语词缀词典`、`英语学习丛书` 等明显 OCR 错项。
  - 版权/CIP 页按渲染图重录，清理了英文版权段落中的连写、错字和重复行。
- 残留问题：
  - PDF p004 中 CIP 分类行 `I．英… II．①金…②李…③南… III．英语—词根—词典 IV．H314.1-61` 原图分辨率有限，已按页面可辨形态保留省略号式写法，未擅自补全。
  - PDF p005 人名版式已规范为空格分隔文本，但未追求印刷级对齐复刻。

### A2：PDF 6-9（前言 / 使用说明）
- 结构已核：是
- 字段已核：前言标题、中英文书名、`Lecture / LECTURE`、词汇等级说明、`1,000` 与 `10,000` 等数字、使用说明页中的示例目录与示例页面说明文字
- 处理说明：
  - 将前言两页按段落重排，修正了 `Vocabulary Workshop 1/2`、`Edward L. Thorndike`、等级星号说明和“攻克英语的前提”等明显 OCR 错误。
  - 将两页“使用说明”改写为稳定 Markdown 结构，保留了页面上的说明文字、示例目录内容和 `LECTURE 1` 示意摘录。
- 残留问题：
  - PDF p009 的示例词条页为缩略示意图，摘录内容已按页面可见范围重录，但个别音标与星级仍建议在后续总审时抽样回看。

### A3：PDF 10-13（前后缀整理表）
- 结构已核：是
- 字段已核：表头 `前缀/后缀 | 含义 | 变形`；前缀 `AB` 至 `TRANS`；后缀 `AGE` 至 `FY`
- 处理说明：
  - 四页表格全部改写为 Markdown 表格，优先恢复每一行的“前缀/后缀、含义、变形”对应关系。
  - 修正了 `AD` 行 `AC→在发“k”音的辅音字母 c, q 之前`、`PRO` 行 `PR→在元音字母之前 o 脱落`、`SUPER` 行 `SUR / SUPR / SOPR` 等高风险项。
- 残留问题：
  - 个别英文语义短语采用页面可见的原样写法，如 `state, that which`、`in place of`；后续仅需做全书层面格式一致性检查，不需再按内容重写。

### A4：PDF 14-19（目录 / 分部扉页）
- 结构已核：是
- 字段已核：`LECTURE 1-200` 的编号、词根组、页码；`附录 补充词根 399`；`I. 词根索引 433`；`II. 单词索引 439`
- 处理说明：
  - 目录条目改为稳定的一行一条格式，修正了分隔符、逗号、空格和若干词根拼写污染。
  - 本轮补完了 `PDF 16-19`，纠正了 `STINCT, STING, STIG, STI·LONG`、`SAG·SCI`、`NEG·NOUNC, NUNCI`、`PHAN·MELL, MEL·POPUL` 等易错目录项。
- 残留问题：
  - 目录页已可作为正文分批的可靠分界表；若后续正文中发现标题与目录不一致，应优先回查目录页原图再统一修订。

### B1：PDF 21-23（`LECTURE 1` 起始批次）
- 结构已核：是
- 字段已核：`LECTURE 1` 标题、目录词根组注释、`词根 DUC, DUCT[DU]` 与 `词根 HOM, HUM`、跨页连续词条、首批例句
- 处理说明：
  - 按词条重排为稳定顺序：词头 -> 音标 -> 词源拆解/释义 -> 派生词/例句。
  - 修正了 `conducive`、`induce`、`production line`、`Europe from America` 等正文粘连和断裂问题。
  - 将 `HOM.HUM` 标题纠正为 `HOM, HUM`，并修复跨页引导句。
- 残留问题：
  - 音标已按人工目读统一为较干净的 Unicode 转写，但全书层面的音标风格一致性仍需后续总审。
  - `Phi Beta Kappa` 说明句已恢复连读；若后续批次发现本书统一采用不同专名写法，再做全书一致性回看。

### B2（部分）：PDF 28-33（`LECTURE 2`）
- 结构已核：是
- 字段已核：`LECTURE 2` 标题、目录词根组注释、`词根 DIC, DICT / COND / VERT, VERS / HOR`、页锚点 `PDF 29-33`、跨页词条 `jurisdiction`
- 处理说明：
  - 将整讲改写为稳定词条顺序：词头 -> 音标 -> 词源拆解/释义 -> 派生词/例句。
  - 修正了 `edict`、`indictment`、`dictatorship`、`jurisdictional`、`advertising`、`horizontal` 等 OCR 粘连、星级与错断问题。
  - 统一恢复了 `LECTURE 2` 中 4 组词根标题，并补齐了 `COND`、`VERT, VERS`、`HOR` 三组引导说明。
- 残留问题：
  - 本讲音标已按渲染图与上下文做人工标准化转写，但 `syndicate`、`tergiversate` 等个别低频词的音标仍建议在最终总审时抽样回看。

### B3（部分）：PDF 34-38（`LECTURE 3`）
- 结构已核：是
- 字段已核：`LECTURE 3` 标题、目录词根组注释、`词根 SOLV, SOLU / TOM[TEM] / JECT, JAC[JET] / LU, LAV, LAU / ROG`、页锚点 `PDF 35-38`、讲末与 `LECTURE 4` 的边界
- 处理说明：
  - 将整讲按统一顺序重排，修复了 `SOLV,SOLU`、`TOMETEM`、`JECTJACJET`、`LU.LAV.LAU` 等标题污染。
  - 修正了 `resolution`、`solution`、`abject`、`inject`、`laundry`、`arrogance` 等词条中的 OCR 粘连、词性错位、例句断裂与根注释错序问题。
  - 明确保留了 `PDF 38` 页底 `LECTURE 4` 之前的收束边界，未将下一讲内容混入本讲。
- 残留问题：
  - `appendectomy`、`hysterotomy`、`surrogate` 等个别低频或专业词条的音标采用了人工标准化转写，建议在最终总审时对照原图抽样回看。

### B4（部分）：PDF 38-43（`LECTURE 4`）
- 结构已核：是
- 字段已核：`LECTURE 4` 标题、目录词根组注释、`词根 TRUD, TRUS / VOC, VOK[VOUC, VOW, VOIC] / ERR[ARR] / ORI[ORT] / RAD, RAS[RAZ]`、页锚点 `PDF 39-43`、`PDF 38` 页底起始边界、讲末与 `LECTURE 5` 的边界
- 处理说明：
  - 按页像真值重写整讲，明确保留了 `PDF 38` 页底的 `LECTURE 4` 起始，而没有误从 `PDF 39` 才开始。
  - 修复了 `TRUD,TRUS`、`VOC,VOK`、`ERR`、`ORI`、`RAD,RAS` 等标题污染，以及 `avocation`、`provoke`、`erratic`、`originality`、`rasp` 等词条中的 OCR 粘连、释义错位和例句断裂。
  - 统一恢复了高风险字段的顺序与格式：词头、音标、根释、词性释义、派生词、例句；并守住了 `LECTURE 5` 的起讲边界。
- 残留问题：
  - `avocation`、`irrevocable`、`aborigines`、`rasp` 等个别词条音标为人工标准化转写，建议在最终总审时抽样回看。

### B5（部分）：PDF 43-47（`LECTURE 5`）
- 结构已核：是
- 字段已核：`LECTURE 5` 标题、目录词根组注释、`词根 CLAIM, CLAM / MOD / QUI / HER, HES`、页锚点 `PDF 44-47`、`PDF 43` 页底起始边界、讲末与 `LECTURE 6` 的边界
- 处理说明：
  - 将整讲按统一格式重排，修复了 `CLAIMCLAM`、`词根HER，HES`、`mode/model` 串行、`acquiesce` 与 `coherent` 跨页错断等问题。
  - 重点清理了 `claim / clamor / counterclaim / exclamation / accommodate / commodity / tranquility / adhere / incoherent` 等词条中的 OCR 粘连、英文句子连写、词性错位与派生项混排。
  - 明确保留了 `PDF 47` 页内的双讲边界：先收束 `LECTURE 5`，再单独起 `LECTURE 6`，没有把 `词根 FLU` 混入本讲。
- 残留问题：
  - `démodé`、`modus operandi`、`inherent` 等个别音标与星级虽已按页像重录，仍建议在最终总审中抽样复看 `PDF 45-47`。

### B6：PDF 47-62（`LECTURE 6`）
- 结构已核：是
- 字段已核：`LECTURE 6` 标题、目录词根组注释、`词根 FLU / LEG, LECT[LIG, LEAG] / PAR[PAIR, PER, PIR, PEER] / PEND, PENS[POND, PENC] / SPECT, SPEC[SPIC, SPI, SPY]`、页锚点 `PDF 48-62`、讲末与 `LECTURE 7` 的边界
- 处理说明：
  - 将整讲改写为稳定词条顺序：词头 -> 音标 -> 词源拆解/释义 -> 派生词/例句。
  - 本轮补完并重写了后半讲 `PAR / PEND, PENS / SPECT, SPEC`，修复了 `transparent / apparatus / separation / pendant / suspension / perspective / suspicion` 等词条中的 OCR 脏字符、跨页断裂、英文连写与词性错位。
  - 统一恢复了 `LECTURE 6` 内 5 组词根标题与页锚点，并明确保留了 `PDF 62` 页底 `LECTURE 7` 起始边界。
- 残留问题：
  - 本讲个别星级与音标已按页像和上下文做人工标准化转写，后续总审时仍建议对 `PAR` 与 `SPECT, SPEC` 两组中的高频词抽样回看。

### B7：PDF 62-67（`LECTURE 7`）
- 结构已核：是
- 字段已核：`LECTURE 7` 标题、目录词根组注释、`词根 SAL[SUL, SIL, SAIL, SAUL] / VENG / CEL, CELER / EQU[IQU]`、页锚点 `PDF 63-67`、`PDF 62` 页底起始边界与 `LECTURE 8` 的交界
- 处理说明：
  - 将整讲按词头 -> 音标 -> 词源拆解/释义 -> 派生词/例句的顺序重写，清理了 `VENG / CEL, CELER / EQU` 三组中大量 OCR 粘连、英文连写和 IPA 脏字符。
  - 修复了 `sally / avenge / revengeful / accelerate / adequate / equality / equivalence / unequivocal` 等词条中的星级、词性和例句错位问题。
  - 明确保留了 `PDF 64-67` 的页锚点，并保持 `LECTURE 8` 仍从 `PDF 67` 页底之后单独起讲。
- 残留问题：
  - `SAL` 与 `EQU` 组内个别音标和星级为人工标准化转写，后续总审时宜抽查 `PDF 64-67` 的高频词频级一致性。

### B8：PDF 67-71（`LECTURE 8`）
- 结构已核：是
- 字段已核：`LECTURE 8` 标题、目录词根组注释、`词根 FLICT / LIG[LI, LEAG, LY] / VAL[VAIL] / COR, CORD[COUR]`、页锚点 `PDF 68-71`、`PDF 67` 页底起始边界与 `LECTURE 9` 的交界
- 处理说明：
  - 将整讲按统一词条顺序重排，修复了 `alliance / obligate / liability / ambivalent / invalidate / equivalent / accord / courage / record` 等词条中的 OCR 粘连、例句错断和根注释错序。
  - 恢复了 `FLICT`、`LIG`、`VAL`、`COR` 四组的完整引导说明，并将 `record` 的名词/动词双读音与 `cordial`、`discordant` 等高风险字段重新校正。
  - 保留了 `PDF 68-71` 页锚点与 `PDF 71` 页底 `LECTURE 9` 起讲边界，没有把下一讲内容混入本讲。
- 残留问题：
  - `VAL` 组中的部分英式/美式 IPA 采用了人工标准化写法，后续总审时建议对 `prevail / valour / valuable` 等词条抽样回看。

### B9：PDF 71-74（`LECTURE 9`）
- 结构已核：是
- 字段已核：`LECTURE 9` 标题、目录词根组注释、`词根 APT[EPT, ATT] / LOT / NE[NA, NO, N] / PAC, PEAS`、页锚点 `PDF 72-74`、`PDF 71` 页底起始边界与 `LECTURE 10` 的交界
- 处理说明：
  - 将整讲按统一结构重写，修复了 `adapt / aptitude / allot / lottery / neuter / neutrality / appease / pacific` 等词条中的 OCR 错拼、根标题损坏和例句断裂。
  - 将错误标题 `词根 NENA,NO,]` 纠正为 `词根 NE[NA, NO, N]`，并恢复了 `PAC, PEAS` 组的完整引导说明。
  - 明确保留 `PDF 72-74` 页锚点，并守住 `PDF 74` 页底 `LECTURE 10` 起讲边界。
- 残留问题：
  - `NE` 组的个别音标与 `naught / nought` 组合写法已按页像标准化，建议在最终总审时再抽查 `PDF 73-74`。

### B10：PDF 74-97（`LECTURE 10-15`）
- 结构已核：是
- 字段已核：`LECTURE 10-15` 标题、目录词根组注释、`词根 SERT / CED, CESS [CEED, CEAS] / PLIC, PLY, PLI, PLE, PLEX, PLO / JOURN / VEN, VENT / GRAV [GRIEV] / NEX, NECT / NIHIL / PORTION / PRECI[PRAIS, PRIS, PRIC, PRIZ] / SPIR / SIMIL[SIMUL] / SUR / CLIM / ALI, ALTER[ULTER, ALTRU] / FIL / LEV[LIEV] / LUD, LUS / PALL / PREHEND, PREHENS[PREN, PREGN, PRIEV] / CERT / SENT, SENS / SAT[SET]`、页锚点 `PDF 74-97`、`LECTURE 12-15` 的跨页起讲边界与 `LECTURE 16` 的下一起点
- 处理说明：
  - 本批正文已覆盖 `LECTURE 10` 至 `LECTURE 15`，并补齐、核稳了六讲内部的章节标题、词根组引导、词条顺序和页锚点链路。
  - 已重点复核高风险字段，包括多变体词根标题 `CED, CESS [CEED, CEAS]`、`PRECI[PRAIS, PRIS, PRIC, PRIZ]`、`ALI, ALTER[ULTER, ALTRU]`、`PREHEND, PREHENS[PREN, PREGN, PRIEV]`、`SENT, SENS`、`SAT[SET]`，以及 `GRAV [GRIEV]`、`LEV[LIEV]` 等易串讲字段。
  - 已守住页内边界控制：`PDF p084` 内转入 `LECTURE 12`，`PDF p087` 内转入 `LECTURE 13`，`PDF p089` 内转入 `LECTURE 14`，`LECTURE 15` 起于 `PDF p094`，并确认下一起点为 `LECTURE 16 @ PDF p098`，未将相邻讲内容混入。
- 残留问题：
  - `LECTURE 10-15` 中仍有部分 IPA、星级和低频词形属于人工标准化转写，最终总审时建议优先抽查 `PRECI / SPIR / ALI, ALTER / PREHEND, PREHENS / SENT, SENS` 几组所在页，核对频级与音标风格一致性。

### B11：PDF 98-151（`LECTURE 16-25`）
- 结构已核：是
- 字段已核：`LECTURE 16-25` 标题、目录词根组注释、页锚点 `PDF 98-151`、`LECTURE 24/25` 于 `PDF p144` 的同页边界、`LECTURE 25/26` 于 `PDF p151` 的同页边界；重点复核了 `MENT / PACT / PLE, PLET, PLI, PLY, PLEN / PRESS / CEPT, CAP, CAPT` 与 `FER / FISC / SEQU, SECUT / SERV` 等高风险词根组
- 处理说明：
  - 已汇总并落盘此前已完成的 `LECTURE 16-23`，并在本轮补完 `LECTURE 24-25` 的整段人工校勘；删除了 `LECTURE 22-25` 一带残留的裸印刷标题行，修正了词根标题污染、正文粘连、页内错断与跨页衔接。
  - `LECTURE 24` 已按 `PDF p136-p144` 重构为稳定顺序，清理了 `MENT / PACT / PLE, PLET, PLI, PLY, PLEN / PRESS / CEPT, CAP, CAPT, CEIV` 内的词头、音标、释义与例句。
  - `LECTURE 25` 已按 `PDF p144-p151` 重构为稳定顺序，守住了 `FER / FISC / SEQU, SECUT[SU] / SERV` 的边界，并补充使用新渲染页图 `p-145.png` 至 `p-152.png` 作为后半批次真值来源。
- 残留问题：
  - `LECTURE 16-25` 中仍有少量词头频级标记与 IPA 属人工标准化转写，最终总审时宜抽查 `PDF p136-p151` 的高密度页。
  - `LECTURE 24` 中 `impression` 例句“蜡上面的〔?〕印”保留 1 个未决字形；`LECTURE 25` 中 `vociferation` 中文释义首字仍以 `〔?〕` 标记。


### B12：PDF 152-191（`LECTURE 26-35`）
- 结构已核：是
- 字段已核：`LECTURE 26-35` 标题、目录词根组注释、页锚点 `PDF 152-191`、`LECTURE 30/31` 于 `PDF p176` 的讲间边界、`LECTURE 35/36` 于 `PDF p191` 的讲间边界；重点复核了 `CRESC, CRET / CUB, CUMB / AN / CURR, CURS / WARD, GUARD / ACT / PRIS / PUNCT, PUNG / CLUD, CLUS / DOL / FLAGR, FLAM / SECR, SACR, SANCT / ROD, ROS / ALESC / LAT / MISER / COC, COCT / STERN / TANG, TACT, TING / ROB / PLAC / DIGN` 等高风险词根组。
- 处理说明：
  - 本批已将 `LECTURE 26-30` 与 `LECTURE 31-35` 全部按页图真值合并回 `ocr.md`，补齐了页内起讲、跨页续条、词根说明块和词条顺序，并清理了裸印刷标题、OCR 连写、IPA 污染、词性错位与例句断裂。
  - 已重点守住 `PDF p176` 页内 `LECTURE 30` 收束与 `LECTURE 31` 起讲边界，以及 `PDF p191` 页底 `LECTURE 35` 收束与 `LECTURE 36` 下一起点，未把相邻讲内容混入。
  - `LECTURE 31-35` 内的高密度讲次已逐页人工整理，重点修正了 `PRIS / PUNCT, PUNG / CLUD, CLUS / SECR, SACR, SANCT / TANG, TACT, TING / DIGN` 等组中词头、音标、词根变体标题和例句英文连写问题。
- 残留问题：
  - `LECTURE 26-35` 中仍有少量 IPA、星级与低频词形属于人工标准化转写；最终总审时宜优先抽查 `PDF p176-p191` 的高密度页与两处同页转讲边界。
  - `LECTURE 31-35` 的宗教词汇、低频法语/拉丁语借词和部分专名较密，后续总审时建议抽查 `sanctimonious / sacrosanct / mare clausum / latitudinarian / complacent / condign` 等词条。

### C1：PDF 418-419（附录开头）
- 结构已核：是
- 字段已核：附录标题、页字母 `A`、双栏阅读顺序、词根 1-28 的主项顺序
- 处理说明：
  - 将原先左右栏交错污染的内容改为“左栏 1-14 -> 右栏 15-28”的人工顺序。
  - 修正了 `Appendix` 标题残缺、`盎格鲁-撒克逊人` 等明显错误。
- 残留问题：
  - 附录页音标密度极高，个别音标为人工标准化转写，后续仍应抽样回看。

### C2（部分）：PDF 420（附录续页）
- 结构已核：是
- 字段已核：`anthracoid -> 痈状的` 跨页续行；词根 29-51 的双栏顺序；`arter / arthr / aster / atlant / aur` 等高风险词根名
- 处理说明：
  - 按“左栏自上而下，再右栏自上而下”的顺序重录整页，并把 `40. arter` 的续项 `arterial / arteriosclerosis` 放回 `41. arthr, art` 之前。
  - 解决了 p419 末行 `anthracoid` 跨页残缺问题，补齐为“似炭疽的，似痈的，痈状的”。
- 残留问题：
  - 本页大量音标与星级系人工目读标准化转写，后续宜与原图做一次抽样二审；`PDF 421-451` 尚未系统复核。

### D1：PDF 452（词根索引扉页）
- 结构已核：是
- 字段已核：`# 索引`、`## I. 词根索引`、说明文字
- 处理说明：
  - 去除了 OCR 产生的缩进噪声与重复空白，保留原页语义。

### D2（封面页）：PDF 458（单词索引扉页）
- 结构已核：是
- 字段已核：`## II. 单词索引`、说明文字
- 处理说明：
  - 将误识别的 `I.单词索引` 改正为 `II. 单词索引`。

### E1：PDF 503（PDF 附带元数据页）
- 结构已核：是
- 字段已核：标题、来源说明、统计项
- 处理说明：
  - 单独归类为 `# PDF 附带元数据`，与原书正文明确隔离。
  - 将混乱重复的文本恢复为一段说明和一个 JSON 代码块。

## 未决问题清单

- p004：CIP 分类行的省略号式缩写未扩写，保留页面可见形态。
- p009 / p420：示意页与附录页中存在较多人工标准化音标转写，仍应在最终总审中抽样回看。
- p043-p047：`LECTURE 5` 中 `MOD / QUI / HER, HES` 若后续全书音标风格统一时回看，可优先抽查 `démodé`、`modus operandi`、`inherent`。
- p047-p062：`LECTURE 6` 中 `imperative / empire / pension / suspect` 等词条的星级与个别音标已按页像重录，最终总审时宜再抽 1-2 页核对频级一致性。
- p063-p074：`LECTURE 7-9` 中 `SAL / EQU / VAL / NE` 的部分 IPA 与个别星级采用了人工标准化转写，最终总审时宜抽 2-3 页统一频级与音标风格。
- p074-p097：`LECTURE 10-15` 中 `PRECI / SPIR / ALI, ALTER / PREHEND, PREHENS / SENT, SENS` 等组别含较多多变体词根标题、低频词形与人工标准化音标，最终总审时宜抽 2-3 页回看边界页与高密度词条页。
- p098-p151：`LECTURE 16-25` 已完成人工清洗，但频级标记与少量 IPA 仍含人工标准化成分；最终总审时宜抽 2-3 页复看 `LECTURE 24-25` 的高密度页与同页转讲边界。
- p152-p191：`LECTURE 26-35` 已完成人工清洗，但部分 IPA、星级与低频词形仍含人工标准化成分；最终总审时宜抽查 `PDF p176-p191` 的高密度页、`LECTURE 30/31` 与 `LECTURE 35/36` 的同页转讲边界，以及 `SECR, SACR, SANCT / TANG, TACT, TING / DIGN` 等高风险组。
- 全书范围：音标转写目前只在已核批次做了清洗，尚未完成全书风格一致性检查。

## 待续批次

- B13-Bn：PDF 192-417（正文 `LECTURE 36-200`）
- C2 后续：PDF 421-451（附录余下双栏页）
- D1-Dn：PDF 453-457、459-502（词根索引正文 / 单词索引正文）

## 本轮验收动作

- 保留页锚点格式 `<!-- PDF pXXX | book pY -->`
- 已修改高风险页后，重新检查了对应锚点、章节标题和索引边界未被破坏
- 已额外核对：
  - `ocr.md` 中 `<!-- PDF p... -->` 页锚点总数仍为 `503`
  - `## LECTURE` 标题总数仍为 `200`
- 待下一轮继续前，建议优先扩展到：
  - B13：正文 `LECTURE 36-40` 或更后续批次
  - C2 后续：附录 `PDF 421-451`
  - D1 正文起始页：PDF 453（词根索引正文）
