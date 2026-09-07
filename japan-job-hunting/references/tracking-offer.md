# Pipeline、时间线与 Offer
application.status 使用 RESEARCHING / INTERESTED / ENTRY / ES_PREPARING / ES_SUBMITTED / DOCUMENT_SCREENING / WEB_TEST / FIRST_INTERVIEW / SECOND_INTERVIEW / FINAL_INTERVIEW / OFFER / REJECTED / WITHDRAWN。
可按实际流程跳步或回退，但保存依据；准备完成不等于已提交，不能自行把 ES_PREPARING 改成 ES_SUBMITTED。提交/面试/结果以用户确认或可靠凭据更新。

“有哪些公司在投”读取全部 applications 与公司映射，给公司、职位、卒年、状态、最近更新、下一步、deadline、风险；空工作区明确暂无记录，不捏造申请。运行 workspace.py overview 可提取保存的总览。
“接下来做什么”按 deadline 排序，逾期、即将到期与未知日期分别显示。保存 Entry、ES、Web Test、説明会、面试、Offer 回复期限等事件，时区默认为 Asia/Tokyo 但保留源时区。只保存日期并不产生提醒；用户明确要求提醒时才调用环境可用自动化工具，设置完成后确认，不宣称后台持续监视。

Offer 逐项对比基本工资、月薪、固定残業金额/小时、奖金、预计年收、地点/住房、远程、福利/休日、内容/技术/成长、行业/兴趣、稳定性、签证/外国籍环境。区分书面保证与浮动奖金、估算与税前税后；已包含在月薪的固定残業不得再加一次。年收估算=保证月薪×支付月数+确认保证奖金+已确认固定补助，浮动部分单列；说明假设。签证、税和劳动法规需查当时官方资料，不能保证个案。

权重按用户，如技术30/薪资20/兴趣20/地点15/WLB15；每维0–5带依据，未知维度不按零分，显示覆盖率和未知风险。硬条件不满足与待确认单列，不能用加权分掩盖。调整权重可直接重算本地已存数据；给建议与取舍，由用户决定，不代为接受/拒绝。
