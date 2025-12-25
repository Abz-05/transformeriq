#!/bin/bash
# deploy.sh - Automated Google Cloud Deployment
set -e

echo "☁️  TransformerIQ - Google Cloud Deployment"
echo "=========================================="
echo ""

if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI is not installed."
    echo "📥 Install from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

echo "✅ gcloud CLI found: $(gcloud --version | head -n 1)"
echo ""

read -p "Enter your Google Cloud Project ID (or press Enter to create new): " PROJECT_ID

if [ -z "$PROJECT_ID" ]; then
    PROJECT_ID="transformeriq-$(date +%s)"
    echo "📝 Creating new project: $PROJECT_ID"
    gcloud projects create $PROJECT_ID --name="TransformerIQ"
    
    echo "⚠️  Remember to enable billing for this project in Cloud Console!"
    echo "   https://console.cloud.google.com/billing"
    read -p "Press Enter after enabling billing..."
fi

gcloud config set project $PROJECT_ID

echo "🔧 Enabling required APIs..."
gcloud services enable cloudbuild.googleapis.com
gcloud services enable run.googleapis.com
gcloud services enable containerregistry.googleapis.com

echo ""
echo "🚀 Deploying to Cloud Run..."
gcloud run deploy transformeriq \
  --source . \
  --platform managed \
  --region us-central1 \
  --allow-unauthenticated \
  --memory 512Mi \
  --timeout 300

echo ""
echo "✅ Deployment successful!"
echo ""
