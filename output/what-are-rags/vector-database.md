# Kết hợp Knowledge Graph và Vector Database trong Retrieval‑Augmented Generation (Graph RAG)

## 1. Mục tiêu học tập

Sau bài học này, bạn sẽ能够:

- Giải thích ý tưởng cơ bản của Retrieval‑Augmented Generation (RAG) và tại sao việc bổ sung ngữ cảnh từ nguồn dữ liệu ngoài giúp LLM trả lời chính xác hơn.  
- Mô tả ba cách chính để sử dụng Knowledge Graph (KG) trong giai đoạn truy xuất của RAG: truy xuất dựa trên vector, truy xuất bằng prompt‑to‑query (SPARQL/Cypher) và phương pháp hybrid (vector + SPARQL).  
- Triển khai truy xuất sémantic và similarity search trên một vector database (Weaviate) bằng cách vector hóa tiêu đề và tóm tắt bài báo khoa học.  
- Xây dựng một Knowledge Graph đơn giản từ dữ liệu cùng structure (RDF/OWL) và thực hiện truy vấn semantic bằng SPARQL.  
- Kết hợp vector database và KG để lọc kết quả, giảm hiện tượng “context poisoning” và cải thiện độ giải thích của kết quả truy xuất.  
- Đánh giá ưu và nhược điểm của mỗi cách tiếp cận (vector‑only, KG‑only, hybrid) về tốc độ, độ chính xác, độ giải thích và overhead triển khai.

## 2. Tổng quan

Retrieval‑Augmented Generation (RAG) là một kỹ thuật waarin chúng ta **truy xuất** thông tin liên quan từ một nguồn dữ liệu ngoài, **augment** (bổ sung) prompt gửi tới LLM, rồi cho LLM **generate** phản hồi. Khi LLM chưa được huấn luyện trên dữ liệu nội bộ, việc cung cấp ngữ cảnh chính xác giúp nó tạo ra câu trả lời phù hợp hơn.

Knowledge Graph (KG) là một mô hình dữ liệu có cấu trúc dưới dạng triple (entity‑relation‑entity), thường được mô tả bằng RDF và truy vấn qua SPARQL. KG mang lại lợi thế về **giải thích** (ta luôn biết tại sao một kết quả được trả về) và khả năng **rich‑metadata** (ví dụ: MeSH terms, quan hệ narrower/broader). Tuy nhiên, truy xuất từ KG thường yêu cầu viết các truy vấn SPARQL phức tạp và có thể chậm nếu không có chỉ mục phù hợp.

Vector database (ví dụ: Weaviate) lưu trữ các vector embedding của văn bản, cho phép tìm kiếm semantic và similarity dựa trên khoảng cách trong không gian vector. Nó rất nhanh để khởi chạy và hoạt động tốt với dữ liệu **unstructured** (tiêu đề, tóm tắt), nhưng thiếu giải thích và có nguy cơ trả về kết quả không liên quan (“context poisoning”).

Bài học này minh họa ba cách tiếp cận bằng một tập dữ liệu bài báo PubMed (tiêu đề, tóm tắt, thẻ MeSH):

1. **Vector‑based retrieval** – vector hóa tiêu đề + tóm tắt và tìm kiếm trong Weaviate.  
2. **KG‑based retrieval** – chuyển dữ liệu sang RDF, truy vấn bằng SPARQL để lấy các bài có thẻ MeSH liên quan (kèm các khái niệm narrower).  
3. **Hybrid (vectorized KG)** – thêm trường URI và thẻ MeSH vào vector database, sau đó dùng KG để lọc/filter kết quả vector (theo ngày, mức truy cập, v.v.).

Trong mỗi bước chúng tôi cũng minh họa cách sử dụng kết quả truy xuất để làm RAG (gửi tới LLM để tóm tắt/trả lời).

## 3. Kiến thức cốt lõi

### 3.1. Vector‑based retrieval (Weaviate)

- **Schema**: Định nghĩa lớp `articles` có hai thuộc tính `title` và `abstractText` (kiểu `text`). Vectorizer được thiết lập là `text2vec-openai` (model `ada`).  
- **Import dữ liệu**: Đọc CSV, thay các giá trị vô hạn bằng chuỗi rỗng, ép kiểu sang `str`, rồi dùng `client.batch` để thêm từng bản ghi vào Weaviate (tạo UUID bằng `generate_uuid5`).  
- **Truy vấn semantic**:  
  ```python
  response = (
      client.query
      .get("articles", ["title","abstractText"])
      .with_additional(["id"])
      .with_near_text({"concepts": ["Mouth Neoplasms"]})
      .with_limit(10)
      .do()
  )
  ```
