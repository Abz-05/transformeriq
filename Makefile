.PHONY: install run deploy test clean

install:
	@echo "📦 Installing dependencies..."
	pip install -r requirements.txt

run:
	@echo "🚀 Starting local server..."
	python app.py

deploy:
	@echo "☁️  Deploying to Google Cloud Run..."       
	gcloud run deploy transformeriq --source . --region us-central1 --allow-unauthenticated

test:
	@echo "🧪 Running tests..."
	pytest tests/

clean:
	@echo "🧹 Cleaning up..."
	rm -rf __pycache__ venv .pytest_cache
	find . -type f -name "*.pyc" -delete

screenshots:
	@echo "📸 Capturing screenshots..."
	python generate_screenshots.py
