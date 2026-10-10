# Ngữ cảnh (Context Layer) – Hệ thống cung cấp kiến thức doanh nghiệp cho mô hình LLM  

## 1. Mục tiêu học tập  

Sau bài học này, người học sẽ:  

- Hiểu tại sao một **vector database** đơn giản không đủ để xây dựng “não bộ” công ty.  
- Giải thích cách hệ thống Context Layer thực hiện **ánh xạ liên tục** từ các nguồn dữ liệu (warehouse, wiki, Slack…) thành các mục có định dạng chuẩn, đồng thời duy trì tính nhất quán, bảo mật và tính mới.  
- Mô tả các **kiểu chỉ mục** (relational ground truth, keyword index, vector index, knowledge graph) và lý do cần phải có nhiều chỉ mục thay vì chỉ một.  
- Phân biệt **truy xuất** (retrieval) như một bài toánorchestration thay vì “top‑k paste” và biết cách xây dựng **skill** (scoped bundle) để giới hạn không gian tìm kiếm.  
- Nêu cách hệ thống **học hỏi** từ dữ liệu khai thác (mined) và từ sự can thiệp của con người (curated knowledge) và cách **hành động** (execute SQL, gọi API…) sau khi trả lời.  
- Giải thích vai trò của **LLM gateway**, cơ chế **tin cậy** (trust infrastructure) và nguyên tắc thiết kế nền tảng để tránh những lỗi thường gặp trong sản xuất.  

## 2. Tổng quan  

Khi một công ty bắt đầu sử dụng LLM, câu hỏi thường gặp là: *“Liệu mô hình có thể biết mọi thứ mà chúng ta biết không?”*  
Để trả lời, cần một **bộ não bộ công ty (company brain)** – một lớp trung gian liên tục thu thập, chuẩn hóa, lập chỉ mục và cung cấp ngữ cảnh liên quan tới từng câu hỏi của người dùng.  

Một dự án cuối tuần (chunk → embed → retrieve top‑k → chèn vào prompt) thường hoạt động tốt với một số câu hỏi đầu tiên, nhưng nhanh chóng sụp đổ trong sản xuất vì thiếu:

- **Cập nhật liên tục** (đối tượng bị xóa, quyền thay đổi, schema cập nhật).  
- **Nhiều loại chỉ mục** phù hợp với các truy vấn khác nhau (từ khóa, vector, đồ thị kiến thức).  
- **Quản lý quyền, đa thuê tenancy, chi phí** dưới dạng ràng buộc đầu tiên.  
- **Mekanism học习 và phản hồi** từ người dùng.  
- **Khả năng thực hiện hành động** (gọi API, chạy SQL) sau khi lấy được ngữ cảnh.  

Bài học này mô tả chi tiết các thành phần cần thiết để xây dựng lớp ngữ cảnh sản xuất, dựa trên kiến trúc thực tế của hệ thống Context Warehouse (Modus).  

## 3. Kiến thức cốt lõi  

### 3.1 Ánh xạ liên tục (Continuous mapping)  

- **Nhận diện không phải là batch job** – mà là một **vòng lặp khớp (reconciliation loop)** chạy không ngừng: mỗi khi bảng bị xóa, kênh được архивирование, trang wiki được sửa đổi, quyền thu hồi, vòng lặp sẽ phát hiện **thiếu** và **lão hóa** (stale) và kích hoạt việc tải lại.  
- **Ontology thay vì tập kết nối** – mỗi nguồn được mô tả dưới dạng **datamap** (bảng phân cấp kiểu):  
  - Warehouse: `connection → database → schema → table → column`  
  - Wiki: `space → page → block`  
  Khi cấu trúc này được biểu diễn dưới dạng dữ liệu, một **engine khai thác duy nhất** có thể xử lý nhiều khoSQL khác nhau mà không cần kiểm tra tên vendor.  
