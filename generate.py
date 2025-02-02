import markdown
import os
import datetime
from jinja2 import Environment, FileSystemLoader

# Load templates
env = Environment(loader=FileSystemLoader('templates'))
base_template = env.get_template('base.html')
post_template = env.get_template('post.html')
index_template = env.get_template('index.html')


BUILD_DIR = 'build'

def render_template(template, **kwargs):
    base_html_start = template.render(kwargs, content="", title="Blog")
    base_html_end = ""
    return template.render({**kwargs, 'base_html_start': base_html_start, 'base_html_end':base_html_end })


def process_markdown_file(markdown_path):
    with open(markdown_path, 'r', encoding='utf-8') as file:
        text = file.read()
    html = markdown.markdown(text)
    return html


def create_post_page(post_path):
    title = os.path.basename(post_path).replace(".md", "").replace("-", " ")
    html = process_markdown_file(post_path)
    output_path = os.path.join(BUILD_DIR, os.path.basename(post_path).replace(".md", ".html"))
    rendered_post = render_template(post_template, post_title=title.capitalize(), post_content=html, title=title.capitalize())

    os.makedirs(os.path.dirname(output_path), exist_ok=True)  # Create output dir if needed
    with open(output_path, 'w', encoding='utf-8') as file:
        file.write(rendered_post)
    return {'title': title.capitalize(), 'url': os.path.basename(output_path)}

def create_index_page(posts):
    rendered_index = render_template(index_template, posts=posts, title="Blog Home")
    output_path = os.path.join(BUILD_DIR, "index.html")
    with open(output_path, "w", encoding="utf-8") as file:
        file.write(rendered_index)

def copy_static_files():
    static_dir = "static"
    dest_dir = os.path.join(BUILD_DIR, "static")
    os.makedirs(dest_dir, exist_ok=True)
    for filename in os.listdir(static_dir):
      src_path = os.path.join(static_dir, filename)
      dest_path = os.path.join(dest_dir, filename)
      with open(src_path, 'rb') as src_file, open(dest_path, 'wb') as dest_file:
          dest_file.write(src_file.read())

def main():
    os.makedirs(BUILD_DIR, exist_ok=True)  # Ensure build directory exists
    posts = []
    for filename in os.listdir('posts'):
       if filename.endswith(".md"):
            posts.append(create_post_page(f'posts/{filename}'))
    create_index_page(posts)
    copy_static_files()
    print(f"Blog generated successfully in '{BUILD_DIR}'!")


if __name__ == "__main__":
  main()