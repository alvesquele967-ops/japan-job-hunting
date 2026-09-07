# Japan Job Hunting · 日本就活 Agent

面向日本新卒、留学生和外国人赴日就业的 Codex Skill。

它可以协助完成公司搜索、企业研究、ES、履歴書、Web Test、面试准备、Offer 对比和申请进度整理。

## 安装

将 `japan-job-hunting` 文件夹放入 Codex 的个人技能目录：

```text
~/.agents/skills/japan-job-hunting/
```

目录中应直接包含 `SKILL.md`。

Windows PowerShell：

```powershell
$skillTarget = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -LiteralPath './japan-job-hunting' -Destination $skillTarget -Recurse
```

macOS / Linux：

```sh
mkdir -p ~/.agents/skills
cp -R ./japan-job-hunting ~/.agents/skills/
```

## 使用

在求职项目中调用：

```text
$japan-job-hunting 我想去日本做 IT，先帮我建立求职画像，再找适合的公司。
```

也可以直接进入具体环节：

```text
$japan-job-hunting 按已有条件找公司，不补充，直接搜索。
$japan-job-hunting 我要投某公司的新卒工程师岗位，帮我研究。
$japan-job-hunting 用我提供的模板生成履歴書。
$japan-job-hunting 模拟目标公司的一面。
$japan-job-hunting 我现在有哪些公司在投？接下来做什么？
```

说“直接查”或“不补充”时，Skill 会用已有资料继续搜索，并将未知条件标记出来。

## 模板

从 [リクナビNEXT 模板页面](https://next.rikunabi.com/tenshokuknowhow/rirekisho/template/) 下载需要的 DOCX、XLSX 或 PDF，放到已安装技能的 `templates/resume/`。

[模板来源清单](japan-job-hunting/templates/resume/manifest.json) 记录了可下载的格式和文件哈希；[模板说明](japan-job-hunting/templates/resume/GUIDE.md) 说明适用场景。公司指定格式优先。

## 数据

个人画像、公司研究和申请进度保存在项目的 `.jobhunt/` 中。仓库的 `.gitignore` 已排除该目录和本地模板，避免将个人求职资料提交到 Git。

## 示例

[演示流程](DEMO.md) 使用完全虚构的求职者和公司，展示从画像补充到岗位研究的结果。[测试记录](demo/TEST_RESULTS.md) 和 [效果图](demo/assets/synthetic-demo.svg) 一并提供。

![演示流程](demo/assets/synthetic-demo.svg)

格式参考：[Codex Skills](https://learn.chatgpt.com/docs/build-skills) 与 [Agent Skills specification](https://agentskills.io/specification)。
