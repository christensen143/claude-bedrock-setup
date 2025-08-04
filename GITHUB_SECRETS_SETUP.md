# GitHub Secrets Setup Guide

This guide walks you through setting up the required GitHub secrets for the claude-setup CI/CD pipeline.

## Required Secrets

### 1. PyPI API Tokens

#### `PYPI_API_TOKEN`
- **Purpose**: Production PyPI publishing
- **How to create**:
  1. Log in to [PyPI](https://pypi.org/)
  2. Go to Account Settings → API tokens
  3. Click "Add API token"
  4. Name: `claude-setup-github-actions`
  5. Scope: Project (once first manual upload is done) or Entire account (for first upload)
  6. Copy the token (starts with `pypi-`)

#### `TEST_PYPI_API_TOKEN`
- **Purpose**: TestPyPI publishing for validation
- **How to create**:
  1. Log in to [TestPyPI](https://test.pypi.org/)
  2. Go to Account Settings → API tokens
  3. Click "Add API token"
  4. Name: `claude-setup-github-actions-test`
  5. Scope: Entire account (TestPyPI doesn't support project-scoped tokens)
  6. Copy the token (starts with `pypi-`)

### 2. Optional Secrets

#### `CODECOV_TOKEN`
- **Purpose**: Code coverage reporting
- **How to create**:
  1. Sign up at [Codecov](https://codecov.io/)
  2. Add your repository
  3. Copy the upload token from the repository settings

## How to Add Secrets to GitHub

1. Navigate to your repository on GitHub
2. Go to **Settings** → **Secrets and variables** → **Actions**
3. Click **New repository secret**
4. Add each secret:
   - Name: Use the exact names above (e.g., `PYPI_API_TOKEN`)
   - Value: Paste the token value
5. Click **Add secret**

## GitHub Environments Setup

For additional security, the release workflow uses GitHub Environments:

### Create `test-release` Environment:
1. Go to **Settings** → **Environments**
2. Click **New environment**
3. Name: `test-release`
4. Add protection rules:
   - Required reviewers: 0 (for automated testing)
   - Deployment branches: Only selected branches → Add `main` and tags `v*`

### Create `production-release` Environment:
1. Click **New environment**
2. Name: `production-release`
3. Add protection rules:
   - Required reviewers: 1+ (add yourself)
   - Deployment branches: Only selected branches → Add tags `v*`
   - Wait timer: 5 minutes (optional safety delay)

## Verification

After setup, you can verify everything is configured correctly:

1. **Test CI**: Push any change to trigger the CI workflow
2. **Test Version Bump**: 
   ```bash
   # Go to Actions → Version Bump → Run workflow
   # Select "patch" and run
   ```
3. **Test Release** (when ready):
   ```bash
   git tag v0.1.1
   git push origin v0.1.1
   ```

## Security Best Practices

1. **Rotate tokens regularly** (every 90 days)
2. **Use project-scoped tokens** when possible (after first PyPI upload)
3. **Enable 2FA** on both PyPI and TestPyPI accounts
4. **Monitor token usage** in PyPI security logs
5. **Never commit tokens** to the repository

## Troubleshooting

### "Invalid token" error
- Ensure the token starts with `pypi-`
- Check for extra spaces or newlines when pasting
- Verify the token hasn't expired

### "Permission denied" error
- For first upload, use account-scoped token
- After first upload, create project-scoped token
- Ensure the PyPI account has maintainer permissions

### TestPyPI vs PyPI
- TestPyPI tokens only work on test.pypi.org
- PyPI tokens only work on pypi.org
- They are not interchangeable

## Next Steps

Once secrets are configured:
1. Test the CI pipeline with a pull request
2. Test version bumping with the manual workflow
3. Create your first release with a git tag
4. Monitor the release workflow execution
5. Approve TestPyPI deployment
6. Approve PyPI deployment

For more information, see the [PyPI API token documentation](https://pypi.org/help/#apitoken).