- **Truy vấn similarity**: Lấy ID của một bài rồi dùng `with_near_object`.  
- **RAG**: Kết hợp `with_generate` để gửi prompt tới LLM (ví dụ: “Please explain this article {title} like you would to someone without a medical degree.”).

**Ưu điểm**: Siêu nhanh để triển khai (khoảng 15  phút với 10 000 bản ghi), hoạt động tốt với văn bản không có thẻ phong phú.  
**Nhược điểm**: “Black box” – không biết tại sao một vector được trả về; nguy cơ context poisoning khi kết quả không liên quan được đưa vào LLM.

### 3.2. Knowledge Graph‑based retrieval (RDF/SPARQL)

- **Chuyển đổi sang RDF**: Mỗi bài báo trở thành một instance của lớp `ex:Article`; thuộc tính như `schema:name` (tiêu đề), `schema:description` (tóm tắt), `schema:datePublished`, `ex:access`. Các thẻ MeSH trở thành instances của `ex:MeSHTerm` và liên quan qua `schema:about`.  
- **Truy vấn semantic**: Lấy danh sách các khái niệm MeSH rộng hơn (alternative names) và narrower concepts từ dịch vụ MeSH SPARQL (`https://id.nlm.nih.gov/mesh/sparql`). Sau đó truy vấn đồ thị地方 để lấy các bài có `schema:about` khớp với bất kỳ khái niệm nào trong danh sách đó, và xếp hạng theo số lượng khóa MeSH trùng khớp.  
- **Similarity search (Jaccard)**: So sánh tập hợp các thẻ MeSH của bài mục tiêu với mỗi bài khác, tính Jaccard similarity = |intersection| / |union|.  
- **RAG**: Sau khi có danh sách bài liên quan, ghép tiêu đề + tóm tắt thành một block text và gửi tới LLM (OpenAI Completion) với prompt tóm tắt.

**Ưu điểm**: Giải thích rõ ràng (ta biết chính xác哪些 MeSH terms导致了匹配); có thể mở rộng truy vấn bằng các quan hệ narrower/broader từ ontology.  
**Nhược điểm**: Xây dựng KG và viết SPARQL có thể tốn thời gian; truy vấn Jaccard trên hàng ngàn bài có thể mất vài chục phút vì phải tính пересечение cho mỗi cặp.

### 3.3. Hybrid approach (vectorized KG)

- **Mở rộng schema vector**: Thêm hai trường mới `meshMajor` (chuỗi chứa danh sách thẻ MeSH) và `Article_URI` (chuỗi URI). Vectorizer vẫn là `text2vec-openai`; cả czterech trường đều được vector hóa cùng lúc.  
- **Lọc kết quả bằng KG**: Sau khi lấy danh sách URI từ vector search (ví dụ: top‑20), chạy một SPARQL query trên KG để:
  - Lọc theo `datePublished` (bài sau một ngày nhất định).  
  - Lọc theo `access` (chỉ giữ những bài mà người dùng có quyền truy cập).  
  - Lọc theo các khóa MeSH cụ thể (ví dụ chỉ giữ bài có thẻ `Mouth Neoplasms` hoặc các khái niệm narrower).  
- **RAG hybrid**: Sau khi lọc, lấy tiêu đề + tóm tắt (hoặc cả `meshMajor`) để tạo context cho LLM.

**Ưu điểm**: Kết hợp tốc độ của vector search với khả năng kiểm soát, giải thích và tính linh hoạt của KG. Giảm context poisoning vì chúng ta có thể loại bỏ các kết quả không liên quan dựa trên metadata KG.  
**Nhược điểm**: Cần duyệt qua cả hai hệ thống và giữ dữ liệu đồng nhất (URI, thẻ MeSH) giữa chúng.

### 3.4. Lưu ý quan trọng từ bài viết

