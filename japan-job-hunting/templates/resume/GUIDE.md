# 模板目录
可继续把空白 DOCX、XLSX、PDF 放在此目录或子目录，下一次扫描自动发现。不要把已填个人简历存回此处。
Rikunabi 下载文件保持原名与原字节，manifest.json 记录 URL、日期、大小和 SHA-256。来源页面提供标准厚生劳动省样式、职历较多、志望动机/自己PR有或无、资格/动机较多、兴趣特长、无照片和兼职简式等类别，A4/B5、Word/Excel/PDF。
选择以实际结构为准：标准/动机PR型可供一般申请评估；职历型偏经验者；兴趣型可用于展示个人特点；无照片型仅在要求允许时使用；兼职型不默认推荐正式新卒。记入例是演示，禁止复用示例个人资料。
这些第三方模板按用户请求下载供其求职使用；版权归来源方，不声称本 Skill 拥有模板版权或提供再分发许可。公开发布技能前应移除第三方模板或取得相应许可。

## GitHub 版本如何补充模板
公开仓库仅包含本说明与 manifest.json 来源清单。清单不是本地文件存在的保证。
从 https://next.rikunabi.com/tenshokuknowhow/rirekisho/template/ 下载所需 Word、Excel 或 PDF，放入当前已安装技能的 templates/resume/。
manifest.json 中 role=blank_template 是空白模板；role=filled_example 是参考示例，不能用于填写。可以按 url 直接下载并用 sha256 核对原始版本；若网站更新文件，以重新检查的版本为准，不忽略哈希变化。
本目录 .gitignore 默认只允许说明、来源清单与忽略配置进入 Git，其余新添模板和文件均留在本地。