- Mỗi artifact khai thác trở thành **context item** có danh tính duy nhất: `(tenant, type, path)`. Độc lập này bảo đảm **idempotence** – orchestrator có thể retry, worker có thể crash mà không làm thay đổi trạng thái cuối cùng.  
- **Vòng lặp覆盖 (coverage query)**: so sánh cấu trúc ontologi với dữ liệu đã lưu để xác định gì còn thiếu, gì đã lỗi thời. Mỗi loại item tự khai báo tần suất làm mới riêng; cần **hàng đợi làm mới** riêng để tránh verhinderea nguồn mới được kết nối bị đói vì backlog.  
- **Orchestrator bền vững** (ví dụ: Temporal, Cadence) cần thiết không vì việc lập lịch khó, mà để:  
  - Loại bỏ tr kích hoạt trùng lặp (deduplication).  
  - Giới hạn phàn-out (cập nhật đồng thời quá nhiều nguồn).  
  - Khôi phục sau sự cố (crash‑resilient).  
- **Xóa (deletion)** là phần khó nhất vì một đối tượng có thể biến mất qua ít nhất sáu kênh:  
  1. Xác nhận từ nguồn.  
  2. Manifest của cha bỏ con.  
  3. Bản ghi cursored hết hạn.  
  4. Probe 404 do stale.  
  5. Quét lại không thấy item.  
  6. Ng dùng ngắt kết nối nguồn.  
  - Đối với **bộ raccol有界** (các cột của một bảng) → cần *full‑rescan tombstoning* (đánh dấu xóa và quét lại toàn bộ).  
  - Đối với **luồng không giới hạn** (vé, PR) → cần *manifest‑diff deletion* (xóa từ watermark trở xuống).  
  - Miss một kênh → hệ thống sẽ “tin tưởng” vào một bảng đã bị xóa từ tháng Ba.  
- **Mine behavior, not just structure** – nhật ký truy vấn cho thấy quais bảng thực sự được dùng, các join thường gặp; những truy vấn hợp lệ sau khi kiểm tra trở thành **golden queries** – những mục có giá trị hơn nhiều so với siêu dữ liệu nguyên thuỷ.  
- **Identity resolution** phải xảy **trước** khi khai thác nội dung có phạm vi權限: ID người dùng trong kênh riêng phải được ánh xạ tới principal nội bộ; nếu không, có thể rò rỉ hoặc ẩn thông tin khỏi người có quyền.  
- **Kết nối ngắt** – bản đồ sẽ ngừng cập nhật im lặng nếu token hết hạn hoặc quyền bị thu hẹp. Mỗi kết nối cần **state machine** (cơ thể trạng thái) được cấp bởi probes và phân loại lỗi; orchestrator tham khảo trạng thái này và UI hiển thị sự cố.  

### 3.2 Lập chỉ mục (Indexing)  

Không tồn tại một chỉ mục duy nhất đáp ứng tất cả nhu cầu. Thay vào đó, cần **nguồn thực tế (source of truth)** và một tập **projections** (chỉ mục tái tạo được):  

| Loại chỉ mục | Mô tả | Lý do cần riêng |
|--------------|-------|-----------------|
| **Relational ground truth** | Mỗi item ở schema Postgres riêng cho mỗi tenant. Ghi vào đây trước, kiểm soát truy cập ở cuối, mọi chỉ mục khác dựng lại từ đây. | Đơn vị điều kiện verdad; tất cả chỉ mục là **cache** của nguồn này. |
| **Keyword index (BM25)** | Tìm kiếm từ vựng (`dim_customers_v3`, `dim_customers_v2`). | Vector embedding không thể phân biệt tốt dựa trên từ khóapure. |
| **Vector index** | - Bộ 1: mô tả tự nhiên (description) – dùng mô hình embedding ngôn ngữ tự nhiên.<br>- Bộ 2: nội dung giống code (SQL đã xác thực) – dùng mô hình embedding code. | Tách biệt vì các loại nội dung có phân bố embedding khác nhau; chỉ biết bằng đo lường thực nghiệm. |
| **Knowledge graph** | Quan hệ: containment, join, lineage dashboard → table. Cho phép truy vấn “nếu xóa bảng này thì gì sẽ hỏng?” bằng **đồ thị traversal**. | Tìm kiếm cosine similarity không phù hợp với các truy vấn cấu trúc. |