- **Context poisoning**: Khi vector database trả về bài báo không liên quan (ví dụ: về ung thư trực tràng khi người dùng hỏi “therapies for mouth neoplasms”), LLM vẫn sẽ tóm tắt chính xác bài đó, nhưng vì nó không phải về chủ đề được hỏi, câu trả lời cuối cùng sẽ là nhầm lẫn.  
- **Explainability**: KG cho phép trả lời “tại sao” kết quả này được chọn (ví dụ: vì bài được gắn th diente `Gingival Neoplasms`).  
- **Hiệu suất**: Vector search chỉ cần vài giây; KG query (đặc biệt khi thực hiện Jaccard) có thể mất几分钟; hybrid giữ được thời gian truy xuất vector nhanh rồi chỉ cần thực hiện một số truy vấn SPARQL trên tập kết quả nhỏ.  
- **Tuỳ chỉnh**: Các trường như `access` hoặc `datePublished` có thể được dùng để thực hiện truy cập có điều kiện (access‑control) hoặc tìm kiếm theo thời gian mà không cần thay đổi vector database.

## 4. Ví dụ minh họa

Dưới đây là một số đoạn code trích trực tiếp từ nguồn (được giữ nguyên để minh họa thực tiễn). Các chú thích bên dưới được thêm vào để giúp người đọc hiểu mục đích của mỗi khối.

### 4.1. Chuẩn bị dữ liệu và kết nối Weaviate

```python
from weaviate.util import generate_uuid5
import weaviate
import json
import pandas as pd

# Đọc dữ liệu PubMed (top 10.000 dòng để giảm thời gian tính toán)
df = pd.read_csv("PubMed Multi Label Text Classification Dataset Processed.csv")

# Kết nối tới cluster Weaviate (thay XXX bằng thông tin thực tế)
client = weaviate.Client(
    url = "XXX",                               # endpoint Weaviate
    auth_client_secret=weaviate.auth.AuthApiKey(api_key="XXX"),  # API key
    additional_headers = {
        "X-OpenAI-Api-Key": "XXX"              # key cho model OpenAI
    }
)

# Định nghĩa schema chỉ vector hóa tiêu đề và tóm tắt
class_obj = {
    "class": "articles",
    "properties": [
        {"name": "title", "dataType": ["text"]},
        {"name": "abstractText", "dataType": ["text"]}
    ],
    "vectorizer": "text2vec-openai",
    "moduleConfig": {
        "text2vec-openai": {
            "vectorizeClassName": True,
            "model": "ada",
            "modelVersion": "002",
            "type": "text"
        },
        "qna-openai": { "model": "gpt-3.5-turbo-instruct" },
        "generative-openai": { "model": "gpt-3.5-turbo" }
    }
}
client.schema.create_class(class_obj)

# Đẩy dữ liệu vào Weaviate (batch size 10, 2 workers)
import logging
import numpy as np
logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s %(levelname)s %(message)s')
df.replace([np.inf, -np.inf], np.nan, inplace=True)
df.fillna('', inplace=True)
df['Title'] = df['Title'].astype(str)
df['abstractText'] = df['abstractText'].astype(str)

with client.batch(batch_size=10, num_workers=2) as batch:
    for index, row in df.iterrows():
        try:
            obj = {"title": row.Title, "abstractText": row.abstractText}
            batch.add_data_object(
                obj,
                class_name="articles",
                uuid=generate_uuid5(obj)
            )
        except Exception as e:
            logging.error(f"Error processing row {index}: {e}")

# Kiểm tra số lượng bản ghi đã được vector hóa
print(client.query.aggregate("articles").with_meta_count().do())
```

### 4.2. Truy vấn semantic và similarity trên vector database

```python
# Semantic search: tìm 10 bài gần nhất với khái niệm “Mouth Neoplasms”
response = (
    client.query
    .get("articles", ["title","abstractText"])
    .with_additional(["id"])
    .with_near_text({"concepts": ["Mouth Neoplasms"]})
    .with_limit(10)
    .do()
)
print(json.dumps(response, indent=4))

# Similarity search: lấy bài gần nhất với bài có ID cụ thể
response = (
    client.query
    .get("articles", ["title","abstractText"])
    .with_near_object({
        "id": "a7690f03-66b9-5d17-b765-8c6eb21f99c8"   # thay bằng ID thực tế
    })
    .with_limit(10)
    .with_additional(["distance"])
    .do()
)
print(json.dumps(response, indent=2))
```

### 4.3. RAG đơn giản bằng vector database

