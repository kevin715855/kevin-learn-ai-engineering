# Lộ trình Kỹ sư AI (AI Engineer Roadmap) - Tiếng Việt

Tài liệu này tổng hợp, dịch thuật và chuẩn hóa toàn bộ nội dung học tập từ roadmap.sh dành cho Kỹ sư AI sang tiếng Việt một cách có cấu trúc.

- **Tổng số Module**: 18
- **Tổng số Bài học đã xử lý**: 167
- **Số bài học lỗi/thiếu dữ liệu**: 0

## Mục lục Module

### [Introduction](./introduction/README.md)
- Số bài học: 16

  - [AI Engineer là gì?](./introduction/what-is-an-ai-engineer.md)
  - [Kỹ sư AI vs Kỹ sư ML](./introduction/ai-engineer-vs-ml-engineer.md)
  - [Mô hình ngôn ngữ lớn (LLM)](./introduction/large-language-model-llm.md)
  - [Suy luận](./introduction/inference.md)
  - [Huấn luyện](./introduction/training.md)
  - [cơ sở dữ liệu vector](./introduction/vector-dbs.md)
  - [RAGs](./introduction/rags.md)
  - [Trợ lý AI](./introduction/ai-agents.md)
  - [Trí tuệ nhân tạo vs Trí tuệ nhân tạo chung](./introduction/ai-vs-agi.md)
  - [Ảnh hưởng đến Phát triển Sản phẩm](./introduction/impact-on-product-development.md)
  - [Vai trò và Trách nhiệm](./introduction/roles-and-responsiblities.md)
  - [Nhúng](./introduction/embeddings.md)
  - [RAG & Bộ lọc động](./introduction/rag-and-dynamic-filters.md)
  - [Nén bối cảnh](./introduction/context-compaction.md)
  - [Cách ly bối cảnh](./introduction/context-isolation.md)
  - [Cửa sổ bối cảnh](./introduction/context-window.md)

### [How LLMs Work](./how-llms-work/README.md)
- Số bài học: 21

  - [Kỹ thuật Prompt](./how-llms-work/prompt-engineering.md)
  - [ReAct](./how-llms-work/react.md)
  - [Top-K](./how-llms-work/top-k.md)
  - [Top-P](./how-llms-work/top-p.md)
  - [Few-Shot](./how-llms-work/few-shot.md)
  - [Điều chỉnh tinh vi](./how-llms-work/fine-tuning.md)
  - [Kỹ thuật ngữ cảnh](./how-llms-work/context-engineering.md)
  - [Định dạng đầu vào](./how-llms-work/input-format.md)
  - [Nhắc nhở hệ thống](./how-llms-work/system-prompting.md)
  - [bối cảnh](./how-llms-work/context.md)
  - [Vai trò & Hành vi](./how-llms-work/role--behavior.md)
  - [Ràng buộc](./how-llms-work/constraints.md)
  - [Đầu ra có cấu trúc](./how-llms-work/structured-output.md)
  - [Gọi Hàm](./how-llms-work/function-calling.md)
  - [Caching prompt](./how-llms-work/prompt-caching.md)
  - [Phản hồi streaming](./how-llms-work/streaming-responses.md)
  - [Nhiệt độ](./how-llms-work/temperature.md)
  - [Bối cảnh vs Kỹ thuật Prompt](./how-llms-work/context-vs-prompt-eng.md)
  - [Nguồn bối cảnh](./how-llms-work/context-sources.md)
  - [Bảo mật ngữ cảnh](./how-llms-work/context-security.md)
  - [Context Layer là gì?](./how-llms-work/what-is-a-context-layer.md)

### [Type of Models](./type-of-models/README.md)
- Số bài học: 8

  - [Mô hình đã được huấn luyện trước](./type-of-models/pre-trained-models.md)
  - [Thực hiện kiểm tra đối kháng](./type-of-models/conducting-adversarial-testing.md)
  - [Thêm ID người dùng cuối trong các lời nhắc](./type-of-models/adding-end-user-ids-in-prompts.md)
  - [Kỹ thuật thiết kế prompt mạnh mẽ](./type-of-models/robust-prompt-engineering.md)
  - [Biết khách hàng của bạn / Các trường hợp sử dụng](./type-of-models/know-your-customers--usecases.md)
  - [Giới hạn đầu ra và đầu vào](./type-of-models/constraining-outputs-and-inputs.md)
  - [Closed vs Open Source Models](./type-of-models/closed-vs-open-source-models.md)
  - [mô hình tự host](./type-of-models/self-hosted-models.md)

