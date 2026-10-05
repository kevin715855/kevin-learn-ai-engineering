---
id: wel7a_gpXqpuDAdmF_4Rp
language: vi
module: how-llms-work
module_id: zdeuA4GbdBl2DwKgiOA4G
module_title: How LLMs Work
order: 3
original_title: Context Security
slug: context-security
source_status: completed
status: completed
title: Context Security
---
# Context Security

Context security covers the risks that come from feeding external or untrusted content into an AI system. A malicious document, email, or web page can contain hidden instructions designed to manipulate the model, a technique known as prompt injection. Poor access controls can also let a model surface data to a user who should not see it, or let sensitive information leak through tool calls and logs. Building context pipelines securely means validating sources, applying permission checks before data reaches the model, and treating retrieved content as data rather than as trusted instructions.

Visit the following resources to learn more:

- [@article@Context Engineering Is Security Engineering. RSA 2026 Made the Case.](https://zenity.io/blog/events/context-engineering-security-engineering)
- [@article@When Data Becomes Instructions: Các tác nhân AI (AI Agents) Need a Chain of Custody for Context](https://blog.checkpoint.com/ai-security/ai-agent-context-chain-of-custody/)