**Pipeline embedding** là một quy trình ETL: trước khi embedding, cần **enrichment** (ví dụ: tạo mô tả LLM cho cột `f_stat_cd`). Mỗi projection có **watermark‑based sync** và **phases dọn dẹp rõ ràng** để tránh lag gây lỗi.  

**Đa thuê (multi‑tenancy)**  
- Cách ly **physical**: schema, index, collection, graph riêng cho mỗi tenant.  
- Không nên đặt tenant filter chỉ bằng `WHERE` vì một quênลืm sẽ造成 **failed open** (lộ dữ liệu); sai tên chỉ mục sẽ gây **failed closed** (không tìm thấy).  
- Chi phí là máy móc cung cấp, teardown theo thứ tự, và watchdog으로 lô orphan – nhưng đều có thể kiểm toán, khác với việc tin tưởng mỗi query nhớ tenant filter.  
- ACLs phải truyền vào mọi projection như bộ lọc, nhưng chỉ mục tìm kiếm chỉ là **pre‑filter permissive**; kiểm tra cuối cùng trước khi đưa vào prompt phải là **relational store** (source of truth).  

### 3.3 Truy xuất là bài toán Orchestration  

- **“Top‑k paste” không đủ** vì một câu hỏi có thể cần: schema kho, ví dụ SQL đã xác thực, trang wiki định nghĩa “doanh nghiệp”, và cuộc trò chuyện Slack về vấn đề dữ liệu connu – mỗi mục ở cấp độ khác nhau, trong indexes khác nhau.  
- **Retrieval bắt đầu bằng scope**, không phải bằng tìm kiếm toàn bộ não bộ. Người dùng định nghĩa **skill** (ví dụ: “phân tích tài chính”) – một lát cắt của bản đồ kèm theo hướng dẫn cho mục đích. Skill này được biên dịch thành **filter clause** đáng tin cậy, dùng lại ở mọi luồng truy xuất và được kiểm tra lại ở ra để đảm bảo mục tiêu không nằm ngoài phạm vi (out‑of‑scope items sẽ không được trả về vì chúng sẽ không khớp với filter).  
- **Engine truy xuất** là một **đồ thị chiến lược động**:  
  - Mỗi nút khai báo predicat (ví dụ: “chạy khi có cụm từ entity và không có ứng viên warehouse”).  
  - Khi predicat đúng, nút sinh ra ứng viên (candidates).  
  - Các nguồn dữ liệu: entity extraction → keyword / embedding search; hierarchy gates → điều hướng dựa trên số lượng ứng viên; repair strategies → khi chỉ thấy các con_ATTRIBUTE (orphaned children) thì truy xuất cha.  
  - Hình dạng đồ thị phụ thuộc vào từng query → linh hoạt hơn pipeline cố định và tránh rỗi if‑else.  
  - Ghi lại đồ thị đã thực thi dưới dạng diagram mỗi lần chạy biến câu hỏi *“Tại sao nó không biết về X?”* thành một **five‑minute trace** thay vì práce archaeology.  
- **Hai nguyên tắc bên trong**:  
  1. **Khi nào không gọi LLM** – dựa trên ngưỡng số lượng ứng viên: ít (< handful) → lấy toàn bộ; trung bình (hunderte) → dùng LLM làm bộ lọc liên quan; nhiều (nghìn) → trước hết dùng vector search + reranker, vì việc serializing hàng nghìn tên cột vào prompt tốn token và kém hiệu quả.  
  2. **Quản lý ngân sách token** ở từng lớp: giảm chi tiết dần (full metadata → summary → chỉ tên). Hai mức độ失敗 khác nhau:  
     - “Item đúng có được lấy ra không?”  
     - “Item đó có 생존 trong 15k token mà mô hình đọc không?”  
     Mỗi loại cần metrics riêng.  

