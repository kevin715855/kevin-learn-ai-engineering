# Hệ thống Multi-Agent Phi Tập Trung với Bối Cảnh Chia Sẻ (DeLM)

## 1. Mục tiêu học tập
Sau khi đọc bài học này, người học sẽ có thể:
- Giải thích tại sao các thiết kế multi-agent truyền thống thường gây ra “bubble” (thời gian chờ đợi hoặc lặp lại công việc) khi chạy các tác vụ dài hạn.
- Mô tả khái niệm chính của **Decentralized Language Models (DeLM)**: bối cảnh chung (shared context) và hàng đợi tác vụ (task queue) thay thế cho đại lý trung tâm.
- Phân tích cách các đại lý trong DeLM hoạt động bất đồng bộ: nhận tác vụ, công bố kết quả ngay khi có, và dựa vào hoặc sửa đổi tiến trình của các đồng nghiệp.
- Đánh giá lợi ích thực nghiệm của DeLM so với các baseline như Codex, Claude Code, AOrchestra dựa trên các bộ dữ liệu Terminal‑Bench 4.0, DeepSWE v1.1, SWE‑bench Verified và ProgramBench.
- Áp dụng ý tưởng bối cảnh chung và hàng đợi tác vụ vào thiết kế hệ thống multi-agent của riêng mình (trong phạm vi giả định hoặc mô phỏng đơn giản).

## 2. Tổng quan
Các hệ thống multi-agent (MAS) thường được sử dụng để mở rộng khả năng của mô hình ngôn ngữ lớn (LLM) trên các tác vụ cần thời gian thực hiện lâu (long‑horizon tasks) bằng cách chạy nhiều agent song song. Tuy nhiên, trong nhiều thiết kế hiện tại, Song song này bị hao tốn do xuất hiện các “bubble”:
- **Agent độc lập** không chia sẻ gì → mỗi agent phải tìm lại những gì đã được đồng nghiệp khám phá.
- **Agent giao tiếp peer‑to‑peer** thường phải chờ các vòng đồng bộ (synchronous rounds) trước khi có thể tiến дальше.
- **Orchestration tập trung** khiến agent chính bị blocked khi chờ kết quả từ các agent phụ, enquanto tiến độ chỉ được chuyển dần.

Bài báo **“Decentralized Multi-Agent Systems with Shared Context”**提出了一种名为 **DeLM (Decentralized Language Models)** 的框架，通过去掉中心代理并引入 **共享上下文 (shared context)** 与 **任务队列 (task queue)**，使得每个代理都能异步地领取任务、立即发布发现、并在全局可见的状态基础上进行后续工作或修正。实验表明，在多个基准上，DeLM 同时提升了准确率（最高上升 17.5 分）和执行速度（最高快达 2.49 倍），并在需要从头重构程序的 ProgramBench 上使通过率提升最高达 19.9 分。

## 3. Kiến thức cốt lõi

### 3.1 Vấn đề của MAS truyền thống
| Loại MAS | Nguyên nhân tạo bubble | Hậu quả |
|----------|------------------------|---------|
| Độc lập (Independent) | Không có chia sẻ kiến thức | Mỗi agent phải “phát hiện lại” (rediscover) kết quả của người khác → công việc lặp lại |
| Giao tiếp peer‑to‑peer (peer‑communicating) | Yêu cầu các vòng đồng bộ | Agent phải chờ đợi đến hết round trước khi tiếp_thức → thời gian chờ đợi |
| Orchestration tập trung | Agent chính blocker khi chờ sub‑agents | Tiến độ của toàn hệ thống phụ thuộc vào agent chậm nhất → bottleneck |

### 3.2 Khái niệm core của DeLM
1. **Shared Context (Bối cảnh chung)**  
   - Một kho lưu trữ dữ liệu có cấu trúc (ví dụ: bảng khóa‑giá trị, log eventi) mà tất cả các agent đều có thể đọc và ghi.  
   - Mỗi khi một agent hoàn thành một tiểu‑công việc, nó ghi **findings** (phát hiện,partial solution, lemma, patch…) vào shared context.  
   - Các agent khác có thể sofort xem những gì đã được công bố, từ đó tránh lặp lại công việc và có thể xây dựng lên kết quả đó.

