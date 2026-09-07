# Japan Job Hunting · 日本就活 Agent

可安装的 Codex Agent Skill，支持日本新卒、留学生及外国人赴日就业：公司发现、企业研究、ES、履歴書、Web Test、面试、Offer 比较和求职进度管理。

## 安装

下载或克隆本仓库，把其中的 `japan-job-hunting` 文件夹复制到个人技能目录 `~/.agents/skills/`。
最终结构应是 `~/.agents/skills/japan-job-hunting/SKILL.md`，不要多嵌套一层。

Windows PowerShell，在仓库根目录运行：

```powershell
$skillTarget = Join-Path $HOME '.agents/skills'
New-Item -ItemType Directory -Force -Path $skillTarget | Out-Null
Copy-Item -LiteralPath './japan-job-hunting' -Destination $skillTarget -Recurse
```

macOS / Linux，在仓库根目录运行：

```sh
mkdir -p ~/.agents/skills
cp -R ./japan-job-hunting ~/.agents/skills/
```

上述是首次安装示例。更新时先备份自己添加的模板，并替换技能代码；私人求职 workspace 独立保存。新任务中查看技能列表；若尚未显示，重启 Codex。

## 怎么用

在用于求职的项目目录打开 Codex，用自然语言调用：

```text
$japan-job-hunting 我想去日本做 IT，先帮我补充求职画像。
$japan-job-hunting 按已保存的条件找公司，不补充，直接搜索。
$japan-job-hunting 我要投某公司的新卒工程师岗位，帮我研究。
$japan-job-hunting 用我提供的模板生成履歴書。
$japan-job-hunting 模拟目标公司的一面。
$japan-job-hunting 我现在有哪些公司在投？接下来要做什么？
```

默认会少量询问关键缺失信息；明确说“不补充”“直接查”就立即执行，未知信息标为 UNKNOWN。以上都是调用示例，不是作者或使用者的个人资料。

## 简历模板

公开版不附带第三方模板二进制文件。到 [リクナビNEXT 模板页面](https://next.rikunabi.com/tenshokuknowhow/rirekisho/template/) 下载需要的 DOCX、XLSX、PDF，放入已安装技能的 `templates/resume/`。已有本地模板可继续使用。
[来源清单](japan-job-hunting/templates/resume/manifest.json)包含分类、下载链接和原始版本哈希；[模板说明](japan-job-hunting/templates/resume/GUIDE.md)说明选择方式。
公司强制格式优先。技能不会把空目录自动替换成自创模板，也不会把网站填写示例当用户经历。

## 数据与 Git

个人画像、公司研究、申请状态与生成材料保存在使用时项目的 `.jobhunt/`，不写入技能目录。
本仓库 `.gitignore` 排除 `.jobhunt/`、本地构建/测试产物、交付报告、ZIP、IDE 配置、缓存和本地模板。运行时 `.jobhunt/` 也会生成自己的忽略规则。
不要把含个人资料的文件随意放入其他可追踪位置。`.gitignore` 对已经提交或追踪的文件不生效，提交前应查看 `git status` 与暂存差异。

## 结构与依赖

- `japan-job-hunting/SKILL.md`：技能入口及模式选择。
- `references/`：各阶段工作流、数据保存和使用说明。
- `scripts/`：字数统计、工作区管理、模板扫描、事实引用校验。
- `schemas/`：结构化记录约定。
- `templates/resume/`：模板说明、来源清单及本地模板位置。

辅助脚本要求 Python 3.10+；PDF 扫描可选 pypdf。在线企业研究需要网页访问，正式文件制作需要运行环境中的文档、表格或 PDF 工具及渲染能力。
本 Skill 不会自行投递申请、发邮件、接受 Offer 或启动后台提醒。正式材料仅使用已确认的个人事实。

## 上传到 GitHub

把仓库源文件提交到自己的 GitHub 仓库即可；不要手工上传本地忽略目录或旧版交付 ZIP。若使用 GitHub 网页上传，可使用单独生成的 GitHub 发布包，其内容已排除本地产物。

技能格式依据：[Codex Skills](https://learn.chatgpt.com/docs/build-skills)、[Agent Skills specification](https://agentskills.io/specification)。

## 虚构效果演示

仓库提供了一个可公开的端到端演示：从 Guided Intake、持久化画像，到带 `NEEDS_VERIFICATION` 标记的岗位研究快照。它使用专门编写的虚构人物、学校、公司和岗位，绝不读取任何使用者工作区。查看 [演示说明](DEMO.md)、[对话记录](demo/transcript.md) 或本地打开 [效果页面](demo/preview.html)。

![虚构流程效果图](demo/assets/synthetic-demo.svg)

完整测试输出见 [演示测试结果](demo/TEST_RESULTS.md)。

运行以下命令可复现演示数据校验：

```powershell
python .\demo\run_demo_tests.py
```
