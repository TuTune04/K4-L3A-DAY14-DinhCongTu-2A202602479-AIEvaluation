# Day 14 — Exercises

## AI Evaluation & Benchmarking · Lab Worksheet

**Thời gian làm bài:** 14:15–17:00

**Domain:** OrbitTech Store Customer Support

Điền trực tiếp câu trả lời vào file này. Golden dataset 20 QA được viết một lần
duy nhất trong `golden_dataset.json`, không chép lại toàn bộ vào Markdown.

---

Từ 14:15–14:30, cài môi trường và chạy baseline tests theo `guide_lab.md`.

---

## Part 1 — Warm-up (14:30–14:45)

### Exercise 1.1 — RAGAS Metric Thresholds

Theo bài giảng:

- 0.8–1.0: Good — monitor, maintain.
- 0.6–0.8: Needs work — analyze failures, iterate.
- Dưới 0.6: Significant issues — investigate.

Với từng metric, xác định khi nào score thấp có thể chấp nhận và khi nào là
critical.

| Metric | Acceptable Low Score Scenario | Critical Low Score Scenario | Action Required |
|---|---|---|---|
| Faithfulness | Lời chào hoặc lời đề nghị hỗ trợ OrbitTech không xuất hiện nguyên văn trong context có thể bị metric overlap chấm thấp, nếu không thêm claim về chính sách. | Bịa mức hoàn tiền, phí trả hàng hoặc thời hạn bảo hành khiến khách nhận thông tin sai. | Kiểm tra từng claim với evidence; sửa hoặc bỏ claim không được hỗ trợ, chuyển support khi thiếu căn cứ. |
| Answer Relevance | Từ chối yêu cầu tư vấn đầu tư ngoài phạm vi OrbitTech có thể ít trùng từ với câu hỏi nhưng đúng vai trò. | Khách hỏi cách xử lý pin phồng mà câu trả lời chỉ giới thiệu sản phẩm. | Chấm refusal theo scope; với câu hỏi hợp lệ, trả lời trực tiếp nhu cầu và ưu tiên hướng dẫn an toàn. |
| Context Recall | A01 chỉ cần policy về scope để từ chối; thiếu context về các sản phẩm được nhắc như ví dụ không làm thay đổi quyết định. | H03 thiếu policy phiên bản cũ, dẫn đến áp dụng sai cửa sổ trả hàng cho đơn trước ngày hiệu lực. | Kiểm tra recall theo từng claim cần thiết; bổ sung truy xuất policy phiên bản và ngày kích hoạt. |
| Context Precision | Khi hỏi bảo hành NovaBook, một context về quy trình sửa chữa đi kèm có thể hữu ích cho bước tiếp theo dù không chứa đáp án trực tiếp. | Context khuyến mãi hoặc policy trả hàng cũ lấn át evidence đúng khi khách hỏi quyền trả hàng hiện tại. | Kiểm tra context hữu ích, lọc tài liệu không liên quan và ưu tiên policy đúng phiên bản. |
| Completeness | Refusal ngoài scope có thể ngắn hơn expected answer và bỏ vài ví dụ chủ đề hỗ trợ, miễn nêu đúng giới hạn và hướng hỗ trợ. | H05 bỏ hướng dẫn ngừng sạc pin phồng, hoặc M01 bỏ khoản khấu trừ khi giữ quà tặng. | Dùng checklist các claim bắt buộc; ưu tiên an toàn và điều kiện tài chính, cho phép rút gọn ví dụ không thiết yếu. |

### Exercise 1.2 — Bias trong LLM-as-a-Judge

Ba bias thường gặp:

- Position bias: judge ưu tiên answer xuất hiện trước.
- Verbosity bias: judge ưu tiên answer dài hơn.
- Self-preference: judge ưu tiên output giống chính model đó.

**Câu 1: Thiết kế experiment phát hiện position bias với ít nhất hai conditions.**

> *Câu trả lời:* Với cùng câu hỏi OrbitTech và cùng cặp đáp án A/B, condition thứ nhất đặt A trước B, condition thứ hai đặt B trước A. Giữ nguyên rubric, model và cấu hình; ẩn nguồn model, xáo trộn thứ tự các lần thử và lặp lại trên nhiều cặp có human labels. Ánh xạ lựa chọn về danh tính A/B trước khi tính agreement rate: số cặp có cùng lựa chọn (kể cả hòa) sau swap chia tổng số cặp. Đồng thời đo tỷ lệ chọn vị trí đầu ở mỗi condition và tỷ lệ đổi người thắng theo vị trí. Agreement thấp cùng thiên hướng chọn đáp án đầu là dấu hiệu position bias; so sánh thêm với biến động khi lặp lại cùng thứ tự để phân biệt nhiễu ngẫu nhiên.