```python
# Gửi top‑1 bài tới LLM để giải thích như với người không chuyên y tế
response = (
    client.query
    .get("articles", ["title","abstractText"])
    .with_near_text({"concepts": ["Gingival metastasis as first sign of multiorgan dissemination of epithelioid malignant mesothelioma"]})
    .with_generate(single_prompt="Please explain this article {title} like you would to someone without a medical degree.")
    .with_limit(1)
    .do()
)
print(json.dumps(response, indent=4))

# Gửi top‑3 bài và yêu cầu tóm tắt dạng bullet point
response = (
    client.query
    .get("articles", ["title","abstractText"])
    .with_near_text({"concepts": ["Mouth Neoplasms"]})
    .with_limit(3)
    .with_generate(grouped_task="Summarize the key information here in bullet points. Make it understandable to someone without a medical degree.")
    .do()
)
print(response["data"]["Get"]["Articles"][0]["_additional"]["generate"]["groupedResult"])
```

### 4.4. Xây dựng Knowledge Graph đơn giản (RDF) và truy vấn semantic

```python
from rdflib import Graph, RDF, RDFS, Namespace, URIRef, Literal
from rdflib.namespace import SKOS, XSD
import pandas as pd
import urllib.parse
import random
from datetime import datetime, timedelta

g = Graph()
schema = Namespace('http://schema.org/')
ex = Namespace('http://example.org/')
for p, ns in [('schema', schema), ('ex', ex), ('skos', SKOS), ('xsd', XSD)]:
    g.bind(p, ns)

# Định nghĩa lớp và thuộc tính
Article = URIRef(ex.Article)
MeSHTerm = URIRef(ex.MeSHTerm)
g.add((Article, RDF.type, RDFS.Class))
g.add((MeSHTerm, RDF.type, RDFS.Class))

title = URIRef(schema.name)
abstract = URIRef(schema.description)
date_published = URIRef(schema.datePublished)
access = URIRef(ex.access)
for prop in [title, abstract, date_published, access]:
    g.add((prop, RDF.type, RDF.Property))

# Hàm hỗ trợ: chuẩn hoá MeSH terms, tạo URI, sinh ngày ngẫu nhiên, mức truy cập
def parse_mesh_terms(mesh_list):
    if pd.isna(mesh_list): return []
    return [term.strip().replace(' ', '_') for term in mesh_list.strip("[]'").split(',')]

def create_valid_uri(base_uri, text):
    if pd.isna(text): return None
    safe = urllib.parse.quote(text.strip().replace(' ', '_')
                             .replace('"','').replace('<','').replace('>','').replace("'", "_"))
    return URIRef(f"{base_uri}/{safe}")

def generate_random_date():
    start = datetime.now() - timedelta(days=5*365)
    return start + timedelta(days=random.randint(0,5*365))

def generate_random_access():
    return random.randint(1,10)

# Đọc DataFrame (cùng df từ bước 4.1) và tạo triple
for index, row in df.iterrows():
    article_uri = create_valid_uri("http://example.org/article", row['Title'])
    if article_uri is None: continue
    g.add((article_uri, RDF.type, Article))
    g.add((article_uri, title, Literal(row['Title'], datatype=XSD.string)))
    g.add((article_uri, abstract, Literal(row['abstractText'], datatype=XSD.string)))
    g.add((article_uri, date_published, Literal(generate_random_date().date(), datatype=XSD.date)))
    g.add((article_uri, access, Literal(generate_random_access(), datatype=XSD.integer)))

    for term in parse_mesh_terms(row['meshMajor']):
        term_uri = create_valid_uri("http://example.org/mesh", term)
        if term_uri is None: continue
        g.add((term_uri, RDF.type, MeSHTerm))
        g.add((term_uri, RDFS.label, Literal(term.replace('_',' '), datatype=XSD.string)))
        g.add((article_uri, schema.about, term_uri))

# Lưu ttl (tùy chọn)
g.serialize(destination='ontology.ttl', format='turtle')
```

#### Truy vấn semantic bằng SPARQL (lấy các bài có thẻ MeSH liên quan tới “Mouth Neoplasms”)

