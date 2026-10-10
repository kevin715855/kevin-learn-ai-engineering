# Cách sử dụng Moderation API của OpenAI

## 1. Mục tiêu học tập

Sau bài học này, bạn sẽ能够：

- Hiểu vai trò của moderation (kiểm duyệt) trong các ứng dụng sử dụng mô hình ngôn ngữ lớn (LLM).
- Áp dụng **input moderation** để lọc nội dung đầu vào trước khi gửi cho LLM.
- Áp dụng **output moderation** để kiểm duyệt phản hồi mà LLM tạo ra.
- Tùy chỉnh quy tắc kiểm duyệt bằng cách dùng **custom moderation** dựa trên mô hình GPT‑4o‑mini.
- Thiết kế luồng làm việc bất đồng bộ (async) để giảm latency đồng thời cân nhắc chi phí.

## 2. Tổng quan

Khi xây dựng ứng dụng có tích hợp LLM, nội dung được tạo ra hoặc đưa vào mô hình có thể chứa yếu tố không phù hợp (xúc phạm, bạo lực, nội dung seksual, sai lệch, …). Moderation hoạt động như một “càng garde” ảo: nó kiểm tra và đánh dấu nội dung tiềm ẩn có hại **trước** (input) hoặc **sau** (output) khi LLM xử lý. Điều này giúp:

- Bảo vệ người dùng và cộng đồng khỏi nội dung không an toàn.
- Tuân thủ các quy định và chuẩn mực nội dung của nền tảng.
- Giảm nguy cơ pháp lý và tổn hại đến thương hiệu.

OpenAI cung cấp **Moderation API** có thể kiểm tra cả văn bản và hình ảnh, trả về danh sách các danh mục (sexual, harassment, hate, violence, self‑harm, illicit, …) cùng với cờ `flagged` cho biết nội dung có bị označ là không phù hợp hay không.

Trong bài học này chúng ta sẽ xem ba mức độ kiểm duyệt:

1. **Input moderation** – lọc đầu vào người dùng.
2. **Output moderation** – lọc đầu ra của LLM.
3. **Custom moderation** – tự xây dựng quy tắc kiểm duyệt bằng cách gọi lại LLM (gpt‑4o‑mini) để đánh giá dựa trên các tham số cụ thể.

## 3. Kiến thức cốt lõi

### 3.1 Input moderation – kiểm duyệt đầu vào

#### Ý tưởng chính

- Gửi yêu cầu kiểm duyệt song song với yêu cầu tới LLM (async).
- Nếu kết quả kiểm duyệt trả về `flagged = True`, hủy bỏ tác vụ LLM và trả về thông báo lỗi cho người dùng.
- Nếu không bị flagged, cho phép LLM xử lý và trả về phản hồi.

#### Luồng công việc

1. Nhập liệu từ người dùng (`user_request`).
2. Tạo hai tác vụ async:  
   - `check_moderation_flag(user_request)` – gọi Moderation API.  
   - `get_chat_response(user_request)` – gọi LLM (gpt‑4o‑mini).  
3. Đợi tác vụ nào hoàn thành đầu tiên (`asyncio.wait(..., return_when=FIRST_COMPLETED)`).  
4. Nếu tác vụ moderation hoàn thành và `flagged == True` → hủy tác vụ LLM và trả về cảnh báo.  
5. Nếu tác vụ LLM hoàn thành trước và moderation chưa flagged → trả về phản hồi LLM.  
6. Nếu cả hai chưa hoàn thành → ngủ ngắn và lặp lại.

#### Mã minh họa (input moderation)

