# Lộ trình Kỹ sư AI (AI Engineer Roadmap) - Tiếng Việt

Tài liệu này tổng hợp, dịch thuật và chuẩn hóa toàn bộ nội dung học tập từ roadmap.sh dành cho Kỹ sư AI sang tiếng Việt một cách có cấu trúc.

- **Tổng số Module**: 18
- **Tổng số Bài học đã xử lý**: 167
- **Số bài học lỗi/thiếu dữ liệu**: 167

## Mục lục Module

### [Introduction](./introduction/README.md)
- Số bài học: 16

  - [AI Engineer là gì?](./introduction/what-is-an-ai-engineer.md)
  - [Kỹ sư AI vs Kỹ sư ML](./introduction/ai-engineer-vs-ml-engineer.md)
  - [Mô hình ngôn ngữ lớn (LLM)](./introduction/large-language-model-llm.md)
  - [Suy luận](./introduction/inference.md)
  - [Huấn luyện](./introduction/training.md)
  - [Cơ sở dữ liệu Vector](./introduction/vector-dbs.md)
  - [RAGs](./introduction/rags.md)
  - [Các tác nhân AI](./introduction/ai-agents.md)
  - [AI vs AGI](./introduction/ai-vs-agi.md)
  - [Ảnh hưởng tới Phát triển sản phẩm](./introduction/impact-on-product-development.md)
  - [Vai trò và Trách nhiệm](./introduction/roles-and-responsiblities.md)
  - [Nhúng](./introduction/embeddings.md)
  - [RAG & Bộ lọc động](./introduction/rag-and-dynamic-filters.md)
  - [Nén ngữ cảnh](./introduction/context-compaction.md)
  - [Cách ly ngữ cảnh](./introduction/context-isolation.md)
  - [Cửa sổ ngữ cảnh](./introduction/context-window.md)

### [How LLMs Work](./how-llms-work/README.md)
- Số bài học: 21

  - [kỹ thuật prompt](./how-llms-work/prompt-engineering.md)
  - [ReAct](./how-llms-work/react.md)
  - [Top-K](./how-llms-work/top-k.md)
  - [Top-P](./how-llms-work/top-p.md)
  - [Few-Shot](./how-llms-work/few-shot.md)
  - [điều chỉnh tinh vi](./how-llms-work/fine-tuning.md)
  - [Kỹ thuật ngữ cảnh](./how-llms-work/context-engineering.md)
  - [Định dạng đầu vào](./how-llms-work/input-format.md)
  - [Hướng dẫn hệ thống](./how-llms-work/system-prompting.md)
  - [Bối cảnh](./how-llms-work/context.md)
  - [Vai trò & Hành vi](./how-llms-work/role--behavior.md)
  - [ràng buộc](./how-llms-work/constraints.md)
  - [đầu ra có cấu trúc](./how-llms-work/structured-output.md)
  - [Gọi hàm](./how-llms-work/function-calling.md)
  - [Prompt Caching](./how-llms-work/prompt-caching.md)
  - [Phản hồi streaming](./how-llms-work/streaming-responses.md)
  - [Nhiệt độ](./how-llms-work/temperature.md)
  - [Bối cảnh vs Kỹ thuật Prompt](./how-llms-work/context-vs-prompt-eng.md)
  - [Nguồn ngữ cảnh](./how-llms-work/context-sources.md)
  - [Bảo mật ngữ cảnh](./how-llms-work/context-security.md)
  - [Lớp ngữ cảnh là gì?](./how-llms-work/what-is-a-context-layer.md)

### [Type of Models](./type-of-models/README.md)
- Số bài học: 8

  - [Mô hình đã được huấn luyện trước](./type-of-models/pre-trained-models.md)
  - [Thực hiện kiểm tra đối nghịch](./type-of-models/conducting-adversarial-testing.md)
  - [Thêm ID người dùng cuối trong các prompt](./type-of-models/adding-end-user-ids-in-prompts.md)
  - [Kỹ thuật thiết kế prompt bền vững](./type-of-models/robust-prompt-engineering.md)
  - [Nắm vững Khách hàng / Các trường hợp sử dụng](./type-of-models/know-your-customers--usecases.md)
  - [Giới hạn các đầu ra và đầu vào](./type-of-models/constraining-outputs-and-inputs.md)
  - [Closed vs Open Source Models](./type-of-models/closed-vs-open-source-models.md)
  - [Mô hình tự lưu trữ](./type-of-models/self-hosted-models.md)

### [Prompt Engineering](./prompt-engineering/README.md)
- Số bài học: 10

  - [Tokens](./prompt-engineering/tokens.md)
  - [bối cảnh](./prompt-engineering/context.md)
  - [Claude của Anthropic](./prompt-engineering/anthropic-claude.md)
  - [Google Gemini](./prompt-engineering/google-gemini.md)
  - [OpenAI (GPT, o-series)](./prompt-engineering/openai-gpt-o-series.md)
  - [Meta Llama](./prompt-engineering/meta-llama.md)
  - [Mistral](./prompt-engineering/mistral.md)
  - [liên kết](./prompt-engineering/cohere.md)
  - [Phạt lặp lại](./prompt-engineering/repetition-penalties.md)
  - [Tham số lấy mẫu](./prompt-engineering/sampling-parameters.md)

