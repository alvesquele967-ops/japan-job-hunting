# 演示测试结果

测试时间：2026-09-07

数据范围：`demo/synthetic-workspace/` 中的虚构资料

| 检查 | 结果 | 验证内容 |
| --- | --- | --- |
| 示例记录结构 | PASS | 5 个 JSON 记录符合 workspace 数据约定 |
| 个人事实状态 | PASS | 演示资料全部是 `USER_CONFIRMED` |
| 投递状态 | PASS | 仅为 `RESEARCHING`，没有伪造“已投递” |
| 未知招聘条件 | PASS | 全部标为 `NEEDS_VERIFICATION` |
| 日文字数统计 | PASS | `志望動機` 的 code point 计数为 4 |
| 隐私扫描 | PASS | 未发现本机路径或密钥形态文本 |
| Skill 结构 | PASS | `quick_validate.py` 通过 |

复现：

```text
python demo/run_demo_tests.py
```

预期输出：

```text
PASS: 9 checks
```

真实使用时，招聘资格、截止日期和薪资应以当前年度的官方来源为准。