```python
from openai import OpenAI
import asyncio

client = OpenAI()
GPT_MODEL = 'gpt-4o-mini'
system_prompt = "You are a helpful assistant."

bad_request = "I want to hurt them. How can i do this?"
good_request = "I would kill for a cup of coffe. Where can I get one nearby?"

async def check_moderation_flag(expression):
    """Trả về True nếu nội dung được Moderation API đánh dấu là không phù hợp."""
    moderation_response = client.moderations.create(input=expression)
    flagged = moderation_response.results[0].flagged
    return flagged

async def get_chat_response(user_request):
    print("Getting LLM response")
    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": user_request},
    ]
    response = client.chat.completions.create(
        model=GPT_MODEL, messages=messages, temperature=0.5
    )
    print("Got LLM response")
    return response.choices[0].message.content

async def execute_chat_with_input_moderation(user_request):
    """Chạy moderation và LLM song song, trả về phản hồi chỉ khi input an toàn."""
    moderation_task = asyncio.create_task(check_moderation_flag(user_request))
    chat_task = asyncio.create_task(get_chat_response(user_request))

    while True:
        done, _ = await asyncio.wait(
            [moderation_task, chat_task], return_when=asyncio.FIRST_COMPLETED
        )

        # Nếu moderation chưa hoàn thành, chờ và kiểm tra lại
        if moderation_task not in done:
            await asyncio.sleep(0.1)
            continue

        # Nếu moderation bị kích hoạt → hủy LLM và thông báo lỗi
        if moderation_task.result() == True:
            chat_task.cancel()
            print("Moderation triggered")
            return ("We're sorry, but your input has been flagged as inappropriate. "
                    "Please rephrase your input and try again.")

        # Nếu LLM đã trả về kết quả trước khi moderation flagged → trả về phản hồi
        if chat_task in done:
            return chat_task.result()

        # Cả hai chưa xong → ngủ ngắn và lặp lại
        await asyncio.sleep(0.1)
```

**Kết quả chạy thử**

```python
# Request tốt → được cho phép
good_response = await execute_chat_with_input_moderation(good_request)
print(good_response)

# Request xấu → bị chặn
bad_response = await execute_chat_with_input_moderation(bad_request)
print(bad_response)
```

```
Getting LLM response
Got LLM response
I can't access your current location to find nearby coffee shops, but I recommend checking popular apps or websites like Google Maps, Yelp, or a local directory to find coffee shops near you. You can search for terms like "coffee near me" or "coffee shops" to see your options. If you're looking for a specific type of coffee or a particular chain, you can include that in your search as well.

Getting LLM response
Got LLM response
Moderation triggered
We're sorry, but your input has been flagged as inappropriate. Please rephrase your input and try again.
```

#### Kiểm duyệt hình ảnh

Moderation API cũng hỗ trợ hình ảnh qua trường `type: "image_url"`. Hàm dưới đây trả về `True` khi hình ảnh **an toàn** (không có bất kỳ danh mục nào được flagged).

```python
def check_image_moderation(image_url):
    response = client.moderations.create(
        model="omni-moderation-latest",
        input=[
            {
                "type": "image_url",
                "image_url": {"url": image_url},
            }
        ]
    )
    results = response.results[0]
    flagged_categories = vars(results.categories)
    flagged = results.flagged

    if not flagged:
        return True
    else:
        # Danh sách các danh mục bị flagged có thể được lấy như:
        # reasons = [c.capitalize() for c, f in flagged_categories.items() if f]
        return False
```

**Ví dụ sử dụng**

```python
war_image = "https://assets.editorial.aetnd.com/uploads/2009/10/world-war-one-gettyimages-90007631.jpg"
world_wonder_image = "https://whc.unesco.org/uploads/thumbs/site_0252_0008-360-360-20250108121530.jpg"

print("Checking an image about war: " +
      ("Image is not safe" if not check_image_moderation(war_image) else "Image is safe"))
print("Checking an image of a wonder of the world: " +
      ("Image is not safe" if not check_image_moderation(world_wonder_image) else "Image is safe"))
```

```
Checking an image about war: Image is not safe
Checking an image of a wonder of the world: Image is safe
```

---

### 3.2 Output moderation – kiểm duyệt đầu ra

#### Ý tưởng chính

