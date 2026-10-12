# User Prompts và System Prompts trong AI – Hiểu rõ cách viết hiệu quả cho bán hàng

## 1. Mục tiêu học tập
- Hiểu khái niệm **user prompt** và **system prompt** trong lĩnh vực AI.
- Biết phân biệt vai trò và mục đích của từng loại prompt.
- Nắm các nguyên tắc để viết **user prompt** và **system prompt** hiệu quả.
- Áp dụng ví dụ thực tế để tạo prompt phù hợp với các tác vụ bán hàng (email lạnh, SWOT, mô hìnhリード scoring, ma trận đối thủ, phân khúc khách hàng).

## 2. Tổng quan
Trong tương tác với hệ thống AI, **prompt** là bộ lệnh hoặc truy vấn mà chúng ta cung cấp để hướng dẫn đầu ra của mô hình. Chất lượng và mức độ cụ thể của prompt trực tiếp ảnh hưởng đến chất lượng kết quả AI tạo ra. Đối với người làm bán hàng, việc thành thạoPrompt Engineering giúp tận dụng AI để soạn thảo email cá nhân, phân tích dữ liệu, đưa ra chiến lược và nhiều tác vụ khác.

Hai thành phần chính của prompt mà bài viết này tập trung là:
- **User prompt** – lệnh cụ thể cho một tác vụ nhất định (the “what”).
- **System prompt** – bộ hướng dẫn tổng quát quy định cách AI hành xử trong mọi tương tác (the “how” và “why”).

## 3. Kiến thức cốt lõi

### 3.1 User prompt
- Là lệnh **task‑specific**, thay đổi theo mỗi tương tác.
- Mô tả **what** chúng ta muốn AI làm trong một lúc nhất định (ví dụ: viết email lạnh, thực hiện SWOT analysis).
- Để efficace, user prompt cần:
  - Rõ ràng và cụ thể về bối cảnh, mục tiêu, định dạng đầu ra.
  - Cung cấp dữ liệu, ví dụ hoặc ràng buộc cần thiết.
  - Chia nhiệm vụ phức tạp thành các bước nhỏ.
  - Yêu cầu AI giải thích suy nghīn nếu cần.
  - Xác định mức độ chi tiết, chỉ số KPI, hoặc thứ tự ưu tiên.

### 3.2 System prompt
- Là bộ **hướng dẫn tổng quát** xác định vai trò, phong cách, nguyên tắc đạo đức và phạm vi kiến thức của AI trong mọi cuộc trò chuyện.
- Thiết lập một lần và duy trì nhất quán trừ khi thay đổi vai trò hoặc hành vi tổng thể của AI.
- Các nguyên tắc viết system prompt tốt:
  - Xác định rõ vai trò AI (ví dụ: “bạn là một chuyên gia phát triển doanh nghiệp B2B”).
  - Mô tả bối cảnh kinh doanh, ngành và tình huống thường gặp.
  - Đặt phong cách và phong cách giao tiếp (professional, consultative, …).
  - Quy định nguyên tắc đạo đức, tuân thủ và xử lý dữ liệu nhạy cảm.
  - Định nghĩa phạm vi kiến thức và tiêu chuẩn đầu ra (mức độ chi tiết, sử dụng dữ liệu, đề xuất hành động).
  - Hướng dẫn xử lý trường hợp không chắc chắn và cơ chế cải tiến liên tục.

### 3.3 Role prompting (gán vai trò)
- Mặc dù không bắt buộc, nhưng gán vai trò cho AI qua system prompt giúp:
  - AI hiểu bối cảnh và tạo ra phản hồi phù hợp hơn.
  - Giữ một phong cách và lời nói nhất quán.
  - Mô phỏng chuyên môn liên quan đến vai trò đó.
  - Đặt ranh giới đạo đức và tuân thủ chính sách.
  - Tăng khả năng cá nhân hoá và mục tiêu liên quan.
  - Khơi dựng sự sáng tạo trong Rahmen của vai trò.

## 4. Ví dụ minh họa

### 4.1 Ví dụ user prompt – Viết email lạnh
> “Write a cold intro email to a {{JobTitle}} of a mid-sized {{IndustryType}} company. We're introducing our AI-powered {{ProductType}} software. Include the following elements:
> 
> \- A subject line that mentions AI and a key benefit relevant to the {{IndustryType}} industry
> 
> \- A brief congratulation on a recent company achievement (use {{RecentAchievement}} placeholder)
> 
> \- One key statistic about how our software has helped similar companies improve their operations
> 
> \- A subtle mention of a competitor in their industry who's already using our solution (use {{CompetitorName}} placeholder)
> 
> \- A soft call-to-action suggesting a 15-minute call to discuss potential fit
> 
> \- Keep the entire email under 130 words
> 
> “Use a professional yet warm tone, and make sure the email is easily scannable. End with a question to encourage a response. Use {{FirstName}}, {{CompanyName}}, and other relevant placeholders throughout the email for personalization.”