### [Hugging Face](./hugging-face/README.md)
- Số bài học: 10

  - [CoT](./hugging-face/cot.md)
  - [Zero-Shot](./hugging-face/zero-shot.md)
  - [Hugging Face Hub](./hugging-face/hugging-face-hub.md)
  - [Nhiệm vụ Hugging Face](./hugging-face/hugging-face-tasks.md)
  - [MCP](./hugging-face/mcp.md)
  - [Chia sẻ ngữ cảnh đa tác nhân](./hugging-face/multi-agent-context-sharing.md)
  - [Đánh giá ngữ cảnh](./hugging-face/context-evaluation.md)
  - [Xử lý ngữ cảnh dài](./hugging-face/long-context-processing.md)
  - [Trạng thái & Bối cảnh lịch sử](./hugging-face/state--historical-context.md)
  - [Hệ thống bộ nhớ](./hugging-face/memory-systems.md)

### [Context Engineering](./context-engineering/README.md)
- Số bài học: 7

  - [Prompt Injection Attacks](./context-engineering/prompt-injection-attacks.md)
  - [Sự thiên vị và sự công bằng](./context-engineering/bias-and-fairness.md)
  - [Bảo mật và Quyền riêng tư](./context-engineering/security-and-privacy-concerns.md)
  - [APIs Kiểm duyệt nội dung](./context-engineering/content-moderation-apis.md)
  - [DeepSeek](./context-engineering/deepseek.md)
  - [Gemma](./context-engineering/gemma.md)
  - [Qwen](./context-engineering/qwen.md)

### [Ollama](./ollama/README.md)
- Số bài học: 11

  - [Hugging Face SDK suy luận](./ollama/hugging-face-inference-sdk.md)
  - [Transformers.js](./ollama/transformersjs.md)
  - [API phản hồi OpenAI](./ollama/openai-response-api.md)
  - [Google Gemini API](./ollama/google-gemini-api.md)
  - [RAG Usecases](./ollama/rag-usecases.md)
  - [RAG so sánh với Fine-tuning](./ollama/rag-vs-fine-tuning.md)
  - [Chế độ lỗi của ngữ cảnh](./ollama/context-failure-modes.md)
  - [PostHog](./ollama/posthog.md)
  - [modus](./ollama/modus.md)
  - [Atlan](./ollama/atlan.md)
  - [Hub dữ liệu](./ollama/datahub.md)

### [Choosing the Right Model ](./choosing-the-right-model-/README.md)
- Số bài học: 5

  - [Tìm kiếm ngữ nghĩa](./choosing-the-right-model-/semantic-search.md)
  - [Hệ thống đề xuất](./choosing-the-right-model-/recommendation-systems.md)
  - [Phát hiện bất thường](./choosing-the-right-model-/anomaly-detection.md)
  - [Phân loại dữ liệu](./choosing-the-right-model-/data-classification.md)
  - [Cohere](./choosing-the-right-model-/cohere.md)

### [Vector Databases](./vector-databases/README.md)
- Số bài học: 5

  - [Open AI Embeddings API](./vector-databases/open-ai-embeddings-api.md)
  - [Gemini Nhúng](./vector-databases/gemini-embedding.md)
  - [Jina](./vector-databases/jina.md)
  - [Sentence Transformers](./vector-databases/sentence-transformers.md)
  - [Các mô hình trên Hugging Face](./vector-databases/models-on-hugging-face.md)

### [OpenRouter](./openrouter/README.md)
- Số bài học: 11

  - [Mục đích và chức năng](./openrouter/purpose-and-functionality.md)
  - [Chroma](./openrouter/chroma.md)
  - [Pinecone](./openrouter/pinecone.md)
  - [Weaviate](./openrouter/weaviate.md)
  - [FAISS](./openrouter/faiss.md)
  - [LanceDB](./openrouter/lancedb.md)
  - [Qdrant](./openrouter/qdrant.md)
  - [Supabase](./openrouter/supabase.md)
  - [MongoDB Atlas](./openrouter/mongodb-atlas.md)
  - [API Tin nhắn Claude](./openrouter/claude-messages-api.md)
  - [APIs tương thích với OpenAI](./openrouter/openai-compatible-apis.md)

### [Embedding Models](./embedding-models/README.md)
- Số bài học: 3

  - [Đánh chỉ mục Embeddings](./embedding-models/indexing-embeddings.md)
  - [Performing Similarity Search](./embedding-models/performing-similarity-search.md)
  - [Multimodal AI Usecases](./embedding-models/multimodal-ai-usecases.md)