```python
from SPARQLWrapper import SPARQLWrapper, JSON

def get_concept_triples_for_term(term):
    sparql = SPARQLWrapper("https://id.nlm.nih.gov/mesh/sparql")
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
    SELECT ?subject ?p ?pLabel ?o ?oLabel
    FROM <http://id.nlm.nih.gov/mesh>
    WHERE {{
        ?subject rdfs:label "{term}"@en .
        ?subject ?p ?o .
        FILTER(CONTAINS(STR(?p), "concept"))
        OPTIONAL {{ ?p rdfs:label ?pLabel . }}
        OPTIONAL {{ ?o rdfs:label ?oLabel . }}
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    triples = set()
    for r in results["results"]["bindings"]:
        triples.add(r.get("oLabel",{}).get("value","No label"))
    triples.add(term)
    return list(triples)

def get_narrower_concepts_for_term(term):
    sparql = SPARQLWrapper("https://id.nlm.nih.gov/mesh/sparql")
    query = f"""
    PREFIX rdf: <http://www.w3.org/1999/02/22-rdf-syntax-ns#>
    PREFIX rdfs: <http://www.w3.org/2000/01/rdf-schema#>
    PREFIX meshv: <http://id.nlm.nih.gov/mesh/vocab#>
    PREFIX mesh: <http://id.nlm.nih.gov/mesh/>
    SELECT ?narrowerConcept ?narrowerConceptLabel
    WHERE {{
        ?broaderConcept rdfs:label "{term}"@en .
        ?narrowerConcept meshv:broaderDescriptor ?broaderConcept .
        ?narrowerConcept rdfs:label ?narrowerConceptLabel .
    }}
    """
    sparql.setQuery(query)
    sparql.setReturnFormat(JSON)
    results = sparql.query().convert()
    concepts = set()
    for r in results["results"]["bindings"]:
        concepts.add(r.get("narrowerConceptLabel",{}).get("value","No label"))
    return list(concepts)

def get_all_narrower_concepts(term, depth=2, cur=1):
    allc = {}
    narrower = get_narrower_concepts_for_term(term)
    allc[term] = narrower
    if cur < depth:
        for c in narrower:
            allc.update(get_all_narrower_concepts(c, depth, cur+1))
    return allc

term = "Mouth Neoplasms"
alt_names = get_concept_triples_for_term(term)
narrow_dict = get_all_narrower_concepts(term, depth=2)

# Flatten để получить список всех связанных MeSH терминов
def flatten(d):
    res = []
    def rec(x):
        for k,v in x.items():
            res.append(k)
            if v: rec(dict.fromkeys(v, []))
    rec(d)
    return res

mesh_terms_flat = flatten({term: narrow_dict})
# chuyển sang URIRef để dùng trong truy vấn đồ thị locally
mesh_uris = [create_valid_uri("http://example.org/mesh", t.replace(' ', '_')) for t in mesh_terms_flat]

# Truy vấn đồ thị để lấy bài có ít nhất một khóa MeSH trùng khớp
query = """
PREFIX schema: <http://schema.org/>
PREFIX ex: <http://example.org/>
SELECT ?article ?title ?abstract ?datePublished ?access ?meshTerm
WHERE {
  ?article a ex:Article ;
           schema:name ?title ;
           schema:description ?abstract ;
           schema:datePublished ?datePublished ;
           ex:access ?access ;
           schema:about ?meshTerm .
  ?meshTerm a ex:MeSHTerm .
}
"""
article_data = {}
for uri in mesh_uris:
    for row in g.query(query, initBindings={'meshTerm': uri}):
        art = row['article']
        if art not in article_data:
            article_data[art] = {'title': row['title'],
                                 'abstract': row['abstract'],
                                 'datePublished': row['datePublished'],
                                 'access': row['access'],
                                 'meshTerms': set()}
        article_data[art]['meshTerms'].add(str(row['meshTerm']))

# Xếp hạng theo số lượng khóa MeSH trùng khớp
ranked = sorted(article_data.items(),
                key=lambda kv: len(kv[1]['meshTerms']),
                reverse=True)
top3 = ranked[:3]
for art_uri, data in top3:
    print(f"Title: {data['title']}")
    print("MeSH Terms:")
    for mt in data['meshTerms']:
        print(f"  - {mt}")
    print()
```

### 4.5. Hybrid: Vector database + KG lọc

Sau khi đã có schema vector bao gồm trường `meshMajor` và `Article_URI` (xem phần “Step 3: use a vectorized knowledge graph” trong nguồn), chúng ta thực hiện:

1. **Vector search** lấy top‑20URI dựa trên near_text `"therapies for mouth neoplasms"`.  
2. **SPARQL filter** giữ lại những URI có `meshMajor` chứa một trong các khóa MeSH liên quan tới “Mouth Neoplasms” (narrow concepts) và có `access` thuộcجموعة cho phép (ví dụ `[3,5,7]`).  
3. **RAG** dùng kết quả đã lọc để tạo prompt cho LLM.

