# Ngữ cảnh layer (Context Layer) – nền tảng cho AI agent hiểu biết nội bộ doanh nghiệp  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ có thể:  

- Giải thích tại sao một “demo” đơn giản (chunk‑embed‑retrieve) không đủ khi triển khai ở quy mô sản xuất.  
- Mô tả vai trò và thành phần chính của một **context layer** (ngữ cảnh layer) theo mô tả của bài viết gốc.  
- Nhận ra các thách thức distributed‑systems trong việc **continuous mapping**, **indexing**, **retrieval**, **learning**, và **acting**.  
- Áp dụng các nguyên tắc thiết kế (identity déterministic, rebuildable projections, evaluation harness) để xây dựng hoặc đánh giá một giải pháp ngữ cảnh cho LLM trong môi trường multi‑tenant.  

## 2. Tổng quan  

Khi một công ty muốn LLM “biết tudo” mà nhân viên biết, cần một hệ thống không chỉ lưu trữ tài liệu mà phải **liên tục đồng bộ** các nguồn dữ liệu (warehouse, wiki, Slack, …), chuẩn hoá chúng thành **context items** có kiểu dữ liệu, identity rõ ràng, và có thể truy xuất nhanh theo ngân sách token.  

Bài viết gốc mô tả hệ thống này như một **context layer** (hay còn gọi “company brain”) gồm:  

- **Continuous mapping** – vòng lặp vô hạn reconcile giữa nguồn thực tế và kho lưu trữ.  
- **Multi‑way indexing** – Postgres làm source of truth,plus keyword, vector và knowledge‑graph indexes.  
- **Retrieval orchestration** – composición động của nhiều chiến lược dựa trên scope (skill) và ngân sách token.  
- **Learning loop** – curated knowledge và usage traces được đưa lại vào bộ sı̂ng như tie‑breaker.  
- **Action execution** – agent có thể viết SQL, gọi API, … với credential riêng và checkpoint‑resume.  
- **LLM gateway** – tập trung routing, fallback, timeout và attribution để quản lý chi phí và độ tin cậy.  
- **Trust infrastructure** – đo lường chất lượng retrieval, bảo mật qua claim‑check, và monitoringพิเศษ.  

Các nguyên tắc nêu ở cuối bài viết (rebuildable projection, deterministic identity, evaluate early) được xem như “đường导” để tránh các lỗi thường thấy như ghost table, cross‑tenant leak, silent retrieval degradation, hoặc bill shock.  

## 3. Kiến thức cốt lõi  

### 3.1 Continuous mapping  

- **Không phải batch job** – là một vòng lặp *reconciliation* chạy vô t elkaar.  
- **Datamap (ontology)** – mô tả nguồn dưới dạng hệ thống phân cấp kiểu (connection → database → schema → table → column, …). Mỗi cấp có kiểu contextitem đi kèm.  
- **Identity** của một item được sinh từ `(tenant, type, path)`. Nhờ này, quá trình tái thử (retry) và crash‑recovery trở thành **idempotent**.  
- **Coverage query** – mỗi loại item xác định tần số làm mới riêng; cần một orchestrator bền (durable workflow) để loại bỏ trùng lặp, kiểm soát fan‑out và chịu lỗi.  
- **Xóa (deletion)** – có 6 kênh có thể khiến một item biến mất; mỗi loại collection (bounded vs unbounded) đòi hỏi semantic xóa khác nhau. Bỏ qua bất kỳ kênh nào sẽ khiến brain “tin tưởng” vào một vật đã bị xóa.  
- **Mine behavior** – log truy vấn thực tế cho biết哪些表真的 đang được sử dụng; những truy vấn hợp lệ đượcGolden‑query làm tiêu chuẩn để xếp hạng.  
- **Identity resolution** – trước khi khai thác nội dung có quyền限制, phải giải thuật ID người dùng từ nguồn sang principal nội bộ; nếu không có thể leak hoặc ẩn蔽 dữ liệu.  
- **Connection health state machine** – mỗi kết nối có máquina trạng thái được feeding bởi probes và phân loại lỗi; orchestrator dựa vào đó để决定 retry hoặc báo警.  

### 3.2 Indexing  

