# `ocr.md` 人工核查记录

- 核查日期：2026-05-13
- 真值来源：源 PDF 渲染页图像；`ocr.md` 与 PDF 文本层仅作辅助
- 当前交付状态：已完成前置部分高风险页、目录页、正文 `LECTURE 1-200`、附录开头与附录续页 `PDF 420` 的人工修订；正文已闭环，全书尚未完成逐页人工核查

## 已完成批次

### B15：PDF 310-336（`LECTURE 101-125` 深校收口）
- 结构已核：是
- 字段已核：`LECTURE 101-125` 标题、目录词根组注释、页锚点 `PDF 310-336`；重点复核 `SCEN / LOQU, LOCUT / OD / DOX / SIT / ALL / GON / PHRAS, PHA, PHE, PHU / OXY[OX] / METER[METR] / JUR / VAD, VAS[WAD] / ANN[ENN] / MEA[ME] / FUNCT / CAU / MAT / SUMPT, SUM / DOMIN / AMBUL[AMBL] / POSTER / MED / TEXT / MON[MIN] / SAG / SCI / CUR / MONT, MOUNT / FUS, FUT, FUND, FOUND`
- 处理说明：
  - 结合 `tmp/pdfs/round3_l101_125/` 页图与对应文本层，连续回扫并补齐了 `LECTURE 101-125` 的讲次边界、词根说明、跨页续条、例句连写和页内错位问题。
  - 已核稳 `LECTURE 109-118`，清除了此前残留的脏串、重复行和半旧半新混排；并进一步收口 `LECTURE 119-125`，重点修复了 `POSTER / MED·TEXT / MON / SAG·SCI / CUR / MONT,MOUNT / FUS,FUT,FUND,FOUND` 一带的结构和正文。
  - 已按页图收束 `LECTURE 125` 后半页高风险脏段，确认 `diffusion / infuse / refuse / suffuse / transfusion / fusion / confound / refute / futile` 等条目已回到可持续复审的稳定状态。
- 残留问题：
  - `LECTURE 101-125` 仍有少量 IPA、频级和低频词形属于人工标准化转写，最终总审时宜抽查 `PDF p329-p337` 的高密度页与 `LECTURE 120 / 122 / 125` 的页内转讲、跨页续条位置。
  - 正文主流程已闭环；附录与双索引仍需逐页核对。

### B15-A：PDF 275-286（`LECTURE 70-81` 深校收口）
- 结构已核：是
- 字段已核：`LECTURE 70-81` 标题、目录词根组注释、页锚点 `PDF 275-286`；重点复核 `HILAR / HORT / PI / PURG / TRIC·BULL·FIG / MAN·MEND·NERV / FET / MERS, MERG / CALCUL / GRAN / IT·NOV / TIM / PART / FLAT / ORD, ORDIN`
- 处理说明：
  - 结合 `tmp/pdfs/round3_l70_l73/`、`tmp/pdfs/round3_l76_100/` 页图与 `tmp/p255_p336_from_pdf.txt`，对正文最后残留的 `LECTURE 70-81` 做了逐页深校和小块收口。
  - 清理了讲间残留脏行、例句断裂、连写污染、个别词头/词性/说明行错位，并修复了 `LECTURE 74-81` 一带的若干显性错项，如括号错配、中文错字、词组粘连与重复讲次标头。
  - 已确认 `LECTURE 70-81` 与相邻 `LECTURE 69 / 82` 的页锚点和讲次边界保持稳定，正文主流程至此闭环。
- 残留问题：
  - `LECTURE 70-81` 仍有少量 IPA 与低频词形属于人工标准化转写，最终总审时宜抽查 `PDF p279-p286` 的高密度页与 `LECTURE 77 / 79 / 81` 的页内长条目。

