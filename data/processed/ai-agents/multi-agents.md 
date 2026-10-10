# Hệ thống đa tác nhân (Multi‑Agent System)

## 1. Mục tiêu học tập

Sau khi học bài này, người học sẽ:

- Nắm được khái niệm tổng quát về hệ thống đa tác nhân (MAS) và vai trò của từng tác nhân (agent) trong đó.  
- Phân biệt hệ thống một tác nhân (single‑agent) và hệ thống đa tác nhân về cách hoạt động và lợi ích.  
- mô tả các kiến trúc chính (tập trung, phi tập trung) và cấu trúc tổ chức phổ biến (hierarchical, holonic, coalition, team).  
- Giải thích một số hành vi coletive thường thấy (flocking, swarming) và cách chúng được áp dụng trong phần mềm và robot.  
- Liệt kê các ứng dụng thực tiễn chính (giao thông, y tế, chuỗi cung ứng, phòng ngự) và ưu điểm cũng như thách thức khi thiết kế MAS.  

## 2. Tổng quan

Hệ thống đa tác nhân (Multi‑Agent System – MAS) là một tập hợp nhiều **AI agent** làm việc cùng nhau để hoàn thành nhiệm vụ thay cho người dùng hoặc một hệ thống khác. Mỗi agent là một thực thể tự quyết, có khả năng lập kế hoạch, gọi công cụ (tool) và học hỏi từ môi trường, nhưng khi hoạt động trong MAS chúng còn phải trao đổi thông tin, điều chỉnh mục tiêu và đóng góp vào thuộc tính toàn cục mong muốn.  

MAS đặc biệt hữu ích khi phải giải quyết các vấn đề lớn, phức tạp đòi hỏi sự phối hợp của hàng trăm, nay ngàn agent (ví dụ: quản lý mạng lưới đường sắt, mô phỏng dịch bệnh, tối ưu chuỗi cung ứng).  

## 3. Kiến thức cốt lõi

### 3.1 AI agent – thành phần cơ bản

- **AI agent**: hệ thống hoặc chương trình có thể tự động thực hiện nhiệm vụ bằng cách thiết kế quy trình làm việc và sử dụng các công cụ có sẵn (dataset bên ngoài, tìm kiếm web, API …).  
- **LLM (Large Language Model)**: nền tảng xử lý ngôn ngữ tự nhiên giúp agent hiểu và tạo ra phản hồi dựa trên đầu vào của người dùng.  
- **Sự khác biệt so với LLM truyền thống**: agent không chỉ sinh văn bản mà còn **lập kế hoạch**, **gọi công cụ** và **cập nhật bộ nhớ** khi thu được thông tin mới, nên có tính général-purpose cao hơn.

### 3.2 Single agent vs Multi‑agent

| Điểm | Single Agent | Multi‑Agent System |
|------|--------------|--------------------|
| Môi trường | Agent tương tác trực tiếp với môi trường, lấy thông qua công cụ (API, database…) nhưng không cần trao đổi với agent khác. | Môi trường chứa nhiều agent; mỗi agent có thể xem agent khác như một phần của Stimuli của mình, nhưng còn phải **mô hình hóa mục tiêu, bộ nhớ và kế hoạch** của đối phương để phối hợp. |
| Truyền thông | Thông thường là một chiều (agent → môi trường). | Có thể **trực tiếp** (gửi tin nhắn) hoặc **gián tiếp** (thay đổi môi trường chung để影響 other agents). |
| Tính tự trị | Cao, agent hoạt động độc lập. | Vẫn tự trị nhưng **phải phối hợp**; sự perdent của một agent có thể ảnh hưởng đến toàn bộ hệ thống nếu kiến trúc không chịu lỗi. |
| Lợi ích | Đơn giản, dễ triển khai. | Tăng cường **chính xác, khả năng thích nghi và mở rộng** nhờ chia sẻ kinh nghiệm và tài nguyên. |

### 3.3 Kiến trúc (Architectures)

1. **Mạng tập trung (Centralized network)**  
   - Một đơn vị trung tâm giữ **knowledge base** toàn cục, kết nối và giám sát tất cả agent.  
   - Ưu điểm: giao tiếp dễ dàng, kiến thức đồng nhất.  
   - Nhược điểm: **single point of failure** – nếu đơn vị trung tâm chết, toàn bộ hệ thống dừng hoạt động.

2. **Mạng phi tập trung (Decentralized network)**  
   - Agent chỉ trao đổi với **láng giềng** của mình; không có knowledge base chung.  
   - Ưu điểm: **độ bền cao** (hỏng một agent không làm sập hệ thống), tính mô-đun.  
   - Nhược điểm: cần cơ chế **điều chỉnh hành vi** để gewährleisten lợi ích chung.