### [What are RAGs?](./what-are-rags/README.md)
- Số bài học: 5

  - [Chunking](./what-are-rags/chunking.md)
  - [Nhúng](./what-are-rags/embedding.md)
  - [Cơ sở dữ liệu vector](./what-are-rags/vector-database.md)
  - [Quy trình truy xuất](./what-are-rags/retrieval-process.md)
  - [Thế hệ](./what-are-rags/generation.md)

### [AI Agents](./ai-agents/README.md)
- Số bài học: 23

  - [Sử dụng SDKs trực tiếp](./ai-agents/using-sdks-directly.md)
  - [Langchain](./ai-agents/langchain.md)
  - [Chỉ mục Llama](./ai-agents/llama-index.md)
  - [Công cụ & Gọi hàm](./ai-agents/tools--function-calling.md)
  - [Các trường hợp sử dụng của Agents](./ai-agents/agents-usecases.md)
  - [ReAct Prompting](./ai-agents/react-prompting.md)
  - [Triển khai thủ công](./ai-agents/manual-implementation.md)
  - [OpenAI AgentKit & Agent SDK](./ai-agents/openai-agentkit--agent-sdk.md)
  - [Claude Agent SDK](./ai-agents/claude-agent-sdk.md)
  - [Đống cỏ](./ai-agents/haystack.md)
  - [RAGFlow](./ai-agents/ragflow.md)
  - [Máy chủ MCP](./ai-agents/mcp-host.md)
  - [Máy chủ MCP](./ai-agents/mcp-server.md)
  - [Khách hàng MCP](./ai-agents/mcp-client.md)
  - [Lớp dữ liệu](./ai-agents/data-layer.md)
  - [Lớp truyền dẫn](./ai-agents/transport-layer.md)
  - [Xây dựng một MCP Server](./ai-agents/building-an-mcp-server.md)
  - [Xây dựng một MCP Client](./ai-agents/building-an-mcp-client.md)
  - [Kết nối tới Máy chủ cục bộ](./ai-agents/connect-to-local-server.md)
  - [Kết nối với máy chủ từ xa](./ai-agents/connect-to-remote-server.md)
  - [Vertex AI Agent Builder](./ai-agents/vertex-ai-agent-builder.md)
  - [Google ADK](./ai-agents/google-adk.md)
  - [đa tác nhân](./ai-agents/multi-agents.md)

### [Multimodal AI](./multimodal-ai/README.md)
- Số bài học: 7

  - [hiểu biết hình ảnh](./multimodal-ai/image-understanding.md)
  - [Sinh ảnh](./multimodal-ai/image-generation.md)
  - [Hiểu Video](./multimodal-ai/video-understanding.md)
  - [OpenAI Vision API](./multimodal-ai/openai-vision-api.md)
  - [DALL-E API](./multimodal-ai/dall-e-api.md)
  - [Whisper API](./multimodal-ai/whisper-api.md)
  - [Hugging Face Models](./multimodal-ai/hugging-face-models.md)

### [Development Tools](./development-tools/README.md)
- Số bài học: 5

  - [Xử lý âm thanh](./development-tools/audio-processing.md)
  - [Chuyển đổi văn bản thành lời nói](./development-tools/text-to-speech.md)
  - [Chuyển đổi giọng nói thành văn bản](./development-tools/speech-to-text.md)
  - [LangChain cho Ứng dụng đa phương thức](./development-tools/langchain-for-multimodal-apps.md)
  - [LlamaIndex cho Ứng dụng đa modal](./development-tools/llamaindex-for-multimodal-apps.md)

### [Regression Testing](./regression-testing/README.md)
- Số bài học: 12

  - [Mã Claude](./regression-testing/claude-code.md)
  - [Song Tử](./regression-testing/gemini.md)
  - [Codex](./regression-testing/codex.md)
  - [Devin](./regression-testing/windsurf.md)
  - [Con trỏ](./regression-testing/cursor.md)
  - [Replit](./regression-testing/replit.md)
  - [API NanoBanana](./regression-testing/nanobanana-api.md)
  - [Đánh giá dựa trên mô hình](./regression-testing/model-based-evals.md)
  - [Đánh giá của con người](./regression-testing/human-evals.md)
  - [Chỉ số đánh giá](./regression-testing/evaluation-metrics.md)
  - [DeepEval](./regression-testing/deepeval.md)
  - [RAGAS](./regression-testing/ragas.md)

### [LLM Observability](./llm-observability/README.md)
- Số bài học: 3

  - [Theo dõi & ghi nhật ký](./llm-observability/tracing--logging.md)
  - [Cost/latency monitoring](./llm-observability/costlatency-monitoring.md)
  - [Giám sát sản xuất](./llm-observability/production-monitoring.md)

