# Static Blog

A modern, lightweight static blog system with **automatic publishing** - just write markdown and push to GitHub!

## ✨ Super Simple Workflow

1. **Write a markdown file** anywhere in your repo
2. **Add frontmatter** (title, date, excerpt) 
3. **Push to GitHub**
4. **Your blog is automatically updated!** 🎉

No Python scripts to run, no manual building - everything happens automatically via GitHub Actions.

## Features

- 🖋️ **Rich Text Editor** - WYSIWYG editor powered by Quill.js
- � **Pure Markdown** - Write in markdown, get beautiful HTML
- 🚀 **Auto-Deploy** - Push and your blog updates automatically
- 📑 **Table of Contents** - Auto-generated from your headers
- 📱 **Responsive Design** - Looks great on all devices
- ⚡ **Fast & Lightweight** - Static files for optimal performance
- 🔗 **Footnotes** - Full footnote support with linking

## Quick Start

### Create Your First Post

**Method 1: Simple Markdown File**
```bash
# Create a new post
touch my-first-post.md
```

Add this content:
```markdown
---
title: My First Post
date: 2025-06-21
excerpt: Welcome to my new blog!
---

# My First Post

Hello world! This is my first automatically published blog post.

## What's Great About This

- No build scripts to run
- No manual HTML conversion
- Just write markdown and push!

The rest happens automatically via GitHub Actions.
```

**Method 2: Use the Web Editor**
- Open `editor.html` in your browser
- Write your post with rich formatting
- Download the markdown file
- Add it to your repo and push

### Deploy Your Blog

```bash
git add my-first-post.md
git commit -m "Add first blog post"
git push
```

Wait ~2 minutes and your blog is live with your new post! ✨

## How It Works

When you push to GitHub:
1. **GitHub Actions** automatically runs
2. **Finds all `.md` files** in your repo (except README.md)
3. **Converts to beautiful HTML** with styling and table of contents
4. **Updates your homepage** with the latest posts
5. **Deploys to GitHub Pages**

## Supported Markdown Features

- **Headers** (with automatic table of contents)
- **Bold**, *italic*, and other formatting
- **Links** and images
- **Code blocks** with syntax highlighting
- **Tables** and lists
- **Footnotes** using `[^1]` syntax
- **Blockquotes** and more

## File Organization

Put markdown files anywhere:
- **Root directory**: `my-post.md`
- **Drafts folder**: `drafts/my-post.md` 
- **Any subfolder**: The system finds them automatically

File names become URLs: `javascript-tips.md` → `yoursite.com/posts/javascript-tips.html`

## Deployment

### GitHub Pages

1. **Create a new GitHub repository**
2. **Push this code to your repository**
3. **Enable GitHub Pages in repository settings**
4. **Choose "Deploy from a branch" and select "main"**
5. **Your blog will be live at `https://yourusername.github.io/repository-name`**

### Manual Deployment

Since this is a static site, you can deploy it anywhere that serves HTML files:
- Netlify
- Vercel
- AWS S3
- Any web hosting service

## Customization

### Styling

Edit `assets/style.css` to customize the appearance. The CSS uses CSS custom properties for easy theming:

```css
:root {
    --primary-color: #000;
    --text-color: #333;
    --light-gray: #666;
    --border-color: #eee;
    --background-color: #fff;
}
```

### Layout

- Modify `index.html` for the homepage layout
- Edit the post template in `scripts/publish_post.py`
- Customize `editor.html` for the writing experience

### Functionality

- Add new Python scripts for additional features
- Extend the markdown to HTML conversion
- Integrate with external services (analytics, comments, etc.)

## Local Development

To preview your blog locally before pushing:

```bash
# Start the development server
python .github/scripts/serve.py

# Or specify a custom port
python .github/scripts/serve.py 8080
```

This will:
- Start a local server at `http://localhost:8000` (or your chosen port)
- Automatically open your blog in the browser
- Serve all files with cache disabled for development
- Show helpful tips and available pages

## Requirements

- Python 3.6+
- Modern web browser
- Text editor (VS Code recommended)

## License

This project is open source and available under the MIT License.

## Contributing

Feel free to fork this project and submit pull requests for improvements!

## Support

If you find this useful, please star the repository and share it with others who might benefit from a simple blogging solution.

---

Happy blogging! 🎉
