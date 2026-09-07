# 本地脚本
要求 Python 3.10+。基础脚本只使用标准库；PDF 文字/表单扫描可选 pypdf，没有它会返回 PDF_TOOL_REQUIRED，不谎报内容检查。生成文档依赖按 resume.md 使用环境已有专业工具。
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
char_count 超限返回2；validate 不通过返回1。不要忽略退出码。workspace put 校验通用信封/个人事实/申请状态并保存旧版本，不负责语义合并。validate 检查数据结构与已声明事实引用；全部材料断言、公司来源真实性与视觉排版仍由 Agent 核查。
模板扫描结果中的 ERROR 需检查损坏文件，LEGACY_CONVERSION_REQUIRED 需保真转换；文件扫描不是渲染 QA。
