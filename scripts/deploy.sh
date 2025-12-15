#!/bin/bash
set -e

# ==============================================================================
# Akshara Local Deployment Script
# ==============================================================================
# Use this for manual deployments from your local machine.
# For production, use GitHub Actions or CF's git integration.
# ==============================================================================

echo "==> Akshara Deployment"
echo ""

# Build the site
echo "==> Running build..."
./scripts/build.sh

# Deploy to Cloudflare Workers
echo ""
echo "==> Deploying to Cloudflare Workers..."

# Check if deploying to production
if [[ "$1" == "--production" ]] || [[ "$1" == "-p" ]]; then
  echo "    Environment: PRODUCTION"
  wrangler deploy --env production
else
  echo "    Environment: preview (use --production for prod)"
  wrangler deploy
fi

echo ""
echo "==> Deployment complete!"
