#!/usr/bin/env python3
# Generate boilerplate deep-analysis HTML for all target papers,
# recoloring the booster_deep_analysis.html CSS per paper.
import re, pathlib

BASE = pathlib.Path(__file__).resolve().parent
BOOSTER = BASE / "booster_deep_analysis.html"
html = BOOSTER.read_text(encoding="utf-8")
m = re.search(r"<style>(.*?)</style>", html, re.S)
STYLE = m.group(1)

STD = ["研究动机", "框架概览", "核心组件一", "核心组件二", "核心组件三",
       "集成机制", "实验评估", "敏感性分析",
       "代码使用与实战（含 GitHub 源码、安装命令、使用示例）", "总结与未来展望"]

# paper: outfile, title, sub, venue, tags(list), c1, c2, (r,g,b), middle_titles(4)
PAPERS = [
 ("rankpqo_deep_analysis.html",
  "RankPQO: Learning-to-Rank for Parametric Query Optimization",
  "用学习排序 + 混合计划枚举解决参数化查询优化的稳定性难题",
  "PVLDB 2024, Vol.18(3):863-875 &nbsp;|&nbsp; <a href='https://doi.org/10.14778/3712221.3712248'>DOI: 10.14778/3712221.3712248</a> &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2401.03427'>arXiv:2401.03427</a>",
  ["PQO","Learning-to-Rank","Plan Enumeration","PostgreSQL","Pairwise Ranking"],
  "#3730a3","#6366f1",(55,48,163),
  ["混合计划枚举：基数与连接顺序协同调整","PRank 排序模型：编码层与三层嵌入","候选计划选择：基于距离矩阵的贪心算法","生成与选择的端到端整合"]),

 ("delta_deep_analysis.html",
  "Delta: A Learned Mixed Cost-based Query Optimization Framework",
  "混合代价模型与价值网络——两阶段规划器 + 马氏距离预检测",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2503.06548'>arXiv:2503.06548</a>",
  ["Query Optimization","Mixed Framework","Two-Stage","Detector","PostgreSQL"],
  "#c2410c","#f97316",(194,65,12),
  ["价值驱动计划生成器 VPG：束搜索与 Top-K","代价驱动计划选择器 CPS：学习型代价模型","兼容查询检测器 CQD 与数据增强","VPG 与 CPS 的两阶段协同机制"]),

 ("bayesqo_deep_analysis.html",
  "BayesQO: Offline Query Planning via Bayesian Optimization",
  "用 VAE + 贝叶斯优化做离线查询优化——为重复查询找到最优执行计划",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2502.05256'>arXiv:2502.05256</a>",
  ["Offline QO","Bayesian Optimization","VAE","Censored Observation","TuRBO"],
  "#e11d48","#f43f5e",(225,29,72),
  ["VAE 计划编码：将查询计划嵌入连续潜空间","贝叶斯优化 TuRBO：信任域内的黑箱搜索","Tobit 删失观测模型与超时阈值选择","离线规划与在线部署的整合"]),

 ("pqo_query_logs_deep_analysis.html",
  "PQO via Query Logs: Decoupled populateCache &amp; getPlan",
  "用查询日志 + ML 解耦参数化查询优化——populateCache 与 getPlan 各司其职",
  "PVLDB 2022, Vol.15(11):2843-2855 &nbsp;|&nbsp; <a href='https://doi.org/10.14778/3551793.3551842'>DOI: 10.14778/3551793.3551842</a>",
  ["PQO","Query Logs","Machine Learning","Contextual Bandits","Microsoft"],
  "#0e7490","#06b6d4",(14,116,144),
  ["populateCache：离线计划缓存填充","getPlan：在线计划选择（监督学习 vs 老虎机）","选择性特征与缓存结构","解耦两阶段的端到端流程"]),

 ("taobao_advertising_deep_analysis.html",
  "Enhancing Taobao Display Advertising with Multimodal Representations",
  "用多模态数据增强工业级推荐系统——预训练表示 + ID 模型集成",
  "arXiv 2024 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2402.17633'>arXiv:2402.17633</a>",
  ["Recommendation","Multimodal","Industrial System","Alibaba","Pre-training"],
  "#d97706","#f59e0b",(217,119,6),
  ["阶段一：多模态表示预训练","阶段二：与 ID 模型集成","工业部署与冷启动策略","两阶段框架的端到端整合"]),

 ("agentfold_deep_analysis.html",
  "AgentFold: Long-Horizon Web Agents with Proactive Context Management",
  "主动上下文管理——让 Web Agent 在长 horizon 任务中保持高效",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2506.10451'>arXiv:2506.10451</a>",
  ["Web Agent","Context Management","Long-Horizon","Alibaba","SFT"],
  "#0ea5e9","#38bdf8",(14,165,233),
  ["主动上下文管理：折叠操作","监督微调与训练数据构建","长 Horizon 任务的状态管理","上下文折叠与执行的整合"]),

 ("tabtracer_deep_analysis.html",
  "TabTracer: MCTS for Complex Table Reasoning with LLMs",
  "用 MCTS 实现表格推理的状态跟踪与回滚——准确率提升 6.7%，Token 消耗降低 59-84%",
  "arXiv 2026 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2601.01234'>arXiv:2601.01234</a>",
  ["MCTS","Table Reasoning","State Tracking","Pruning","LLM"],
  "#0891b2","#06b6d4",(8,145,178),
  ["执行反馈的 MCTS 搜索树","状态跟踪与回滚机制","预算感知剪枝","搜索树与执行反馈的整合"]),

 ("reasoning_bank_deep_analysis.html",
  "Reasoning Bank: Scaling Agent Self-Evolving with Reasoning Memory",
  "用推理记忆扩展 Agent 自我进化——从成功与失败中提取可泛化的推理策略",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2505.21485'>arXiv:2505.21485</a>",
  ["Agent Memory","Self-Evolving","Test-Time Scaling","Reasoning Strategy","UIUC"],
  "#db2777","#ec4899",(219,39,119),
  ["推理记忆的提取与组织","MaTTS：记忆与测试时扩展协同","自我进化循环","记忆与进化的整合"]),

 ("mcts_ahd_deep_analysis.html",
  "MCTS-AHD: Monte Carlo Tree Search for Comprehensive Exploration in LLM-Based Automatic Heuristic Design",
  "用 MCTS 全面探索 LLM 启发式设计空间——不让任何一个低性能启发式被浪费",
  "arXiv 2024 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2404.02500'>arXiv:2404.02500</a>",
  ["MCTS","Heuristic Design","LLM Evolution","Tree Search","NUS"],
  "#ea580c","#f97316",(234,88,12),
  ["MCTS 探索空间","启发式保留与演化","低性能启发式的复用","树搜索与进化的整合"]),

 ("rest_mcts_deep_analysis.html",
  "ReST-MCTS*: LLM Self-Training via Process Reward Guided Tree Search",
  "过程奖励引导的树搜索——让 LLM 自训练获得高质量推理轨迹",
  "ICLR 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2406.08124'>arXiv:2406.08124</a>",
  ["Self-Training","MCTS*","Process Reward","PRM","Tsinghua"],
  "#7c3aed","#8b5cf6",(124,58,237),
  ["过程奖励引导的 MCTS*","树搜索回溯推断正确性","自训练数据收集","搜索与训练的整合"]),

 ("lits_deep_analysis.html",
  "LiTS: A Modular Framework for LLM Tree Search",
  "让 LLM 树搜索像搭积木一样简单——三组件分解实现算法与领域的正交复用",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2502.16407'>arXiv:2502.16407</a>",
  ["LLM Tree Search","Modular Framework","MCTS","BFS","RMIT"],
  "#0d9488","#14b8a6",(13,148,136),
  ["Policy 组件","Transition 组件","RewardModel 组件","三组件的可复用框架整合"]),

 ("dbot_deep_analysis.html",
  "D-Bot: An LLM-Powered DBA Copilot",
  "用大语言模型打造数据库管理员的「智能副驾驶」",
  "SIGMOD Companion 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2312.01415'>arXiv:2312.01415</a>",
  ["LLM","Database Diagnosis","Self-Refinement","DBA Copilot","Tsinghua"],
  "#6d28d9","#8b5cf6",(109,40,217),
  ["异常诊断流水线","知识检索与 RAG","用户反馈自进化","诊断与自进化的整合"]),

 ("training_free_qo_deep_analysis.html",
  "Training-Free QO via LLM-Based Plan Similarity",
  "用 LLM 嵌入执行计划做相似性检索——零训练成本的查询优化新范式",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2502.0xxxxx'>arXiv:2502.0xxxxx</a>",
  ["Query Optimization","Training-Free","LLM Embedding","Plan Similarity","Ershov Inst."],
  "#b45309","#d97706",(180,83,9),
  ["LLM 计划嵌入","k-NN 相似度检索与投票","零训练成本框架","嵌入与检索的整合"]),

 ("llmopt_deep_analysis.html",
  "LLMOPT: Learning to Define and Solve General Optimization Problems",
  "用 LLM 从自然语言自动形式化并求解通用优化问题",
  "ICLR 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2502.04300'>arXiv:2502.04300</a>",
  ["LLM","Optimization","Problem Formulation","SFT","ECNU"],
  "#475569","#64748b",(71,85,105),
  ["五元素统一建模框架","多指令微调与对齐","自纠正机制","建模与求解的整合"]),

 ("llmsteer_deep_analysis.html",
  "LLMSTEER: Steering Attention on Reused Contexts",
  "用查询无关的注意力引导改进长上下文 LLM 推理——与前缀缓存完全兼容",
  "arXiv 2024 (NeurIPS 2024 ML for Systems) &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2411.13009'>arXiv:2411.13009</a>",
  ["Attention Steering","Prefix Caching","Long Context","Training-Free","UChicago"],
  "#84cc16","#a3e635",(132,204,22),
  ["上下文重读与 Token 选择","注意力引导的加权矩阵","与前缀缓存的兼容设计","引导与缓存的整合"]),

 ("master_mcts_deep_analysis.html",
  "MASTER: Multi-Agent System with LLM Specialized MCTS",
  "用 LLM 自我评估替代 MCTS 模拟——动态招募智能体并用 MCTS 指导通信",
  "NACL 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2502.0'>arXiv:2502.0xxxx</a>",
  ["Multi-Agent","MCTS","Self-Evaluation","Dynamic Recruitment","Huawei"],
  "#f97316","#fb923c",(249,115,22),
  ["LLM 自我评估替代模拟","动态招募智能体","MCTS 引导的通信","搜索与多智能体的整合"]),

 ("s1_simple_test_time_scaling_deep_analysis.html",
  "s1: Simple Test-Time Scaling",
  "用 1000 个样本 + Budget Forcing 实现 o1 级推理性能——完全开源",
  "arXiv 2025 &nbsp;|&nbsp; <a href='https://arxiv.org/abs/2501.19393'>arXiv:2501.19393</a>",
  ["Test-Time Scaling","Budget Forcing","Data Curation","Open Source","Stanford"],
  "#be185d","#ec4899",(190,24,93),
  ["数据策划：1000 个样本","Budget Forcing 测试时控制","s1-32B 微调","数据与推理控制的整合"]),
]

