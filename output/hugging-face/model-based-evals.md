---
id: LJ6_U5lOdc0uRngutj7Ro
slug: model-based-evals
title: "Model-Based Evals"
original_title: "Model-Based Evals"
module_id: v99C5Bml2a6148LCJ9gy9
module_title: "Hugging Face"
language: vi
source_status: completed
---

# Model-Based Evals

Model-based evals use a separate AI model to automatically score or assess the outputs of your LLM application. Instead of writing manual rules or relying on human reviewers, you delegate the judgment to another model, a technique commonly known as LLM-as-a-Judge. You write a prompt describing the evaluation criteria, and the judge model rates the response. This approach handles subjective, open-ended quality dimensions that rules cannot capture, while scaling far more cheaply than human review, though it requires careful prompt design to avoid bias and inconsistency in the judges themselves.

Visit the following resources to learn more:

- [@article@A pragmatic guide to LLM evals for devs](https://newsletter.pragmaticengineer.com/p/evals)
- [@article@LLM-as-a-judge: a complete guide to using LLMs for evaluations](https://www.evidentlyai.com/llm-guide/llm-as-a-judge)
- [@video@LLM as a Judge: Scaling AI Evaluation Strategies](https://www.youtube.com/watch?v=trfUBIDeI1Y)