### B14：PDF 286-309（`LECTURE 82-100` 深校推进）
- 结构已核：是
- 字段已核：`LECTURE 82-100` 标题、目录词根组注释、页锚点 `PDF 286-309`；重点复核 `VET / VULN[VULT] / MUT / PUGN / ANIM·AVI / CALC[CULC] / FIRM / SCRUT / SURG, SURRECT / TEMPER / VEH, VECT[VEIGH, VEX] / PECU / TURB / OR / NAT, NASC[NAISS, NAIV]`
- 处理说明：
  - 结合 `tmp/pdfs/round3_l76_100/` 页图，重点回看了 `p-301.png` 至 `p-309.png` 与对应裁图，补齐并清理了 `LECTURE 82-100` 内高风险 OCR 噪声、词根标题污染、英文连写和页内续条错位。
  - 已核稳 `LECTURE 92-100`，重写了 `MUT / PUGN / ANIM·AVI / CALC·FIRM / SCRUT / SURG,SURRECT / TEMPER / VEH,VECT / PECU / TURB / OR / NAT,NASC` 等脏段，确认 `mutual*** / affirm*** / confirm*** / insurgent*** / temperature*** / vehicle*** / disturb*** / adore*** / national*** / native*** / renaissance***` 等条目的星级与主体释义。
  - 已回扫 `sinous / commutean / wentontowinthegame / Ithinkanimaltesting / unanimous+*+` 等前序高风险脏词，确认相关讲次已无旧污染残留。
- 残留问题：
  - `LECTURE 82-100` 仍有少量 IPA、频级与低频词形属于人工标准化转写，最终总审时宜抽查 `PDF p301-p309` 的高密度页与 `LECTURE 94/95`、`99/100` 的页内转讲边界。
  - 正文主流程已闭环；附录与双索引仍需逐页核对。

### B13-P：PDF 255-274（`LECTURE 59-69` 深校收口）
- 结构已核：是
- 字段已核：`LECTURE 59-69` 标题、目录词根组注释、页锚点 `PDF 255-274`；重点复核 `NUMER / ALT[HAUT] / STINCT, STING, STIG, STI / LONG / RADIC[RADIS] / LIP / MANU[MAN] / HOD[OD] / ORB / TERMIN / LUC[LUX, LUS] / EMPT, EM[EEM, MPT, M, ANSOM] / TOL / GREG / LIC / RUD / VAN[VAIN]`
- 处理说明：
  - 以 `tmp/pdfs/round4_l59_69/p-255.png` 至 `p-274.png` 页图为准，回查了此前批量修订后最可疑的星级、重复行和连写污染。
  - 已确认并保留 `numerous*** / manipulate** / manifest*** / manifestation** / manual*** / manufacture*** / manufacturer*** / manure*** / periodical*** / translucent** / Lucifer** / lustre*** / lusty** / illustrative** / segregate** / aggregate*** / congregation*** / leisurely*** / rudimentary** / evanescent**` 等条目。
  - 已修复 `numerable` 重复条、`vain*` 星级回退，以及 `elicitation / illicitly / leisure / leisurely / rudimentary / evanescence` 附近的连写、空格和断行错误。
- 残留问题：
  - `LECTURE 59-69` 仍有少量 IPA 细节属于低收益人工标准化问题，可放到全书最终总审时抽样处理。
  - 正文主流程已闭环；附录与双索引仍需逐页核对。

