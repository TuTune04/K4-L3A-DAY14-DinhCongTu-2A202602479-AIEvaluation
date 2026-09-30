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
