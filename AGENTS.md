# Project Agent Guidelines

## Codebase Navigation — MANDATORY

You MUST use codebase-index MCP tools FIRST when exploring or navigating the codebase. This is not optional.

- ALWAYS start with: get_project_summary, find_symbol, get_function_source, get_class_source, get_structure_summary, get_dependencies, get_dependents, get_change_impact, get_call_chain, search_codebase
- Only fall back to Read/Glob/Grep when codebase-index tools genuinely don't have what you need.
- If you catch yourself reaching for Glob/Grep/Read to find or understand code, STOP and use codebase-index instead.

## Codebase Indexing

- When the user requests to "index the codebase", "scan the codebase", "build the index", or similar, you MUST call codebase-index.index_project.
- Do NOT ask questions. Do NOT suggest manual indexing. Just call the tool.
- If the index already exists, you may ask the user if they want to re-index or skip, but only after calling codebase-index.get_project_summary to check the current state.
- If the user says "update", "refresh", or "sync", call codebase-index.index_project.
- If the user says "clear", "reset", or "delete index", call codebase-index.clear_index.
- If the user says "status", "what's indexed", or "show index", call codebase-index.get_project_summary.
- If the user says "search", "find", or "look for", use codebase-index.search_codebase first. Only use Glob/Grep/Read if codebase-index returns no results and you're sure the code exists.
- If the user says "dependencies", "dependents", or "call graph", use codebase-index.get_dependencies, codebase-index.get_dependents, or codebase-index.get_call_chain. Do NOT try to infer this from file names or directory structure.
- If the user says "diff", "changes", or "compare", use codebase-index.get_change_impact. Do NOT try to infer this from file names or directory structure.
- If you say "structure", "outline", or "hierarchy", use codebase-index.get_structure_summary. Do NOT try to infer this from file names or directory structure.

# MCP Servers Configuration
This project utilizes several MCP servers to extend agent capabilities:

## Filesystem MCP
Provides restricted access to the host filesystem.
- **Allowed Roots**: `c:\Users\Bartosz\Desktop\BBTP`, `c:\Users\Bartosz\Desktop\Nous`
- **Usage**: Use for cross-project file operations within allowed paths.

## Context7 MCP
Retrieves live documentation and code examples.
- **Usage**: Use for library/API research. Always resolve library ID first with `resolve-library-id`, then call `query-docs`.
- **When to use**: When you need up-to-date docs for an external library (e.g. Firebase, React, Node.js).

## Sequential Thinking MCP
Enables structured, step-by-step reasoning for complex tasks.
- **Usage**: Use `sequential_thinking` for architectural planning, multi-step debugging, and complex refactoring decisions.
- **When to use**: Before making non-trivial design decisions or when a problem requires more than 2 reasoning steps.

## Memory MCP
Persistent graph-based knowledge storage across sessions.
- **Usage**: Store entities/relationships with `create_entities` / `create_relations`. Retrieve with `search_nodes` or `read_graph`.
- **When to use**: Store key architectural decisions, recurring patterns, or user preferences. Retrieve at conversation start to restore context.

<!-- gitnexus:start -->
# GitNexus — Code Intelligence

This project is indexed by GitNexus as **BBTP** (1994 symbols, 2321 relationships, 15 execution flows). Use the GitNexus MCP tools to understand code, assess impact, and navigate safely.

> If any GitNexus tool warns the index is stale, run `npx gitnexus analyze` in terminal first.

## Always Do

- **MUST run impact analysis before editing any symbol.** Before modifying a function, class, or method, run `gitnexus_impact({target: "symbolName", direction: "upstream"})` and report the blast radius (direct callers, affected processes, risk level) to the user.
- **MUST run `gitnexus_detect_changes()` before committing** to verify your changes only affect expected symbols and execution flows.
- **MUST warn the user** if impact analysis returns HIGH or CRITICAL risk before proceeding with edits.
- When exploring unfamiliar code, use `gitnexus_query({query: "concept"})` to find execution flows instead of grepping. It returns process-grouped results ranked by relevance.
- When you need full context on a specific symbol — callers, callees, which execution flows it participates in — use `gitnexus_context({name: "symbolName"})`.

## Never Do

- NEVER edit a function, class, or method without first running `gitnexus_impact` on it.
- NEVER ignore HIGH or CRITICAL risk warnings from impact analysis.
- NEVER rename symbols with find-and-replace — use `gitnexus_rename` which understands the call graph.
- NEVER commit changes without running `gitnexus_detect_changes()` to check affected scope.

## Resources

| Resource | Use for |
|----------|---------|
| `gitnexus://repo/BBTP/context` | Codebase overview, check index freshness |
| `gitnexus://repo/BBTP/clusters` | All functional areas |
| `gitnexus://repo/BBTP/processes` | All execution flows |
| `gitnexus://repo/BBTP/process/{name}` | Step-by-step execution trace |

## CLI

| Task | Read this skill file |
|------|---------------------|
| Understand architecture / "How does X work?" | `.claude/skills/gitnexus/gitnexus-exploring/SKILL.md` |
| Blast radius / "What breaks if I change X?" | `.claude/skills/gitnexus/gitnexus-impact-analysis/SKILL.md` |
| Trace bugs / "Why is X failing?" | `.claude/skills/gitnexus/gitnexus-debugging/SKILL.md` |
| Rename / extract / split / refactor | `.claude/skills/gitnexus/gitnexus-refactoring/SKILL.md` |
| Tools, resources, schema reference | `.claude/skills/gitnexus/gitnexus-guide/SKILL.md` |
| Index, status, clean, wiki CLI commands | `.claude/skills/gitnexus/gitnexus-cli/SKILL.md` |

<!-- gitnexus:end -->
