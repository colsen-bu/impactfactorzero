#!/usr/bin/env python3
"""
Automatic blog builder for GitHub Actions
Converts markdown files to HTML and updates the index
"""

import os
import re
import html
import frontmatter
import markdown
from datetime import datetime
from pathlib import Path

def generate_table_of_contents(content):
    """Generate table of contents from headers"""
    # Find all headers in the content
    headers = re.findall(r'<h([2-4])[^>]*>([^<]+)</h[2-4]>', content)
    
    if not headers:
        return None
    
    toc_html = ['<div class="table-of-contents">']
    toc_html.append('<h3>Table of Contents</h3>')
    toc_html.append('<ul>')
    
    for level, text in headers:
        # Create a slug for the anchor
        slug = text.lower().strip()
        slug = re.sub(r'[^a-z0-9\s-]', '', slug)
        slug = re.sub(r'\s+', '-', slug)
        slug = re.sub(r'-+', '-', slug)
        slug = slug.strip('-')
        
        # Add ID to the header in content for linking
        old_header = f'<h{level}>{text}</h{level}>'
        new_header = f'<h{level} id="{slug}">{text}</h{level}>'
        content = content.replace(old_header, new_header, 1)
        
        # Add to TOC
        css_class = f'h{level}' if level != '2' else ''
        toc_html.append(f'<li class="{css_class}"><a href="#{slug}">{text}</a></li>')
    
    toc_html.append('</ul>')
    toc_html.append('</div>')
    
    return '\n'.join(toc_html), content

def create_html_post(title, content, metadata, slug):
    """Create complete HTML post"""
    date_str = metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
    try:
        date_obj = datetime.strptime(str(date_str), '%Y-%m-%d')
        formatted_date = date_obj.strftime('%B %d, %Y')
    except:
        formatted_date = str(date_str)
    
    excerpt = metadata.get('excerpt', '')
    
    # Generate table of contents
    toc_result = generate_table_of_contents(content)
    if toc_result:
        toc_html, content = toc_result
        post_class = "post-with-toc"
        post_content = f'''                <div class="post-content-wrapper">
                    <article class="post">
                        <header>
                            <h1>{html.escape(title)}</h1>
                            <div class="post-meta">
                                Published on {formatted_date}
                            </div>
                        </header>
                        <div class="post-content">
                            {content}
                        </div>
                    </article>
                </div>
                {toc_html}'''
    else:
        post_class = "post"
        post_content = f'''                <article class="post">
                    <header>
                        <h1>{html.escape(title)}</h1>
                        <div class="post-meta">
                            Published on {formatted_date}
                        </div>
                    </header>
                    <div class="post-content">
                        {content}
                    </div>
                </article>'''
    
    html_template = f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{html.escape(title)}</title>
    <link rel="stylesheet" href="../assets/style.css">
    <meta name="description" content="{html.escape(excerpt)}">
</head>
<body>
    <header>
        <h1><a href="../index.html" style="text-decoration: none; color: inherit;">Impact Factor Zero</a></h1>
        <nav>
            <ul>
                <li><a href="../index.html">← Back to Home</a></li>
            </ul>
        </nav>
    </header>

    <main>
        <div class="{post_class}">
{post_content}
        </div>
    </main>

    <footer>
        <p>&copy; 2025 Impact Factor Zero</p>
    </footer>
    
    <script>
        // Highlight active TOC item on scroll
        document.addEventListener('DOMContentLoaded', function() {{
            const tocLinks = document.querySelectorAll('.table-of-contents a');
            const headers = document.querySelectorAll('.post h2, .post h3, .post h4');
            
            if (tocLinks.length === 0 || headers.length === 0) return;
            
            function updateActiveTocItem() {{
                let activeHeader = null;
                const scrollPos = window.scrollY + 100; // Offset for better UX
                
                for (let i = headers.length - 1; i >= 0; i--) {{
                    if (headers[i].offsetTop <= scrollPos) {{
                        activeHeader = headers[i];
                        break;
                    }}
                }}
                
                // Remove active class from all links
                tocLinks.forEach(link => link.classList.remove('active'));
                
                // Add active class to current section
                if (activeHeader) {{
                    const activeLink = document.querySelector(`.table-of-contents a[href="#${{activeHeader.id}}"]`);
                    if (activeLink) {{
                        activeLink.classList.add('active');
                    }}
                }}
            }}
            
            // Update on scroll
            window.addEventListener('scroll', updateActiveTocItem);
            updateActiveTocItem(); // Initial update
        }});
    </script>