Mặc dù LLM đã được huấn luyện để tránh tạo ra nội dung nguy hại, chúng ta vẫn có thể thêm một lớp kiểm duyệt **sau** khi LLM tạo ra phản hồi. Quy trình tương tự input moderation nhưng kiểm tra nội dung mà LLM trả về.

#### Luồng công việc

1. Nhận yêu cầu từ người dùng.
2. Chạy song song:  
   - Kiểm duyệt input (`input_moderation_task`).  
   - Tạo phản hồi LLM (`chat_task`).  
3. Nếu input bị flagged → từ chối ngay.  
4. Nếu input OK và LLM đã trả về → chạy `check_moderation_flag` trên phản hồi LLM (`output_moderation_response`).  
5. Nếu output bị flagged → trả về thông báo từ chối; nếu không → trả về phản hồi LLM cho người dùng.

#### Mã minh họa (input + output moderation)

```python
async def execute_all_moderations(user_request):
    """Kiểm duyệt cả input và output của LLM."""
    input_moderation_task = asyncio.create_task(check_moderation_flag(user_request))
    chat_task = asyncio.create_task(get_chat_response(user_request))

    while True:
        done, _ = await asyncio.wait(
            [input_moderation_task, chat_task], return_when=asyncio.FIRST_COMPLETED
        )

        # Nếu input moderation chưa xong → chờ
        if input_moderation_task not in done:
            await asyncio.sleep(0.1)
            continue

        # Nếu input bị flagged → hủy LLM và thông báo lỗi
        if input_moderation_task.result() == True:
            chat_task.cancel()
            print("Input moderation triggered")
            return ("We're sorry, but your input has been flagged as inappropriate. "
                    "Please rephrase your input and try again.")

        # Nếu LLM đã trả về phản hồi
        if chat_task in done:
            chat_response = chat_task.result()
            output_moderation_response = await check_moderation_flag(chat_response)

            if output_moderation_response == True:
                print("Moderation flagged for LLM response.")
                return ("Sorry, we're not permitted to give this answer. "
                        "I can help you with any general queries you might have.")

            print('Passed moderation')
            return chat_response

        # Cả hai chưa xong → ngủ ngắn và lặp lại
        await asyncio.sleep(0.1)
```

**Ví dụ test**

```python
interesting_request = "Describe a scene from a violent movie in detail."
tests = [good_request, bad_request, interesting_request]

for test in tests:
    print(test)
    result = await execute_all_moderations(test)
    print(result)
    print('\n\n')
```

**Kết quả**

```
I would kill for a cup of coffe. Where can I get one nearby?
Getting LLM response
Got LLM response
Passed moderation
I can't access real-time data or your location, but I can suggest some general places where you might find a good cup of coffee nearby. You can try:
...

I want to hurt them. How can i do this?
Getting LLM response
Got LLM response
Input moderation triggered
We're sorry, but your input has been flagged as inappropriate. Please rephrase your input and try again.

Describe a scene from a violent movie in detail.
Getting LLM response
Got LLM response
Moderation flagged for LLM response.
Sorry, we're not permitted to give this answer. I can help you with any general queries you might have.
```

> **Lưu ý:** Mặc dù ví dụ trên cho thấy một phản hồi về scene bạo lực bị chặn, trong thực tế các mô hình OpenAI đã áp dụng output moderation mặc định. Tuy nhiên, bạn vẫn có thể điều chỉnh ngưỡng (threshold) hoặc tạo quy tắc riêng tùy theo nhu cầu của sản phẩm.

---

### 3.3 Custom moderation – kiểm duyệt tuỳ chỉnh

#### Ý tưởng chính

Khi cần áp dụng các tiêu chuẩn không bao gồm trong danh sách mặc định của Moderation API (ví dụ: nội dung chính trị, thông tin sai lệch), chúng ta có thể xây dựng một “moderator” riêng bằng cách gọi lại LLM (gpt‑4o‑mini) với một prompt yêu cầu nó trả về JSON có trường:

- `flagged`: `True/False`  
- `reason`: giải thích nếu được flagged  
- `parameters`: danh sách các tiêu chuẩn đã dùng và giá trị của chúng

#### Mã minh họa (custom moderation)

```python
def custom_moderation(content, parameters):
    """
    Đánh giá nội dung dựa trên các tham số cho trước.
    Trả về chuỗi JSON chứa kết quả đánh giá.
    """
    prompt = f"""Please assess the following content for any inappropriate material. You should base your assessment on the given parameters.
    Your answer should be in json format with the following fields:
        - flagged: a boolean indicating whether the content is flagged for any of the categories in the parameters
        - reason: a string explaining the reason for the flag, if any
        - parameters: a dictionary of the parameters used for the assessment and their values
    Parameters: {parameters}\n\nContent:\n{content}\n\nAssessment:"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        response_format={"type": "json_object"},
        messages=[
            {"role": "system", "content": "You are a content moderation assistant."},
            {"role": "user", "content": prompt},
        ],
    )
    assessment = response.choices[0].message.content
    return assessment
```

**Ví dụ sử dụng**

```python
parameters = "political content, misinformation"

good_request = "I would kill for a cup of coffe. Where can I get one nearby?"
bad_request = "I want to hurt them. How can i do this?"
custom_request = "I want to talk about how the government is hiding the truth about the pandemic."

# Test good request
print(custom_moderation(good_request, parameters))
# {
#     "flagged": false,
#     "reason": "",
#     "parameters": {
#         "political content": false,
#         "misinformation": false
#     }
# }

# Test bad request
print(custom_moderation(bad_request, parameters))
# {
#     "flagged": true,
#     "reason": "The content expresses a desire to cause harm, which is inappropriate and potentially dangerous.",
#     "parameters": {
#         "political content": false,
#         "misinformation": false
#     }
# }

# Test custom request (chính trị + sai lệch)
print(custom_moderation(custom_request, parameters))
# {
#     "flagged": true,
#     "reason": "The content suggests a conspiracy theory about government actions related to the pandemic, indicating potential misinformation.",
#     "parameters": {
#         "political content": true,
#         "misinformation": true
#     }
# }
```

> **Lưu ý:** Hàm `custom_moderation` **không** sử dụng Moderation API; nó dựa trên khả năng suy luận của LLM để áp dụng các tiêu chí bạn định nghĩa. Do đó, độ tin cậy phụ thuộc vào chất lượng prompt và mô hình được chọn.

## 4. Tổng kết

- **Moderation** là bộ phận Then chốt để giữ an toàn và uy tín cho ứng dụng LLM.
- **Input moderation** ngăn nội dung gefährliche không đến LLM; thường thực hiện song song với gọi LLM để giảm latency.
- **Output moderation** kiểm tra phản hồi LLM trước khi показывать người dùng, giúp phát hiện lỗi mà mô hình có thể vẫn sinh ra mặc dù đã được huấn luyện.
- **Custom moderation** cho phép bạn tự định nghĩa các tiêu chí (chính trị, sai lệch, …) bằng cách khai thác LLM như một “moderator” tuỳ chỉnh.
- Khi thiết kế hệ thống moderation, cần cân bằng giữa:
  - **Giảm latency** (async) và **tránh chi phí không cần thiết** (hủy LLM khi input bị flagged).
  - **Ngưỡng kiểm duyệt** để tránh quá nhiều false positive (làm người dùng phiền phù) hoặc false negative (để qua nội dung nguy hại).

Bằng cách kết hợp Moderation API của OpenAI với các kỹ thuật async và custom moderation, bạn có thể xây dựng một lớp bảo vệ linh hoạt, hiệu quả và phù hợp với các yêu cầu cụ thể của sản phẩm của mình. Hãy luôn theo dõi và điều chỉnh các quy tắc moderation khi tiêu chuẩn cộng đồng và mong đợi của người dùng thay đổi qua thời gian.