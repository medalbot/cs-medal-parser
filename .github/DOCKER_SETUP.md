# Docker Hub Setup for GitHub Actions

This document explains how to set up Docker Hub integration for automated image building and publishing.

## Prerequisites

1. **Docker Hub Account**: Create an account at [hub.docker.com](https://hub.docker.com)
2. **Docker Hub Repository**: Create a repository named `cs-medal-parser`

## Setup Instructions

### 1. Create Docker Hub Access Token

1. Log in to Docker Hub
2. Go to **Account Settings** → **Personal access tokens**
3. Click **New Access Token**
4. Name: `GitHub Actions cs-medal-parser`
5. Permissions: **Read, Write, Delete**
6. Copy the generated token (you won't see it again!)

### 2. Configure GitHub Repository Secrets

Go to your GitHub repository → **Settings** → **Secrets and variables** → **Actions**

Add the following **Repository secrets**:

| Secret Name          | Value                        | Description             |
| -------------------- | ---------------------------- | ----------------------- |
| `DOCKERHUB_USERNAME` | Your DockerHub username      | Used for authentication |
| `DOCKERHUB_TOKEN`    | The access token from step 1 | Used for authentication |

### 3. Workflow Behavior

The workflow will automatically:

- **On any push**: Build and push with appropriate tags
- **On pull requests to main**: Build only (no push) for testing
- **Branch-based tagging**: Each branch gets its own tag (e.g., `main`, `develop`, `feature-xyz`)
- **Latest tag**: Only applied to pushes from the default branch (main)

### 4. Multi-Platform Builds

The workflow builds for:

- `linux/amd64` (Intel/AMD x64)
- `linux/arm64` (ARM64/Apple Silicon)

### 5. Image Tags

Examples of generated tags:

- `username/cs-medal-parser:latest` (from main branch only)
- `username/cs-medal-parser:main` (from main branch)
- `username/cs-medal-parser:develop` (from develop branch)
- `username/cs-medal-parser:feature-auth` (from feature-auth branch)
- `username/cs-medal-parser:bugfix-123` (from bugfix-123 branch)

## Usage

Once set up, users can pull your optimized image:

```bash
# Pull latest version
docker pull username/cs-medal-parser:latest

# Pull specific version
docker pull username/cs-medal-parser:1.0.0

# Run the container
docker run --rm -v $(pwd)/data:/app/data username/cs-medal-parser:latest
```

## Troubleshooting

### Build Fails with Authentication Error

- Verify `DOCKERHUB_USERNAME` and `DOCKERHUB_TOKEN` secrets are set correctly
- Ensure the Docker Hub access token has Read/Write permissions
- Check that the repository exists on Docker Hub

### Multi-platform Build Issues

- The workflow uses Docker Buildx for cross-platform builds
- If builds fail, check the GitHub Actions logs for platform-specific errors

### Cache Issues

- The workflow uses GitHub Actions cache for faster builds
- If builds behave unexpectedly, the cache can be cleared from the Actions tab

## Security Notes

- Never commit Docker Hub credentials to the repository
- Use access tokens instead of passwords
- Regularly rotate access tokens
- Limit token permissions to what's needed (Read/Write for this use case)
