from pathlib import Path


path = Path("word.tex")
text = path.read_text(encoding="utf-8")

start = text.index(r"\chapter{PORT}")
end = text.index(r"\chapter{SCRUT}")

new_chunk = r"""\chapter{PORT}

\begin{itemize}
  \item 词根 PORT 来自拉丁语，意为 to carry，核心含义是“携带、运送、带来、负担”。
\end{itemize}

\begin{word}[*]{inopportune}{ɪnˈɑːpərtuːn}
  \wordbreakdown{不在合适时机“带来”的：in-（不）+ opportune（适时的）}
  \wordfamily{opportune（恰当的）；opportunity（机会）；opportunism（机会主义）；importune（纠缠请求）}
  \wordsense{a. 不合时宜的；来得不是时候的}
  \wordphrase{an inopportune moment / an inopportune interruption（不合时宜的时刻／不合时宜的打断）}
  \wordexample{His phone call came at a particularly inopportune moment.（他的电话来得特别不是时候。）}
\end{word}



\begin{word}[*]{importune}{ɪmˈpɔːrtuːn}
  \wordbreakdown{不断向人“施加、带去”请求：im-（向内、向着）+ port（带）}
  \wordfamily{importunate（纠缠不休的）；importunity（纠缠强求）；opportune（恰当的）；inopportune（不合时宜的）}
  \wordsense{vt. 纠缠着请求；一再恳求}
  \wordphrase{importune sb for money / importune sb for help（缠着某人要钱／反复请求某人帮忙）}
  \wordexample{She kept importuning the manager for another interview.（她一直缠着经理再给她一次面试机会。）}
\end{word}



\begin{word}[*]{rapport}{ræˈpɔːr}
  \wordbreakdown{彼此“带到一起”而形成的融洽关系}
  \wordfamily{rapporteur（报告员）；report（报告）；support（支持）；comport（行为举止；相符）}
  \wordsense{n. 融洽关系；和谐气氛}
  \wordphrase{build rapport with clients / establish rapport（与客户建立融洽关系／建立默契）}
  \wordexample{Good teachers quickly build rapport with new students.（优秀教师很快就能与新生建立融洽关系。）}
\end{word}



\begin{word}[**]{portable}{ˈpɔːrtəbl}
  \wordbreakdown{可携带的：port（带）+ -able}
  \wordfamily{portability（便携性）；porter（搬运工）；transport（运输）；passport（护照）}
  \wordsense{a. 便携的；轻便的；可移动的}
  \wordphrase{a portable device / a portable speaker（便携设备／便携音箱）}
  \wordexample{The team uses a portable scanner for fieldwork.（团队在外业工作中使用便携式扫描仪。）}
\end{word}



\begin{word}[*]{opportune}{ˈɑːpərtuːn}
  \wordbreakdown{时机正好“带到面前”的：ob-（朝向）+ port（带来）}
  \wordfamily{opportunity（机会）；opportunely（适时地）；inopportune（不合时宜的）；opportunism（机会主义）}
  \wordsense{a. 恰好的；时机适当的；及时的}
  \wordphrase{an opportune moment / opportune timing（恰当时机／时机正好）}
  \wordexample{She raised the issue at an opportune moment.（她在恰当的时候提出了这个问题。）}
\end{word}



\begin{word}[**]{purport}{ˈpɜːrpɔːrt}
  \wordbreakdown{把意思“带出来”：pur<pro（向前）+ port（带）}
  \wordfamily{report（报告）；support（支持）；comport（相符；举止）；import（输入；含义）}
  \wordsense{n. 大意；主旨；含义}
  \wordphrase{the purport of a statement（声明的大意）}
  \wordexample{I could not grasp the purport of his remarks at first.（起初我没弄明白他那番话的主旨。）}
  \wordsense{vt. 声称；意指；以……为主旨}
  \wordphrase{purport to prove / purport to show（声称证明／声称表明）}
  \wordexample{The article purports to explain the recent market decline.（这篇文章声称解释了近期市场下跌的原因。）}
\end{word}



\begin{word}[*]{comport}{kəmˈpɔːrt}
  \wordbreakdown{一起“带着自己”行动，或与某物相一致：com-（共同）+ port（带）}
  \wordfamily{comportment（举止）；deportment（举止）；report（报告）；support（支持）}
  \wordsense{vi. comport oneself 举止；表现}
  \wordphrase{comport oneself with dignity（举止庄重）}
  \wordexample{He comported himself calmly throughout the crisis.（在整个危机中他都表现得很镇定。）}
  \wordsense{vi. comport with 与……一致；符合}
  \wordphrase{comport with the facts / comport with the evidence（与事实相符／与证据一致）}
  \wordexample{Her explanation does not comport with what we observed.（她的解释与我们观察到的情况并不一致。）}
\end{word}



\begin{word}[**]{deport}{dɪˈpɔːrt}
  \wordbreakdown{把人“带走”：de-（离开）+ port（带）}
  \wordfamily{deportation（驱逐出境）；deportee（被驱逐者）；deportment（举止）；comport（举止；相符）}
  \wordsense{vt. 驱逐出境；递解}
  \wordphrase{deport illegal immigrants / deport a suspect（驱逐非法移民／驱逐嫌疑人）}
  \wordexample{The government decided to deport the foreign criminal after the trial.（审判结束后，政府决定将该外国罪犯驱逐出境。）}
  \wordsense{vi. deport oneself 举止；表现}
  \wordphrase{deport oneself well（举止得体）}
  \wordexample{She deported herself gracefully at the reception.（她在招待会上举止优雅。）}
\end{word}



\begin{word}[*]{deportation}{ˌdiːpɔːrˈteɪʃn}
  \wordbreakdown{驱逐、递解的行为：deport + -ation}
  \wordfamily{deport（驱逐）；deportee（被驱逐者）；deportable（可驱逐的）；deportment（举止）}
  \wordsense{n. 驱逐出境；递解}
  \wordphrase{face deportation proceedings（面临遣返程序）}
  \wordexample{He appealed the deportation order in court.（他向法院上诉反对遣返令。）}
\end{word}



\begin{word}[**]{deportment}{dɪˈpɔːrtmənt}
  \wordbreakdown{一个人“把自己带出来”的样子：deport oneself 引申而来}
  \wordfamily{deport（驱逐；举止）；comportment（举止）；comport（举止）；deportation（驱逐）}
  \wordsense{n. 举止；风度；行为表现}
  \wordphrase{calm deportment / graceful deportment（沉着的举止／优雅的风度）}
  \wordexample{Her calm deportment impressed everyone on the panel.（她沉着的举止给小组里的每个人都留下了印象。）}
\end{word}



\begin{word}[*]{disport}{dɪsˈpɔːrt}
  \wordbreakdown{把自己“带开去玩”：dis-（分开）+ port（带）}
  \wordfamily{sport（运动；娱乐）；deportment（举止）；comport（举止）；transport（运送）}
  \wordsense{vi. 嬉戏；玩乐；消遣（文）}
  \wordphrase{disport oneself in the water（在水中嬉戏）}
  \wordexample{Children disported themselves on the beach all afternoon.（孩子们整个下午都在海滩上嬉戏。）}
\end{word}



\begin{word}[**]{export}{ɪkˈspɔːrt; ˈekspɔːrt}
  \wordbreakdown{向外“带出去”：ex-（向外）+ port（带）}
  \wordfamily{exporter（出口商）；exportable（可出口的）；import（进口）；transport（运输）}
  \wordsense{vt. 出口；输出；传播}
  \wordphrase{export machinery / export software（出口机械／输出软件）}
  \wordexample{The country exports most of its coffee to Europe.（这个国家把大部分咖啡出口到欧洲。）}
  \wordsense{n. 出口；出口商品}
  \wordphrase{a major export / export earnings（主要出口商品／出口收入）}
  \wordexample{Tea is one of the region's main exports.（茶叶是这个地区的主要出口商品之一。）}
\end{word}



\begin{word}[**]{import}{ɪmˈpɔːrt; ˈɪmpɔːrt}
  \wordbreakdown{向内“带进来”：im-（向内）+ port（带）}
  \wordfamily{important（重要的）；importance（重要性）；importer（进口商）；importune（纠缠请求）}
  \wordsense{vt. 进口；输入}
  \wordphrase{import oil / import fresh fruit（进口石油／进口新鲜水果）}
  \wordexample{The country imports most of its energy from abroad.（这个国家的大部分能源都依赖进口。）}
  \wordsense{n. 意义；要旨；重要性；进口货}
  \wordphrase{the import of a message / cheap imports（信息的含义／廉价进口商品）}
  \wordexample{We did not fully grasp the import of his warning at the time.（当时我们没有充分理解他那番警告的重要含义。）}
\end{word}



\begin{word}[***]{important}{ɪmˈpɔːrtnt}
  \wordbreakdown{被“带进来”而有分量的，后引申为重要的：import + -ant}
  \wordfamily{importance（重要性）；import（含义；进口）；importantly（重要地）；unimportant（不重要的）}
  \wordsense{a. 重要的；重大的}
  \wordphrase{an important decision / an important issue（重要决定／重要问题）}
  \wordexample{It is important to keep accurate records.（保存准确记录是很重要的。）}
  \wordsense{a. 有地位的；有影响力的}
  \wordphrase{an important guest / important people（重要来宾／有头有脸的人）}
  \wordexample{Several important figures attended the ceremony.（几位重要人物出席了典礼。）}
\end{word}



\begin{word}[***]{opportunity}{ˌɑːpərˈtuːnəti}
  \wordbreakdown{适时来到面前的时机：opportune 的名词形式}
  \wordfamily{opportune（恰当的）；opportunism（机会主义）；opportunist（机会主义者）；inopportune（不合时宜的）}
  \wordsense{n. 机会；良机}
  \wordphrase{miss an opportunity / seize the opportunity（错过机会／抓住机会）}
  \wordexample{She saw the move as an opportunity to start over.（她把这次变动看作重新开始的机会。）}
\end{word}



\begin{word}[*]{opportunism}{ˌɑːpərˈtuːnɪzəm}
  \wordbreakdown{只抓住对自己有利时机的做法：opportunity + -ism}
  \wordfamily{opportunist（机会主义者）；opportune（恰当的）；opportunity（机会）；inopportune（不合时宜的）}
  \wordsense{n. 机会主义}
  \wordphrase{political opportunism / sheer opportunism（政治机会主义／纯粹的投机）}
  \wordexample{Critics accused the party of naked opportunism.（批评者指责该党赤裸裸地搞机会主义。）}
\end{word}



\begin{word}[***]{report}{rɪˈpɔːrt}
  \wordbreakdown{把信息“带回来”：re-（回）+ port（带）}
  \wordfamily{reporter（记者）；reportedly（据报道）；rapport（融洽关系）；support（支持）}
  \wordsense{vt. 报告；汇报；报道}
  \wordphrase{report an accident / report to the manager（报告事故／向经理汇报）}
  \wordexample{Please report any safety problem immediately.（任何安全问题都请立即上报。）}
  \wordsense{n. 报告；报道；成绩单}
  \wordphrase{an annual report / a weather report（年度报告／天气预报）}
  \wordexample{The newspaper published a detailed report on the trial.（报纸刊登了一篇关于那场审判的详细报道。）}
\end{word}



\begin{word}[***]{support}{səˈpɔːrt}
  \wordbreakdown{从下面“托着、带着”：sub-（在下方）+ port（带）}
  \wordfamily{supportive（支持性的）；supporter（支持者）；unsupported（无支撑的）；transport（运输）}
  \wordsense{vt. 支持；支撑；供养}
  \wordphrase{support a policy / support a family（支持一项政策／养家）}
  \wordexample{Her parents supported her decision to study abroad.（她父母支持她出国留学的决定。）}
  \wordsense{n. 支持；支撑；援助}
  \wordphrase{emotional support / financial support（情感支持／经济支持）}
  \wordexample{The project received strong support from the local community.（这个项目得到了当地社区的大力支持。）}
\end{word}



\begin{word}[***]{transport}{trænsˈpɔːrt; ˈtrænspɔːrt}
  \wordbreakdown{横向“带过去”：trans-（跨越）+ port（带）}
  \wordfamily{transportation（运输）；transporter（运输者）；portable（便携的）；porter（搬运工）}
  \wordsense{vt. 运输；运送}
  \wordphrase{transport goods / transport passengers（运输货物／运送乘客）}
  \wordexample{The trucks transport supplies to remote villages.（卡车把补给运送到偏远村庄。）}
  \wordsense{n. 运输；交通工具}
  \wordphrase{public transport / air transport（公共交通／航空运输）}
  \wordexample{Public transport is the best way to get around the city.（公共交通是在城里出行的最佳方式。）}
  \wordsense{n. 狂喜；激动（较旧用法）}
  \wordphrase{in a transport of joy（欣喜若狂）}
  \wordexample{She was in a transport of delight when the results arrived.（结果到来时她欣喜若狂。）}
\end{word}



\begin{word}[*]{transportation}{ˌtrænspɔːrˈteɪʃn}
  \wordbreakdown{运输或运送的过程：transport + -ation}
  \wordfamily{transport（运输）；transporter（运输者）；transportable（可运输的）；public transport（公共交通）}
  \wordsense{n. 运输；运送；交通系统}
  \wordphrase{rail transportation / transportation costs（铁路运输／运输成本）}
  \wordexample{The bridge improved transportation between the two towns.（这座桥改善了两镇之间的交通。）}
\end{word}



\begin{word}[**]{portage}{ˈpɔːrtɪdʒ}
  \wordbreakdown{需要人力“搬带”过去的运输：port（带）+ -age}
  \wordfamily{porter（搬运工）；portable（便携的）；transport（运输）；passport（护照）}
  \wordsense{n. 陆路转运；搬运；搬运费}
  \wordphrase{a portage route / pay portage（陆路转运线路／支付搬运费）}
  \wordexample{The explorers made a difficult portage around the waterfall.（探险者们艰难地绕过瀑布进行了陆路搬运。）}
\end{word}



\begin{word}[***]{porter}{ˈpɔːrtər}
  \wordbreakdown{负责“搬带”东西的人：port（带）+ -er}
  \wordfamily{portage（搬运）；portable（便携的）；transport（运输）；support（支持）}
  \wordsense{n. 搬运工；行李员；门房}
  \wordphrase{a hotel porter / a railway porter（旅馆行李员／火车站搬运工）}
  \wordexample{The porter carried our bags up to the room.（行李员把我们的包送到了房间。）}
\end{word}



\begin{word}[**]{portfolio}{pɔːrtˈfoʊlioʊ}
  \wordbreakdown{把文件“带着走”的夹子，后引申为作品集、投资组合等}
  \wordfamily{portable（便携的）；porter（搬运工）；report（报告）；transport（运输）}
  \wordsense{n. 公文包；文件夹}
  \wordphrase{carry a leather portfolio（拿着皮质文件夹）}
  \wordexample{She brought a slim portfolio to the interview.（她带着一个轻便文件夹去参加面试。）}
  \wordsense{n. 作品集；投资组合；部长职责范围}
  \wordphrase{a design portfolio / an investment portfolio（设计作品集／投资组合）}
  \wordexample{The artist updated her portfolio before applying to graduate school.（那位艺术家在申请研究生前更新了自己的作品集。）}
\end{word}



\begin{word}[**]{portly}{ˈpɔːrtli}
  \wordbreakdown{原与“举止、仪态”相关，后多指体态端重而偏胖}
  \wordfamily{comport（举止）；deportment（举止）；portable（便携的）；portal（门户）}
  \wordsense{a. 肥胖而庄重的；魁梧的}
  \wordphrase{a portly gentleman（肥胖而庄重的绅士）}
  \wordexample{A portly man in a dark suit greeted us at the door.（一位穿深色西装的魁梧男子在门口迎接我们。）}
\end{word}



\begin{word}[**]{portico}{ˈpɔːrtɪkoʊ}
  \wordbreakdown{建筑前面可供通行的“门廊、柱廊”}
  \wordfamily{portal（入口）；porch（门廊）；portable（便携的）；passport（护照）}
  \wordsense{n. 柱廊；门廊}
  \wordphrase{a marble portico / stand under the portico（大理石柱廊／站在柱廊下）}
  \wordexample{We waited under the portico until the rain stopped.（我们在柱廊下等到雨停。）}
\end{word}



\begin{word}[**]{portal}{ˈpɔːrtl}
  \wordbreakdown{进入时需要“通过、带入”的门口：与 porte, portico 同源}
  \wordfamily{portico（柱廊）；porch（门廊）；passport（护照）；transport（运输）}
  \wordsense{n. 门；入口；门户}
  \wordphrase{a stone portal / an online portal（石制门户／在线门户网站）}
  \wordexample{Students can check their grades through the university portal.（学生可以通过大学门户网站查询成绩。）}
\end{word}



\begin{word}[**]{portmanteau}{pɔːrtˈmæntoʊ}
  \wordbreakdown{原指可携带的大旅行箱，后引申为“混成词”}
  \wordfamily{portable（便携的）；portfolio（文件夹）；porter（搬运工）；passport（护照）}
  \wordsense{n. 旅行箱；大衣箱}
  \wordphrase{pack a portmanteau（收拾旅行箱）}
  \wordexample{The old portmanteau was still covered in faded labels.（那个旧旅行箱上仍贴满褪色的标签。）}
  \wordsense{n. 混成词}
  \wordphrase{a portmanteau word（混成词）}
  \wordexample{The word “brunch” is a famous portmanteau.（“brunch” 是一个著名的混成词。）}
\end{word}



\begin{word}[*]{heliport}{ˈhelipɔːrt}
  \wordbreakdown{供直升机“起降、运送”的地点：heli-（螺旋；直升机）+ port（运送点）}
  \wordfamily{airport（机场）；transport（运输）；portable（便携的）；porter（搬运工）}
  \wordsense{n. 直升机场；直升机停机坪}
  \wordphrase{a hospital heliport（医院直升机停机坪）}
  \wordexample{The injured climber was flown to a nearby heliport.（受伤的登山者被空运到附近的直升机场。）}
\end{word}



\begin{word}[***]{passport}{ˈpæspɔːrt}
  \wordbreakdown{让人“通过关口”的证件：pass + port}
  \wordfamily{passage（通行）；portable（便携的）；porter（搬运工）；transport（运输）}
  \wordsense{n. 护照}
  \wordphrase{apply for a passport / carry a valid passport（申请护照／携带有效护照）}
  \wordexample{You must show your passport at border control.（你必须在边检处出示护照。）}
  \wordsense{n. 通行证；获得某事的保证}
  \wordphrase{a passport to success（通往成功的通行证）}
  \wordexample{For many students, education is seen as a passport to a better future.（对许多学生来说，教育被视为通往更好未来的通行证。）}
\end{word}



\begin{word}[***]{porch}{pɔːrtʃ}
  \wordbreakdown{门前可出入停留的廊子：与 portal, portico 同族}
  \wordfamily{portico（柱廊）；portal（入口）；passport（护照）；portable（便携的）}
  \wordsense{n. 门廊；走廊式入口}
  \wordphrase{sit on the porch / a front porch（坐在门廊上／前门廊）}
  \wordexample{They sat on the porch watching the sunset.（他们坐在门廊上看日落。）}
\end{word}

\chapter{TEGR}

\begin{itemize}
  \item 词根 TEGR 表示 touch，引申为“不被碰坏、完整、未受损”。
\end{itemize}

\begin{word}[***]{integrity}{ɪnˈteɡrəti}
  \wordbreakdown{不被触碰破坏的完整状态：in-（不）+ tegr（触碰）}
  \wordfamily{integral（完整的；积分的）；integrate（使结合）；disintegrate（瓦解）；redintegration（复原）}
  \wordsense{n. 完整；完好}
  \wordphrase{the structural integrity of a bridge（桥梁的结构完整性）}
  \wordexample{Engineers checked the integrity of the dam after the storm.（工程师们在暴风雨后检查了大坝的结构完整性。）}
  \wordsense{n. 正直；诚实}
  \wordphrase{personal integrity / professional integrity（个人操守／职业操守）}
  \wordexample{She is widely respected for her integrity.（她因其正直而广受尊敬。）}
\end{word}



\begin{word}[**]{disintegrate}{dɪsˈɪntɪɡreɪt}
  \wordbreakdown{失去完整性：dis-（分开）+ integrate / tegr（完整）}
  \wordfamily{disintegration（瓦解）；integrity（完整；正直）；integrate（整合）；integral（完整的）}
  \wordsense{vi./vt. 瓦解；崩解；使分裂}
  \wordphrase{disintegrate into dust / social order disintegrates（碎成尘土／社会秩序瓦解）}
  \wordexample{The old manuscript began to disintegrate in the damp air.（那份古老手稿在潮湿空气中开始破碎。）}
\end{word}



\begin{word}[*]{redintegration}{riˌdɪntɪˈɡreɪʃn}
  \wordbreakdown{重新恢复完整：re-（再）+ integration（完整、结合）}
  \wordfamily{integrity（完整）；disintegrate（瓦解）；integrate（整合）；reintegration（重新整合）}
  \wordsense{n. 复原；恢复；重建}
  \wordphrase{the redintegration of society after war（战后社会的重建）}
  \wordexample{The treaty was followed by the slow redintegration of public life.（条约签订后，公共生活开始缓慢恢复。）}
\end{word}

\chapter{VET}

\begin{itemize}
  \item 词根 VET 表示 old，核心义是“年久、资深、根深蒂固”。
\end{itemize}

\begin{word}[**]{inveterate}{ɪnˈvetərət}
  \wordbreakdown{在里面 오래扎根变老的：in-（在内）+ veter（老）}
  \wordfamily{veteran（老兵；老手）；veterinary（兽医的）；veteran status（老资格）；vet（审查；兽医）}
  \wordsense{a. 根深蒂固的；积习难改的}
  \wordphrase{an inveterate smoker / an inveterate liar（老烟民／积习难改的说谎者）}
  \wordexample{He is an inveterate traveler who never stays home for long.（他是个积习已深的旅行者，从不在家久留。）}
\end{word}



\begin{word}[***]{veteran}{ˈvetərən}
  \wordbreakdown{年长而有经验的人：vet（老）}
  \wordfamily{inveterate（根深蒂固的）；veterinary（兽医的）；vet（审查；兽医）；veterancy（老资格）}
  \wordsense{n. 老兵；老手；经验丰富的人}
  \wordphrase{a war veteran / a veteran journalist（退伍老兵／资深记者）}
  \wordexample{The team relied on a veteran goalkeeper in the final.（球队在决赛中依靠一位经验丰富的守门员。）}
  \wordsense{a. 经验丰富的；老资格的}
  \wordphrase{a veteran player / veteran staff（资深球员／老资格员工）}
  \wordexample{The veteran teacher handled the class with ease.（这位资深教师轻松地掌控了课堂。）}
\end{word}



\begin{word}[**]{veterinary}{ˈvetərɪneri}
  \wordbreakdown{与老式拉丁词 veterina（役畜）相关，现指兽医的}
  \wordfamily{veterinarian（兽医）；veteran（老兵；老手）；vet（兽医）；veterinary science（兽医学）}
  \wordsense{a. 兽医的；牲畜疾病的}
  \wordphrase{veterinary medicine / a veterinary clinic（兽医学／兽医诊所）}
  \wordexample{She is studying veterinary medicine at college.（她正在大学学习兽医学。）}
\end{word}

\chapter{VULN[VULT]}

\begin{itemize}
  \item 词根 VULN / VULT 表示 wound 或 tear，核心义是“伤害、撕裂、受伤”。
\end{itemize}

\begin{word}[**]{invulnerable}{ɪnˈvʌlnərəbl}
  \wordbreakdown{不会受伤的：in-（不）+ vulnerable（易受伤的）}
  \wordfamily{vulnerable（脆弱的）；vulnerability（脆弱性）；vulture（秃鹫）；invulnerability（不可战胜）}
  \wordsense{a. 刀枪不入的；不会受伤的}
  \wordphrase{feel invulnerable / an invulnerable hero（觉得自己刀枪不入／无懈可击的英雄）}
  \wordexample{Young athletes sometimes act as if they were invulnerable.（年轻运动员有时表现得仿佛自己不会受伤。）}
  \wordsense{a. 无懈可击的；不可战胜的}
  \wordphrase{an invulnerable argument / an invulnerable position（无懈可击的论点／稳固地位）}
  \wordexample{For years the company seemed invulnerable to competition.（多年来这家公司似乎完全不怕竞争。）}
\end{word}



\begin{word}[**]{vulnerable}{ˈvʌlnərəbl}
  \wordbreakdown{容易受伤的：vuln（伤）+ -able}
  \wordfamily{vulnerability（脆弱性）；invulnerable（不可伤害的）；vulture（秃鹫）；wound（伤口）}
  \wordsense{a. 易受伤的；脆弱的}
  \wordphrase{vulnerable children / vulnerable communities（脆弱儿童／弱势社区）}
  \wordexample{Older people are particularly vulnerable to heat.（老年人尤其容易受到高温伤害。）}
  \wordsense{a. 易受攻击的；有漏洞的}
  \wordphrase{a vulnerable network / a vulnerable position（有漏洞的网络／易受攻击的位置）}
  \wordexample{The report found the system highly vulnerable to cyberattacks.（报告发现该系统很容易受到网络攻击。）}
\end{word}



\begin{word}[**]{vulture}{ˈvʌltʃər}
  \wordbreakdown{与撕咬、伤害相关，后特指食腐猛禽}
  \wordfamily{vulnerable（脆弱的）；invulnerable（不会受伤的）；vulnerability（脆弱性）；carrion bird（食腐鸟）}
  \wordsense{n. 秃鹫}
  \wordphrase{a circling vulture（盘旋的秃鹫）}
  \wordexample{Vultures gathered above the desert carcass.（秃鹫聚集在沙漠里的动物尸体上空。）}
  \wordsense{n. 贪婪无情的人}
  \wordphrase{a financial vulture（贪婪的金融掠夺者）}
  \wordexample{The tabloids were accused of behaving like vultures.（那些小报被指责像秃鹫一样贪婪无情。）}
\end{word}

\chapter{MUT}

\begin{itemize}
  \item 词根 MUT 表示 change，核心义是“变化、转换、交换”。
\end{itemize}

\begin{word}[**]{immutable}{ɪˈmjuːtəbl}
  \wordbreakdown{不能改变的：im-（不）+ mut（变）}
  \wordfamily{mutability（可变性）；mutable（可变的）；transmute（转变）；mutual（相互的）}
  \wordsense{a. 不可改变的；固定不变的}
  \wordphrase{immutable law / immutable principle（不可改变的规律／不变原则）}
  \wordexample{The constitution was treated as if it were immutable.（这部宪法被对待得仿佛不可更改一般。）}
\end{word}



\begin{word}[**]{transmute}{trænzˈmjuːt}
  \wordbreakdown{变成另一种状态：trans-（转移、跨越）+ mut（变）}
  \wordfamily{transmutation（转化）；mutable（可变的）；immutable（不可变的）；permute（置换）}
  \wordsense{vt./vi. 使变形；使转化；变化}
  \wordphrase{transmute fear into courage / transmute metals（把恐惧化为勇气／使金属嬗变）}
  \wordexample{Artists often transmute private pain into public beauty.（艺术家常常把私人的痛苦转化为公共的美。）}
\end{word}



\begin{word}[*]{mutable}{ˈmjuːtəbl}
  \wordbreakdown{能够改变的：mut（变）+ -able}
  \wordfamily{mutability（可变性）；immutable（不可变的）；transmute（转化）；commute（通勤；减刑）}
  \wordsense{a. 易变的；可变的}
  \wordphrase{a mutable schedule / mutable opinion（可变的时间表／容易改变的看法）}
  \wordexample{Fashion is notoriously mutable.（时尚向来以变化无常著称。）}
\end{word}



\begin{word}[**]{commute}{kəˈmjuːt}
  \wordbreakdown{来回交换、转换：com-（共同）+ mut（变）}
  \wordfamily{commutation（交换；减刑）；commuter（通勤者）；mutable（可变的）；mutual（相互的）}
  \wordsense{vi. 通勤}
  \wordphrase{commute by train / commute to the city（乘火车通勤／通勤去城里）}
  \wordexample{He commutes two hours a day from the suburbs.（他每天从郊区通勤两小时。）}
  \wordsense{vt. 减轻；折换（刑罚、付款方式等）}
  \wordphrase{commute a sentence / commute pension payments（减刑／折换养老金支付方式）}
  \wordexample{The governor agreed to commute the prisoner's sentence.（州长同意减轻那名囚犯的刑罚。）}
\end{word}



\begin{word}[*]{commutation}{ˌkɑːmjuˈteɪʃn}
  \wordbreakdown{交换、折换、转换的行为：commute + -ation}
  \wordfamily{commute（通勤；减刑）；commuter（通勤者）；mutable（可变的）；mutual（相互的）}
  \wordsense{n. 交换；折换；减刑}
  \wordphrase{commutation of a sentence / fare commutation（减刑／票价折算）}
  \wordexample{The commutation of his sentence was announced yesterday.（对他刑期的减轻于昨天公布。）}
\end{word}



\begin{word}[**]{commuter}{kəˈmjuːtər}
  \wordbreakdown{每天来回转换地点的人：commute + -er}
  \wordfamily{commute（通勤）；commutation（交换；减刑）；transport（运输）；portable（便携的）}
  \wordsense{n. 通勤者}
  \wordphrase{daily commuters / a commuter train（每日通勤者／通勤列车）}
  \wordexample{Thousands of commuters were delayed by the strike.（成千上万的通勤者因罢工而耽搁。）}
\end{word}



\begin{word}[*]{permute}{pərˈmjuːt}
  \wordbreakdown{彻底地变换次序：per-（彻底）+ mut（变）}
  \wordfamily{permutation（排列；置换）；mutable（可变的）；transmute（转化）；mutual（相互的）}
  \wordsense{vt. 排列；置换；交换顺序}
  \wordphrase{permute the numbers / permute the letters（排列数字／调换字母次序）}
  \wordexample{The program can permute the list in every possible way.（这个程序可以把列表按所有可能的方式重新排列。）}
\end{word}



\begin{word}[***]{mutual}{ˈmjuːtʃuəl}
  \wordbreakdown{彼此交换和作用的：mut（交换、变化）}
  \wordfamily{mutually（相互地）；commute（通勤；减刑）；mutable（可变的）；commutation（交换）}
  \wordsense{a. 相互的；彼此的}
  \wordphrase{mutual respect / mutual support（相互尊重／互相支持）}
  \wordexample{Trust is built on mutual respect.（信任建立在相互尊重的基础上。）}
  \wordsense{a. 共同的；共有的}
  \wordphrase{a mutual friend / mutual benefit（共同朋友／互利）}
  \wordexample{They were introduced by a mutual friend.（他们是由一位共同的朋友介绍认识的。）}
\end{word}

\chapter{PUGN}

\begin{itemize}
  \item 词根 PUGN 表示 fight，核心义是“打斗、攻击、争辩”。
\end{itemize}

\begin{word}[*]{impugn}{ɪmˈpjuːn}
  \wordbreakdown{朝着某物发起攻击：im-（向着）+ pugn（斗）}
  \wordfamily{repugnant（令人反感的）；oppugn（公开抨击）；pugnacious（好斗的）；pugilist（拳击手）}
  \wordsense{vt. 指责；质疑；抨击}
  \wordphrase{impugn sb's motives / impugn the evidence（质疑某人的动机／质疑证据）}
  \wordexample{The defense tried to impugn the witness's credibility.（辩方试图质疑证人的可信度。）}
\end{word}



\begin{word}[**]{repugnant}{rɪˈpʌɡnənt}
  \wordbreakdown{与自己发生冲突、令人反感的：re-（反）+ pugn（斗）}
  \wordfamily{repugnance（厌恶）；impugn（抨击）；pugnacious（好斗的）；oppugn（驳斥）}
  \wordsense{a. 令人厌恶的；令人反感的}
  \wordphrase{repugnant behavior / morally repugnant（令人作呕的行为／道德上令人厌恶的）}
  \wordexample{The proposal was repugnant to many voters.（这一提议让许多选民感到反感。）}
  \wordsense{a. 与……抵触的；不相容的}
  \wordphrase{repugnant to reason / repugnant to the law（有悖于理性／与法律相抵触）}
  \wordexample{Such conduct is repugnant to the principles of justice.（这种行为有悖于正义原则。）}
\end{word}



\begin{word}[*]{oppugn}{əˈpjuːn}
  \wordbreakdown{公开反对、攻击：ob-（反向）+ pugn（斗）}
  \wordfamily{impugn（质疑）；pugnacious（好斗的）；repugnant（令人厌恶的）；pugilist（拳击手）}
  \wordsense{vt. 反驳；驳斥；抨击}
  \wordphrase{oppugn a doctrine / oppugn an argument（驳斥一种学说／反驳一个论点）}
  \wordexample{The scholar oppugned the accepted theory in a famous essay.（这位学者在一篇著名论文中驳斥了被普遍接受的理论。）}
\end{word}



\begin{word}[**]{pugnacious}{pʌɡˈneɪʃəs}
  \wordbreakdown{爱打斗的：pugn（斗）}
  \wordfamily{pugnacity（好斗）；pugilist（拳击手）；impugn（抨击）；repugnant（令人反感的）}
  \wordsense{a. 好斗的；爱争吵的}
  \wordphrase{a pugnacious temperament / a pugnacious child（好斗的性格／爱打架的孩子）}
  \wordexample{He became pugnacious whenever anyone challenged his authority.（每当有人挑战他的权威时，他就变得咄咄逼人。）}
\end{word}



\begin{word}[**]{pugilist}{ˈpjuːdʒɪlɪst}
  \wordbreakdown{从“打斗”义引申，特指拳击手}
  \wordfamily{pugilism（拳击）；pugnacious（好斗的）；impugn（质疑）；repugnant（令人反感的）}
  \wordsense{n. 拳击手}
  \wordphrase{a professional pugilist（职业拳击手）}
  \wordexample{The young pugilist trained before dawn every day.（这位年轻拳击手每天黎明前就开始训练。）}
\end{word}

\chapter{ANIM}

\begin{itemize}
  \item 词根 ANIM 表示 life, breath, mind，核心义是“生命、精神、心气、灵魂”。
\end{itemize}

\begin{word}[**]{inanimate}{ɪnˈænɪmət}
  \wordbreakdown{没有生命和气息的：in-（不）+ anim（生命、气息）}
  \wordfamily{animate（赋予生命；生动的）；animation（活力；动画）；animal（动物）；animism（泛灵论）}
  \wordsense{a. 无生命的；死气沉沉的}
  \wordphrase{inanimate objects / an inanimate face（无生命物体／毫无生气的脸）}
  \wordexample{The museum displayed tools alongside inanimate household objects.（博物馆把工具和无生命的家用器物一同陈列。）}
\end{word}



\begin{word}[**]{animosity}{ˌænɪˈmɑːsəti}
  \wordbreakdown{心里充满敌意的状态：anim（心气、精神）}
  \wordfamily{animus（敌意）；animate（使有活力）；unanimous（一致的）；equanimity（平静）}
  \wordsense{n. 敌意；憎恶}
  \wordphrase{deep animosity / animosity between rivals（深仇敌意／对手间的敌意）}
  \wordexample{Years of competition created animosity between the two families.（多年的竞争在两个家族之间造成了敌意。）}
\end{word}



\begin{word}[**]{equanimity}{ˌekwəˈnɪməti}
  \wordbreakdown{心境保持平衡：equa-（平等）+ anim（心）}
  \wordfamily{equanimous（镇定的）；animate（使有活力）；animosity（敌意）；unanimous（一致的）}
  \wordsense{n. 镇定；平和；沉着}
  \wordphrase{maintain equanimity / face criticism with equanimity（保持镇定／平静面对批评）}
  \wordexample{She handled the crisis with remarkable equanimity.（她以惊人的镇定应对了这场危机。）}
\end{word}



\begin{word}[**]{animate}{ˈænɪmeɪt; ˈænɪmət}
  \wordbreakdown{赋予生命、气息或精神：anim（生命、气息）}
  \wordfamily{animation（活力；动画）；animated（活泼的）；animal（动物）；inanimate（无生命的）}
  \wordsense{vt. 赋予生命；使有生气；鼓舞}
  \wordphrase{animate a character / animate a discussion（给角色赋予生命／使讨论活跃）}
  \wordexample{Her enthusiasm animated the whole meeting.（她的热情使整个会议都活跃了起来。）}
  \wordsense{a. 有生命的；活跃的}
  \wordphrase{animate beings / an animate conversation（有生命的生物／生动的谈话）}
  \wordexample{The children became more animate when the music started.（音乐一响起，孩子们就更活跃了。）}
\end{word}



\begin{word}[**]{animation}{ˌænɪˈmeɪʃn}
  \wordbreakdown{生命感、活力或赋活动画的过程：animate + -ion}
  \wordfamily{animate（使有生气）；animated（生动的）；animal（动物）；inanimate（无生命的）}
  \wordsense{n. 活力；生气；兴奋}
  \wordphrase{speak with animation / full of animation（兴致勃勃地说／充满活力）}
  \wordexample{He told the story with great animation.（他非常生动地讲述了这个故事。）}
  \wordsense{n. 动画制作；动画片}
  \wordphrase{computer animation / an animation studio（电脑动画／动画工作室）}
  \wordexample{She works in animation for a major film company.（她在一家大型电影公司从事动画制作工作。）}
\end{word}



\begin{word}[***]{animal}{ˈænɪml}
  \wordbreakdown{有生命和气息的存在：anim（生命、气息）}
  \wordfamily{animate（使有生气）；animation（活力；动画）；animism（泛灵论）；animalistic（兽性的）}
  \wordsense{n. 动物}
  \wordphrase{wild animals / domestic animals（野生动物／家养动物）}
  \wordexample{Many animals migrate south in winter.（许多动物会在冬天向南迁徙。）}
  \wordsense{a. 动物的；兽性的}
  \wordphrase{animal instincts / animal desire（动物本能／兽欲）}
  \wordexample{The novel explores the animal instincts beneath civilized behavior.（这部小说探讨了文明行为之下的动物本能。）}
\end{word}



\begin{word}[*]{animism}{ˈænɪmɪzəm}
  \wordbreakdown{认为万物有灵：anim（生命、灵魂）+ -ism}
  \wordfamily{animist（泛灵论者）；animal（动物）；animate（赋予生命）；animus（精神；敌意）}
  \wordsense{n. 泛灵论；万物有灵论}
  \wordphrase{belief in animism（相信泛灵论）}
  \wordexample{The anthropologist studied traces of animism in local rituals.（这位人类学家研究了当地仪式中的泛灵论痕迹。）}
\end{word}



\begin{word}[*]{animadvert}{ˌænɪmædˈvɜːrt}
  \wordbreakdown{把注意力和心神转向某事并加以批评：anim（心神）+ advert（转向）}
  \wordfamily{animadversion（批评）；animosity（敌意）；animus（敌意）；animate（使有活力）}
  \wordsense{vi. 批评；责难（正式）}
  \wordphrase{animadvert on a policy / animadvert on misconduct（批评一项政策／指责不当行为）}
  \wordexample{The editorial animadverted sharply on the minister's remarks.（社论尖锐批评了部长的言论。）}
\end{word}



\begin{word}[*]{animus}{ˈænɪməs}
  \wordbreakdown{内心的气息和心意，后常指敌意}
  \wordfamily{animosity（敌意）；animism（泛灵论）；equanimity（镇定）；unanimous（一致的）}
  \wordsense{n. 敌意；恶意}
  \wordphrase{personal animus / political animus（私人敌意／政治敌意）}
  \wordexample{There was no personal animus behind her criticism.（她的批评背后并没有私人恶意。）}
  \wordsense{n. 意图；精神（较正式）}
  \wordphrase{the animus of the law（法律的精神）}
  \wordexample{The ruling violated the animus of the constitution.（这一裁决违背了宪法精神。）}
\end{word}



\begin{word}[*]{pusillanimous}{ˌpjuːsɪˈlænɪməs}
  \wordbreakdown{小心小气的灵魂：pusill-（很小的）+ anim（心、气）}
  \wordfamily{pusillanimity（胆小）；animus（敌意）；equanimity（沉着）；unanimous（一致的）}
  \wordsense{a. 胆小的；怯懦的}
  \wordphrase{a pusillanimous response / a pusillanimous leader（怯懦的回应／胆小的领导者）}
  \wordexample{The committee was accused of taking a pusillanimous approach to reform.（该委员会被指责在改革问题上态度怯懦。）}
\end{word}



\begin{word}[**]{unanimous}{juˈnænɪməs}
  \wordbreakdown{同一条心的：uni-（一）+ anim（心意、精神）}
  \wordfamily{unanimously（一致地）；equanimity（镇定）；animus（心意；敌意）；animosity（敌意）}
  \wordsense{a. 一致同意的；无异议的}
  \wordphrase{a unanimous decision / unanimous support（一致决定／一致支持）}
  \wordexample{The committee reached a unanimous decision after a long debate.（经过长时间讨论后，委员会作出了一致决定。）}
\end{word}

\chapter{AVI[AU]}

\begin{itemize}
  \item 词根 AVI / AU 与 bird 有关，核心义是“鸟、飞行、观鸟占兆”。
\end{itemize}

\begin{word}[*]{inauspicious}{ˌɪnɔːˈspɪʃəs}
  \wordbreakdown{不是吉兆的：in-（不）+ auspicious（吉利的）}
  \wordfamily{auspicious（吉利的）；auspice（赞助；吉兆）；aviation（航空）；aviator（飞行员）}
  \wordsense{a. 不吉利的；不祥的；不顺利的}
  \wordphrase{an inauspicious start / inauspicious signs（不吉利的开端／不祥之兆）}
  \wordexample{The campaign began under rather inauspicious circumstances.（这场活动是在颇为不利的情况下开始的。）}
\end{word}



\begin{word}[**]{auspicious}{ɔːˈspɪʃəs}
  \wordbreakdown{由观鸟得出的吉兆：au<avi（鸟）+ spic（看）}
  \wordfamily{auspice（吉兆；赞助）；inauspicious（不吉利的）；aviation（航空）；aviator（飞行员）}
  \wordsense{a. 吉利的；有前途的；顺利的}
  \wordphrase{an auspicious beginning / auspicious timing（吉利的开端／好时机）}
  \wordexample{The negotiations opened in an auspicious atmosphere.（谈判在一个良好的气氛中开始了。）}
\end{word}



\begin{word}[***]{aviation}{ˌeɪviˈeɪʃn}
  \wordbreakdown{像鸟一样飞行的事业：avi（鸟）}
  \wordfamily{aviator（飞行员）；aviary（鸟舍）；auspicious（吉利的）；inauspicious（不吉利的）}
  \wordsense{n. 航空；航空业}
  \wordphrase{civil aviation / aviation safety（民航／航空安全）}
  \wordexample{She has worked in aviation for over twenty years.（她在航空业工作了二十多年。）}
\end{word}



\begin{word}[***]{aviator}{ˈeɪvieɪtər}
  \wordbreakdown{像鸟一样飞的人：avi（鸟）+ -ator}
  \wordfamily{aviation（航空）；aviary（鸟舍）；pilot（飞行员）；aircraft（飞机）}
  \wordsense{n. 飞行员；航空家}
  \wordphrase{a military aviator / early aviators（军用飞行员／早期航空先驱）}
  \wordexample{The museum honors the aviators who opened the first air route.（博物馆纪念开辟首条航线的飞行员们。）}
\end{word}

\chapter{CALC[CULC]}

\begin{itemize}
  \item 词根 CALC / CULC 表示 tread, kick，核心义是“踩、踢、反复踏入”。
\end{itemize}

\begin{word}[*]{inculcate}{ˈɪnkʌlkeɪt}
  \wordbreakdown{反复踩进心里，后引申为“灌输”：in-（向内）+ culc<calc（踩）}
  \wordfamily{inculcation（灌输）；recalcitrant（反抗的）；culture（文化，远亲同源）；cultivate（培养）}
  \wordsense{vt. 反复灌输；谆谆教诲}
  \wordphrase{inculcate discipline / inculcate values（灌输纪律／灌输价值观）}
  \wordexample{Parents try to inculcate honesty in their children.（父母努力把诚实这一品质灌输给孩子。）}
\end{word}



\begin{word}[**]{recalcitrant}{rɪˈkælsɪtrənt}
  \wordbreakdown{向后踢、拒绝前行：re-（向后）+ calc（踢、踩）}
  \wordfamily{recalcitrance（顽抗）；inculcate（灌输）；stubborn（顽固的）；defiant（反抗的）}
  \wordsense{a. 顽抗的；不服从的；难控制的}
  \wordphrase{a recalcitrant child / recalcitrant behavior（不听话的孩子／反抗行为）}
  \wordexample{The police struggled to control the recalcitrant crowd.（警方费力控制那群不服管束的人群。）}
\end{word}

\chapter{FIRM}

\begin{itemize}
  \item 词根 FIRM 表示 strong, fix，核心义是“坚固、稳固、确认、坚定”。
\end{itemize}

\begin{word}[**]{infirmity}{ɪnˈfɜːrməti}
  \wordbreakdown{不够强健的状态：in-（不）+ firm（强壮、稳固）}
  \wordfamily{infirm（虚弱的）；firm（稳固的）；affirm（断言）；confirm（证实）}
  \wordsense{n. 虚弱；病弱；衰弱}
  \wordphrase{the infirmities of old age（老年人的体弱）}
  \wordexample{He struggled with the infirmities of age in his final years.（晚年时他一直与年老体衰作斗争。）}
  \wordsense{n. 弱点；缺陷}
  \wordphrase{human infirmity（人性的弱点）}
  \wordexample{The novel portrays kindness toward ordinary human infirmity.（这部小说对普通人的弱点表现出宽容。）}
\end{word}



\begin{word}[***]{affirm}{əˈfɜːrm}
  \wordbreakdown{使立场坚定下来：af<ad（向）+ firm（坚定）}
  \wordfamily{affirmation（确认；断言）；affirmative（肯定的）；confirm（证实）；firm（稳固的）}
  \wordsense{vt. 断言；确认；申明}
  \wordphrase{affirm a belief / affirm one's innocence（断言一种信念／申明自己无罪）}
  \wordexample{She affirmed that the document was authentic.（她确认这份文件是真的。）}
\end{word}



\begin{word}[***]{affirmative}{əˈfɜːrmətɪv}
  \wordbreakdown{表示肯定和确认的：affirm + -ative}
  \wordfamily{affirm（确认）；affirmation（肯定）；confirm（证实）；negative（否定的）}
  \wordsense{a. 肯定的；赞成的；积极的}
  \wordphrase{an affirmative answer / affirmative action（肯定回答／平权行动）}
  \wordexample{The board gave an affirmative response to the proposal.（董事会对这项提议作出了肯定答复。）}
  \wordsense{n. 肯定答复}
  \wordphrase{answer in the affirmative（作肯定回答）}
  \wordexample{When asked if she would lead the project, she replied in the affirmative.（当被问到是否愿意负责这个项目时，她给出了肯定答复。）}
\end{word}



\begin{word}[***]{confirm}{kənˈfɜːrm}
  \wordbreakdown{使更加稳固：con-（加强）+ firm（坚定、固定）}
  \wordfamily{confirmation（确认）；confirmed（已确认的；根深蒂固的）；affirm（确认）；firm（稳固的）}
  \wordsense{vt. 证实；确认}
  \wordphrase{confirm a booking / confirm the news（确认预订／证实消息）}
  \wordexample{The test results confirmed the doctor's suspicion.（检测结果证实了医生的怀疑。）}
  \wordsense{vt. 批准；使坚定}
  \wordphrase{confirm an appointment / confirm sb in a belief（批准任命／使某人更加坚信）}
  \wordexample{The senate confirmed her as the new minister.（参议院批准她出任新部长。）}
\end{word}



\begin{word}[***]{confirmed}{kənˈfɜːrmd}
  \wordbreakdown{已经被固定或证实的：confirm 的过去分词形容词用法}
  \wordfamily{confirm（证实）；confirmation（确认）；affirm（断言）；infirmity（虚弱）}
  \wordsense{a. 已被证实的；确定的}
  \wordphrase{a confirmed case / confirmed data（确诊病例／已确认数据）}
  \wordexample{The hospital reported three confirmed cases that morning.（那天早晨医院报告了三例确诊病例。）}
  \wordsense{a. 根深蒂固的；惯常的}
  \wordphrase{a confirmed bachelor / a confirmed pessimist（老单身汉／十足的悲观主义者）}
  \wordexample{He is a confirmed coffee lover who starts every day with two cups.（他是个十足的咖啡爱好者，每天都以两杯咖啡开始。）}
\end{word}



\begin{word}[***]{confirmation}{ˌkɑːnfərˈmeɪʃn}
  \wordbreakdown{使事情稳固并得到证实：confirm + -ation}
  \wordfamily{confirm（证实）；confirmed（已确认的）；affirmation（断言）；affirmative（肯定的）}
  \wordsense{n. 证实；确认；确认书}
  \wordphrase{written confirmation / seek confirmation（书面确认／寻求证实）}
  \wordexample{We are still waiting for official confirmation of the results.（我们仍在等待对结果的正式确认。）}
  \wordsense{n. 坚振礼（宗）}
  \wordphrase{a confirmation ceremony（坚振礼仪式）}
  \wordexample{The family attended the boy's confirmation at the church.（这家人参加了男孩在教堂举行的坚振礼。）}
\end{word}



\begin{word}[***]{firmament}{ˈfɜːrməmənt}
  \wordbreakdown{像被固定起来一样稳固的天空：firm（稳固）}
  \wordfamily{firm（稳固的）；confirm（证实）；affirm（断言）；infirmity（虚弱）}
  \wordsense{n. 苍穹；天空}
  \wordphrase{the starry firmament（繁星点点的天空）}
  \wordexample{Clouds drifted slowly across the dark firmament.（云缓缓飘过漆黑的苍穹。）}
\end{word}

"""

path.write_text(text[:start] + new_chunk + text[end:], encoding="utf-8")
