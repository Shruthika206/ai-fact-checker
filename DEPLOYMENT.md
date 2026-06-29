# AI Fact Checker - Azure Deployment Guide

## Prerequisites
- Azure CLI installed
- Docker installed (for local testing)
- Python 3.11+

## Deployment Options

### Option 1: Azure Container Registry + App Service (Recommended)

1. **Build and push Docker image:**
   ```bash
   az acr build --registry <registry-name> --image aifactchecker:latest .
   ```

2. **Deploy to App Service:**
   ```bash
   az webapp create --resource-group <rg-name> --plan <app-plan> --name <app-name> --deployment-container-image-name <registry-name>.azurecr.io/aifactchecker:latest
   ```

3. **Configure environment variables:**
   ```bash
   az webapp config appsettings set --name <app-name> --resource-group <rg-name> \
     --settings FOUNDRY_PROJECT_ENDPOINT="<your-endpoint>" \
     FOUNDRY_MODEL="<your-model>"
   ```

### Option 2: Direct Deployment (Python)

1. **Deploy from local:**
   ```bash
   az webapp deployment source config-zip --name <app-name> --resource-group <rg-name> --src deploy.zip
   ```

2. **Set startup command in Azure Portal:**
   - App Service > Settings > Startup command: `streamlit run AgentWeb.py --server.port=8000 --server.address=0.0.0.0`

## Environment Variables Required
- `FOUNDRY_PROJECT_ENDPOINT` - Your Azure Foundry project endpoint
- `FOUNDRY_MODEL` - Model deployment name

## Troubleshooting

If container timeout occurs:
- Increase container timeout in App Service settings
- Pre-warm dependencies in Dockerfile
- Use Azure Container Registry for faster deployments