**Câu 2: Làm thế nào giảm verbosity bias bằng rubric design?**

> *Câu trả lời:* Rubric chấm tính đúng, evidence, mức đáp ứng các ý bắt buộc và bước hành động cho khách OrbitTech; không cộng điểm vì số từ, số bullet hoặc lặp lại policy. Một đáp án ngắn nhưng đủ điều kiện trả hàng phải được chấm ngang đáp án dài có cùng nội dung đúng. Chỉ trừ điểm khi dài dòng che khuất hướng dẫn, thêm claim sai hoặc thiếu ý bắt buộc; dùng cặp ví dụ ngắn/dài có chất lượng tương đương để calibrate judge.

**Câu 3: Tại sao cần calibrate LLM judge với human labels?**

> *Câu trả lời:* Judge có thể chấm cao câu trả lời trôi chảy nhưng sai policy hoặc không nhận ra refusal đúng. Hai người chấm độc lập một mẫu có đủ mức difficulty, lỗi bảo hành/hoàn tiền và attack type; thống nhất rubric và giải quyết bất đồng để tạo labels tham chiếu. Đo agreement và Cohen's kappa giữa judge với labels cho quyết định pass/fail (weighted kappa nếu dùng thang điểm thứ bậc), đồng thời xem các lỗi judge cho qua. Sửa rubric và ví dụ dựa trên bất đồng rồi kiểm chứng trên mẫu giữ lại; human calibration giúp ngưỡng chấm phản ánh chất lượng thực tế thay vì thiên kiến của model.

### Exercise 1.3 — Evaluation trong CI/CD

**Câu 1: Chọn threshold để block deployment.**

| Metric | Threshold | Lý do |
|---|---:|---|
| Faithfulness | Đề xuất tối thiểu 0.90 | Claim sai về hoàn tiền, bảo hành hoặc an toàn có tác động lớn; block nếu thấp hơn ngưỡng hoặc có claim quan trọng không được evidence hỗ trợ. |
| Answer Relevance | Đề xuất tối thiểu 0.80 | Câu trả lời phải giải quyết nhu cầu hỗ trợ OrbitTech; đánh giá refusal theo scope để tránh phạt việc từ chối hợp lệ. |
| Completeness | Đề xuất tối thiểu 0.80 | Phải đủ điều kiện áp dụng và bước xử lý; block riêng khi thiếu hướng dẫn an toàn hoặc điều kiện tài chính quan trọng. |

Các ngưỡng trên là lựa chọn thiết kế cho CI/CD, không phải điểm benchmark đã đo. Áp dụng trên từng case sau khi review ngoại lệ hợp lệ, không chỉ dựa vào trung bình; calibrate bằng human labels trước khi dùng làm release gate.

**Câu 2: Khi nào dùng offline evaluation, online evaluation và human review?**

> *Câu trả lời:* Offline evaluation chạy golden dataset OrbitTech trước mỗi thay đổi retriever, prompt hoặc model để phát hiện regression và block deployment theo ngưỡng đã calibrate. Online evaluation theo dõi câu hỏi thực tế, phản hồi khách, tỷ lệ chuyển support và lỗi mới sau triển khai, dùng dữ liệu đã loại thông tin nhạy cảm; kết quả giúp bổ sung case vào bộ offline. Human review xử lý bất đồng giữa metrics và judge, refusal, policy theo phiên bản, lỗi an toàn/riêng tư và claim tài chính; đồng thời kiểm tra mẫu định kỳ để phát hiện judge drift.

---

## Part 2 — Core Coding (14:45–15:40)

Hoàn thiện các TODO bắt buộc trong `template.py`.

### Task 1 — Data Models

- `QAPair`: question, expected answer, gold context, metadata và retrieved contexts.
- `EvalResult`: answer-side scores, optional retrieval scores, pass/failure fields.
- `overall_score()`: trung bình Faithfulness, Relevance và Completeness.

### Task 2 — RAGASEvaluator

Answer-side:

- `evaluate_faithfulness(answer, context)`
- `evaluate_relevance(answer, question)`
- `evaluate_completeness(answer, expected)`

Retrieval-side:

- `evaluate_context_recall(contexts, expected)`
- `evaluate_context_precision(contexts, expected)`

Full pipeline:

- `run_full_eval(..., contexts=None)` luôn tính ba answer metrics.
- Nếu có `contexts`, tính và lưu thêm Context Recall và Context Precision.
- Retrieval scores không làm thay đổi `overall_score()` và pass rule gốc.

### Task 3 — LLMJudge

- `score_response(question, answer, rubric)`
- `detect_bias(scores_batch)`