### B13：PDF 364-387（`LECTURE 151-188` 深校续推）
- 结构已核：是
- 字段已核：`LECTURE 151-188` 标题、目录词根组注释、页锚点 `PDF 364-387`；重点复核了 `VERB / MIR / CHRON / PROX / CUSS / DOC / CULP, PECC / CEL / MAR / OP, OPT, OPHTHALM / MATR, PATR / REG / CRUC / COLOSS / NOCT / NOMIN / BAN / PRIM / DIG / RAD / VIG / FERV / DORM / MILIT / VAG / DULG / CHAL / OP / SOMN / CORP / MUN / COMIT / MORD, MORS / CLAR / MERC / BAT / AUG, AUCT / MAND, MEND / MIM / GRAPH, GRAM / CAUST, CAUT / CRAT, CRACY / THET, THES / AX / POLIT / EGYR / ECO / LITH / NARC / PRAG, PRACT / PTO / NOT / VOR / DEXTR / CAVAL / MAGN / GRAT / MERIT` 等高风险组。
- 处理说明：
  - 结合 `tmp/pdfs/round3_l151_200/p-364.png` 至 `p-387.png` 页图，持续清理了 `LECTURE 151-188` 中的高置信 OCR 噪声，修复了词根标题、词性、星级、例句英文连写、中文错字与少量标点污染。
  - 已特别修正 `LECTURE 167-176` 内的高密度问题，如 `optional / autopsy / optical illusion / regular / sovereign / nominal / denomination / banal / vigilant / invigilate / operational / somnolent / corpulence / munificent` 等词条。
  - 已继续顺推 `LECTURE 177-188`，按页图修复了 `concomitant / remorse / clarify / declare / arbitrary / auxiliary / mandatory / command / mimic / telegraph / bureaucratic / synthetic / politic / economy / notorious / voracious / ambidextrous / chivalrous / magnanimous / gratuitous / meritorious` 等词条中的显著 OCR 错项。
- 残留问题：
  - `LECTURE 151-188` 内仍有少量 IPA 细节、星级风格与低频词形属于人工标准化转写，最终总审时宜抽查 `PDF 375-387` 的高密度页。

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
- p152-p200：`LECTURE 26-35` 与 `LECTURE 151-200` 已完成人工清洗，但部分 IPA、星级与低频词形仍含人工标准化成分；最终总审时宜抽查 `PDF p176-p191` 的高密度页、`LECTURE 30/31` 与 `LECTURE 35/36` 的同页转讲边界，以及 `SECR, SACR, SANCT / TANG, TACT, TING / DIGN` 等高风险组。
- p286-p309：`LECTURE 82-100` 已完成人工清洗，但 `MUT / FIRM / TEMPER / NAT,NASC` 等页仍有少量 IPA 与频级属于人工标准化转写；最终总审时宜抽查 `PDF p301-p309` 的高密度页与 `LECTURE 94/95`、`99/100` 的页内转讲边界。
- 全书范围：音标转写目前只在已核批次做了清洗，尚未完成全书风格一致性检查。

## 待续批次

- C2 后续：PDF 421-451（附录余下双栏页）
- D1-Dn：PDF 453-457、459-502（词根索引正文 / 单词索引正文）

## 本轮验收动作

- 保留页锚点格式 `<!-- PDF pXXX | book pY -->`
- 已修改高风险页后，重新检查了对应锚点、章节标题和索引边界未被破坏
- 已额外核对：
  - `ocr.md` 中 `<!-- PDF p... -->` 页锚点总数仍为 `503`
  - `## LECTURE` 标题总数仍为 `200`
- 待下一轮继续前，建议优先扩展到：
  - C2 后续：附录 `PDF 421-451`
  - D1 正文起始页：PDF 453（词根索引正文）

## 增补记录（2026-05-10）

### B13-C：PDF 224-228（`LECTURE 45-47`）
- 结构已核：是
- 字段已核：
  - `LECTURE 45`：`FAC / MEN[MEAN]`
  - `LECTURE 46`：`LEC[LET, LIC, LIG] / LIN, LIGN`
  - `LECTURE 47`：`LINQU[LIC, LICT] / PREC / PRED`
  - 页锚点：`<!-- PDF p225 | book p206 -->`、`<!-- PDF p226 | book p207 -->`、`<!-- PDF p227 | book p208 -->`、`<!-- PDF p228 | book p209 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/p-224.png` 到 `p-228.png` 为真值，重建了 `LECTURE 45-47`。
  - 修复了此前 `LECTURE 45` 整块串入别讲内容的严重错位问题；原 `FAC / MEN` 讲次现已按页图恢复。
  - 纠正了高风险字段：词根标题、词头、例句英文连写、跨页续行，以及 `LEC·LIN, LIGN`、`LINQU[LIC, LICT]` 等易错标题。
  - `LECTURE 45` 的 `book p205` 起讲点位于 `PDF p224` 页中部，页锚点继续保留在上一讲内；本次未改动该锚点位置，只修正讲内正文。
