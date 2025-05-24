CODE_FILES := assets bin blackmarblepy docs notebooks src static web .dockerignore .editorconfig .gitattributes \
    .gitignore .gitmodules CONTRIBUTING.md docker-compose.prod.yaml docker-compose.yaml Dockerfile Dockerfile.prod \
    environment.yaml Makefile pyproject.toml README.md requirements.dev.txt requirements.txt

TARGETS := FS25_P1-code-readme.zip

.PHONY: all
all: $(TARGETS)

FS25_P1-code-readme.zip: $(CODE_FILES)
	zip FS25_P1-code-readme.zip $(CODE_FILES)
