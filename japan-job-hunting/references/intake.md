# 画像与补充
先合并当前对话、已存 Candidate Profile、本次新增条件；新增明确修正覆盖当前值并保存旧版本。没有明确“补充／不补充”时默认补充；不补充优先，不因信息缺失停止搜索。

每轮通常 2–4 个关键问题，够用即开始，不发大表单。先查本地画像→公司档案→对话→可公开搜索的信息，最后问用户。未知最低工资不作为硬筛选；未提供签证条件标 UNKNOWN。拒绝补充不代表零要求。

按需记录以下字段，不要求填满：identity（姓名、假名、出生日期、联系方式）；education（学校、专业、学历、入学与毕业年月、毕业年度、卒業見込み）；new_grad_eligibility；location；visa_support；languages（JLPT 与实际沟通分别记录、英语）；skills；projects；internships；employment；research；competitions；clubs；certifications；github；portfolio；media；achievements；career_goals。

preferences 保存目标职位、行业、工作内容、技术方向、地区及备选、转勤、remote/hybrid、最低工资与币种及期间、年收、固定残業接受度、加班上限、奖金、住房补贴、公司规模、日企外企、自社开发／SIer、稳定性、成长、WLB、外国人招聘经验及其他要求。
每项条件有 kind=HARD_CONSTRAINT 或 PREFERENCE、value、用户依据 fact_id、priority/weight。用户没有表达“必须”不得擅自升级硬条件。优先级可以自然语言提取，但有歧义时暂作偏好并说明。

STAR 素材分 situation/task/action/result/quantitative_evidence/difficulty/decision/learning/skills_demonstrated/values_demonstrated/applicable_es_questions/applicable_interview_questions；每个可用于正式文书的断言链接个人 fact_id。