- 残留问题：
  - 少量音标与个别星级仍属于人工标准化转写，最终总审时宜优先回看 `PDF p224-p228`。
  - 建议重点抽查：`facial / commence / promenade / delicatessen / lineal / deprecate / depredation`。

### B13-D：PDF 214-224（`LECTURE 43-44`）
- 结构已核：是
- 字段已核：
  - `LECTURE 43`：`CREP / MOL, MOLL`
  - `LECTURE 44`：`RID, RIS / ST, STAT, STIT, SIST`
  - 页锚点：`<!-- PDF p215 | book p196 -->`、`<!-- PDF p216 | book p197 -->`、`<!-- PDF p217 | book p198 -->`、`<!-- PDF p218 | book p199 -->`、`<!-- PDF p219 | book p200 -->`、`<!-- PDF p220 | book p201 -->`、`<!-- PDF p221 | book p202 -->`、`<!-- PDF p222 | book p203 -->`、`<!-- PDF p223 | book p204 -->`、`<!-- PDF p224 | book p205 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/p-214.png` 到 `p-224.png` 为真值，正式并入并复核了此前仅存在于 `tmp/lecture43_44_replacement.md` 的 clean draft。
  - 清除了原块中大量的 OCR 粘连、音标脏字、词根标题错形和例句断裂，恢复了 `CREP / MOL, MOLL / RID, RIS / ST, STAT, STIT, SIST` 的正常层级与词条顺序。
  - 重点守住了 `PDF p215` 页底转入 `LECTURE 44` 的讲间边界，以及 `PDF p224` 页顶 `insistent -> transistor` 收束后转入 `LECTURE 45` 的页内边界。
- 残留问题：
  - 少量 IPA 与个别星级仍属于人工标准化转写，最终总审时宜回看 `extant / constitution / obstinate / sectionalism / coexistence` 等高密度词条页。

### B13-E：PDF 229-231（`LECTURE 48`）
- 结构已核：是
- 字段已核：
  - `LECTURE 48`：`CRED[CREED, CRE] / CRET, CERN[CREET, CRE] / EST, ESS, ENT`
  - 页锚点：`<!-- PDF p229 | book p210 -->`、`<!-- PDF p230 | book p211 -->`、`<!-- PDF p231 | book p212 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/p-229.png` 到 `p-231.png` 为真值，重建了 `LECTURE 48` 的三组词根与整讲条目顺序。
  - 修复了此前 `CRET / CERN`、`EST / ESS / ENT` 组内的断行、误拼、释义错位与例句英文连写问题。
  - 同步确认 `PDF p232 | book p213` 不属于 `LECTURE 48`，而属于下一讲 `LECTURE 49` 的起讲页。
- 残留问题：
  - `creditable / concern / quintessence` 等条目的少量 IPA 与频级标记仍建议在总审时抽查一次。

### B13-F：PDF 232-235（`LECTURE 49`）
- 结构已核：是
- 字段已核：
  - `LECTURE 49`：`SECT / LAPID / MIN[MEN]`
  - 页锚点：`<!-- PDF p232 | book p213 -->`、`<!-- PDF p233 | book p214 -->`、`<!-- PDF p234 | book p215 -->`、`<!-- PDF p235 | book p216 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/p-232.png` 到 `p-235.png` 为真值，整讲重写了 `LECTURE 49`，并补回缺失的 `PDF p232` 起讲锚点。
  - 恢复了 `SECT` 页首词根说明、`LAPID` 与 `MIN[MEN]` 的分组边界，以及 `minus` 跨页续例到 `PDF p235` 的衔接。
  - 清除了原块中的词根说明错位、条目粘连、英中混排错断和 `LECTURE 50` 前的页内脏字符。
