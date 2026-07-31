# Account Profile Template

Copy this file into a private workspace location such as `.wechat-article/profile.md`. Do not commit the completed copy or place it in the installed skill directory.

```markdown
# My WeChat Account Profile

- Account name:
- Audience and region:
- Content lanes:
- Editorial voice:
- Topics or claims to avoid:
- Preferred article forms:
- Default length range:
- Image and watermark policy:
- Required fact-check sources:
- Optional local style-lint executable (absolute path; no shell command string):
- Optional human-editing workflow:
- Draft upload adapter/profile path (no credentials):
```

Store AppID, Secret, Cookie, token, phone number, subscriber data, and private asset paths in the account owner's protected local configuration, never in this profile or Git. Treat any executable path as trusted configuration: confirm it before the first run, pass article values as separate argv arguments, and never use shell interpolation or command substitution.
