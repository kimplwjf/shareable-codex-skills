# PPTX Toolchain and Dependency Matrix

## Installation boundary

`pptx-production-suite` is a workflow router, not a skill bundle. Installing it does not install any row in this table. Each dependency has its own upstream, license, version, and update cycle; install it separately from a trusted source. The suite must check for a dependency before selecting a route and must stop if a required dependency is missing.

## Required by route

| Capability | Required when | Notes |
| --- | --- | --- |
| PPTX authoring/export engine | Producing or changing an editable PPTX | `ppt-master` is a common route. It must be installed separately; an equivalent may be used only with user approval. |
| Independent delivery review | Finalizing a deck | Install a separate review capability. Review source authority, package outputs, images, artifacts, and acceptance criteria. |
| Native PowerPoint playback | Validating transitions/object animation | Preferred proof for native behavior. |

## Optional adapters

| Capability | Use only when | Not a default dependency |
| --- | --- | --- |
| Image generation/editing | User approves AI imagery | Retain prompt/provenance and inspect generated text/artifacts. |
| Browser preview/comments | A preview or annotation workflow exists | Reuse an existing service; do not launch one speculatively. |
| HTML slide tooling | HTML is an input or visual reference | Never convert screenshots into final editable slides. |
| LibreOffice rendering | Extra static geometry check is useful | Does not prove PowerPoint animation behavior. |
| Figma/Notion | The project specifically authorizes it | Do not assume an integration is installed. |

## Minimum preparation template

```markdown
PPTX preparation checklist

- Task type:
- Content authority:
- Chosen authoring route:
- Required tools and availability:
- Conditional tools and trigger:
- Existing materials:
- Missing materials:
- Next confirmation:
- Final deliverable and validation:
```
