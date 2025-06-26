# Python Virtual Environment Setup

This project uses a Python virtual environment to manage dependencies and ensure consistent builds.

## Quick Start

1. **Setup the environment** (run once):
   ```bash
   ./setup_env.sh
   ```

2. **Build the blog**:
   ```bash
   ./build_blog.sh
   ```

## Manual Virtual Environment Management

### Activate the environment:
```bash
source venv/bin/activate
```

### Install/update dependencies:
```bash
pip install -r requirements.txt
```

### Run the blog builder manually:
```bash
python .github/scripts/build_blog.py
```

### Deactivate the environment:
```bash
deactivate
```

## Dependencies

The project dependencies are defined in `requirements.txt`:
- `python-frontmatter`: For parsing markdown frontmatter
- `markdown`: For converting markdown to HTML
- `pygments`: For syntax highlighting in code blocks
- `beautifulsoup4` & `lxml`: For HTML parsing (if needed)

## Troubleshooting

- If you get import errors, make sure the virtual environment is activated
- If packages are missing, run `pip install -r requirements.txt`
- If the virtual environment is corrupted, delete the `venv/` folder and run `./setup_env.sh` again
