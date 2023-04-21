---
title: Zeno Evals Hub
emoji: 🏃
colorFrom: pink
colorTo: indigo
sdk: docker
pinned: false
license: mit
fullWidth: true
---

# Dashboard for exploring OpenAI Evals results

### Running

`poetry install`

`python -m zeno-evals-hub evals/evals.yaml`

### Deployment

We are using [Railway]() for deployment. To deploy, run:

1. `railway login`
2. `railway link`
3. `railway up`