- 残留问题：
  - `intersect / preeminent / ministerial / minutiae` 等条目的 IPA 与个别星级采用了人工标准化转写，后续总审时宜优先抽查 `PDF p232-p235`。

### B13-G：PDF 238-241（`LECTURE 51-52`）
- 结构已核：是
- 字段已核：
  - `LECTURE 51`：`VERG`
  - `LECTURE 52`：`VULG[MULG] / FID[FI, FY, FEDER, FEAL]`
  - 页锚点：`<!-- PDF p238 | book p219 -->`、`<!-- PDF p239 | book p220 -->`、`<!-- PDF p240 | book p221 -->`、`<!-- PDF p241 | book p222 -->`
- 处理说明：
  - 采用子代理并行起草、主线程并入复核的方式，先修复了 `PDF p238` 同页内 `LECTURE 50 -> 51 -> 52` 的连续边界，再并入 `LECTURE 51-52` 的整讲替换块。
  - `LECTURE 51` 已恢复为 `VERG` 单讲，并明确其起讲位置依附于 `PDF p238` 既有页锚点，不误并到下一页。
  - `LECTURE 52` 已按 `PDF p239-p241` 恢复 `VULG[MULG] / FID[...]` 两组词根及条目顺序，清理了词根说明灰字、词条粘连和英中混排错断。
- 残留问题：
  - `verge / vulgarian / bona fide / confederation / fealty` 等条目的 IPA 与少量频级标记仍含人工标准化成分，后续总审时宜优先抽查 `PDF p238-p241`。

### B13-H：PDF 235-238（`LECTURE 50`）
- 结构已核：是
- 字段已核：
  - `LECTURE 50`：`PEL, PULS[PEAL] / SUAD, SUAS[SUAV] / ARM`
  - 页锚点：`<!-- PDF p236 | book p217 -->`、`<!-- PDF p237 | book p218 -->`、`<!-- PDF p238 | book p219 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/p-235.png` 到 `p-238.png` 为真值，重建了 `LECTURE 50` 全块，修复了 `PEL, PULS[PEAL]`、`SUAD, SUAS[SUAV]`、`ARM` 三组词根说明与条目顺序。
  - 重新校正了 `dispel / impel / expulsion / repellent / appeal / compel / propel / pulse / dissuade / persuade / suave / alarm / armistice / armor / army` 等高风险词条中的 OCR 粘连、音标脏字符和释义错位。
  - 明确保住了 `PDF p238` 同页内 `LECTURE 50 -> LECTURE 51` 的讲间边界，没有把 `VERG` 误并入本讲，也没有把 `ARM` 词条截断。
- 残留问题：
  - `repellent / appeal / propellant / forearm / armada` 等个别条目的 IPA 与频级仍带少量人工标准化成分，后续总审时宜优先回看 `PDF p236-p238`。

## 增补记录（2026-05-11）

### B13-I：PDF 250-252（`LECTURE 57`）
- 结构已核：是
- 字段已核：
  - `LECTURE 57`：`POT[POW, POSS] / PASS / BOL,BL,BAL`
  - 页锚点：`<!-- PDF p251 | book p232 -->`、`<!-- PDF p252 | book p233 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/p251_fix.png`、`hires-251.png`、`hires-252.png` 为真值，重建了 `LECTURE 57` 的 `PASS` 与 `BOL, BL, BAL` 两段，补正了页内换行、词头星级、词根拆解和例句连写。
  - 同步修正了 `potentiality`、`passer-by`、`pastime`、`emblem`、`parable`、`balance` 等高风险词条的频级与释义错位问题。
  - 该批保留了 `PDF p250` 页内讲首与上一讲收尾的自然衔接，不跨越到 `LECTURE 58`。
