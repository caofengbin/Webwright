# Webwright

<p align="center">
  <img src="assets/webwright_logo.svg" alt="Webwright logo" width="320">
</p>

<p align="center"><b>让你的编码模型成为最先进的浏览器智能体</b></p>

<p align="center">
  <img src="https://img.shields.io/badge/python-%E2%89%A53.10-blue?logo=python&logoColor=white" alt="Python">
  <img src="https://img.shields.io/badge/playwright-chromium-green" alt="Playwright">
  <img src="https://img.shields.io/badge/backends-OpenAI%20%7C%20Anthropic%20%7C%20OpenRouter%20%7C%20DeepSeek-orange" alt="Backends">
  <img src="https://img.shields.io/badge/footprint-%E2%89%A4~1.5k%20LoC-brightgreen" alt="Footprint">
</p>

- 📝 **博客:** [Webwright: A Terminal Is All You Need For Web Agents](https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/)
- 🌐 **项目主页:** [microsoft.github.io/Webwright](https://microsoft.github.io/Webwright/)
- 🌍 **语言:** [English](README.md) | 中文

Webwright 为大语言模型(LLM)提供一个终端环境,模型可以在其中启动多个浏览器会话以检查页面并完成网络任务。它仅在需要时捕获和检查页面截图/状态。它强制要求每个网络任务都在一个可重新运行的 Python 脚本中端到端地完成,也就是说,你的网络代理浏览历史就是一个单一的代码文件。没有多智能体系统,没有图引擎,没有插件层,没有隐藏的编排——只有一个终端、一个浏览器和一个模型。

已经拥有自己最喜爱的代理,并希望让 Claude Code、Codex、Hermes、OpenClaw 在浏览器任务中变得更强大?可以考虑添加 [Webwright 插件/技能](#-作为插件使用)!

---

## 📰 新闻

- **2026-06-01** — 新增 DeepSeek 官方 API 后端;可通过 `model_deepseek.yaml` 和 `.env` 中的 `DEEPSEEK_API_KEY` 使用。
- **2026-05-11** — 支持 Task2UI 模式:Webwright 完成任务后将任务结果渲染为基于 HTML 的 Web 应用,你可以方便地查看和复用。
- **2026-05-06** — 添加了 Codex 和 Claude Code 的插件清单;通过 `/plugin install webwright@webwright` 安装。OpenClaw 和 Hermes Agent 集成已上线;同一个 `skills/webwright/` 目录现在可在 Claude Code、Codex、OpenClaw 和 Hermes 中加载。
- **2026-05-04** — 首次公开发布:约 1.5k 行代码,支持 OpenAI / Anthropic / OpenRouter 后端,Playwright 环境。

---

<details>
<summary><strong>💡 动机:在有状态浏览器中超越逐步式网页交互</strong></summary>

如今,大多数网络代理将浏览器会话本身视为工作空间:在每一步,模型接收当前页面状态并预测单个下一步操作——一次点击、一次输入、一个 DOM 选择器或一次简短的工具调用。无论格式如何,代理都被锁定在预定义的交互循环中,一次只预测一个网络动作。当 LLM 较弱时这种框架是有用的。但随着模型在编写和调试代码方面变得更强,同一框架反而成为瓶颈。

Webwright 采取了不同的立场:**将代理与浏览器分离**,把浏览器视为代理在开发程序时可以启动、检查和丢弃的资源。持久化的成果不是浏览器会话——而是**本地工作空间中的代码和日志**。

- 🧱 **稳健、可复用的网页环境交互** —— 不再使用脆弱的像素级动作,带终端的编码代理可以查询元素、等待条件、处理懒加载或重渲染等动态行为。生成的脚本可以重新运行、改编并在不同任务间共享,而不是从头重新发现。
- ⚡ **复杂工作流的高效组合** —— 选日期、填表单等多步骤交互变成一段紧凑的程序。循环、函数和抽象使代理能在相似任务(例如不同日期)上泛化,无需重新预测相同的低级序列。更少的交互轮次、更快的执行速度、长时序任务上更少的错误累积。
- 🧪 **以工作空间为状态,而非以浏览器为状态** —— 代理可以编写探索性脚本、启动新的浏览器会话,并自行决定何时截图和检查失败,就像人类工程师迭代 RPA 脚本一样。
- 🪄 **极简却出奇有效** —— 这种精简的设置在处理复杂任务,尤其是长时序网络任务方面表现良好(参见[性能](#-性能))。

</details>

---

<details>
<summary><strong>🌟 为什么选择 Webwright</strong></summary>

大多数网络代理框架将真正的代理循环掩埋在层层抽象之下。Webwright 采取相反的立场:

- 🪶 **轻量级设计** —— 核心代理循环位于单个 ~450 行文件中,Playwright 环境约 570 行,CLI 约 150 行。
- 🧩 **可插拔模型后端** —— OpenAI、Anthropic、OpenRouter 和 DeepSeek,每个约 150–200 行。
- 🔍 **零隐藏框架** —— 仅依赖 `httpx`、`pydantic`、`playwright` 和 `typer`。
- 🔁 **扁平的 提示 → 观察 → 执行 脚本循环** —— 端到端可读,易于调试,易于 fork。
- 🧪 **以运行产物为先** —— 每次运行都将轨迹和截图写入磁盘以供检查。

如果你想要一个最小化、易于调试的浏览器代理起点,而不是另一个重量级平台,这就是它。

</details>

---

<details>
<summary><strong>🆚 Webwright 与其他浏览器代理仓库的不同之处</strong></summary>

它们在架构层面的差异:

|                     | **Stagehand (Browserbase)**                                  | **agent-browser (Vercel)**                                                | **browser-use**                                       | **Webwright**                                                       |
| ------------------- | ------------------------------------------------------------ | ------------------------------------------------------------------------- | ----------------------------------------------------- | ------------------------------------------------------------------------- |
| **范式**        | 混合式:代码 + NL 原语 (`act` / `extract` / `agent`)   | CLI 工具,由*另一个*代理(Claude Code、Codex 等)调用            | 在 DOM/AX 快照上自主运行的 LLM 代理循环       | **带终端的编码代理**;浏览器只是它启动的一个环境 |
| **动作空间**    | Playwright 代码,或 NL → LLM 翻译为 Playwright           | 离散子命令(`open`、`click @e2`、`snapshot`、`eval`)            | 由 LLM 选择的索引化点击/输入动作         | **自由形式的 Python(自行编写 Playwright 脚本)**                       |
| **"状态"是什么?**| 浏览器会话                                          | 浏览器会话(由守护进程跨 CLI 调用维持)                     | 浏览器会话                                   | **本地工作空间——代码、截图、日志。** 浏览器是一次性的。 |
| **循环形态**      | 命令式;`agent()` 在需要时执行多步操作            | 每个 CLI 调用一个微步骤                                         | 观察 → 预测下一动作 → 执行 → 重复      | 编写代码 → 执行 → 检查截图 → 修复(代码即动作)      |
</details>


---

## 🎥 演示
https://github.com/user-attachments/assets/4ed94cd5-11be-4daa-b2d7-1260a803baca

---

## 📊 性能

在两个真实网站基准上,以 100 步预算达到当前最先进水平 —— 完整细节请参见[博客文章](https://www.microsoft.com/en-us/research/articles/webwright-a-terminal-is-all-you-need-for-web-agents/)。

- 🏆 **Online-Mind2Web (300 个任务):** 使用 GPT-5.4 达到 **86.7%** —— 在 AutoEval 类别中位居开源框架最高水平。Claude Opus 4.7 达到 **84.7%**,在困难子集上更强(**80.5%** vs. GPT-5.4 在 N=100 时的 76.6%)。
- 🚀 **Odysseys (200 个长时序任务):** 使用 GPT-5.4 达到 **60.1%**(平均 76.1 步) —— 比之前的 SOTA(Opus 4.6 的 44.5%,使用基于视觉的方法和持久浏览器)**高出 15.6 个百分点**,比基础 GPT-5.4(33.5%,使用 xy 坐标预测和持久浏览器)**高出 26.6 个百分点**。
- 🧠 **代码即动作胜过坐标预测:** 在所有难度划分上,Webwright 显著优于复现的 GPT-5.4 截图+xy 坐标基线。
- 🧰 **小模型 + 可复用工具:** 生成的脚本可以打包为参数化的 CLI 工具——即使是 **Qwen-3.5-9B** 在拥有 5 个以上工具的情况下也能很好地完成 Online-Mind2Web 网站上的任务。

<p align="center">
  <img src="assets/odysseys_eval_step100.png" alt="Odysseys long-horizon eval @ 100 steps" width="49%">
  <img src="assets/om2w_autoeval_step100.png" alt="Online-Mind2Web AutoEval @ 100 steps" width="49%">
</p>

---

## 🗺️ 项目结构

```
webwright/
├── pyproject.toml           # 包: webwright
├── src/webwright/
│   ├── run/cli.py           # CLI 入口 (`webwright`)
│   ├── agents/default.py    # 核心代理循环
│   ├── environments/        # Playwright 浏览器工作空间
│   ├── tools/               # image_qa、self_reflection
│   ├── models/              # openai_model、anthropic_model、deepseek_model、base
│   ├── config/              # base.yaml、model_openai.yaml、model_claude.yaml、model_deepseek.yaml
│   └── utils/
├── assets/
│   └── task_showcase/       # 用于可重复运行的小型 Flask 仪表盘
│       ├── app.py
│       ├── templates/       # dashboard.html、task.html
│       └── tasks/<short_id>/ # 每个任务的 task.json + report.json
├── tests/
└── outputs/                 # 运行产物(轨迹、截图)
```

---

## 📰 任务展示(可重复运行的仪表盘)

[`assets/task_showcase/`](assets/task_showcase/README.md) 下的小型 Flask 应用将
**可重复**的 odyssey 任务(优惠、库存、列表、招聘信息、天气等)的 Webwright 运行结果
整合到一个仪表盘中。每个任务仅需两个文件—— `task.json`(元数据)和
`report.json`(精心策划、结构化的输出:来源 + 表格、列表、摘要等结果章节)
—— 模板会以通用方式渲染它们,因此添加新任务只需在
`assets/task_showcase/tasks/` 中放入新文件夹即可。

```bash
pip install flask
python assets/task_showcase/app.py    # http://127.0.0.1:5005
```

要让 Webwright 在运行时生成可供渲染器使用的任务文件夹,请叠加 Task Showcase 配置:

```bash
python -m webwright.run.cli \
    -c base.yaml -c model_openai.yaml -c task_showcase.yaml \
    -t "<可重复的网页任务>" \
    --task-id my_repeatable_task \
    -o outputs/default
```

> **注意:** 仅当包含 `-c task_showcase.yaml` 时才会生成 `report.json`。普通的 `base.yaml`
> 运行会生成 `trajectory.json` 和调试产物,但不会生成 `report.json`。

该运行会在输出工作空间内写入 `task_showcase/tasks/<short_id>/task.json` 和
`report.json`。无需将这些生成的文件复制回仓库即可渲染:

```bash
python assets/task_showcase/app.py \
    --tasks-dir outputs/default/<run>/task_showcase/tasks
```

---

## 🚀 快速开始

### 前置条件

- Python 3.10+
- 通过 Playwright 安装的 Chromium
- 所选后端的 API 密钥(OpenAI、Anthropic、OpenRouter 或 DeepSeek)

### 安装

```bash
pip install -e .
playwright install chromium
```

### 运行

为已配置的后端导出凭据,或将凭据写入项目 `.env` 文件。例如,使用
`model_openai.yaml` 时设置 `OPENAI_API_KEY`,使用 `model_claude.yaml` 时设置
`ANTHROPIC_API_KEY`,使用 `model_deepseek.yaml` 时设置 `DEEPSEEK_API_KEY`。
`image_qa` 和 `self_reflection` 工具默认使用相同的已配置模型,因此 Anthropic 或
DeepSeek 运行无需 OpenAI 密钥。然后:

```bash
python -m webwright.run.cli \
    -c base.yaml -c model_openai.yaml \
    -t "Search for flights from SEA to JFK on 2026-08-15 to 2026-08-20" \
    --start-url https://www.google.com/flights \
    --task-id demo_openai \
    -o outputs/default
```

使用 DeepSeek 时,在 `.env` 中添加:

```bash
DEEPSEEK_API_KEY=your_deepseek_api_key
```

然后运行:

```bash
python -m webwright.run.cli \
    -c base.yaml -c model_deepseek.yaml \
    -t "Search for flights from SEA to JFK on 2026-08-15 to 2026-08-20" \
    --start-url https://www.google.com/flights \
    --task-id demo_deepseek \
    -o outputs/default
```

### 🚩 命令行参数

| 参数 | 说明 |
|------|-------------|
| `-c` | 来自 `src/webwright/config/` 的配置文件(可叠加)。 |
| `-t` | 任务指令。 |
| `--start-url` | 初始页面。 |
| `--task-id` | 输出子文件夹名称。 |
| `-o` | 输出目录。 |

---

## 🔌 作为插件使用

Webwright 同时为 [Claude Code](https://docs.claude.com/en/docs/claude-code/plugins)([`.claude-plugin/plugin.json`](.claude-plugin/plugin.json))和 [OpenAI Codex](https://developers.openai.com/codex/plugins)([`.codex-plugin/plugin.json`](.codex-plugin/plugin.json))提供插件清单,共享技能位于 [`skills/webwright/`](skills/webwright/),斜杠命令位于 [`skills/webwright/commands/`](skills/webwright/commands/)。宿主代理原生驱动 Webwright 循环——除你的宿主订阅外,无需额外的 LLM API 密钥或费用。原生读取 PNG 截图的宿主会跳过 `image_qa` / `self_reflection` 工具。

通用运行时依赖(任意路径完成后安装一次):

```bash
pip install -e .
playwright install chromium
```

<details>
<summary><b>Claude Code</b></summary>

### 安装

通过 Claude Code 内置的市场安装:

```text
# 1. 将此仓库添加为 Claude Code 插件市场
/plugin marketplace add microsoft/Webwright

# 2. 从该市场安装插件
/plugin install webwright@webwright
```

更喜欢本地检出?将 marketplace 命令指向克隆的仓库:

```text
/plugin marketplace add /absolute/path/to/Webwright
/plugin install webwright@webwright
```

### 使用

安装后**启动一个新的 Claude Code 会话** —— 插件在会话开始时加载,只有重启后才会出现。

你可以用纯英语向 Claude Code 提问(技能根据其描述自动激活),也可以使用斜杠命令之一:

```
/webwright:run search Google Flights for flights from SEA to JFK on 2026-08-15 to 2026-08-20
/webwright:craft search a ticket on Google Flights from LAX to SFO depart June 7 return June 14
```

- `/webwright:run`(或任何普通提示)为字面任务值生成**一次性**的 `final_script.py`。
- `/webwright:craft` 生成**可复用的 CLI 工具**:`final_script.py` 变成一个参数化函数,带有 Google 风格的 `Args:` 文档字符串,以及 `argparse` 包装器,其参数标志默认为具体的任务值,因此你可以稍后用不同参数重新运行——例如 `python final_script.py --origin JFK --destination LAX --depart-date 2026-07-01`。

在两种模式下,Claude Code 都会搭建一个含 `plan.md` 的工作空间,在 `final_runs/run_<id>/` 下运行带插桩的 Playwright 脚本,并针对保存的截图对每个关键点进行视觉自验证。

</details>

<details>
<summary><b>OpenAI Codex</b></summary>

### 安装

Codex 读取 Claude 风格的市场,因此同一仓库可作为 Codex 插件市场。在 Codex CLI 中:

```bash
# 1. 将此仓库添加为 Codex 插件市场
codex plugin marketplace add microsoft/Webwright

# 2. 打开插件浏览器并安装 Webwright
codex
/plugins
```

更喜欢本地检出?

```bash
codex plugin marketplace add /absolute/path/to/Webwright
```

然后重启 Codex 以拾取新的市场和插件。

### 使用

在新的 Codex 线程中,可以用纯英语提问(技能根据其描述自动激活),也可以使用 `@webwright` 显式调用捆绑技能:

```
@webwright search Google Flights for flights from SEA to JFK on 2026-08-15 to 2026-08-20
```

Codex 会搭建一个含 `plan.md` 的工作空间,在 `final_runs/run_<id>/` 下运行带插桩的 Playwright 脚本,并针对保存的截图对每个关键点进行视觉自验证。

要在不卸载的情况下关闭插件,请在 `~/.codex/config.toml` 中将其条目设为 `enabled = false` 并重启 Codex。

</details>

<details>
<summary><b>🦞 OpenClaw</b></summary>

### 安装

直接从本地检出安装(支持路径、归档、npm 规范、git 仓库或 `clawhub:` 规范):

```bash
openclaw plugins install /absolute/path/to/Webwright
openclaw gateway restart   # 重新加载以拾取插件和技能
```

验证:

```bash
openclaw plugins list | grep webwright
openclaw skills  list | grep webwright   # 应显示 "✓ ready"
```

### 使用

`webwright` 技能现已可用于任何 OpenClaw 代理界面(CLI、Telegram 等)——可通过自然语言向代理发问调用它,或通过 [`skills/webwright/commands/`](skills/webwright/commands/) 下的斜杠命令调用,例如 `/webwright run <task>`。

卸载:`openclaw plugins uninstall webwright`。

</details>

<details>
<summary><b>Hermes Agent</b></summary>

### 安装

[Hermes Agent](https://github.com/NousResearch/hermes-agent) 是一个[兼容 skills 的客户端](https://agentskills.io),因此同一个 `skills/webwright/` 文件夹可作为 Hermes 技能加载。将其符号链接到你的 Hermes 用户技能目录:

```bash
mkdir -p ~/.hermes/skills
ln -sfn /absolute/path/to/Webwright/skills/webwright ~/.hermes/skills/webwright
```

无需 Hermes 特定的清单;只加载 `SKILL.md`。

### 使用

启动 Hermes (`hermes`) 并以自然语言要求其执行网页任务——技能根据其描述自动激活。你也可以使用 `/webwright` 显式调用。

注意:[`skills/webwright/commands/`](skills/webwright/commands/) 下提供的命名子命令(`/webwright:run`、`/webwright:craft`)是 Claude Code / Codex 的约定,在 Hermes 中无效;但技能本身仍可端到端工作。

</details>

## 📃 轨迹比较与查看器

你可以使用 Webwright 框架及其 Codex / GitHub Copilot 技能变体运行相同的任务,并查看不同框架之间的 token 使用情况和轨迹对比。轨迹查看器支持 Codex、GitHub Copilot 和 Webwright 框架的轨迹。

![Trajectory comparison](assets/trajectory-compare.png)

### 使用方法

```bash
cd assets/compare_trajectory/
python3 -m http.server
```

在浏览器中打开网页,并上传 Webwright 的 `raw_responses.jsonl` 并附加 `trajectory.json` 来查看。然后在另一侧上传 Codex 或 GitHub Copilot 的轨迹。

### 获取 Codex 轨迹:

```
ls ~/.codex/sessions/2026/MONTH/DAY/SESSION_ID.jsonl
```

### 获取 GitHub Copilot 轨迹:

```
/export file session
-> session.md 是可上传的轨迹
```

### 快速比较

#### "查找 2005-2015 年间制造、价格在 25,000 至 50,000 美元之间、里程少于或等于 50,000 英里的最便宜的二手 8 缸宝马。"

| Tokens | Webwright Harness (Local Browser Mode) | Codex Webwright Skill |
| --- | ---: | ---: |
| Input | 420,433 | 3,271,143 |
| Output | 3,593 | 20,040 |
| Reasoning | 0 | 4,410 |
| Cached | 217,216 | 3,081,3440 |
| Total | 424,026 | 3,291,183 |

具体运行结果可能有所不同。

---

## 致谢

- [SWE-agent/mini-swe-agent](https://github.com/SWE-agent/mini-swe-agent/tree/main) —— 最小代理循环的设计灵感来源。
- [Playwright](https://playwright.dev/) —— 浏览器自动化。

## 引用

如果你在研究中使用 Webwright 或在其基础上构建,请引用此仓库:

```bibtex
@misc{webwright2026,
  title        = {Webwright: A terminal is all you need for web agents},
  author       = {Lu, Yadong and Xu, Lingrui and Huang, Chao and Awadallah, Ahmed},
  year         = {2026},
  howpublished = {\url{https://github.com/microsoft/Webwright}},
  note         = {GitHub repository}
}
```