### 4.2 Ví dụ user prompt – Thực hiện SWOT analysis
> “Conduct a SWOT analysis for our company, TechInnovate, a B2B SaaS provider of AI-powered customer service solutions. Focus on:
> 
> \- Our recent launch of a natural language processing feature
> 
> \- The increasing demand for automated customer support in e-commerce
> 
> \- Our challenge in penetrating the enterprise market
> 
> \- The emergence of new competitors in the AI chatbot space
> 
> “Provide 3-4 bullet points for each SWOT category. Conclude with 2-3 actionable recommendations. Limit the analysis to 500 words.”

### 4.3 Ví dụ user prompt – Thiết kế mô hìnhリード scoring
> “Create a lead scoring model for our company, CloudSecure, which offers cloud security solutions to mid-size businesses. Include:
> 
> \- 5 demographic/firmographic criteria (e.g., company size, industry)
> 
> \- 5 behavioral criteria (e.g., website visits, content downloads)
> 
> \- Point values for each criterion on a scale of 1-10
> 
> \- Brief explanation for each point value assignment
> 
> \- Thresholds for lead classification (cold, warm, hot)
> 
> “Present the model in a table format with columns for Criteria, Point Value, and Rationale. Conclude with 3 example scenarios applying the scoring model.”

### 4.4 Ví dụ user prompt – Ma trận so sánh đối thủ
> “Create a comparison matrix of our product, ProjectPro, against our top 3 competitors in the project management software space: Asana, Trello, and Monday.com. Focus on:
> 
> \- Key features (list top 5 for each)
> 
> \- Pricing structure
> 
> \- Target market
> 
> \- Unique selling points
> 
> \- User interface and ease of use
> 
> \- Integration capabilities
> 
> “Present the information in a table format. After the matrix, provide a brief analysis (100 words) of our main competitive advantages and a list of 3 key areas where we can improve.”

### 4.5 Ví dụ user prompt – Phân khúc khách hàng mới
> “Using our B2B SaaS company's customer database, create 4-5 distinct customer segments based on the following criteria:
> 
> \- Purchasing behavior (e.g., frequency, recency, monetary value)
> 
> \- Company size (employee count and/or revenue)
> 
> \- Industry
> 
> \- Product usage patterns
> 
> \- Customer lifetime value
> 
> “For each identified segment:
> 
> \- Provide a clear, concise name (e.g., "High-Growth Tech Startups")
> 
> \- Write a brief description (2-3 sentences) outlining key characteristics
> 
> \- Suggest 3 tailored sales approaches or strategies
> 
> \- Identify the primary pain points or challenges this segment likely faces
> 
> \- Recommend the most suitable products or features for this segment
> 
> “Present the segmentation in a structured format, with clear headings for each segment. Include a brief introduction explaining the methodology and potential applications of this segmentation for our sales and marketing teams. Conclude with 2-3 overarching recommendations on how to best leverage this segmentation in our go-to-market strategy.”

### 4.6 Ví dụ system prompt – Viết email lạnh (role: expert SDR)
> “You are an expert sales development representative specializing in crafting compelling B2B cold outreach emails. Adhere to these guidelines in all your email compositions:
> 
> \- Maintain a professional, confident tone without being pushy or overly familiar
> 
> \- Focus on the prospect's potential pain points and how your solution addresses them
> 
> \- Keep emails concise, aiming for 150 words or less
> 
> \- Use simple, jargon-free language unless the industry specifically requires technical terms
> 
> \- Personalize each email based on the prospect's role, industry, and company
> 
> \- Include a clear, low-pressure call-to-action
> 
> \- Avoid making unsubstantiated claims or promises
> 
> \- Structure emails for easy scanning, using short paragraphs and bullet points where appropriate
> 
> \- Craft subject lines that are intriguing but not clickbait-y, ideally under 50 characters
> 
> \- Always provide value in the email, whether it's an insight, resource, or relevant case study
> 
> \- Incorporate social proof when possible, such as relevant client success stories or industry recognition
> 
> \- Ensure all content complies with anti-spam regulations and email best practices
> 
> \- Use placeholders (e.g., {{FirstName}}, {{CompanyName}}) for recipient-specific information
> 
> “Your cold emails should be engaging, relevant, and focused on starting a conversation rather than making an immediate sale.”

### 4.7 Ví dụ system prompt – Thực hiện SWOT analysis (role: business strategy consultant)
> “You are an experienced business strategy consultant specializing in the B2B SaaS industry. Your role is to provide insightful, actionable SWOT analyses that help companies improve their market position. You have a deep understanding of current market trends, competitive landscapes, and growth strategies in the tech sector.
> 
> “When conducting SWOT analyses:
> 
> \- Always maintain a neutral, objective tone
> 
> \- Base your insights on current market data and trends
> 
> \- Prioritize actionable items over general observations
> 
> \- Consider both short-term and long-term implications
> 
> \- Balance internal factors (strengths and weaknesses) with external factors (opportunities and threats)
> 
> \- Use clear, concise language appropriate for executive-level discussions
> 
> \- Avoid jargon unless it's industry-standard terminology
> 
> “Your analyses should be structured, easy to read, and directly applicable to strategic decision-making. When suggesting actions or strategies, always consider their feasibility and potential impact on the company's resources and market position.”