### 3.4 Não bộ phải được dạy và phải học  

- **Pure mined brain** ngừng phát triển vì kiến thức quý giá nhất thường không được ghi lại ở bất kỳ nơi nào có thể khai thác được.  
- Người dùng cần cách **thêm ghi chú, file, truy vấn đã lưu** dưới dạng **context item** với cùng danh tính, ACL, và vòng đời như các item được khai thác. Ghi chú này được gắn vào tài sản (asset) để khi tài sản đó được truy xuất, ghi chú luôn kèm theo.  
- Khi có xung đột, **tri thức được curạt (curated knowledge)** phải **ưuออก hơn** siêu dữ liệu được sinh ra, vì sự sửa đổi của con người là tín hiệu mà mô hình sinh ra thiếu.  
- **Học từ sử dụng**: khai thác các cuộc trò chuyện thật thành structured learnings (ví dụ: “khi người dùng hỏi về churn họ thực sự muốn `customer_events` chứ không phải `churn_raw`”), curated định kỳ để tránh mâu thuẫn, và feed các learning còn sống trở thành **tie‑breakers** trong việc xếp hạng (ranking). Đây là **ảnh hưởng**, không phải quyền nhất định – để một suy luận sai không thể chiếm đoạt toàn bộ truy xuất.  
- Não bộ chỉ đọc nguồn là một **công cụ tìm kiếm**; não bộ ghi nhớ những lần được sửa chữa sẽ trở thành một **hệ thống học hỏi liên tục**.  

### 3.5 Trả lời nghĩa là Hành động  

- Một câu hỏi xứng đáng nhận **câu trả lời**, không chỉ là danh sách đọc. Do đó, **trên lớp trên cùng (agent)** thực hiện: viết SQL vào kho, gọi API của tracker, lấy dashboard.  
- **Thực thi credentials** phải được tách riêng khỏi credentials khai thác:  
  - Một identidad crawl metadata vào ban đêm.  
  - Một identity khác chạy truy vấn của người dùng lúc 2 pm.  
  Chúng có **bán đường (blast radius)** và **ngân sách giới hạn tốc độ** khác nhau.  
- Mọi thao tác ghi (write) cần **interrupt‑and‑approve**: runtime phải ngừng giữa đồ thị, lưu trạng thái một cách bền vững, và có thể tiếp sau khi người dùng phản hồi ngày mai – điều này khiến **checkpoint infrastructure** trở thành cấu trúc chịu lực.  
- Hệ thống cũng phải **trả lời ở nơi người dùng đang làm việc**: chatbot, API, SDK, MCP server để các AI assistant khác có thể sử dụng cùng một bộ ngữ cảnh và cùng quyền. Khách hàng khó đáp nhất của não bộ lại là một **máy khác**, và mỗi bề mặt là một **chế độ xác thực** nơi ACLs phải vẫn然 được áp dụng.  

### 3.6 Cổng LLM (LLM Gateway)  

Với hàng nghìn cuộc gọi LLM mỗi giờ (mining, enrichment, filtering, chat), việc đặt SDK của provider rải rác trong mã ứng dụng là **nguy cơ và hạch toán kém**.  

**Lợi ích của một gateway**:  

1. **Route‑level fallback** – đơn vị lỗi là `model × provider × transport × tier`. Các trạng thái cooldown được lưu trữ ở trạng thái chung, nên một route bị throttle không làm ảnh hưởng đến route khỏe mạnh cho cùng model.  
2. **First‑token timeout** – một số provider mở stream nhưng không bao giờ trả về token. Với bounded retries, thời gian chờ chết 120 s trở thành một failover trong suốt.  
3. **Mandatory usage attribution** – mỗi cuộc gọi kèm theo `tenant, user, feature, surface`, được bắt đầu tại constructor client để loại bỏ cuộc gọi ẩn danh. Điều này làm cho bất kỳ spikes trong bill trở thành thể hiện ngay từ một truy vấn và gần như không thể bổ sung sau này.  