2. **Task Queue (Hàng đợi tác vụ)**  
   - Danh sách các micro‑task cần thực hiện, được khởi tạo từ mục tiêu tổng thể (ví dụ: “sửa lỗi hàm X”, “viết unit test cho module Y”).  
   - Các agent **độc lập** (không có central scheduler) **đ revendication** (claim) một task từ queue khi chúng sẵn sàng.  
   - Việc claim thường là атомис: một task chỉ được giao cho một agent duy nhất,防止两个 agent 同时做同一件事。

3. **Asynchronous Operation & Visibility**  
   - Không có vòng đồng bộ chung; mỗi agent làm việc ở tốc độ của mình.  
   - Sau khi hoàn tác vụ, agent ngay lập tức:  
     a) Đánh dấu task là “done” trong queue.  
     b) Đẩy kết quả (findings) vào shared context.  
   - Trạng thái của mỗi agent (đang làm task nào, đã hoàn thành gì, kết quả gần nhất) được publish lên shared context, nên mọi agent đều có **global view** về tiến độ.

4. **Feedback & Correction Loop**  
   - Vì findings là công khai, một agent có thể nhận ra rằng kết quả của agent khác không chính xác hoặc thiếu sót → nó có thể ghi **sửa đổi (correction)** hoặc **ghi chú** vào same context.  
   - Cơ chế này tạo ra một môi trường自我修正 (self‑correcting) mà không cần can thiệp từ một jednost trusted.

### 3.3 So sánh với các baseline
| Baseline | Cách thức hoạt động | Nhược điểm chủ yếu (theo bài báo) |
|----------|--------------------|-----------------------------------|
| Codex / Claude Code (native subagents) | Một agent chính điều phối các sub‑agents qua lời gọi đồng bộ hoặc luồng dữ liệu tuyến tính | Agent chính thường block; sub‑agents thường chờ lệnh hoặc phải làm lại công việc |
| AOrchestra | Orchestrator tập trung quản lý việc分配任务 và汇总结果 | Giống orchestrator tập trung → bottleneck và 대기시간 |
| **DeLM** | Shared context + task queue + asynchronous claiming | Loại bỏ trung gian đồng bộ; tối ưu hoá parallelism; giảm bubble |

## 4. Ví dụ minh họa (giả định)

> **Lưu ý:** Đoạn code dưới đây chỉ là mô tả概念性 (conceptual) để minh họa luồng работы trong DeLM; nó không phải là triển khai thực tế từ paper.

```python
# ------------------- Shared Context (giả sử dùng dict) -------------------
shared_context = {
    "findings": [],   # список открытий от агентов
    "task_status": {} # {task_id: "pending"/"in_progress"/"done"}
}

# ------------------- Task Queue (giả sử dùng queue.Queue) ---------------
import queue, threading, time, uuid

task_queue = queue.Queue()
# Thêm một số micro‑task mẫu
for desc in ["sửa lỗi hàm parse_input", "viết test cho module auth",
             "tái cấu trúc lớp DataLoader", "đánh giá coverage"]:
    task_queue.put({"id": str(uuid.uuid4()), "desc": desc, "status": "pending"})

# ------------------- Agent function ------------------------------------
def agent(agent_id):
    while not task_queue.empty():
        try:
            # prétends to claim atomically
            task = task_queue.get_nowait()
        except queue.Empty:
            break

        # đánh dấu task đang được thực hiện
        shared_context["task_status"][task["id"]] = "in_progress"
        print(f"[Agent {agent_id}] Đang làm: {task['desc']}")

        # ------ Giả lập công việc (tìm lỗi, viết code, etc.) ------
        # Ở đây chúng ta chỉ sinh ra một “finding” giả
        finding = {
            "task_id": task["id"],
            "agent": agent_id,
            "result": f"Patch cho {task['desc']} - completed at {time.time()}"
        }

        # Đăng kết quả lên shared context
        shared_context["findings"].append(finding)
        shared_context["task_status"][task["id"]] = "done"
        print(f"[Agent {agent_id}] Hoàn thành: {task['desc']}")
        # task được coi là xong, không remettre vào queue

# ------------------- Khởi chạy nhiều agent -------------------------------
threads = []
for i in range(4):  # 4 agents song song
    t = threading.Thread(target=agent, args=(i,))
    t.start()
    threads.append(t)

for t in threads:
    t.join()

# ------------------- Kiểm tra kết quả -----------------------------------
print("\n=== Shared Context Findings ===")
for f in shared_context["findings"]:
    print(f"- Agent {f['agent']}: {f['result']}")

print("\n=== Task Status ===")
for tid, status in shared_context["task_status"].items():
    print(f"Task {tid[:8]}: {status}")
```

