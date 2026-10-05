# Contract D: Processed Lesson Specification & Template

This contract defines the standard specification, frontmatter metadata format, and structure template for processed lessons in the AI Engineer Roadmap project.

## 1. Frontmatter Metadata Specification

Every processed lesson Markdown file (`.md`) must start with a YAML frontmatter block enclosed between `---` delimiters containing the following fields:

| Field | Type | Required | Description |
| :--- | :--- | :--- | :--- |
| `id` | String | Yes | Unique identifier of the lesson from roadmap.sh (e.g., `jpSel6gPj1d0EhH73Knm7`) |
| `title` | String | Yes | Translated and normalized lesson title in Vietnamese |
| `original_title` | String | Yes | Original English title of the lesson |
| `slug` | String | Yes | URL-friendly slug identifier (e.g., `mcp`) |
| `module_id` | String | Yes | Unique identifier of the parent module |
| `module_title` | String | Yes | Title of the parent module |
| `module` | String | No | Module identifier/slug alias (supported for compatibility) |
| `order` | Integer | No | Display order within the module |
| `status` | String | No | Status of processing (e.g., `completed`, `pending`) |
| `language` | String | Yes | Language code (default: `vi`) |
| `source_status` | String | Yes | Status of source extraction (`completed`) |

### Example Frontmatter:
```yaml
---
id: jpSel6gPj1d0EhH73Knm7
slug: mcp
title: "Giao thức Ngữ cảnh Mô hình (MCP)"
original_title: "MCP"
module_id: v99C5Bml2a6148LCJ9gy9
module_title: "Hugging Face"
module: "hugging-face"
order: 1
status: "completed"
language: vi
source_status: completed
---
```

---

## 2. Six-Section Content Template

Following the frontmatter, the markdown body must be structured according to the standard 6-section template:

### 1. Title
- **Format**: Level 1 Markdown Heading (`# [Translated Title]`)
- **Purpose**: Main title heading of the lesson.

### 2. Overview
- **Format**: Level 2 Heading (`## Tổng quan` / `## Overview`)
- **Purpose**: High-level introduction explaining what the lesson covers and its relevance to AI Engineering.

### 3. Core Concepts
- **Format**: Level 2 Heading (`## Các khái niệm chính` / `## Core Concepts`)
- **Purpose**: Detailed explanation of technical terms, principles, architecture, or terminology (e.g., using domain glossary terms like *Mô hình Ngôn ngữ Lớn (LLM)*, *Biểu diễn nhúng (Embeddings)*).

### 4. Code Example
- **Format**: Level 2 Heading (`## Ví dụ mã nguồn` / `## Code Example`)
- **Purpose**: Practical code snippets, API calls, or implementation examples enclosed in code blocks (e.g., Python, JavaScript/TypeScript, cURL). Note: Code block contents remain untouched by translation scripts to preserve syntax correctness.

### 5. Practice / Checkpoint
- **Format**: Level 2 Heading (`## Thực hành / Kiểm tra` / `## Practice/Checkpoint`)
- **Purpose**: Actionable exercises, self-assessment questions, or verification steps for the learner.

### 6. References
- **Format**: Level 2 Heading (`## Tài liệu tham khảo` / `## References`)
- **Purpose**: External links, official documentation, GitHub repositories, and video tutorials formatted using roadmap annotation conventions (`[@official@...]`, `[@article@...]`, `[@video@...]`).

---

## 3. Compliance and Verification
- **Processor Compliance**: `RoadmapProcessor` generates frontmatter and translated markdown adhering to this specification.
- **Frontend Compliance**: `generate_roadmap_json.py` parses this frontmatter and body into `roadmap-data.json`, which is fully readable by `LessonView.jsx` and `ModuleDetail.jsx`.