### 3.7 Cơ sở tin cậy (Trust infrastructure)  

- **Đo lường chất lượng truy xuất** là bắt buộc; người dùng редко gửi ticket nói “context giảm 8% tuần này”.  
- Thiết lập làm việc:  
  - **Bộ dữ liệu vàng (golden dataset)** gồm câu hỏi thực tế có ground truth được gắn nhãn (quái mục bắt buộc cho câu hỏi).  
  - Tính **precision/recall** deterministically dựa trên tập hợp mục mà composer thực sự chọn ra.  
  - Đo **recall@token‑budget** tại nhiều điểm kiểm tra.  
  - Dùng **LLM judge** chỉ cho những khía cạnh không thể quyết định bằng quy tắc (ví dụ: mức độ liên quan ngữ nghĩa).  
  - Chạy **hàng đêm** với **cảnh báo hồi quy**. Mỗi thay đổi stratégie, mô hình embedding, hoặc prompt filter là một **thử nghiệm** chống lại bộ harness này, không phải “cảm nhận”.  
- **APM thông thường không đủ** vì nó chỉ thấy lưu lượng nhưng không thấy prompt.  
- **Rò rỉ tư qua trạng thái bền vững**:  
  - Orchestrator lưu input/output của mọi hoạt động trong lịch sử sự kiện; nếu không áp dụng **claim‑check pattern**, dữ liệu khách hàng sẽ dồn vào storage của nhà cung cấp orchestrator. Giải pháp: déplacer các payload có kích thước trên ngưỡng nhỏ vào kho mã hoá riêng và chỉ lưu trữ tham chiếu.  
  - Áp dụng cùng nguyên tắc cho **agent checkpoints** và bất kỳ hàng đợi bền vững nào.  

### 3.8 Lời khuyên kết luận  

Mỗi thành phần trên ra đời vì thiếu nó đã gây ra một lỗi cụ thể:  

- Bảng ma (ghost tables) do không xóa đúng.  
- Nguy cơ lộ dữ liệu giữa các tenant (cross‑tenant near‑misses).  
- Hồi truy xuất suy giảm lặng lẽ (silent retrieval regressions).  
- Đợn nhà cung cấp LLM khiến chatbot ngừng hoạt động.  
- Hóa đơn API 5‑chữ số không thể truy nguồn.  

**Ba nguyên tắc nén hầu hết bài học**:  

1. **Mọi thứ xuống dòng relational store là một projection có thể tái tạo** – ngay khi một chỉ mục trở thành “truth” không thể tái tạo, bạn đã mất khả năng sửa lỗi.  
2. **Danh tính phải deterministc và mọi thao tác idempotent** – trong kiến trúc này, retry không phải là trường hợp đặc biệt, mà là **nguyên tắc thiết kế**.  
3. **Xây dựng bộ đánh giá (evaluation harness) trước khi triển khai chiến lược truy xuất thứ ba, chứ không phải sau khi đã có ba mươi chiến lược** – nếu không đo lường, bạn không thể tái cấu trúc an toàn, và chất lượng truy xuất sẽ suy giảm lặng lẽ theo mặc định.  

> **Xây dựng vs mua** – Xây dựng nếu lớp ngữ cảnh **là sản phẩm chính** của bạn; mua nếu nó chỉ là **tính năng**. Dự án cuối tuần có thể làm một demo;而一个真正的“公司脑”需要一个平台团队——这之间的差距正是本文的核心。  

---  

*Tomar Mesika là CTO và nhà sáng lập共同創辦人 của Modus. Trước Modus, ông là Head of Architecture tại Cyera, nơi đã xây dựng hệ thống bảo mật dữ liệu doanh nghiệp được sử dụng trên khoảng 10% Fortune 500. At Modus, ông johta công trình Context Warehouse – lớp nền tảng được thiết kế để cung cấp cho các AI agent kiến thức nội bộ chính xác, giúp các團隊 nội bộ trả lời nhanh và đáng tin cậy về kinh doanh của mình.*