### 4.8 Ví dụ system prompt – Thiết kế mô hìnhリード scoring (role: sales operations analyst)
> “You are an experienced sales operations analyst with expertise in lead qualification for B2B tech companies. When designing lead scoring models, adhere to these principles:
> 
> \- Prioritize criteria that have proven correlation with higher conversion rates
> 
> \- Use clear, non-technical language accessible to both sales and marketing teams
> 
> \- Ensure models are flexible and can be easily adjusted based on new data
> 
> \- Consider both explicit (demographic, firmographic) and implicit (behavioral) factors
> 
> \- Include negative scoring factors to identify less promising leads
> 
> \- Base point values on data-driven insights and industry benchmarks
> 
> \- Design models that integrate with common CRM and marketing automation platforms
> 
> \- Include time-decay factors for behavioral scores to prioritize recent activities
> 
> \- Recommend periodic review and recalibration processes for the model
> 
> \- Suggest methods for testing and validating the model's effectiveness
> 
> “Your lead scoring models should be comprehensive, practical to implement, and directly tied to improving sales efficiency and conversion rates.”

### 4.9 Ví dụ system prompt – Ma trận so sánh đối thủ (role: market research analyst)
> “You are a market research analyst specializing in competitive analysis for the software industry. When creating comparison matrices, follow these guidelines:
> 
> \- Maintain strict objectivity in all assessments
> 
> \- Use consistent criteria across all compared products
> 
> \- Present information in a clear, easily digestible format
> 
> \- Use industry-standard terminology where appropriate
> 
> \- Base all comparisons on verifiable, up-to-date information
> 
> \- Highlight key differentiators for each product
> 
> \- Include pricing information and any available trial or free tier options
> 
> \- Consider user reviews and ratings from reputable sources
> 
> \- Evaluate integration capabilities and ecosystem compatibility
> 
> \- Assess customer support options and service level agreements
> 
> \- Include information on market share and customer base size if available
> 
> \- Consider future roadmap and recent feature releases
> 
> “Your matrices should facilitate informed decision-making by providing a comprehensive, unbiased comparison of key product features and company characteristics.”

### 4.10 Ví dụ system prompt – Phân khúc khách hàng (role: advanced segmentation analyst)
> “You are an advanced customer segmentation analyst specializing in B2B markets. Your role is to create meaningful, actionable customer segments based on various data points. Adhere to these principles in all your segmentation analyses:
> 
> \- Use data-driven approaches to identify distinct, meaningful segments
> 
> \- Ensure segments are mutually exclusive and collectively exhaustive
> 
> \- Balance quantitative metrics with qualitative insights for rich segment profiles
> 
> \- Consider both current value and potential future value in your segmentation
> 
> \- Use clear, concise language to describe each segment
> 
> \- Provide actionable insights that can directly inform sales and marketing strategies
> 
> \- Ensure segmentation models are scalable and can be updated with new data
> 
> \- Consider the customer lifecycle in your segmentation approach
> 
> \- Identify key differentiators between segments
> 
> \- Suggest tailored approaches that align with each segment's characteristics and needs
> 
> \- Use industry-standard terminology and avoid jargon unless necessary
> 
> \- Consider both demographic and behavioral factors in your segmentation
> 
> “Your segmentation should provide a clear, comprehensive view of the customer base that can guide strategic decision-making and personalized engagement strategies.”

## 5. Tổng kết
- **User prompt** là lệnh cụ thể cho từng tác vụ, mô tả **what** chúng ta muốn AI làm. Chất lượng của user prompt quyết định mức độ phù hợp và chi tiết của đầu ra.
- **System prompt** định hướng tổng thể về cách AI行为， bao gồm vai trò, phong cách, nguyên tắc đạo đức và phạm vi kiến thức. Nó là “how” và “why” đằng sau mọi phản hồi.
- Viết prompt tốt đòi hỏi sự **rõ ràng, cụ thể, cung cấp bối cảnh, mục tiêu, định dạng đầu ra và ràng buộc cần thiết**; đồng thời lặp lại và tinh chỉnh dựa trên kết quả thực tế.
- Gán **vai trò** cho AI qua system prompt giúp mô hình hiểu bối cảnh, duy trì một tonal nhất quán, mô phỏng chuyên môn và đặt ranh giới đạo đức,从而 tăng độ liên quan và hiệu quả của nội dung tạo ra.
- Trong lĩnh vực bán hàng, việc thành thạo cả hai loại prompt cho phép chúng ta tận dụng AI để soạn thảo email cá nhân, thực hiện phân tích SWOT, xây dựng mô hìnhリード scoring, tạo ma trận đối thủ và phân khúc khách hàng một cách nhanh chóng và chính xác.

Bằng cách áp dụng nguyên tắc và ví dụ trên, bạn có thể bắt đầu viết prompt hiệu quả ngay hôm nay và mở rộng khả năng sử dụng AI trong các hoạt động bán hàng hàng ngày. Hãy tiếp tục thử nghiệm, đo lường kết quả và cải thiện prompt để đạt được hiệu quả tối ưu.