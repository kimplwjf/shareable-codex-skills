# SMS Pre-send Review Rules

## Modes

- **Template**: variables may remain only with defined syntax, source field, missing-value behavior, and a rendered example.
- **Final message**: placeholders, internal notes, temporary links, and unresolved choices block sending.
- **Image input**: transcribe character by character and mark unreadable portions as `[无法确认：位置]`.

## Verdicts

1. **可发送** — language, facts, audience, safety, and mechanics pass with a reliable source.
2. **模板可入库，发送前需联调** — wording is sound but dynamic fields still require mapping and rendering checks.
3. **待事实核验** — wording is usable but critical facts lack a current authoritative source.
4. **修改后再审** — correctable wording, formatting, audience, or instruction issue exists.
5. **禁止发送** — unresolved variables, conflicting facts, wrong audience, broken link, serious misleading claim, or safety harm risk exists.

## Required checks

- Sender identity, recipient segment, and action instruction agree.
- Dates, time-relative words, venue, status, deadline, contact method, and link match the current official execution source.
- Parentheses/quotes close correctly; Chinese punctuation, spacing, units, and terminology are consistent.
- Health, emergency, cancellation, weather, marketing, and refund messages use verified instructions and necessary authorization.
- SMS length and segment count are checked, but cost and carrier behavior remain subject to the sending provider.

## Response shape

```text
结论：<五级结论之一>

关键问题：
| 级别 | 原文位置 | 问题 | 修改/核验建议 |

事实核验：
- 已确认：...
- 待确认：...

建议定稿：
<只修正已确认的语言问题；未知事实写为 [待确认：字段]>

发送前最后检查：
- 变量渲染：
- 受众抽样：
- 链接/号码：
- 平台预览与分段：
```