- 残留问题：
  - `problematic / embolism / balanced` 等少数词条的 IPA 与中文义项已按图像校正，但后续总审时仍建议抽查一次原页。

### B13-J：PDF 253-254（`LECTURE 58`）
- 结构已核：是
- 字段已核：
  - `LECTURE 58`：`BAR / BODY / CROCH[CROACH, CROUCH, CROTCH, CRUTCH, CROOK]`
  - 页锚点：`<!-- PDF p253 | book p234 -->`、`<!-- PDF p254 | book p235 -->`
- 处理说明：
  - 以 `tmp/pdfs/round2_l26_l100/l58-253.png`、`l58-254.png` 为真值，重写了 `LECTURE 58` 的 `BAR`、`BODY`、`CROCH` 三组词根说明与条目顺序。
  - 修复了 `embargo / barrage / embarrassment / barrel / embody / bodily / buddy / encroach / crutch / crook / crooked` 等高风险词条中的 OCR 粘连、词性错位、音标脏字符与讲内标题损坏。
  - 明确保住了 `PDF p254` 页底 `LECTURE 58 -> LECTURE 59` 的页内讲间边界，未把 `GROSS` 组并入本讲。
- 残留问题：
  - `encroach` 例句中文译文、`barrage` 的渠/堰义项注音、以及个别英式 IPA 仍建议在总审时对照原页再抽查一次。

### 进度覆盖说明（更新至 2026-05-11 本轮）
- 当前已确认深校：`LECTURE 36-58`
- 当前已完成首轮结构/高风险字段修补：`LECTURE 59-69`
- 当前仍待逐页深校：`LECTURE 59-200`、附录 `PDF 421-451`、索引正文 `PDF 453-457` 与 `PDF 459-502`

### B13-K：PDF 191-193（`LECTURE 36` 补充核查）
- 结构已核：是
- 字段已核：
  - `LECTURE 36`：`SIGN / SUMM`
  - 页锚点：`<!-- PDF p191 | book p172 -->`、`<!-- PDF p192 | book p173 -->`、`<!-- PDF p193 | book p174 -->`
- 处理说明：
  - 对照 `l36-191.png`、`l36-192.png`、`l36-193.png` 复核 `LECTURE 36` 段，未见需要修正的明显 OCR 错字，也未发现缺失页锚点。
  - 本次仅补记核查结果，正文保持不动。
- 残留问题：无

### B13-L：PDF 254-274（`LECTURE 59-69` 首轮结构修补）
- 结构已核：是
- 字段已核：
  - `LECTURE 59-69` 词根标题：`GROSS[GROC] / AM[EM, IM, M] / CUMB, CUB / PER[PIR, PAR] / NUMER / ALT[HAUT] / STINCT, STING, STIG, STI / LONG / RADIC[RADIS] / LIP / MANU[MAN] / HOD[OD] / ORB / TERMIN / LUC[LUX, LUS] / EMPT, EM[EEM, MPT, M, ANSOM] / TOL / GREG / LIC / RUD / VAN[VAIN]`
  - 页锚点：`<!-- PDF p254 | book p235 -->` 至 `<!-- PDF p274 | book p255 -->`
- 处理说明：
  - 对照 `tmp/pdfs/task_36_59_69/render254-254.png` 与 `l59_69-255.png` 至 `l59_69-273.png`，修复了 `LECTURE 59-69` 内被 OCR 打坏的讲标题、词根标题和若干显著词头。
  - 本轮已明确修正 `tailor / belladonna / bellicose / rebel / imperil / pirate / elucidate / illustration / luxury / luxurious / redemptive / rude` 等高风险字段，并校直了 `LECTURE 59-69` 的讲内词根边界。
  - 本轮仍以结构和高风险字段为主，没有对 59-69 的全部词头星级、IPA 和例句逐条重录。
- 残留问题：
  - `LECTURE 59-69` 内仍有少量星级、IPA、英文例句粘连和个别词头残点，后续总审时应优先回看 `searchlight / peril / prompt / vanish / vanity` 等仍存疑行。