- **Relational ground truth** – mỗi tenant có một schema Postgres riêng; mọi ghi đầu tiên được commit ở đây, ACL được áp dụng cuối cùng; mọi chỉ số khác rebuild từ đây.  
- **Keyword index** (BM25) – cần cho việc tìm kiếm lexical chính xác như `dim_customers_v3`.  
- **Vector index** –至少 две коллекции: một cho mô tả tự nhiên (NL) và một cho nội dung dạng code (SQL đã được validate); mỗi tập sử dụng mô hình embeddings khác nhau, được xác định bằng measurement.  
- **Knowledge graph** – biểu hiện containment, joins, lineage dashboard→table; các câu hỏi typu “What breaks if I drop this table?” được trả lời bằng traversal, không phải similarity search.  
- **Embedding pipelines** – là ETL: trước khi embed, cần enrich (ví dụ: sinh mô tả LLM cho cột `f_stat_cd`). Mỗi pipeline phải có giai đoạn dọn dẹp rõ ràng và run‑book rebuild.  
- **Multi‑tenancy** – cách cô lập **physical**: schema, index, collection, graph riêng cho mỗi tenant; tránh sử dụng WHERE clause để cô lập vì một quên lọc sẽ导致数据泄漏, sai tên chỉ số sẽ导致查询全部失败. ACL phải được truyền vào mọi projection dưới dạng filter; chỉ mục tìm kiếm chỉ là pre‑filter permissive, kiểm tra cuối cùng phải đến từ relational store.  

### 3.3 Retrieval là vấn đề orchestration  

- **Scope (skill)** – người dùng định nghĩa một “bundle” gồm một đoạn map và hướng dẫn cho một mục đích (ví dụ: “finance analyst”). Scope được biên dịch thành một bộ lọc filter được dùng lại ở mọi đường truy xuất và kiểm tra lại ở saída để đảm bảo rằng các tài sản đã xóa trả về **nothing** chứ không phải **everything**.  
- **Retrieval graph** – một DAG động các chiến lược (keyword search, vector search, hierarchy gate, repair strategy, …). Mỗi chiến lược khai báo predicate (kiedy chạy) và đóng góp ứng viên khi predicate đúng.  
- **Token‑budget aware** – trên mỗi tầng, đếm số ứng viên: handful → fetch whole; hundreds → LLM relevance filter; thousands → vector search + reranker. Token được phân cấp (full metadata → summary → name only).  
- **Metrics** – cần phân biệt “right item retrieved?” vs “did it survive into the 15k tokens the model read?”.  
- **Logging** – thực thi graph được ghi dưới dạng diagram mỗi lần chạy, chuyển câu hỏi “Why didn’t it know about X?” thành một trace 5‑phút thay vì việc khai thác cổ xa.  

### 3.4 Học tập và sửa đổi  

- **Curated knowledge** – người dùng có thể gắn note, file, saved query trực tiếp lên tài sản (table, column, …). Những item này có cùng identity, ACL, lifecycle với dữ liệu được khai thác và **outranks** metadata sinh ra khi xung đột.  
- **Usage traces** – các cuộc hội thoại thực tế được biến thành structured learnings (ví dụ: “khi người dùng hỏi về churn họหมายถึง `customer_events`, không phải `churn_raw`”). Những học tập được curate định kỳ để tránh mâu thuẫn, sau đó cung cấp lại như tie‑breaker (ảnh hưởng, không phải quyền veto).  
- Brain chỉ đọc nguồn → là công cụ tìm kiếm; brain ghi nhớ sửa chữa → trở thành hệ thống **self‑improving**.  

### 3.5 Hành động (Acting)  

- Agent trên đầu thực hiện: viết SQL, gọi API tracker, lấy dashboard. Credentials để **crawl metadata** và để **thực hiện truy vấn người dùng** phải được tách riêng (blast‑radius và rate‑limit khác nhau).  
- Mọi thao tác ghi phải hỗ trợ **interrupt‑and‑approve**: runtime có thể dừng mid‑graph, lưu trạng thái dauer (checkpoint), và tiếp sau khi người dùng trả lời ngày mai.  
- Phản hồi nên xuất hiện ở nơi người dùng đặt câu hỏi (Slack thread, chatbot, …) – do đó cần API/SDK, MCP server để các AI assistant khác cũng tiêu thụ cùng context và cùng permission.  

### 3.6 LLM Gateway  

- Một gateway trung tâm xử lý hàng nghìn cuộc gọi LLM/giờ (mining, enrichment, filtering, chat). Nó cung cấp:  
  1. **Route‑level fallback** – trạng thái共享 cho model×provider×transport×tier, cooldown được áp dụng mức route, không làm ảnh hưởng tới route khỏe mạnh.  
  2. **First‑token timeout** – giới thoi gian chờ token đầu tiên; bounded retries biến một chờ 120 s chết thành failover minh bạch.  
  3. **Mandatory usage attribution** – mỗi gọi mang tenant, user, feature, surface, được ép tại client constructor → không thể có cuộc gọi ẩn danh → chi phí có thể truy vết tới mỗi truy vấn.  

### 3.7 Trust infrastructure  