### [Prompt Engineering](./prompt-engineering/README.md)
- Số bài học: 10

  - [Tokens](./prompt-engineering/tokens.md)
  - [Bối cảnh](./prompt-engineering/context.md)
  - [Anthropic Claude](./prompt-engineering/anthropic-claude.md)
  - [Google Gemini](./prompt-engineering/google-gemini.md)
  - [OpenAI (GPT, o-series)](./prompt-engineering/openai-gpt-o-series.md)
  - [Meta Llama](./prompt-engineering/meta-llama.md)
  - [Mistral](./prompt-engineering/mistral.md)
  - [Cohere](./prompt-engineering/cohere.md)
  - [Phạt lặp](./prompt-engineering/repetition-penalties.md)
  - [Tham số lấy mẫu](./prompt-engineering/sampling-parameters.md)

### [Hugging Face](./hugging-face/README.md)
- Số bài học: 10

  - [Chuỗi suy nghĩ](./hugging-face/cot.md)
  - [Zero-Shot](./hugging-face/zero-shot.md)
  - [Hugging Face Hub](./hugging-face/hugging-face-hub.md)
  - [Nhiệm vụ Hugging Face](./hugging-face/hugging-face-tasks.md)
  - [MCP](./hugging-face/mcp.md)
  - [Chia sẻ bối cảnh multi-agent](./hugging-face/multi-agent-context-sharing.md)
  - [Đánh giá ngữ cảnh](./hugging-face/context-evaluation.md)
  - [Xử lý ngữ cảnh dài](./hugging-face/long-context-processing.md)
  - [Trạng thái & Bối cảnh lịch sử](./hugging-face/state--historical-context.md)
  - [Hệ thống bộ nhớ](./hugging-face/memory-systems.md)

### [Context Engineering](./context-engineering/README.md)
- Số bài học: 7

  - [Các cuộc tấn công tiêm Prompt](./context-engineering/prompt-injection-attacks.md)
  - [Sự thiên vị và công bằng](./context-engineering/bias-and-fairness.md)
  - [Vấn đề về bảo mật và quyền riêng tư](./context-engineering/security-and-privacy-concerns.md)
  - [APIs kiểm duyệt nội dung](./context-engineering/content-moderation-apis.md)
  - [DeepSeek](./context-engineering/deepseek.md)
  - [Gemma](./context-engineering/gemma.md)
  - [Qwen](./context-engineering/qwen.md)

### [Ollama](./ollama/README.md)
- Số bài học: 11

  - [Hugging Face Inference SDK](./ollama/hugging-face-inference-sdk.md)
  - [Transformers.js](./ollama/transformersjs.md)
  - [API Phản hồi OpenAI](./ollama/openai-response-api.md)
  - [Google Gemini API](./ollama/google-gemini-api.md)
  - [RAG trường hợp sử dụng](./ollama/rag-usecases.md)
  - [RAG so với Fine-tuning](./ollama/rag-vs-fine-tuning.md)
  - [Bối cảnh các chế độ lỗi](./ollama/context-failure-modes.md)
  - [PostHog](./ollama/posthog.md)
  - [modus](./ollama/modus.md)
  - [Atlan](./ollama/atlan.md)
  - [DataHub](./ollama/datahub.md)

### [Choosing the Right Model ](./choosing-the-right-model-/README.md)
- Số bài học: 5

  - [Tìm kiếm ngữ nghĩa](./choosing-the-right-model-/semantic-search.md)
  - [Hệ thống gợi ý](./choosing-the-right-model-/recommendation-systems.md)
  - [Phát hiện bất thường](./choosing-the-right-model-/anomaly-detection.md)
  - [Phân loại dữ liệu](./choosing-the-right-model-/data-classification.md)
  - [liên kết](./choosing-the-right-model-/cohere.md)

### [Vector Databases](./vector-databases/README.md)
- Số bài học: 5

  - [API Embeddings của Open AI](./vector-databases/open-ai-embeddings-api.md)
  - [Nhúng Gemini](./vector-databases/gemini-embedding.md)
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

  - [Lập chỉ mục các nhúng](./embedding-models/indexing-embeddings.md)
  - [Thực hiện tìm kiếm tương đồng](./embedding-models/performing-similarity-search.md)
  - [Các trường hợp sử dụng AI đa phương thức](./embedding-models/multimodal-ai-usecases.md)

### [What are RAGs?](./what-are-rags/README.md)
- Số bài học: 5

  - [Chunking](./what-are-rags/chunking.md)
  - [Nhúng](./what-are-rags/embedding.md)
  - [Cơ sở dữ liệu vector](./what-are-rags/vector-database.md)
  - [Quá trình truy xuất](./what-are-rags/retrieval-process.md)
  - [sinh](./what-are-rags/generation.md)