**Giải thích מה происходит trong ví dụ:**
1. **Task Queue** chứa các micro‑task cần làm. Mỗi agent tự lấy một task khi queue không rỗng (mô phỏng hành động *claim* nguyên tử).
2. KhiAgent bắt đầu task, nó ghi trạng thái `in_progress` vào **shared context** để các agent khác biết task đang được xử lý.
3. Sau khi hoàn thành, agent tạo một **finding** (patch, test, v.v.) và lưu vào `shared_context["findings"]`. Đồng thời, cập nhật trạng thái task thành `"done"`.
4. Các agent khác, khi späteren lường qua queue, có thể đọc `shared_context["findings"]` để tránh lặp lại công việc hoặc dựa trên kết quả đã có để cải tiến.
5. Không có bất kỳ điểm đồng bộ trung tâm nào; toàn hệ thống tiến theo tốc độ từng agent, giảm thiểu thời gian chờ đợi (bubbles).

### Kết quả thực nghiệm (trích từ paper)
- Trên **Terminal‑Bench 4.0**, **DeepSWE v1.1** và **SWE‑bench Verified**, DeLM đạt **accuracy** cao hơn **17.5 điểm** so với baseline mạnh nhất (thường là Claude Code + subagents) và chạy **2.49×** nhanh hơn so với harness gốc mà nó xây dựng trên.
- Trên **ProgramBench** (task yêu cầu viết lại chương trình từ đầu), DeLM giúp agent đạt được **test pass rate** cao hơn **19.9 điểm** so với Claude Code trong cùng ngân sách thời gian 120 phút.
- Những cải thiện này xuất hiện đồng đều ở mọi cài đặt (số agent khác nhau, mức độ khó task khác nhau), chứng minh rằng việc thay thế trung tâm bằng **bối cảnh chung + hàng đợi tác vụ** thực sự thu được lợi ích từ việc song song mà không tạo ra bubbles.

## 5. Tổng kết
- Các hệ thống multi-agent truyền thống thường lãng phí tính song song do sự chờ đợi, lặp lại công việc hoặc bottleneck ở trung tâm điều phối.
- **DeLM** giải quyết vấn đề này bằng cách **loại bỏ trung tâm**, thay vào đó sử dụng một **shared context** để tất cả các agent có thể đọc/ghi kiến thức và một **task queue** để các agent tự ý nhận việc làm.
- Mỗi agent hoạt động **bất đồng bộ**: claim task → thực hiện → công bố kếtרך ngay lập tức → cập nhật trạng thái công việc.
- Kết quả là giảm thiểu “bubbles”, tăng cả **accuracy** và **speed** trên nhiều benchmark dài hạn (Terminal‑Bench, DeepSWE, SWE‑bench, ProgramBench).
- Ý tưởng **bối cảnh chung + hàng đợi tác vụ** có thể được ứng dụng rộng rãi trong thiết kế các hệ thống agent współpracie mà không cần một zentral orchestrator phức tạp, đặc biệt phù hợp với các场景 requiring long‑horizon reasoning, code generation, hoặc bug fixing.