Đoạn code minh họa các bước lọc (được lấy trực tiếp từ nguồn):

```python
# Giả sử `response` là kết quả từ .do() của vector search
article_uris = [URIRef(a["article_URI"]) for a in response["data"]["Get"]["Articles_with_abstracts_and_URIs"]]

# Xây dựng chuỗi VALUES cho SPARQL
article_uris_string = ", ".join(f"<{str(u)}>" for u in article_uris)

query = f"""
PREFIX schema: <http://schema.org/>
PREFIX ex: <http://example.org/>
SELECT ?article ?title ?abstract ?datePublished ?access ?meshTerm
WHERE {{
  VALUES ?article {{ {article_uris_string} }}
  ?article a ex:Article ;
           schema:name ?title ;
           schema:description ?abstract ;
           schema:datePublished ?datePublished ;
           ex:access ?access ;
           schema:about ?meshTerm .
  ?meshTerm a ex:MeSHTerm .
}}
"""

article_data = {}
for mesh_term in mesh_uris:                     # mesh_uris đã được chuẩn bị từ bước 4.4
    for row in g.query(query, initBindings={'meshTerm': mesh_term}):
        art = row['article']
        if art not in article_data:
            article_data[art] = {'title': row['title'],
                                 'abstract': row['abstract'],
                                 'datePublished': row['datePublished'],
                                 'access': row['access'],
                                 'meshTerms': set()}
        article_data[art]['meshTerms'].add(str(row['meshTerm']))

# Xếp hạng theo số khóa MeSH trùng khớp (giống như bước semantic search trên KG)
ranked = sorted(article_data.items(),
                key=lambda kv: len(kv[1]['meshTerms']),
                reverse=True)

# In ra kết quả sau khi lọc
for art_uri, data in ranked:
    print(f"Title: {data['title']}")
    print(f"Abstract: {data['abstract']}")
    print("MeSH Terms:")
    for mt in data['meshTerms']:
        print(f"  - {mt}")
    print()
```

Cuối cùng, ghép `title` + `abstract` của các bài đã lọc và gửi tới LLM để tóm tắt (cùng hàm `generate_summary` từ phần 4.3).

## 5. Tổng kết

- **Vector database** là lựa chọn nhanh chóng để triển khai truy vấn semantic và similarity trên văn bản không cấu trúc; tuy nhiên, kết quả có thể thiếu giải thích và có nguy cơ “context poisoning” khi được dùng trong RAG.  
- **Knowledge graph** cung cấp mô tả rõ ràng về mối quan hệ giữa các thực thể (thông qua ontology, narrower/broader) và cho phép lọc kết quả dựa trên metadata phong phú (ngày, cấp truy cập, chủ đề). Tuy nhiên, việc xây dựng KG và viết các truy vấn SPARQL có thể tốn thời gian và tài nguyên tính toán, đặc biệt khi tính similarity dựa trên các tập hợp thẻ (Jaccard).  
- **Phương pháp hybrid** – vector hóa dữ liệu cùng với trường URI và các thẻ MeSH, sau đó dùng KG để lọc/filter kết quả vector – mang lại cả **tốc độ** của vector search và **chính xác/giải thích** của KG. Điều này giúp giảm context poisoning, cho phép truy cập có điều kiện và tùy chỉnh kết quả dựa trên các thuộc tính bất kỳ (ngày, mức truy cập, v.v.).  
- Trong thực tiễn, một quy trình RAG thực tế thường sẽ:
  1. Thực hiện vector search để lấy một tập合候选 (top‑N) nhanh chóng.  
  2. Đánh giá các候选 bằng các ràng buộc SPARQL (thể loại, ngày, quyền truy cập, các khái niệm narrower) để loại bỏ kết quả không liên quan.  
  3. Gửi tập hợp bài báo đã qua lọc tới LLM để tạo câu trả lời cuối cùng.  

Những bước trên đã được minh họa cụ thể bằng code Python, Weaviate, RDFlib và OpenAI API trong nguồn bài viết, và bạn có thể sao chép và điều chỉnh chúng để áp dụng cho tập dữ liệu hoặc trường sử dụng của riêng mình. 

--- 

*Lưu ý: Đoạn mã trong bài học được sao chép nguyên từ nguồn để đảm bảo tính chính xác. Những giá trị placeholder như `"XXX"` trong URL hoặc khóa API cần được thay bằng thông tin thực tế của bạn trước khi chạy.*