### [AI Agents](./ai-agents/README.md)
- Số bài học: 23

  - [Sử dụng SDKs trực tiếp](./ai-agents/using-sdks-directly.md)
  - [Langchain](./ai-agents/langchain.md)
  - [Chỉ mục Llama](./ai-agents/llama-index.md)
  - [Công cụ & Gọi Hàm](./ai-agents/tools--function-calling.md)
  - [Agents Usecases](./ai-agents/agents-usecases.md)
  - [Gợi nhắc ReAct](./ai-agents/react-prompting.md)
  - [Triển khai thủ công](./ai-agents/manual-implementation.md)
  - [OpenAI AgentKit & Agent SDK](./ai-agents/openai-agentkit--agent-sdk.md)
  - [SDK Đại lý Claude](./ai-agents/claude-agent-sdk.md)
  - [đống cùi](./ai-agents/haystack.md)
  - [RAGFlow](./ai-agents/ragflow.md)
  - [MCP Host](./ai-agents/mcp-host.md)
  - [Máy chủ MCP](./ai-agents/mcp-server.md)
  - [Khách hàng MCP](./ai-agents/mcp-client.md)
  - [Lớp dữ liệu](./ai-agents/data-layer.md)
  - [Lớp Vận tải](./ai-agents/transport-layer.md)
  - [Xây dựng một máy chủ MCP](./ai-agents/building-an-mcp-server.md)
  - [Xây dựng một MCP Client](./ai-agents/building-an-mcp-client.md)
  - [Kết nối tới máy chủ địa phương](./ai-agents/connect-to-local-server.md)
  - [Kết nối tới máy chủ từ xa](./ai-agents/connect-to-remote-server.md)
  - [Công cụ Xây dựng Trình Đại lý Vertex AI](./ai-agents/vertex-ai-agent-builder.md)
  - [Google ADK](./ai-agents/google-adk.md)
  - [Nhiều tác nhân](./ai-agents/multi-agents.md)

### [Multimodal AI](./multimodal-ai/README.md)
- Số bài học: 7

  - [Hiểu biết hình ảnh](./multimodal-ai/image-understanding.md)
  - [Tạo hình ảnh](./multimodal-ai/image-generation.md)
  - [Hiểu video](./multimodal-ai/video-understanding.md)
  - [API Thị giác OpenAI](./multimodal-ai/openai-vision-api.md)
  - [API DALL-E](./multimodal-ai/dall-e-api.md)
  - [Whisper API](./multimodal-ai/whisper-api.md)
  - [Mô hình Hugging Face](./multimodal-ai/hugging-face-models.md)

### [Development Tools](./development-tools/README.md)
- Số bài học: 5

  - [Xử lý âm thanh](./development-tools/audio-processing.md)
  - [Chuyển đổi văn bản thành giọng nói](./development-tools/text-to-speech.md)
  - [Giọng nói thành văn bản](./development-tools/speech-to-text.md)
  - [LangChain cho Ứng dụng đa chế độ](./development-tools/langchain-for-multimodal-apps.md)
  - [LlamaIndex cho Ứng dụng đa phương tiện](./development-tools/llamaindex-for-multimodal-apps.md)

### [Regression Testing](./regression-testing/README.md)
- Số bài học: 12

  - [Claude Code](./regression-testing/claude-code.md)
  - [Song Tử](./regression-testing/gemini.md)
  - [Codex](./regression-testing/codex.md)
  - [Devin](./regression-testing/windsurf.md)
  - [con trỏ](./regression-testing/cursor.md)
  - [Replit](./regression-testing/replit.md)
  - [API NanoBanana](./regression-testing/nanobanana-api.md)
  - [Đánh giá dựa trên mô hình](./regression-testing/model-based-evals.md)
  - [Đánh giá của con người](./regression-testing/human-evals.md)
  - [Chỉ số đánh giá](./regression-testing/evaluation-metrics.md)
  - [DeepEval](./regression-testing/deepeval.md)
  - [RAGAS](./regression-testing/ragas.md)

### [LLM Observability](./llm-observability/README.md)
- Số bài học: 3

  - [Theo dõi & ghi log](./llm-observability/tracing--logging.md)
  - [Giám sát chi phí/độ trễ](./llm-observability/costlatency-monitoring.md)
  - [Giám sát sản xuất](./llm-observability/production-monitoring.md)

### [LLM Evaluations](./llm-evaluations/README.md)
- Số bài học: 5

  - [LangSmith](./llm-evaluations/langsmith.md)
  - [Langfuse](./llm-evaluations/langfuse.md)
  - [Helicone](./llm-evaluations/helicone.md)
  - [Arize AI](./llm-evaluations/arize-ai.md)
  - [Deterministic Evals](./llm-evaluations/deterministic-evals.md)