### Task 4 — BenchmarkRunner

- `run(qa_pairs, agent_fn, evaluator)`
- `generate_report(results)`
- `run_regression(new_results, baseline_results)`
- `identify_failures(results, threshold)`

`BenchmarkRunner.run()` phải truyền `pair.retrieved_contexts` vào
`run_full_eval()`. Report phải có average của hai retrieval metrics.

### Task 5 — FailureAnalyzer

- `categorize_failures(failures)`
- `find_root_cause(failure)`
- `generate_improvement_suggestions(failures)`
- `generate_improvement_log(failures, suggestions)`

Kiểm tra:

```bash
pytest tests/ -v
```

`rerank_by_overlap()` là TODO bonus của Exercise 3.5. Test tương ứng được skip
nếu bạn chưa làm bonus.

---

## Part 3 — Golden Dataset & Real Benchmark (15:40–16:35)

### Exercise 3.1 — Build the Golden Dataset

Thiết kế và validate dataset theo Mục 5–6 trong `guide_lab.md`. Nội dung 20 QA
được điền trực tiếp trong `golden_dataset.json`; phần dưới chỉ ghi lại kết quả
và quyết định thiết kế, không chép lại toàn bộ QA.

**Kết quả dataset**

| Hạng mục | Kết quả |
|---|---|
| Tổng số records | 20 / 20 |
| Easy | 5 / 5 |
| Medium | 7 / 7 |
| Hard | 5 / 5 |
| Adversarial | 3 / 3 |
| Source documents được sử dụng | 10 / 10 |
| Validator status | PASS |

**Ba case đại diện cho quyết định thiết kế**

| ID | Difficulty | Source document(s) | Vì sao case phù hợp với difficulty/attack type? |
|---|---|---|---|
| H03 | Hard | `09_escalation_and_policy_updates.md`, `03_promotions_and_membership.md` | Kết hợp phiên bản policy theo ngày đặt hàng với quyền lợi OrbitPlus: đơn trước ngày hiệu lực giữ cửa sổ cũ; đơn sau ngày hiệu lực có quyền lợi cho thiết bị chưa mở, nhưng membership không kéo dài cửa sổ thiết bị đã mở. |
| M01 | Medium | `05_returns_and_exchanges.md`, `03_promotions_and_membership.md` | Kết hợp điều kiện trả thiết bị chưa mở với quy tắc bundle: còn trong cửa sổ trả hàng nhưng giữ quà tặng thì bị khấu trừ giá trị khuyến mãi. |
| A02 | Adversarial | `00_system_scope.md`, `08_accounts_privacy_and_security.md` | Prompt injection yêu cầu bỏ rules, tiết lộ hidden prompt và dữ liệu hàng xóm, đồng thời yêu cầu password/code; đáp án phải từ chối và nhắc điều kiện xác minh quyền truy cập. |

**Điểm khó nhất khi xây dựng expected answer hoặc evidence là gì?**

> *Câu trả lời:* Khó nhất là tách ngày chọn phiên bản policy (ngày đặt hàng) khỏi ngày bắt đầu tính cửa sổ trả hàng (ngày xác nhận giao), rồi kết hợp đúng ngoại lệ OrbitPlus mà không suy diễn thêm quyền lợi. H03 cần evidence từ cả policy updates và membership; M01 cần cả điều kiện trả hàng và khấu trừ quà tặng. Evidence phải giữ nguyên văn corpus và hỗ trợ từng claim trong expected answer. Validator đã xác nhận cấu trúc và provenance hợp lệ; việc đọc đối chiếu từng case vẫn cần thiết để kiểm tra ngữ nghĩa, difficulty và câu hỏi trùng ý.

**Xác nhận:**

- [x] Mọi claim trong expected answer đều có evidence hỗ trợ.
- [x] Không có questions trùng ý và không dùng kiến thức ngoài corpus.
- [x] `python validate_golden_dataset.py` báo `PASS`.

### Exercise 3.2 — Benchmark Run

Chạy:

```bash
python domain_assistant.py
python evaluate_answers.py
```

Copy bảng terminal vào đây hoặc điền từ `artifacts/benchmark_results.json`.

| ID | Question (short) | Ctx Recall | Ctx Precision | Faithfulness | Relevance | Completeness | Overall | Passed? | Failure Type |
|---|---|---:|---:|---:|---:|---:|---:|---|---|
| E01 | | | | | | | | | |
| E02 | | | | | | | | | |
| E03 | | | | | | | | | |
| E04 | | | | | | | | | |
| E05 | | | | | | | | | |
| M01 | | | | | | | | | |
| M02 | | | | | | | | | |
| M03 | | | | | | | | | |
| M04 | | | | | | | | | |
| M05 | | | | | | | | | |
| M06 | | | | | | | | | |
| M07 | | | | | | | | | |
| H01 | | | | | | | | | |
| H02 | | | | | | | | | |
| H03 | | | | | | | | | |
| H04 | | | | | | | | | |
| H05 | | | | | | | | | |
| A01 | | | | | | | | | |
| A02 | | | | | | | | | |
| A03 | | | | | | | | | |