### 3.4 Cấu trúc tổ chức (Structures)

| Cấu trúc | Mô tả | Đặc điểm nổi bật |
|----------|------|------------------|
| **Hierarchical** | Cây-like, các agent có mức độ tự trị khác nhau. Trong cấu trúc đơn giản, một agent có quyền ra quyết định; trong cấu trúc đồng đều, trách nhiệm được chia sẻ. | Dễ quản lý, quy trình rõ ràng. |
| **Holonic** | Agent được gom thành **holarchies**; mỗi *holon* là một thực thể không thể tồnakt thành phần của nó (ví dụ: cơ thể người ↔ cácofficial organ). Trong MAS, một “leader agent” có thể có nhiều sub‑agent, nhưng sub‑agent cũng có thể tham gia vào nhiều holon khác. | Tự organiztion, linh hoạt trong việc chia sẻ sub‑agent giữa các mục tiêu. |
| **Coalition** | Các agent tạm thời hợp lại khi một agent riêng lẻ không đạt được hiệu suất mong muốn. Sau khi mục tiêu đạt, coalition được giải tán. | Cần **re‑group** thường xuyên trong môi trường thay đổi. |
| **Team** | Giống coalition nhưng agent **luôn làm việc cùng nhau**, không hoạt động độc lập; cấu trúc thường bậc hơn và phụ thuộc lẫn nhau mạnh. | Độ ổn định cao, nhưng ít linh hoạt hơn coalition. |

### 3.5 Hành vi coletive (Behaviors)

- **Flocking (đồn căț)** – mô phỏng hành động của Chim, cá, hoặc người đi bộ.  
  - *Separation*: tránh va chạm với agent lân cận.  
  - *Alignment*: tentativa về vận tốc bằng agent lân cận.  
  - *Cohesion*: giữ khoảng cách近 với các agent lân cận.  
  - Ứng dụng: điều khiển hệ thống giao thông đường sắt, điều khiển xe tải tự động.

