<!-- ---
title: Zeno Evals Hub
emoji: 🏃
colorFrom: pink
colorTo: indigo
sdk: docker
pinned: false
license: mit
fullWidth: true
--- -->

# Zeno + OpenAI Evals

OpenAI's [Evals library](https://github.com/openai/evals) is a great resource providing evaluation sets for LLMS.

This repo provides a hub for exploring these results using the [Zeno](https://zenoml.com) evaluation tool.

## Add New Evals

To add new evals, add a new entry to `evals/evals.yaml` with the following fields:

- `results-file`: The first `.jsonl` result from `oaievals`
- `link`: A link to the evals commit for this evaluation
- `description`: A succint description of what the evaluation is testing
- `second-results-file`: An optional second `.jsonl` result from `oaievals`. Must be the same dataset as the first one.
- `functions-file`: An optional Python file with [Zeno functions](https://zenoml.com/docs/api) for the evaluations.

Make sure you test your evals locally before submitting a PR!

### Running

`poetry install`

`python -m zeno-evals-hub evals/evals.yaml`
