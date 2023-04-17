all: lint typecheck clean

.PHONY: install
install:
	@echo "==> 📦 Installing"
	@cd frontend && npm i && npm run build
	@poetry install

.PHONY: lint
lint:
	@echo "==> 👕 Linting"
	@poetry check
	@poetry run black zeno-evals-hub/
	@poetry run usort format zeno-evals-hub/
	@poetry run flake8 zeno-evals-hub --statistics
	@cd frontend && npm run lint

.PHONY: typecheck
typecheck:
	@echo "==> ✅ Type checks"
	@poetry run mypy -p zeno-evals-hub 
	@poetry run pyright zeno-evals-hub 
	@cd frontend && npm run check

.PHONY: build
build:
	@echo "==> 👷‍♀️ Build"
	@cd frontend && npm run build
	@cd frontend && node build.js
	@mv zeno-evals-hub/frontend/index.html zeno-evals-hub/frontend/index_og.html
	@mv zeno-evals-hub/frontend/index_tmp.html zeno-evals-hub/frontend/index.html
	@poetry build -v
	@rm zeno-evals-hub/frontend/index.html
	@mv zeno-evals-hub/frontend/index_og.html zeno-evals-hub/frontend/index.html

.PHONY: clean
clean:
	@rm -rf dist
	@rm -rf ./.zeno-evals-hub_cache
	@find . -type d -name '.mypy_cache' -exec rm -rf {} +
	@find . -type d -name '__pycache__' -exec rm -rf {} +
	@find . -type d -name '*pytest_cache*' -exec rm -rf {} +
	@find . -type f -name "*.py[co]" -exec rm -rf {} +
	@find . -type d -name '*.ipynb_checkpoints' -exec rm -r {} +

.PHONY: publish
publish:
	@echo "==> 🚀 Publishing"
	@git commit -am "chore: bump version to $(shell poetry version -s)"
	@git tag "v$(shell poetry version -s)"
	@make build
	@poetry publish
	@git push && git push --tags