### B13-L1: PDF 255-274 (LECTURE 59-69) second pass
- Fixed obvious headword/star errors: `enlightened`, `searchlight`, `Belgium`, `bellied`, `bellyful`, `peril`, `exemplary`, `peremptory`, `preempt`, `exempt`, `prompt`, `redeem`, `redemption`, `extol`, `tolerance`, `toll`, `vanish`, `vanity`.
- Scope stayed on high-risk fields only; no full sentence re-draft.
- Remaining: some IPA, spacing, and punctuation still need final review.
### B13-L2: PDF 259-271 (LECTURE 61-69) targeted pass
- Fixed `empirical`, `prompt`, and `promptitude` from page-image truth.
- Kept the pass narrow: only headwords, IPA, and root-splitting text were corrected.
- Remaining: adjacent punctuation/spacing sweep around the same cluster still worth one final read.
### B13-L3: PDF 259-271 (LECTURE 61-69) cleanup follow-up
- Normalized `empirical` root split to `em<en`.
- Corrected `prompt` / `promptitude` IPA and root spacing from the page image.
- Verified the full file still reports 200 `LECTURE` blocks and 503 PDF anchors.
### B13-L4: PDF 271 (LECTURE 69) root-chain cleanup
- Normalized `premium`, `redeem`, and `ransom` root splits on the same page.
- Kept the edit constrained to root etymology text and punctuation.
### B13-L5: PDF 274 (LECTURE 69) page-end IPA cleanup
- Corrected `vanish` and `vanity` IPA from the rendered page image.
- This was a narrow phonetic-only pass; wording and examples stayed unchanged.
### B13-L6: PDF 273-274 (LECTURE 69) IPA sweep
- Corrected `gregarious`, `aggregate`, `congregate`, and `desegregate` IPA from the rendered pages.
- Kept the sweep localized to phonetic lines and did not rewrite examples.

## 增补记录（2026-05-12）

### B13-M：PDF 279-280（`LECTURE 74-75`）定点修补
- 结构已核：是
- 字段已核：
  - `LECTURE 74`：`MERS, MERG`
  - `LECTURE 75`：`CALCUL`
  - 页锚点：`<!-- PDF p279 | book p260 -->`、`<!-- PDF p280 | book p261 -->`
- 处理说明：
  - 以 `tmp/pdfs/round3_l70_l73/p-279.png`、`p-280.png` 为真值，对 `LECTURE 74-75` 做了小范围人工清洗，不重写整讲，只修复明显影响可读性的 OCR 断裂。
  - 更正了 `MERS, MERG` 词根标题及释义说明中的连写问题，并修补了 `immerse / emerge / emergency / submerge / merged into curiosity` 一带的空格、误字和跨页续句。
  - 纠正了 `LECTURE 75` 中 `to reckon`、`100 digits`、`calculate / calculation / calculus` 等明显错拼与连写，并删除了跨页续句 `Curiosity...` 在 `LECTURE 75` 标题下的重复残留。
- 残留问题：
  - 本次仍属于定点修补而非逐条深校；`LECTURE 74-75` 内的部分 IPA、符号风格和例句间距仍建议后续总审时结合 `PDF p279-p280` 回看。

### B13-M1：PDF 274-279（相邻讲次结构字段顺手清理）
- 结构已核：部分
- 处理说明：
  - 结合 `tmp/pdfs/round3_l70_l73/p-274.png` 到 `p-279.png` 的同批渲染页图，顺手修复了若干会影响后续继续审校的明显结构错误。
  - 本轮仅限标题级/词头级清理：`hilarious`、`hortative`、`TRIC[TRIG]`、`MAN[MN, MAIN]`、`mansion`、`remains`、`nerve`、`nervous`、`fetal`。
- 残留问题：
  - `LECTURE 70-73` 仍未完成逐条深校；本次没有系统回扫相邻讲次中的 IPA、例句和频级标记。