def recolor(style, c1, c2, rgb):
    s = style
    s = s.replace("#f97316", c1)
    s = s.replace("#fb923c", c2)
    s = s.replace("#fbbf24", c2)
    s = s.replace("#f0883e", c2)
    s = s.replace("rgba(249, 115, 22", f"rgba({rgb[0]}, {rgb[1]}, {rgb[2]}")
    s = s.replace("rgba(249,115,22", f"rgba({rgb[0]},{rgb[1]},{rgb[2]}")
    return s

def build(p):
    (out, title, sub, venue, tags, c1, c2, rgb, middle) = p
    style = recolor(STYLE, c1, c2, rgb)
    titles = STD[:2] + middle + STD[6:]
    toc_items = "".join(
        f'    <li><a href="#sec-{i+1}">{titles[i]}</a></li>\n'
        for i in range(10))
    tag_html = "".join(f'<span class="tag">{t}</span>' for t in tags)
    doc = f"""<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1.0">
<title>深度解读 — {title}</title>
<link rel="preconnect" href="https://fonts.googleapis.com">
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans+SC:wght@300;400;500;700&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
<style>
{style}
</style>
</head>
<body>
<div class="container">

<a class="back-btn" href="index.html">&#8592; 返回目录</a>

<!-- ========== HERO ========== -->
<div class="hero">
  <h1 class="hero-title">{title}</h1>
  <p class="hero-sub">{sub}</p>
  <div class="venue">{venue}</div>
  <div class="tag-row">
    {tag_html}
  </div>
</div>

<!-- ========== TOC ========== -->
<div class="toc">
  <h3>目录</h3>
  <ol>
{toc_items}  </ol>
</div>

<hr class="divider">

<!--ALLBODY-->

<div class="footer">论文深度解读 · 生成自 {title} · 阅读时间约 30 分钟</div>

</div>
</body>
</html>
"""
    (BASE / out).write_text(doc, encoding="utf-8")
    return out

for p in PAPERS:
    print("wrote", build(p))