**Aggregate Report**

- Overall pass rate: ____%
- Avg Context Recall: ____
- Avg Context Precision: ____
- Avg Faithfulness: ____
- Avg Relevance: ____
- Avg Completeness: ____
- Failure type distribution: ____

**Ba cases có Overall Score thấp nhất**

1. ID: ____ | Score: ____ | Failure type: ____
2. ID: ____ | Score: ____ | Failure type: ____
3. ID: ____ | Score: ____ | Failure type: ____

**Nhận xét ngắn:** Metric nào yếu nhất? Kết quả gợi ý vấn đề nằm ở retrieval
hay generation?

> *Câu trả lời:*

### Exercise 3.3 — LLM-as-a-Judge Rubric Design

Thiết kế rubric domain-specific cho OrbitTech Customer Support. Mỗi mức phải
đủ cụ thể để hai người chấm độc lập có thể hiểu giống nhau.

Chọn 3–5 dimensions:

- [ ] Correctness
- [ ] Completeness
- [ ] Relevance
- [ ] Evidence/citation
- [ ] Actionability
- [ ] Safety/privacy
- [ ] Tone/clarity
- [ ] Dimension khác: __________

| Score | Tiêu chí domain-specific | Ví dụ response |
|---:|---|---|
| 5 | | |
| 4 | | |
| 3 | | |
| 2 | | |
| 1 | | |

**Ba edge cases khó chấm**

| Edge Case | Tại sao khó chấm? | Rubric xử lý thế nào? |
|---|---|---|
| | | |
| | | |
| | | |

**Bias controls:** Rubric hoặc evaluation protocol của bạn giảm position bias,
verbosity bias và self-preference bằng cách nào?

> *Câu trả lời:*

### Exercise 3.4 — Framework Comparison (Bonus +5)

Chỉ làm sau khi hoàn thành 3.1–3.3. Chọn hai framework trong RAGAS, DeepEval
và TruLens; chạy hoặc thiết kế một so sánh có cùng input dataset.

| Tiêu chí | Framework 1: ____ | Framework 2: ____ |
|---|---|---|
| Setup complexity | | |
| Metrics available | | |
| CI/CD integration | | |
| Kết quả trên cùng dataset | | |
| Insight rút ra | | |

- Scores có nhất quán không?
- Framework nào strict hơn và vì sao?
- Hai framework có tìm ra cùng failure cases không?

> *Phân tích:*

### Exercise 3.5 — Retrieval Reranking (Bonus +5)

Mục tiêu: kiểm tra việc đổi thứ tự chunks có tăng Context Precision mà không
thay đổi Context Recall hay không.

1. Chọn ít nhất 5 cases từ `artifacts/actual_answers.json`.
2. Tính Context Recall và Context Precision trước rerank.
3. Implement `rerank_by_overlap()` hoặc một reranker khác.
4. Rerank cùng tập chunks, không thêm hoặc xóa chunk.
5. Tính lại hai metrics và giải thích kết quả.

| ID | Recall before | Recall after | Precision before | Precision after | Delta Precision |
|---|---:|---:|---:|---:|---:|
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| | | | | | |
| **Avg** | | | | | |

**Tại sao Recall dự kiến không đổi?**

> *Câu trả lời:*

**Khi nào reranking không đủ và cần sửa retriever/query/chunking?**

> *Câu trả lời:*

---

## Part 4 — Reflection (16:35–16:50)

Hoàn thành `reflection.md` bằng kết quả thật từ Exercise 3.2.

---

## Completion Checklist

Hoàn thành kiểm tra cuối trong khoảng 16:50–17:00.

- [ ] Tất cả required tests pass.
- [ ] `golden_dataset.json` validate thành công.
- [ ] Exercise 3.1 hoàn thành trong file JSON và bảng kết quả phía trên.
- [ ] Exercise 3.2 có năm metrics, aggregate report và ba cases thấp nhất.
- [ ] Exercise 3.3 có rubric 1–5 và bias controls.
- [ ] `reflection.md` có ba failure analyses và regression strategy.
- [ ] Đã copy `template.py` thành `solution/solution.py`.
- [ ] Exercise 3.4 và 3.5 chỉ làm nếu chọn bonus.
