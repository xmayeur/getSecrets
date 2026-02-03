# ReadTheDocs Setup Guide

This guide will walk you through publishing your getSecrets documentation on ReadTheDocs.

## Prerequisites

✅ Documentation files are ready in `docs/` directory
✅ `.readthedocs.yaml` configuration file is at project root
✅ Local build tested successfully
✅ Project is in a Git repository

## Step 1: Commit and Push Documentation

First, commit all documentation files to your repository:

```bash
git add .readthedocs.yaml docs/ README.md
git commit -m "Add Sphinx documentation with ReadTheDocs configuration"
git push origin master
```

## Step 2: Create ReadTheDocs Account

1. Go to https://readthedocs.org/
2. Click "Sign Up" or "Log In"
3. You can sign in with:
    - GitHub account (recommended)
    - GitLab account
    - Bitbucket account
    - Email

## Step 3: Import Your Project

### Option A: Automatic Import (GitHub/GitLab/Bitbucket)

1. After logging in, click **"Import a Project"**
2. Click **"Import Manually"** or select from your connected repositories
3. If using manual import:
    - **Name**: `getSecrets` (or your preferred name)
    - **Repository URL**: Your Git repository URL
    - **Repository type**: Git
    - **Default branch**: `master` (or `main`)
    - **Advanced Settings**:
        - Programming Language: Python
        - Documentation type: Sphinx Html

### Option B: Manual Configuration

1. Go to https://readthedocs.org/dashboard/
2. Click **"Import a Project"**
3. Click **"Import Manually"**
4. Fill in the project details:
   ```
   Name: getSecrets
   Repository URL: https://github.com/yourusername/getSecrets
   Repository type: Git
   Default branch: master
   ```
5. Click **"Next"**

## Step 4: Configure Project Settings

After importing, configure your project:

1. Go to **Admin → Settings**
2. Verify these settings:
    - **Name**: getSecrets
    - **Repository URL**: Correct URL
    - **Default branch**: master
    - **Programming Language**: Python

3. Go to **Admin → Advanced Settings**:
    - **Documentation type**: Sphinx Html
    - **Requirements file**: `docs/requirements.txt`
    - **Python interpreter**: CPython 3.9
    - **Install Project**: ✓ (checked)

4. Click **"Save"**

## Step 5: Build Documentation

1. Go to your project dashboard on ReadTheDocs
2. Click **"Build Version"** or wait for automatic build
3. The build should start automatically
4. Monitor the build progress in the **"Builds"** tab

## Step 6: Check Build Status

### If Build Succeeds ✅

1. Your documentation will be available at:
   ```
   https://getsecrets.readthedocs.io/
   ```
   Or:
   ```
   https://your-project-name.readthedocs.io/
   ```

2. Update your README.md badge URL if needed:
   ```markdown
   [![Documentation Status](https://readthedocs.org/projects/getsecrets/badge/?version=latest)](https://getsecrets.readthedocs.io/en/latest/?badge=latest)
   ```

### If Build Fails ❌

1. Click on the failed build in the **"Builds"** tab
2. Review the build log for errors
3. Common issues:
    - Missing dependencies in `docs/requirements.txt`
    - Python version mismatch
    - Import errors in code
    - Configuration errors in `conf.py`

4. Fix issues, commit, and push:
   ```bash
   git add .
   git commit -m "Fix documentation build issues"
   git push
   ```

5. ReadTheDocs will automatically rebuild

## Step 7: Enable Automatic Builds

1. Go to **Admin → Integrations**
2. Add a webhook integration for your Git provider
3. This enables automatic builds on every push

## Step 8: Configure Versions

1. Go to **Versions**
2. Activate the versions you want to build:
    - **latest** (always points to default branch)
    - **stable** (points to latest release tag)
    - Specific version tags

## Optional: Custom Domain

To use a custom domain (e.g., docs.yourdomain.com):

1. Go to **Admin → Domains**
2. Click **"Add Domain"**
3. Follow the DNS configuration instructions

## Verification Checklist

- [ ] Documentation builds successfully
- [ ] All pages render correctly
- [ ] Navigation works properly
- [ ] Search functionality works
- [ ] API documentation displays correctly
- [ ] Examples are formatted properly
- [ ] Badge in README.md links correctly

## Updating Documentation

After setup, any push to your repository will automatically rebuild the documentation:

```bash
# Make changes to docs
vim docs/source/examples.rst

# Commit and push
git add docs/
git commit -m "Update examples documentation"
git push

# ReadTheDocs will automatically rebuild
```

## Troubleshooting

### Build Timeout

If builds timeout, try:

1. Reduce dependencies
2. Use more specific version pins in `requirements.txt`
3. Contact ReadTheDocs support for increased timeout

### Import Errors

If Python can't import your module:

1. Verify `sys.path.insert(0, os.path.abspath('../../src'))` in `conf.py`
2. Ensure your package structure is correct
3. Check that dependencies are in `docs/requirements.txt`

### Theme Not Loading

If RTD theme doesn't load:

```bash
pip install sphinx-rtd-theme
```

Add to `docs/requirements.txt`:

```
sphinx-rtd-theme>=1.0.0
```

## Support

- ReadTheDocs Documentation: https://docs.readthedocs.io/
- ReadTheDocs Support: https://readthedocs.org/support/
- Sphinx Documentation: https://www.sphinx-doc.org/

## Your Documentation is Ready!

Once published, share your documentation URL:

- In your README.md
- In your package description on PyPI
- In your project documentation

**Documentation URL**: https://getsecrets.readthedocs.io/

Happy documenting! 📚
