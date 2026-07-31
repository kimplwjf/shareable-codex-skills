# WeChat Article Adapter Profile Template

Copy to a private workspace location such as `.wechat-article/profile.md`, complete it locally, and keep the completed file out of Git.

```markdown
# My WeChat Article Adapter

- Account display name:
- Private credential configuration path (do not include values):
- Adapter executable path (absolute path; no shell command string):
- Adapter invocation contract: `list`, `preview --article <path> --style <style> [--cover <path>]`, `upload-draft --article <path> --style <style> [--cover <path>]`:
- Available styles/themes:
- Default style:
- Cover validation rules:
- Output/preview directory:
- Idempotency or draft-status check:
```

The adapter receives article path, style, and optional cover as separate argv values; it must support a non-uploading preview mode. Never put a shell command, inline argument string, `$VAR`, `$(...)`, backtick, or article-derived value in this profile. Keep credentials in environment variables or a permission-restricted local env file.