</body>
</html>"""
    return html_template

def process_markdown_files():
    """Process all markdown files and create HTML posts"""
    posts_data = []
    
    # Create posts directory if it doesn't exist
    os.makedirs('posts', exist_ok=True)
    
    # Process all markdown files recursively in all directories
    markdown_files = []
    
    # Recursively find all .md files in the entire repository
    for file in Path('.').rglob('*.md'):
        # Skip documentation files and files in .github directory
        if (file.name not in ['README.md'] and 
            '.github' not in str(file) and
            '.git' not in str(file)):
            markdown_files.append(file)
    
    for md_file in markdown_files:
        try:
            print(f"Processing {md_file}")
            
            # Read and parse markdown
            with open(md_file, 'r', encoding='utf-8') as f:
                post = frontmatter.load(f)
            
            # Extract metadata
            title = post.metadata.get('title', md_file.stem.replace('-', ' ').title())
            date = post.metadata.get('date', datetime.now().strftime('%Y-%m-%d'))
            
            # Ensure date is in string format for consistent handling
            if isinstance(date, datetime):
                date = date.strftime('%Y-%m-%d')
            else:
                date = str(date)
                
            excerpt = post.metadata.get('excerpt', f'A blog post about {title.lower()}')
            slug = md_file.stem
            
            # Convert markdown to HTML
            md = markdown.Markdown(extensions=[
                'markdown.extensions.fenced_code',
                'markdown.extensions.tables',
                'markdown.extensions.toc',
                'markdown.extensions.codehilite',
                'markdown.extensions.footnotes'  # Add footnotes support
            ])
            content = md.convert(post.content)
            
            # Create HTML file
            html_content = create_html_post(title, content, post.metadata, slug)
            html_file = f'posts/{slug}.html'
            
            with open(html_file, 'w', encoding='utf-8') as f:
                f.write(html_content)
            
            # Store post data for index
            posts_data.append({
                'title': title,
                'date': date,
                'excerpt': excerpt,
                'slug': slug,
                'filename': f'{slug}.html'
            })
            
            print(f"Created {html_file}")
            
        except Exception as e:
            print(f"Error processing {md_file}: {e}")
    
    return posts_data

def update_index(posts_data):
    """Update the index.html with all posts"""
    # Sort posts by date (newest first) - improved date handling
    for post in posts_data:
        if isinstance(post['date'], datetime):
            post['date'] = post['date'].strftime('%Y-%m-%d')
        else:
            post['date'] = str(post['date'])
    
    # Sort by date (newest first) and then by title for consistent ordering
    posts_data.sort(key=lambda x: (x['date'], x['title']), reverse=True)
    
    # Generate posts HTML with proper post items structure
    posts_html = []
    for i, post in enumerate(posts_data):
        try:
            date_obj = datetime.strptime(str(post['date']), '%Y-%m-%d')
            formatted_date = date_obj.strftime('%B %d, %Y')
        except:
            formatted_date = str(post['date'])
        
        # Add post-item class wrapper for proper styling and dividers
        post_html = f'''                <article class="post-item">
                    <h3><a href="posts/{post['filename']}">{html.escape(post['title'])}</a></h3>
                    <div class="post-meta">{formatted_date}</div>
                    <div class="post-excerpt">{html.escape(post['excerpt'])}</div>
                </article>'''
        posts_html.append(post_html)
    
    posts_section = '\n'.join(posts_html)
    
    # Read current index.html or create a template
    index_template = '''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Impact Factor Zero</title>
    <link rel="stylesheet" href="assets/style.css">
</head>
<body>
    <header>
        <h1>Impact Factor Zero</h1>
    </header>

    <main>
        <div class="post-list">
{posts_section}
        </div>
    </main>

    <footer>
        <p>&copy; 2025 Impact Factor Zero</p>
    </footer>
</body>
</html>'''
    
    # Try to read existing index.html and preserve custom content
    if os.path.exists('index.html'):
        try:
            with open('index.html', 'r', encoding='utf-8') as f:
                existing_content = f.read()
            
            # Replace the post-list section - more flexible regex
            pattern = r'(<div class="post-list">\s*)(.*?)(\s*</div>\s*</main>)'
            replacement = f'\\1\n{posts_section}\n            \\3'
            
            new_content = re.sub(pattern, replacement, existing_content, flags=re.DOTALL)
            
            if new_content != existing_content:
                with open('index.html', 'w', encoding='utf-8') as f:
                    f.write(new_content)
                print("Updated existing index.html")
            else:
                print("No changes needed to index.html")
        except Exception as e:
            print(f"Error updating existing index.html: {e}")
            # Fall back to template
            with open('index.html', 'w', encoding='utf-8') as f:
                f.write(index_template.format(posts_section=posts_section))
            print("Created new index.html from template")
    else:
        # Create new index.html
        with open('index.html', 'w', encoding='utf-8') as f:
            f.write(index_template.format(posts_section=posts_section))
        print("Created new index.html")

def main():
    print("🚀 Building blog...")
    
    # Process markdown files
    posts_data = process_markdown_files()
    print(f"Processed {len(posts_data)} posts")
    
    # Update index
    update_index(posts_data)
    
    print("✅ Blog build complete!")
    print(f"Generated {len(posts_data)} posts")

if __name__ == "__main__":
    main()