- **Đo lường chất lượng retrieval** – bộ dữ liệu vàng (golden dataset) gồm các câu hỏi thực tế với ground truth được gán; đo precision/recall deterministic dựa trên مَا mà composer thực sự chọn; recall@token‑budget tại một số checkpoints; dùng LLM judge chỉ cho phần không xác định được bởi determinism; chạy hàng ngày với cảnh báoRegression.  
- **Bảo mật durable state** – orchestrator lưu mọi input/output trong event history; để tránh rò rỉ dữ liệu vào storage của vendor, áp dụng **claim‑check**: offload payload > ngưỡng nhỏ tới storage tự mã hóa, lưu chỉ reference trong history. Cùng nguyên tắc áp dụng cho agent checkpoints và hàng đợi bền.  

### 3.8 Ba nguyên tắc nén  

1. **Mọi thứ dưới relational store là projection có thể rebuild** – khi một chỉ số trở thành “truth không thể rebuild”, bạn đã mất khả năng sửa sai.  
2. **Identity phải determinist và mọi thao tác idempotent** – retry không phải exception mà là bản chất kiến trúc.  
3. **Xây dựng evaluation harness trước khi thêm chiến lược truy xuất thứ ba** – không thể safely refactor những gì không đo lường; chất lượng truy xuất sẽ suy giảm im lặng nếu không có đo lường.  

## 4. Ví dụ minh họa  

### 4.1 Định nghĩa Datamap (trong YAML – minh hoạ)  

```yaml
# warehouse datamap (mô tả nguồn SQL warehouse)
type: warehouse
connection:
  - postgres
database:
  - sales
schema:
  - public
table:
  - dim_customers
column:
  - customer_id
  - f_stat_cd          # sẽ được enrich bằng mô tả LLM trước khi embed
```

### 4.2 Truy vấn scope (skill) – “finance analyst”  

```json
{
  "name": "finance analyst",
  "scope": {
    "include": [
      "warehouse.sales.public.dim_customers",
      "wiki.finance.revenue_definition",
      "slack.#finance-incidents"
    ],
    "exclude": ["archive.*"]
  },
  "instructions": "Trả về schema, ví dụ SQL hợp lệ vànote về bất kỳ vấn đề dữ liệu nổi tiếng."
}
```

Khi người dùng đặt câu hỏi:  
> “Doanh thu Q3 có thay đổi so với Q2 không?”  

- **Scope filter** chỉ cho phép các item trong danh sách `include`.  
- **Retrieval graph** có thể thực hiện:  
  1. **Keyword search** trên `dim_customers_v3` (BM25) để lấy cột `customer_id`.  
  2. **Vector search** trên mô tả NL của cột `f_stat_cd` (embedding model A).  
  3. **Knowledge‑graph traversal** từ dashboard “Revenue Q3” tới bảng `fact_sales`.  
- Mỗi chiến lược trả về ứng viên; orchestrator gộp, áp dụng **token‑budget** (full metadata → summary → name only) và gửi vào LLM.  

### 4.3 Một “golden query” được khai thác từ log  

```sql
-- Golden query: khi người dùng hỏi về churn, họ thực sự cần bảng customer_events
SELECT customer_id, churn_flag
FROM customer_events
WHERE event_date >= DATE_SUB(CURDATE(), INTERVAL 30 DAY);
```

Query này được lưu như một **context item** (identity: `(tenant, golden_query, churn_q3)`) và được ưu tiên so với mô tả schema sinh ra khi cùng một câu hỏi được xử lý.  

## 5. Tổng kết  

- Một **context layer** không chỉ là vector database; đó là hệ thống đồng bộ liên tục, nhiều chiều chỉ mục, orchestration retrieval, học hỏi từ con người và usage, có khả năng thực hiện hành động và được bảo vệ bằng gateway và foundation tin cậy.  
- Các thách thức thực sự (continuous mapping, deletion, multi‑tenancy, token budget, provider failure, privacy) đều có giải pháp được nêu trong bài viết: **datamap dichiarative**, **workflow orchestrator durable**, **physical multi‑tenant isolation**, **token‑aware retrieval composition**, **LLM gateway với fallback và attribution**, **claim‑check cho durable state**.  
- Ba nguyên tắc “rebuildable projection”, **identity determinist + idempotent**, và **evaluation harness early** là nền tảng để tránh các lỗi thầm lặng (ghost table, silent degradation, unexpected cost).  
- Nếu ngữ cảnh layer là sản phẩm chính, việc **xây dựng** là lựa chọn phù hợp; nếu chỉ là tính năng trong sản phẩm lớn hơn, việc **mua** có thể tối ưu hơn.  

Bài học trên cung cấp một bản蓝 print chi tiết để người học có thể đánh giá, triển khai hoặc cải thiện một hệ thống ngữ cảnh cho LLM trong môi trường doanh nghiệp thực tế.