### B13-N：PDF 337-359（`LECTURE 126-150`）人工续校
- 结构已核：是
- 字段已核：
  - `LECTURE 126-138`：`AL / CLIV / TEG, TECT / BURS / FORT, FORC / TARD / HAB[HIB] / JUVEN / LEN / VIL / NEG / NOUNC, NUNCI / SCIND, SCIS / TAC[TIC] / DUB[DOUB] / MONSTR / PUD`
  - `LECTURE 139-150`：`TRENCH / OL, OD / FULG / SPLEND / FRACT, FRAG[FRA, FRING] / PLANT / CINCT / RAP, RAV[REP] / PLU / CILI / MIT, MISS[MIS, MESS] / FORM / SCEND[SCENT, SCENS, SCAN] / VEST`
  - 页锚点：`<!-- PDF p337 | book p318 -->` 至 `<!-- PDF p359 | book p340 -->`
- 处理说明：
  - 以 `tmp/pdfs/round3_l126_150/p-337.png` 到 `p-359.png` 为真值，对 `LECTURE 126-150` 做了连续人工清洗，守住了 `PDF p353`、`p355`、`p357`、`p358` 的页内起讲边界以及 `PDF p359` 页尾到第二部分扉页的分界。
  - 修正了该区段内大量高风险 OCR 污染：词根标题分隔符、词头星级、坏词性标记、损坏音标括号、英文例句连写，以及 `prolific / alma mater / enforce / comfortable / rehabilitate / juvenile / renounce / rescind / olfactory / resplendent / fraction / ravish / supercilious / surmise / commit / formulate / transcend / travesty / vesture` 等条目的显著错项。
  - 本轮同时补做了 `LECTURE 147-150` 的逐页回看，清掉了 `MIT, MISS / FORM / SCEND / VEST` 四讲里最影响继续审校的结构噪声和断裂字段。
- 残留问题：
  - `LECTURE 126-150` 已完成本轮人工校勘，但仍有少量 IPA、英中间距和个别低频词释义属于人工标准化结果；最终总审时建议优先抽查 `PDF p347-p359` 的高密度页。
  - 本批不再向后越界；下一轮正文宜回到 `LECTURE 59-125` 的连续深校，或从 `LECTURE 151` 继续后推。

### B13-O：PDF 411-417（`LECTURE 192-200`）深校收口
- 结构已核：是
- 字段已核：
  - `LECTURE 192-200`：`VARIC / ULTIM / ORN / SCAL / ONER / INSUL[ISOL] / STIP / CAST[CEST,CHAST] / PAT / CRASTIN / FLIG / ART / ACERB / BIL / FUSC / RAT / JUST`
  - 页锚点：`<!-- PDF p411 | book p392 -->` 至 `<!-- PDF p418 | book NA -->`
- 处理说明：
  - 以 `tmp/pdfs/round3_l151_200/p-411.png` 到 `p-417.png` 为真值，完成了 `LECTURE 192-200` 的连续人工深校，并把目标推进到 `LECTURE 200`。
  - 本轮集中清掉了英文例句连写、词性错位、中文错字和明显结构噪声，涉及 `prevaricate / ultimate / ultimatum / ornament / adorn / escalate / exonerate / insulate / isolation / stipulate / castigate / expatiate / peripatetic / profligate / articulate / artifice / artful / exacerbate / debilitate / ratify / rate / ratio / rationalize / justify / justice / unjust / maladjustment` 等条目。
  - 同时复核了全文件结构计数，确认 `ocr.md` 仍保持 `200` 个 `LECTURE` 标题和 `503` 个 PDF 页锚点。
- 残留问题：
  - `LECTURE 192-200` 的高风险正文错误已基本清完，但少量 IPA 细节和个别符号风格仍可能保留原书式 OCR 痕迹；如果后续要做最终出版级清样，建议再对 `PDF p412-p417` 做一轮纯音标/标点专项回看。
