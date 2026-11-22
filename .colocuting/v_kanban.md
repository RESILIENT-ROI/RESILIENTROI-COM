---
version: 0.5
# status markup, copy verbatim into the status column:
#   <b class="dbj_red">tbd</b>
#   <b class="dbj_yellow">doing</b>
#   <b class="dbj_green">done</b>
statuses:
  - tbd
  - doing
  - done
---

<style>
b.dbj_red, b.dbj_yellow, b.dbj_green { color:#000; padding:1px 6px; border-radius:3px; white-space:nowrap; }
b.dbj_red { background:#f4a6a6; } b.dbj_yellow { background:#f7e27a; } b.dbj_green { background:#a8dca8; }
</style>


| UID_TIMESTAMP | status | comments |
|---|---|---|
| 007-2026-NOV-22 | <b class="dbj_green">done</b> | Checked raw HTML of https://resilientroi.com/ directly (curl, not WebFetch's markdown conversion): no front matter, no template syntax, nothing leaked. Only `<meta name=generator content="Hugo 0.157.0">`, which is normal. No leak, no fix needed |
| 006-2026-NOV-22 | <b class="dbj_green">done</b> | "organization(s)" → "organisation(s)" in [hugo.toml](../hugo.toml) (Enablement and Onboarding cards); no other US spellings found in site copy |
| 005-2026-NOV-22 | <b class="dbj_green">done</b> | Reworded in [hugo.toml](../hugo.toml), DBJ chose to keep the nautical voice: "from boarding to following the operating model" → "from boarding to sailing the operating model"; "at the presence of the AI storm" → "manage the risks the AI storm brings" |
| 004-2026-NOV-22 | <b class="dbj_green">done</b> | Comma removed in [hugo.toml](../hugo.toml): "Every mature organisation reaches the point…" |
| 003-2026-NOV-22 | <b class="dbj_green">done</b> | Fixed in [hugo.toml](../hugo.toml): "An organisation's Key Performance Indicator…" |
| 002-2026-NOV-22 | <b class="dbj_red">tbd</b> | DBJ ruling: leave as-is for now, no team/client/case-study content to add yet. Revisit once real material exists |
| 001-2026-NOV-22 | <b class="dbj_green">done</b> | DBJ ruling: use Luton everywhere. Fixed both copyright strings in [hugo.toml](../hugo.toml) (site-wide `copyright` param and footer `terms.copyright`) to "Luton, UK" |

---
<br/>
<br/>
<br/>
<br/>
DBJ_VERTICAL_KANBAN | &copy; 2026 by dbj@dbj.org | MIT License
