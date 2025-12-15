#!/bin/bash
set -e

# ==============================================================================
# Akshara Build Script for Cloudflare Workers
# ==============================================================================
# This script installs Hugo and builds the site in the CF Workers environment.
# CF Workers build image doesn't guarantee Hugo version, so we install it ourselves.
# ==============================================================================

# Configuration - Update these versions as needed
HUGO_VERSION="0.139.3"
NODE_VERSION="20"

echo "==> Starting Akshara build..."
echo "    Hugo version: ${HUGO_VERSION}"

# Function to check if running in Cloudflare Workers build environment
is_cf_build() {
  [[ -n "${CF_PAGES:-}" ]] || [[ -n "${CF_WORKERS:-}" ]] || [[ -d "/opt/buildhome" ]]
}

# Install Hugo if not present or if in CF build environment
install_hugo() {
  # Check if hugo exists and is correct version
  if command -v hugo &> /dev/null; then
    local current_version=$(hugo version | grep -oP 'v\K[0-9]+\.[0-9]+\.[0-9]+' | head -1)
    if [[ "$current_version" == "$HUGO_VERSION" ]]; then
      echo "==> Hugo ${HUGO_VERSION} already installed"
      return 0
    fi
  fi

  echo "==> Installing Hugo ${HUGO_VERSION} (extended)..."

  # Determine architecture
  local arch="64bit"
  if [[ "$(uname -m)" == "aarch64" ]] || [[ "$(uname -m)" == "arm64" ]]; then
    arch="arm64"
  fi

  # Download and extract Hugo extended edition
  local hugo_url="https://github.com/gohugoio/hugo/releases/download/v${HUGO_VERSION}/hugo_extended_${HUGO_VERSION}_linux-${arch}.tar.gz"

  echo "    Downloading from: ${hugo_url}"

  # Create temp directory and download
  local temp_dir=$(mktemp -d)
  curl -sL "${hugo_url}" -o "${temp_dir}/hugo.tar.gz"

  # Extract to /usr/local/bin or local bin
  if [[ -w "/usr/local/bin" ]]; then
    tar -xzf "${temp_dir}/hugo.tar.gz" -C /usr/local/bin hugo
  else
    mkdir -p "${HOME}/.local/bin"
    tar -xzf "${temp_dir}/hugo.tar.gz" -C "${HOME}/.local/bin" hugo
    export PATH="${HOME}/.local/bin:${PATH}"
  fi

  # Cleanup
  rm -rf "${temp_dir}"

  echo "==> Hugo installed: $(hugo version)"
}

# Install Node dependencies
install_deps() {
  if [[ -f "package.json" ]]; then
    echo "==> Installing Node dependencies..."
    npm ci --prefer-offline 2>/dev/null || npm install
  fi
}

# Build Hugo site
build_site() {
  echo "==> Building Hugo site..."
  hugo --gc --minify
  echo "    Generated $(find public -name '*.html' | wc -l) HTML files"
}

# Build search index with Pagefind
build_search() {
  echo "==> Building search index with Pagefind..."
  npx pagefind --site public --output-path public/pagefind
}

# Main build process
main() {
  # Install Hugo (in CF environment or if not present)
  if is_cf_build || ! command -v hugo &> /dev/null; then
    install_hugo
  fi

  # Install dependencies
  install_deps

  # Build the site
  build_site

  # Build search index
  build_search

  echo ""
  echo "==> Build complete!"
  echo "    Output: ./public"
  echo "    Size: $(du -sh public | cut -f1)"
}

# Run main
main
