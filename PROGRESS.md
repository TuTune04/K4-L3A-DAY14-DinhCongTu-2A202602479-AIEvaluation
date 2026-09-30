# Progress Log

## Task 3: LLMJudge — `score_response` and `detect_bias`
- Implemented LLMJudge initialization and a single-call rubric prompt that scores answer content rather than length.
- Added JSON parsing with embedded-object fallback, score normalization and clamping, and neutral defaults for invalid values.
- Implemented leniency, severity, and positional bias detection from numeric scores.
- Copied template.py to solution/solution.py and verified that they match.
- Validation: all 4 LLMJudge tests and additional edge checks passed; the required full suite finished with 21 passed and 21 skipped for pending tasks.

## Task 4: BenchmarkRunner — `run`, `generate_report`, `run_regression`, `identify_failures`
- Implemented BenchmarkRunner.run with retrieval context forwarding and original QA pair preservation.
- Added aggregate reports with pass rates, answer metric averages, optional retrieval averages, and failure counts.
- Implemented typed regression comparisons and threshold-based failure identification.
- Copied template.py to solution/solution.py.
- Validation: 12 Task 4 acceptance tests passed; required full suite passed with 32 passed and 10 pending skips.

## Task 5: FailureAnalyzer — categorize, root cause, suggestions, improvement log
- Implemented FailureAnalyzer category counts and exact score-based root cause messages.
- Added frequency-ordered, case-insensitive OrbitTech improvement suggestions with generic fallback actions.
- Added Markdown improvement logs with metadata IDs, escaped pipes, suggestion fallback, and Open status.
- Copied template.py to solution/solution.py and verified the demo runs successfully.
- Required pytest command passed: 41 passed, 1 skipped.

## Task 6: Golden dataset — 20 QA with verbatim evidence
- Filled all 20 golden QA records in English while preserving metadata and record order.
- Added short verbatim evidence excerpts covering all 10 corpus documents.
- Covered policy exceptions and three adversarial cases with scope evidence.
- Added dataset tests for validation, record count, difficulty distribution, and full document coverage.
- Dataset validation prints PASS; the required pytest command reports 42 passed and 1 skipped.

## Task 7: Generate actual answers (real RAG run) and the benchmark artifact
- Added a deterministic ExtractiveGenerator that ranks retrieved sentences by question token overlap and provides an evidence fallback.
- Added offline generation tests covering extraction order, missing context, absent overlap, and all 20 dataset questions.
- Kept offline CLI output separate at artifacts/actual_answers_offline.json to preserve real submitted answers.
- Ran the real domain assistant with gpt-4o-mini and saved 20 answers without errors, plus benchmark JSON and Markdown artifacts.
- Verified artifact acceptance checks and both pytest commands: 46 passed, 1 skipped; no .env appears in git status.

## Task 8: `exercises.md` Part 1 and Exercise 3.1
- Completed Exercises 1.1–1.3 with OrbitTech metric scenarios, judge bias experiments, human calibration, and proposed deployment thresholds.
- Filled Exercise 3.1 with validated dataset counts, source coverage, and the PASS result.
- Documented representative H03, M01, and A02 cases, evidence challenges, and all three confirmations.
- Verified the requested sections contain no placeholders or empty answers; left other worksheet sections unchanged.
- Required pytest command and plain pytest both passed: 46 passed, 1 skipped.

## Task 9: `exercises.md` Exercise 3.2 (benchmark) and Exercise 3.3 (judge rubric)
- Filled Exercise 3.2 with all 20 benchmark rows, artifact-derived averages, failure counts, and the three lowest-scoring cases.
- Identified gpt-4o-mini as the generator and diagnosed retrieval versus generation issues, including overlap-metric limits for refusals.
- Completed Exercise 3.3 with four dimensions, concrete OrbitTech scoring levels and examples, three edge cases, and bias controls.
- Verified all benchmark row scores against benchmark_results.json; required pytest command passed with 46 passed and 1 skipped.

## Task 10: `reflection.md` — summary, 5 Whys, clustering, improvement log, regression strategy
- Completed all seven reflection sections using the recorded benchmark and answer traces.
- Calculated metric summaries, score buckets, and failure distributions from artifacts.
- Analyzed A02, A01, and M02 with verbatim answers, evidence comparisons, and five-level root causes.
- Preserved the improvement log verbatim and documented prioritized fixes, regression gates, and monitoring.
- Verified report placeholders and artifact quotations; both pytest commands passed with 46 passed and 1 skipped.

## Task 11: Bonus Exercise 3.5 — reranking experiment
- Implemented stable question-token overlap reranking and copied template.py to solution/solution.py.
- Added a pure reranking comparison function and a script that joins saved cases by ID, writes JSON results, and prints a Markdown table with averages.
- Generated artifacts/rerank_results.json for all 20 cases; average precision increased from 0.963 to 0.984 while recall stayed unchanged.
- Filled only Exercise 3.5 with artifact-derived scores and explanations of recall invariance and retrieval limitations.
- Added tests for chunk preservation, stable ties, question-only ranking, precision improvement, and recall invariance; both required and plain pytest runs passed all 53 tests with no skips.

## Task 12: Bonus Exercise 3.4 — framework comparison
- Implemented offline RAGAS-style continuous metrics and DeepEval-style normal/strict assertions over identical saved inputs.
- Generated per-case scores, pass flags, means, pass rates, failure IDs, agreement rates, and lab-core references for all 20 records.
- Filled only Exercise 3.4 with artifact-backed results, framework setup details, sources, and explicit offline-proxy limitations.
- Added tests for sentence support, threshold boundaries, strict rounding, empty inputs, and artifact reproducibility.
- Verified both plain pytest and the required pending_ok command: 60 tests passed.

## Task 13: Final consistency checks and deliverables test
- Added deliverables tests for completed code, matching solution files, filled worksheets, an untracked .env, and 20 benchmark results.
- Synced template.py to solution/solution.py and confirmed identical contents.
- Removed the remaining worksheet placeholder and checked every completion item, including Exercises 3.4 and 3.5.
- Validated the golden dataset and reproduced the benchmark artifact without changing its scores.
- Both plain pytest and the required pending_ok command passed: 68 passed, 0 skipped; removed generated caches.