### [LLM Evaluations](./llm-evaluations/README.md)
- Số bài học: 5

  - [LangSmith](./llm-evaluations/langsmith.md)
  - [Langfuse](./llm-evaluations/langfuse.md)
  - [Helicone](./llm-evaluations/helicone.md)
  - [Arize AI](./llm-evaluations/arize-ai.md)
  - [Đánh giá Deterministic](./llm-evaluations/deterministic-evals.md)

## Báo cáo Bài học Lỗi / Thiếu dữ liệu

- **What is an AI Engineer?** (`what-is-an-ai-engineer` - ID: `GN6SnI7RXIeW8JeD-qORW`): Content missing or too short / malformed
- **AI Engineer vs ML Engineer** (`ai-engineer-vs-ml-engineer` - ID: `jSZ1LhPdhlkW-9QJhIvFs`): Content missing or too short / malformed
- **Large Language Model (LLM)** (`large-language-model-llm` - ID: `wf2BSyUekr1S1q6l8kyq6`): Content missing or too short / malformed
- **Inference** (`inference` - ID: `4NtUD9V64gkp8SFudj_ai`): Content missing or too short / malformed
- **Training** (`training` - ID: `xostGgoaYkqMO28iN2gx8`): Content missing or too short / malformed
- **Vector DBs** (`vector-dbs` - ID: `dzPKW_fn82lY1OOVrggk3`): Content missing or too short / malformed
- **RAGs** (`rags` - ID: `IX1BJWGwGmB4L063g0Frf`): Content missing or too short / malformed
- **Prompt Engineering** (`prompt-engineering` - ID: `VjXmSCdzi2ACv-W85Sy9D`): Content missing or too short / malformed
- **AI Agents** (`ai-agents` - ID: `Uffu609uQbIzDl88Ddccv`): Content missing or too short / malformed
- **AI vs AGI** (`ai-vs-agi` - ID: `5QdihE1lLpMc3DFrGy46M`): Content missing or too short / malformed
- **Impact on Product Development** (`impact-on-product-development` - ID: `qJVgKe9uBvXc-YPfvX_Y7`): Content missing or too short / malformed
- **Roles and Responsiblities** (`roles-and-responsiblities` - ID: `K9EiuFgPBFgeRxY4wxAmb`): Content missing or too short / malformed
- **Pre-trained Models** (`pre-trained-models` - ID: `d7fzv_ft12EopsQdmEsel`): Content missing or too short / malformed
- **Tokens** (`tokens` - ID: `2WbVpRLqwi3Oeqk1JPui4`): Content missing or too short / malformed
- **Context** (`context` - ID: `vvpYkmycH0_W030E-L12f`): Content missing or too short / malformed
- **Anthropic Claude** (`anthropic-claude` - ID: `hy6EyKiNxk1x84J63dhez`): Content missing or too short / malformed
- **Google Gemini** (`google-gemini` - ID: `oe8E6ZIQWuYvHVbYJHUc1`): Content missing or too short / malformed
- **OpenAI (GPT, o-series)** (`openai-gpt-o-series` - ID: `3PQVZbcr4neNMRr6CuNzS`): Content missing or too short / malformed
- **Meta Llama** (`meta-llama` - ID: `OkYO-aSPiuVYuLXHswBCn`): Content missing or too short / malformed
- **Mistral** (`mistral` - ID: `n-Ud2dXkqIzK37jlKItN4`): Content missing or too short / malformed
- **Cohere** (`cohere` - ID: `a7qsvoauFe5u953I699ps`): Content missing or too short / malformed
- **ReAct** (`react` - ID: `Waox7xR_yUeSnOtQFzU4c`): Content missing or too short / malformed
- **CoT** (`cot` - ID: `nyBgEHvUhwF-NANMwkRJW`): Content missing or too short / malformed
- **Zero-Shot** (`zero-shot` - ID: `15XOFdVp0IC-kLYPXUJWh`): Content missing or too short / malformed
- **Top-K** (`top-k` - ID: `qzvp6YxWDiGakA2mtspfh`): Content missing or too short / malformed
- **Top-P** (`top-p` - ID: `FjV3oD7G2Ocq5HhUC17iH`): Content missing or too short / malformed
- **Few-Shot** (`few-shot` - ID: `DZPM9zjCbYYWBPLmQImxQ`): Content missing or too short / malformed
- **Prompt Injection Attacks** (`prompt-injection-attacks` - ID: `cUyLT6ctYQ1pgmodCKREq`): Content missing or too short / malformed
- **Bias and Fairness** (`bias-and-fairness` - ID: `lhIU0ulpvDAn1Xc3ooYz_`): Content missing or too short / malformed
- **Security and Privacy Concerns** (`security-and-privacy-concerns` - ID: `sWBT-j2cRuFqRFYtV_5TK`): Content missing or too short / malformed
- **Conducting adversarial testing** (`conducting-adversarial-testing` - ID: `Pt-AJmSJrOxKvolb5_HEv`): Content missing or too short / malformed
- **Content Moderation APIs** (`content-moderation-apis` - ID: `ljZLa3yjQpegiZWwtnn_q`): Content missing or too short / malformed
- **Adding end-user IDs in prompts** (`adding-end-user-ids-in-prompts` - ID: `4Q5x2VCXedAWISBXUIyin`): Content missing or too short / malformed
- **Robust prompt engineering** (`robust-prompt-engineering` - ID: `qmx6OHqx4_0JXVIv8dASp`): Content missing or too short / malformed
- **Know your Customers / Usecases** (`know-your-customers--usecases` - ID: `t1SObMWkDZ1cKqNNlcd9L`): Content missing or too short / malformed
- **Constraining outputs and inputs** (`constraining-outputs-and-inputs` - ID: `ONLDyczNacGVZGojYyJrU`): Content missing or too short / malformed
- **Closed vs Open Source Models** (`closed-vs-open-source-models` - ID: `RBwGsq9DngUsl8PrrCbqx`): Content missing or too short / malformed
- **Hugging Face Hub** (`hugging-face-hub` - ID: `YLOdOvLXa5Fa7_mmuvKEi`): Content missing or too short / malformed
- **Hugging Face Inference SDK** (`hugging-face-inference-sdk` - ID: `3kRTzlLNBnXdTsAEXVu_M`): Content missing or too short / malformed
- **Transformers.js** (`transformersjs` - ID: `bGLrbpxKgENe2xS1eQtdh`): Content missing or too short / malformed
- **OpenAI Response API** (`openai-response-api` - ID: `ro3vY_sp6xMQ-hfzO-rc1`): Content missing or too short / malformed
- **Google Gemini APi** (`google-gemini-api` - ID: `TsG_I7FL-cOCSw8gvZH3r`): Content missing or too short / malformed
- **Semantic Search** (`semantic-search` - ID: `eMfcyBxnMY_l_5-8eg6sD`): Content missing or too short / malformed
- **Recommendation Systems** (`recommendation-systems` - ID: `HQe9GKy3p0kTUPxojIfSF`): Content missing or too short / malformed
- **Anomaly Detection** (`anomaly-detection` - ID: `AglWJ7gb9rTT2rMkstxtk`): Content missing or too short / malformed
- **Data Classification** (`data-classification` - ID: `06Xta-OqSci05nV2QMFdF`): Content missing or too short / malformed
- **Open AI Embeddings API** (`open-ai-embeddings-api` - ID: `l6priWeJhbdUD5tJ7uHyG`): Content missing or too short / malformed
- **Cohere** (`cohere` - ID: `y0qD5Kb4Pf-ymIwW-tvhX`): Content missing or too short / malformed
- **Gemini Embedding** (`gemini-embedding` - ID: `4GArjDYipit4SLqKZAWDf`): Content missing or too short / malformed
- **Jina** (`jina` - ID: `apVYIV4EyejPft25oAvdI`): Content missing or too short / malformed
- **Sentence Transformers** (`sentence-transformers` - ID: `ZV_V6sqOnRodgaw4mzokC`): Content missing or too short / malformed
- **Models on Hugging Face** (`models-on-hugging-face` - ID: `dLEg4IA3F5jgc44Bst9if`): Content missing or too short / malformed
- **Purpose and Functionality** (`purpose-and-functionality` - ID: `WcjX6p-V-Rdd77EL8Ega9`): Content missing or too short / malformed
- **Chroma** (`chroma` - ID: `dSd2C9lNl-ymmCRT9_ZC3`): Content missing or too short / malformed
- **Pinecone** (`pinecone` - ID: `_Cf7S1DCvX7p1_3-tP3C3`): Content missing or too short / malformed
- **Weaviate** (`weaviate` - ID: `VgUnrZGKVjAAO4n_llq5-`): Content missing or too short / malformed
- **FAISS** (`faiss` - ID: `JurLbOO1Z8r6C3yUqRNwf`): Content missing or too short / malformed
- **LanceDB** (`lancedb` - ID: `rjaCNT3Li45kwu2gXckke`): Content missing or too short / malformed
- **Qdrant** (`qdrant` - ID: `DwOAL5mOBgBiw-EQpAzQl`): Content missing or too short / malformed
- **Supabase** (`supabase` - ID: `9kT7EEQsbeD2WDdN9ADx7`): Content missing or too short / malformed
- **MongoDB Atlas** (`mongodb-atlas` - ID: `j6bkm0VUgLkHdMDDJFiMC`): Content missing or too short / malformed
- **Indexing Embeddings** (`indexing-embeddings` - ID: `5TQnO9B4_LTHwqjI7iHB1`): Content missing or too short / malformed
- **Performing Similarity Search** (`performing-similarity-search` - ID: `ZcbRPtgaptqKqWBgRrEBU`): Content missing or too short / malformed
- **RAG Usecases** (`rag-usecases` - ID: `GCn4LGNEtPI0NWYAZCRE-`): Content missing or too short / malformed
- **RAG vs Fine-tuning** (`rag-vs-fine-tuning` - ID: `qlBEXrbV88e_wAGRwO9hW`): Content missing or too short / malformed
- **Chunking** (`chunking` - ID: `mX987wiZF7p3V_gExrPeX`): Content missing or too short / malformed
- **Embedding** (`embedding` - ID: `grTcbzT7jKk_sIUwOTZTD`): Content missing or too short / malformed
- **Vector Database** (`vector-database` - ID: `zZA1FBhf1y4kCoUZ-hM4H`): Content missing or too short / malformed
- **Retrieval Process** (`retrieval-process` - ID: `OCGCzHQM2LQyUWmiqe6E0`): Content missing or too short / malformed
- **Generation** (`generation` - ID: `2jJnS9vRYhaS69d6OxrMh`): Content missing or too short / malformed
- **Using SDKs Directly** (`using-sdks-directly` - ID: `WZVW8FQu6LyspSKm1C_sl`): Content missing or too short / malformed
- **Langchain** (`langchain` - ID: `jM-Jbo0wUilhVY830hetJ`): Content missing or too short / malformed
- **Llama Index** (`llama-index` - ID: `JT4mBXOjvvrUnynA7yrqt`): Content missing or too short / malformed
- **Tools & Function Calling** (`tools--function-calling` - ID: `eOqCBgBTKM8CmY3nsWjre`): Content missing or too short / malformed
- **DeepSeek** (`deepseek` - ID: `UGYYh2W1XnnbgYNY8L8Hb`): Content missing or too short / malformed
- **Agents Usecases** (`agents-usecases` - ID: `778HsQzTuJ_3c9OSn5DmH`): Content missing or too short / malformed
- **ReAct Prompting** (`react-prompting` - ID: `voDKcKvXtyLzeZdx2g3Qn`): Content missing or too short / malformed
- **Manual Implementation** (`manual-implementation` - ID: `6xaRB34_g0HGt-y1dGYXR`): Content missing or too short / malformed
- **OpenAI AgentKit & Agent SDK** (`openai-agentkit--agent-sdk` - ID: `Sm0Ne5Nx72hcZCdAcC0C2`): Content missing or too short / malformed
- **Claude Agent SDK** (`claude-agent-sdk` - ID: `xXLyuUNrKEc32XLQxMjgT`): Content missing or too short / malformed
- **Multimodal AI Usecases** (`multimodal-ai-usecases` - ID: `sGR9qcro68KrzM8qWxcH8`): Content missing or too short / malformed
- **Image Understanding** (`image-understanding` - ID: `fzVq4hGoa2gdbIzoyY1Zp`): Content missing or too short / malformed
- **Image Generation** (`image-generation` - ID: `49BWxYVFpIgZCCqsikH7l`): Content missing or too short / malformed
- **Video Understanding** (`video-understanding` - ID: `TxaZCtTCTUfwCxAJ2pmND`): Content missing or too short / malformed
- **Audio Processing** (`audio-processing` - ID: `mxQYB820447DC6kogyZIL`): Content missing or too short / malformed
- **Text-to-Speech** (`text-to-speech` - ID: `GCERpLz5BcRtWPpv-asUz`): Content missing or too short / malformed
- **Speech-to-Text** (`speech-to-text` - ID: `jQX10XKd_QM5wdQweEkVJ`): Content missing or too short / malformed
- **OpenAI Vision API** (`openai-vision-api` - ID: `CRrqa-dBw1LlOwVbrZhjK`): Content missing or too short / malformed
- **DALL-E API** (`dall-e-api` - ID: `LKFwwjtcawJ4Z12X102Cb`): Content missing or too short / malformed
- **Whisper API** (`whisper-api` - ID: `OTBd6cPUayKaAM-fLWdSt`): Content missing or too short / malformed
- **Hugging Face Models** (`hugging-face-models` - ID: `EIDbwbdolR_qsNKVDla6V`): Content missing or too short / malformed
- **LangChain for Multimodal Apps** (`langchain-for-multimodal-apps` - ID: `j9zD3pHysB1CBhLfLjhpD`): Content missing or too short / malformed
- **LlamaIndex for Multimodal Apps** (`llamaindex-for-multimodal-apps` - ID: `akQTCKuPRRelj2GORqvsh`): Content missing or too short / malformed
- **Haystack** (`haystack` - ID: `ebXXEhNRROjbbof-Gym4p`): Content missing or too short / malformed
- **RAGFlow** (`ragflow` - ID: `d0ontCII8KI8wfP-8Y45R`): Content missing or too short / malformed
- **MCP Host** (`mcp-host` - ID: `MabZ9jOrSj539C5qZrVBd`): Content missing or too short / malformed
- **MCP Server** (`mcp-server` - ID: `8Xkd88EjX3GE_9DWQhr7G`): Content missing or too short / malformed
- **MCP Client** (`mcp-client` - ID: `po0fIZYaFhRbNlza7sB37`): Content missing or too short / malformed
- **Data Layer** (`data-layer` - ID: `Z0920V57_ziDhXbQJMN9O`): Content missing or too short / malformed
- **Transport Layer** (`transport-layer` - ID: `o4gHDZ5p9lyeHuCAPvAKz`): Content missing or too short / malformed
- **Building an MCP Server** (`building-an-mcp-server` - ID: `oLGfKjcqBzJ3vd6Cg-T1B`): Content missing or too short / malformed
- **Building an MCP Client** (`building-an-mcp-client` - ID: `0Rk0rCbmRFJT2GKwUibQS`): Content missing or too short / malformed
- **Connect to Local Server** (`connect-to-local-server` - ID: `H-G93SsEgsA_NGL_v4hPv`): Content missing or too short / malformed
- **Connect to Remote Server** (`connect-to-remote-server` - ID: `2t4uINxmzfx8FUF-_i_2B`): Content missing or too short / malformed
- **Vertex AI Agent Builder** (`vertex-ai-agent-builder` - ID: `AxzTGDCC2Ftp4G66U4Uqr`): Content missing or too short / malformed
- **Google ADK** (`google-adk` - ID: `mbp2NoL-VZ5hZIIblNBXt`): Content missing or too short / malformed
- **Fine-tuning** (`fine-tuning` - ID: `zTvsCNS3ucsZmvy1tHyeI`): Content missing or too short / malformed
- **Context Engineering** (`context-engineering` - ID: `kCiHNaZ9CgnS9uksIQ_SY`): Content missing or too short / malformed
- **Input Format** (`input-format` - ID: `LCHse57rXf3sl8ml1ow0T`): Content missing or too short / malformed
- **System Prompting** (`system-prompting` - ID: `S46Vaq8hYq6Ee1Id_-fSQ`): Content missing or too short / malformed
- **Context** (`context` - ID: `9oUpeEnaMWctQLTobbmY7`): Content missing or too short / malformed
- **Role & Behavior** (`role--behavior` - ID: `N3TzWYxU0jgv1l99Ts58n`): Content missing or too short / malformed
- **Constraints** (`constraints` - ID: `PT3uDiUjiKhO8laOkCmgP`): Content missing or too short / malformed
- **Structured Output** (`structured-output` - ID: `zqhmLzHsmDlrTFVHzhq6-`): Content missing or too short / malformed
- **Function Calling** (`function-calling` - ID: `wFfjHkGLrcCyLyXV4BiFM`): Content missing or too short / malformed
- **Prompt Caching** (`prompt-caching` - ID: `bqqY0gsZkBpcHMZw1hcZ5`): Content missing or too short / malformed
- **Streaming Responses** (`streaming-responses` - ID: `MUDBYjR7uCUZQ-kQxi2K_`): Content missing or too short / malformed
- **Self-Hosted Models** (`self-hosted-models` - ID: `_qqITQ8O0Q0RWUeZsUXnY`): Content missing or too short / malformed
- **Repetition Penalties** (`repetition-penalties` - ID: `0_pa739kMPWHfuSQV-VO7`): Content missing or too short / malformed
- **Gemma** (`gemma` - ID: `MNtaY1_kOJHeoWuM-abb4`): Content missing or too short / malformed
- **Qwen** (`qwen` - ID: `c0RPhpD00VIUgF4HJgN2T`): Content missing or too short / malformed
- **Claude Messages API** (`claude-messages-api` - ID: `nxwMVla0-PNG8nlocKK5v`): Content missing or too short / malformed
- **OpenAI-compatible APIs** (`openai-compatible-apis` - ID: `vnXtUupJUlyU_uCbZBbnk`): Content missing or too short / malformed
- **Multi-agents** (`multi-agents` - ID: `kG1bkF2oY21CJOm9zhdpn`): Content missing or too short / malformed
- **Hugging Face Tasks** (`hugging-face-tasks` - ID: `YKIPOiSj_FNtg0h8uaSMq`): Content missing or too short / malformed
- **Embeddings** (`embeddings` - ID: `XyEp6jnBSpCxMGwALnYfT`): Content missing or too short / malformed
- **Claude Code** (`claude-code` - ID: `wr5ddjutC-fX_ixysTHaT`): Content missing or too short / malformed
- **Gemini** (`gemini` - ID: `hzeEo8COf2l07iu5EdlFo`): Content missing or too short / malformed
- **Codex** (`codex` - ID: `XY2l96sry3WyLzzo3KUeU`): Content missing or too short / malformed
- **Devin** (`windsurf` - ID: `Xsl8mx6J182TxPPtNP471`): Content missing or too short / malformed
- **Cursor** (`cursor` - ID: `MWhoqhNnBaoeCdN_8i15k`): Content missing or too short / malformed
- **Replit** (`replit` - ID: `Ubk4GN0Z4XlDJ3EbRXdxg`): Content missing or too short / malformed
- **NanoBanana API** (`nanobanana-api` - ID: `6y73FLjshnqxV8BTGUeiu`): Content missing or too short / malformed
- **Sampling Parameters** (`sampling-parameters` - ID: `LbB2PeytxRSuU07Bk0KlJ`): Content missing or too short / malformed
- **Temperature** (`temperature` - ID: `_bPTciEA1GT1JwfXim19z`): Content missing or too short / malformed
- ** RAG & Dynamic Filters** (`rag-and-dynamic-filters` - ID: `LnQ2AatMWpExUHcZhDIPd`): Content missing or too short / malformed
- **Context Compaction** (`context-compaction` - ID: `9XCxilAQ7FRet7lHQr1gE`): Content missing or too short / malformed
- **Context Isolation** (`context-isolation` - ID: `9JwWIK0Z2MK8-6EQQJsCO`): Content missing or too short / malformed
- **Tracing & logging** (`tracing--logging` - ID: `cdapQf0Owxdx6olAHTrbq`): Content missing or too short / malformed
- **Cost/latency monitoring** (`costlatency-monitoring` - ID: `CG3XTMPug98s-EP0_rn1Y`): Content missing or too short / malformed
- **Production monitoring** (`production-monitoring` - ID: `3gwVG4XaO83z3Yzdd84Z-`): Content missing or too short / malformed
- **LangSmith** (`langsmith` - ID: `bN_ReFUQgkJmWOAFMLXMg`): Content missing or too short / malformed
- **Langfuse** (`langfuse` - ID: `Xw6-crHimGrVC1u1xujc6`): Content missing or too short / malformed
- **Helicone** (`helicone` - ID: `82LE-qxw1H_FYfVUdgkN9`): Content missing or too short / malformed
- **Arize AI** (`arize-ai` - ID: `jx57heeBnacrlCyQPhlEi`): Content missing or too short / malformed
- **Deterministic Evals** (`deterministic-evals` - ID: `kSDTJK74Tq0KHBfIawJuT`): Content missing or too short / malformed
- **Model-Based Evals** (`model-based-evals` - ID: `LJ6_U5lOdc0uRngutj7Ro`): Content missing or too short / malformed
- **Human Evals** (`human-evals` - ID: `QIx5nT75l2Cn2q75-TxfD`): Content missing or too short / malformed
- **Evaluation Metrics** (`evaluation-metrics` - ID: `Z8MBleL51wJuV9BkS1djI`): Content missing or too short / malformed
- **DeepEval** (`deepeval` - ID: `hyN5v8dg1lHJLpdZZdtJE`): Content missing or too short / malformed
- **RAGAS** (`ragas` - ID: `CZ_-PSDzzSrSon5XdzLen`): Content missing or too short / malformed
- **Context vs Prompt Eng.** (`context-vs-prompt-eng` - ID: `s2YrrjXbvNIyW5WSFj2po`): Content missing or too short / malformed
- **Context Sources** (`context-sources` - ID: `x0G0WD8MUflucdBqf2j5k`): Content missing or too short / malformed
- **Context Window** (`context-window` - ID: `SF07y6d-JcE1-pzXeBOU7`): Content missing or too short / malformed
- **MCP** (`mcp` - ID: `jpSel6gPj1d0EhH73Knm7`): Content missing or too short / malformed
- **Multi-agent Context Sharing** (`multi-agent-context-sharing` - ID: `wQfU09yhZ5sd-UPHkq2n0`): Content missing or too short / malformed
- **Context Evaluation** (`context-evaluation` - ID: `SzW-BtzGsSfGGa5DbSlr4`): Content missing or too short / malformed
- **Context Security** (`context-security` - ID: `wel7a_gpXqpuDAdmF_4Rp`): Content missing or too short / malformed
- **What is a Context Layer?** (`what-is-a-context-layer` - ID: `5b2-GXozMVOqZF1Ga-HE8`): Content missing or too short / malformed
- **Long-Context Processing** (`long-context-processing` - ID: `BfmhnGPe1UdnThdpr7m1i`): Content missing or too short / malformed
- **State & Historical Context** (`state--historical-context` - ID: `unoZLoE2oJbKPOCBYUnMZ`): Content missing or too short / malformed
- **Context Failure Modes** (`context-failure-modes` - ID: `mfiiWDVZEeUGFa6KKUGLB`): Content missing or too short / malformed
- **PostHog** (`posthog` - ID: `31UjRzoh7wQKk6uAZ7aVM`): Content missing or too short / malformed
- **modus** (`modus` - ID: `xTqTaiKLo6EE_4JVFdjEt`): Content missing or too short / malformed
- **Atlan** (`atlan` - ID: `e_Mgd4pxKPdxL5DNxlxQ_`): Content missing or too short / malformed
- **Memory Systems** (`memory-systems` - ID: `4HkJJigCBBO4eOef8qvhz`): Content missing or too short / malformed
- **DataHub** (`datahub` - ID: `sFYcBgG9I0n1iKpwlp_7B`): Content missing or too short / malformed
