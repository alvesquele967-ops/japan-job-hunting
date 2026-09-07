# 本地脚本
要求 Python 3.10+。首次运行执行 `python -m pip install -r <skill>/requirements.txt`。记录校验依赖 jsonschema；PDF 文字/表单扫描使用 pypdf，没有它会返回 PDF_TOOL_REQUIRED，不谎报内容检查。生成文档依赖按 resume.md 使用环境已有专业工具。
在任意工作目录用技能脚本绝对路径运行，<skill> 为实际安装根，<root> 为用户项目/.jobhunt：

```text
python <skill>/scripts/workspace.py init --root <root>
python <skill>/scripts/workspace.py put --root <root> --path companies/example/company.json --input <prepared-record.json>
python <skill>/scripts/workspace.py overview --root <root>
python <skill>/scripts/char_count.py --file <answer.txt> --limit 400
python <skill>/scripts/char_count.py --file <answer.txt> --limit 400 --mode utf16 --exclude-newlines
python <skill>/scripts/template_scan.py --directory <skill>/templates/resume
python <skill>/scripts/validate.py --root <root> --claims <document.claims.json>
```
char_count 超限返回2；validate 不通过返回1。不要忽略退出码。workspace put 按 record.schema.json 校验结构与字段类型，检查记录种类与规范路径一致，并保存旧版本，不负责语义合并。validate 检查数据结构与已声明事实引用；全部材料断言、公司来源真实性与视觉排版仍由 Agent 核查。
模板扫描结果中的 ERROR 需检查损坏文件，LEGACY_CONVERSION_REQUIRED 需保真转换；文件扫描不是渲染 QA。

validate 递归检查工作区 JSON；history/cache 不属于当前记录，documents 中的非记录字段映射和 QA JSON 不按记录校验。误放在其他路径的记录会报错。公司与岗位中提供的 facts/sources 按 Schema 检查；来源真实性仍需人工核实。
