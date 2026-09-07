# 安装与规范
本包使用 SKILL.md 的 name/description frontmatter，agents/openai.yaml 提供 Codex UI 元数据，详细任务按 references 渐进加载。标准核对日期：2026-09-07。
- https://learn.chatgpt.com/docs/build-skills
- https://agentskills.io/specification

个人安装：将仓库中的整个 `japan-job-hunting/` 文件夹复制到 `~/.agents/skills/japan-job-hunting/`。`~` 表示当前用户主目录，不是作者的本机路径。不要重复安装两个同名技能。
自动发现或用 `$japan-job-hunting` 调用。新安装若尚未显示，开启新任务或重启应用后检查技能列表；静态验证不代表已在本轮动态加载。
私人数据在运行时用户项目的 `.jobhunt/`，不随 Skill 升级移动或打包。更换机器分别迁移技能和私人 workspace，公开分发前移除私人资料和无分发授权第三方模板。
