CODE_FILES := assets bin blackmarblepy docs notebooks src static web .dockerignore .editorconfig .gitattributes \
    .gitignore .gitmodules CONTRIBUTING.md docker-compose.prod.yaml docker-compose.yaml Dockerfile Dockerfile.prod \
    environment.yaml Makefile pyproject.toml README.md requirements.dev.txt requirements.txt

REPORT_FILES := assets/teaser_image.png assets/poster.pdf assets/report.pdf

TARGETS := FS25_P1-code-readme.zip FS25_P1-teaser-poster-report.zip

.PHONY: all
all: $(TARGETS)

FS25_P1-code-readme.zip: $(CODE_FILES)
	zip -r $@ $(CODE_FILES) -x "*/__pycache__/*" "*/.next/*" "*/node_modules/*" "*/.env" "*/.env.*"

FS25_P1-teaser-poster-report.zip: $(REPORT_FILES)
	zip -rj $@ $(REPORT_FILES)