- **Swarming (đồn ro'** – tương tựBehavior của ong, cá đồng.  
  - Agent tự organização và tập hợp dưới sự điều khiển phi tập trung.  
  - Lợi ích: một toán tử có thể quản lý整个 swarm thay vì phải đào tạo cho từng agent riêng; giảm chi phí tính toán và tăng độ tin cậy.  

### 3.6 Trường hợp sử dụng thực tế

| Ngành | Ứng dụng cụ thể của MAS | Lợi ích chính |
|-------|------------------------|--------------|
| **Giao thông** | Quản lý mạng lưới đường sắt, phân bổ xe tải, điều khiển tàu thuỷ cheg lại cùng cảng. | Điều phối real‑time, tối ưu sử dụng tài nguyên, giảm tắc nghẽn. |
| **Y tế & Công cộng health** | Dự đoán và phòng ngừa bệnh qua phân tích gen; mô phỏng lan truyền dịch bệnh bằng mạng neuraston epidemiologic + ML. | Cung báo sớm, hỗ trợ quyết định chính sách công cộng. |
| **Quản lý chuỗi cung ứng** | Kết nối các thành phần (nơi sản xuất, kho, vận chuyển) bằng agent thương lượng; giải quyết xung đột mục tiêu giữa cácpartner. | Tăng khả năng phản hồi, giảm rủi ro, tối ưu chi phí. |
| **Hệ thống phòng ngự** | Mô phỏng vụ tấn công hải đạo; các agent làm việc theo **team** để phát hiện DDoS, giám sát các phân đoạn mạng. | Phát hiện sớm, phản hồi nhanh, giảm thiểu hĐa của tấn công. |

### 3.7 Ưu điểm của MAS

- **Linh hoạt (Flexibility)** – dễ dàng thêm, bớt hoặc thay đổi agent khi môi trường thay đổi.  
- **Khả năng mở rộng (Scalability)** – hợp tác nhiều agent tạo nên kho tri thức và tài nguyên chung lớn hơn, cho phép giải quyết bài toán phức tạp hơn.  
- **Chuyên môn hoá miền (Domain specialization)** – mỗi agent có thể tập trung vào một lĩnh vực cụ thể thay vì một agent phải “là tutti”.  
- **Hiệu suất cao (Greater performance)** – sự hợp tác cho phép chia sẻ kế hoạch, kiến thức và phản hồi giữa các agent chuyên môn, dẫn tới tổng hợp thông tin tốt hơn và giảm lặp lại việc học.  

### 3.8 Thách thức khi thiết kế MAS

- **Hỏng hóc agent (Agent malfunctions)** – khi các agent được xây dựng từ cùng một **foundation model**, một lỗi chung có thể lan tới toàn bộ hệ thống hoặc làm lộ điểm yếu trước tấn công. Cần có **quản lý dữ liệu** và quy trình kiểm tra kỹ lưỡng.  
- **Phức tạp về điều phối (Coordination complexity)** – phải xây dựng cơ chế để agent **w သ đàm판, negotiate** và đạt được sự đồng thuận về mục tiêu và hành động.  
- **Hành vi không thể đoán trước (Unpredictable behavior)** – trong mạng络 phi tập trung, agent hoạt động độc lập có thể prowadzić tới xung đột hoặc行为 нестабильный; việc phát hiện và xử lý vấn đề trong quy mô lớn trở nên khó khăn.  

## 4. Ví dụ minh họa

### Ví dụ 1: Flocking trong quản lý đường sắt

Giả sử chúng ta có 20 agent, mỗi agent đại diện cho một đoạn đường sắt. Mỗi agent có trách nhiệm điều chỉnh tốc độ của chuyến tàu qua đoạn mình nhằm tránh va chạm và giữ khoảng cách an toàn với tàu trước và sau.

- **Separation**: agent kiểm tra vị trí tàu gần nhất; nếu khoảng cách < d_min, agentIssue lệnh giảm tốc.  
- **Alignment**: agent tính vận tốc trung bình của hai agent lân cận và điều chỉnh tốc độ của mình về phía giá trị trung bình.  
- **Cohesion**: agent cố gắng giữ đoạn tàu mình không xa hơn d_max so với agent lân cận để đảm bảo luồng liikTransport không ngắt quãng.

Kết quả: toàn bộ hệ thống tàu hoạt động như một đàn cattle, tự điều chỉnh tốc độ khi có sự cố-local (ví dụ:ateur bị trễ ở một trạm) mà không cần một trung tâm điều phối toàn cục.

### Ví dụ 2: Coalition trong chuỗi cung ứng

Trong một mạng lưới sản xuất điện tử, có ba loại agent:  
- **Nguyên liệu agent (N)** – chịu trách nhiệm đặt mua linh kiện.  
- **Sản xuất agent (P)** – lên lịch sản xuất trên các đường chuyền.  
- **Phân phối agent (D)** – quản lý kho và vận chuyển sản phẩm tới khách hàng.

Giả sử ở một quý, agent **P** báo hiệu quá tải vì thiếu linh kiện. Thay vì Re‑plan toàn bộ hệ thống, các agent **N** và **D** lập **coalition tạm thời**:  
- **N** tăng tần suất đặt mua và ưu tiên các linh kiện cần thiết.  
- **D** giải phóng một phần kho chứa sản phẩm đã hoàn thành để giảm áp lực lên **P**.  

Sau khi **P** hồi phục đủ nguyên liệu, coalition được giải tán; mỗi agent quay lại hoạt động bình thường. Mô hình này cho phép hệ thống phản hồi nhanh mà không phải xây dựng lại toàn bộ logic lập kế hoạch.

## 5. Tổng kết

- Hệ thống đa tác nhân (MAS) cho phép nhiều **AI agent** tự quyết hợp tác để giải quyết các vấn đề lớn và phức tạp mà một agent đơn lẻ khó khăn xử lý.  
- Các kiến trúc **tập trung** và **phi tập trung**, cùng với các **cấu trúc tổ chức** (hierarchical, holonic, coalition, team) cung cấp các lựa chọn phù hợp với mức độ kiểm soát và độ bền mong muốn.  
- Hành vi **flocking** và **swarming** cho thấy cách princípio tự nhiên có thể được áp dụng vào phần mềm và robot để đạt được đồng bộ và tự organizzation.  
- MAS được ứng dụng thành công trong giao thông, y tế, chuỗi cung ứng và phòng ngự, mang lại ưu điểm về linh hoạt, mở rộng, chuyên môn và hiệu suất.  
- Tuy nhiên, việc thiết kế MAS cũng đối mặt với thách thức về lỗi chung của agent, phức tạp trong điều phối và khó đoán trước hành vi trong môi trường phi tập trung; việc quản lý dữ liệu, kiểm tra rigor và thiết kế cơ chế đàm판 là cần thiết để giảm thiểu rủi ro.  

Việc nắm vững các khái niệm trên sẽ giúp bạn đánh giá khi nào nên áp dụng MAS và cách构建 một hệ thống agent ổn định, hiệu quả trong thực tiễn.