# 本地数据契约
使用 UTF-8 JSON，schema_version=1；无需数据库或额外 YAML 依赖。通用信封见 schemas/record.schema.json。所有记录有 id、kind、updated_at、data。动态业务字段在 data 中，以下键为各类型约定，不把 UNKNOWN 写为虚假的 0/false。

.jobhunt/
- candidate/profile.json：长期个人字段；值使用 fact_ids 引用 facts.json，避免多份事实各自变化。
- candidate/facts.json：data.facts 数组，每项 id、field、value、status、evidence、confirmed_at；status 为四种个人事实状态。
- candidate/preferences.json：data.constraints 数组、priorities、weights。
- candidate/stories.json：data.stories 数组、STAR 与 fact_ids。
- companies/<slug>/company.json：公司研究及 sources；jobs/<year-role>.json 存岗位；es/、interviews/、offers/、documents/ 保存各阶段记录。
- applications/<id>.json：独立公司×岗位×年度申请，避免跨年覆盖。
- documents/：输出文件与同名 claims.json 事实清单。
- history/：修改前原记录及变更；cache/：公开来源及查询结果。
- discoveries/<timestamp>.json：当次固定 rank→company_id/job_id 映射和排序依据。

公司/岗位 data.facts 每项包括 field、value、source_ids、recruitment_year、year_status、verification_status。sources 每项 id、title、url、source_type、official、publication_date、last_updated、recruitment_year、retrieved_at、confidence。未知日期写 UNKNOWN。confidence 应说明强弱依据，非伪精确概率。

application data: company_id/job_id/recruitment_year/status/deadlines/next_action/documents/pending/last_update。
ES data: questions[{id,text,max_chars,count_rule,required,instructions,source_ids,year_status,deadline}]，版本保留 draft/revision/final 与 used_fact_ids。
interview data: stage/date/questions/answers/followups/feedback/result；Offer data: terms/source_ids/verified_at/response_deadline/risks。

每个公司 last_verified_at，截止日期使用带 +09:00 的 ISO 时间或 UNKNOWN，日期未给具体时刻时保留原文，不默认午夜。历史信息保留原年份；没有自动迁移未知 schema 版本，先另存备份后显式迁移。

使用 workspace.py put 从外部 JSON 写入规范位置并自动备份；已有数据先读取再合并。脚本拒绝路径穿越、写入安装目录与无效信封。文件级原子替换不等于多进程事务，同一 workspace 避免同时写同一记录。

正式材料建立 claims.json：{"claims":[{"text":"文中具体断言","fact_id":"f1","value":"对应事实原值"}]}。运行 validate.py 的事实门禁；它只能检查引用和精确值，不能证明所有自然语言断言都已列出，仍须人工语义检查全文。
