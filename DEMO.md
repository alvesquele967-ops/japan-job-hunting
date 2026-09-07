# Skill 演示：虚构用户的完整就活流程

> **隐私说明**：本目录的姓名、学校、公司、岗位、日期、薪资、链接和经历均为专门创建的虚构测试资料，不对应任何真实个人、公司或招聘信息；不会读取、复制或上传使用者的 `.jobhunt/`。

## 场景

虚构用户「林澄（リン・チョウ）」是中国某大学软件工程专业的 2027 年毕业生，持有 JLPT N2，目标是东京的 Java 后端新卒岗位，需要工作签证支持。她要求先补充信息，再搜索。

这个演示测试两件事：先以少量高价值问题完成画像，再把缺少官方来源的岗位清楚标为 `NEEDS_VERIFICATION`，而不是把演示数据包装成真实招聘推荐。

## 对话记录

**用户**：`$japan-job-hunting 我想去日本做 IT，先帮我建立求职画像，再找适合的公司。`

**Agent**：我先确认会影响资格与排序的四项：毕业年月和是否新卒、后端技术与项目、日语实际沟通能力、是否需要签证支持。

**用户（虚构）**：2027 年 6 月本科毕业，软件工程。Java、Spring Boot、MySQL、Docker，做过校园预约系统；JLPT N2，可以用日语介绍项目。人在中国，需要签证支持。优先东京，后端优先，薪资和公司规模暂时不设硬条件。

**Agent**：已保存 8 条 `USER_CONFIRMED` 事实和 3 条偏好。接下来会优先搜索「2027卒 Java バックエンド 東京 新卒採用」，以公司官方当前年度页面核验资格、签证、薪资和截止时间。任何尚未确认的条件会显示为 `UNKNOWN` 或 `NEEDS_VERIFICATION`。

**用户（虚构）**：先给我一个结果长什么样的演示，不要把虚构公司当作真的。

**Agent**：以下是演示排序快照；三家公司均为虚构，绝不应拿来投递。

| 排名 | 公司／岗位 | 资格 | 已知匹配 | 待核实风险 | 下一步 |
| --- | --- | --- | --- | --- | --- |
| 1 | 青凪ソフトウェア／2027卒 Backend Engineer | NEEDS_VERIFICATION | Java、Spring Boot、东京偏好 | 卒年、签证、薪资、截止日期 | 查官方募集要项 |
| 2 | 星環データ／2027卒 Platform Engineer | NEEDS_VERIFICATION | Docker、MySQL、后端方向 | 外国籍応募、日语要求、工作地点 | 查官方採用 FAQ |
| 3 | 北斗クラウド／2027卒 Application Engineer | NEEDS_VERIFICATION | Java 项目经历 | 配属、固定残业、选考流程 | 查官方职位页 |

**用户（虚构）**：第一家公司详细看看。

**Agent**：已创建 `companies/aonagi-software/` 和 `applications/aonagi-backend-2027.json`。由于这是演示资料，岗位事实全部保留为 `UNKNOWN`，申请状态为 `RESEARCHING`；没有生成、提交或声称存在 ES。

## 产生的可审计文件

- `demo/synthetic-workspace/`：只有虚构内容的工作区快照；模拟真实 `.jobhunt/` 的数据结构。
- `demo/transcript.md`：更简洁的逐轮记录。
- `demo/preview.html`：适合本地打开或 GitHub Pages 预览的效果页，明确标注虚构。

## 如何复现

在仓库根目录运行：

```powershell
python .\demo\run_demo_tests.py
```

它会校验演示 JSON、申请状态、个人事实门禁、字符计数和文本隐私扫描。测试只读取 `demo/synthetic-workspace/`，不会接触项目 `.jobhunt/`。

预期输出：`PASS: 9 checks`。
