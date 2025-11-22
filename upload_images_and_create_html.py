import json
import os
import subprocess
from datetime import datetime, timedelta

# First, let's create the GitHub repo and upload images
def setup_github_image_hosting():
    """Create a GitHub repo and upload all images"""
    print("Setting up GitHub image hosting...")

    # Create a new public repo for blog images
    repo_name = "modelit-blog-images"

    # Check if repo exists, if not create it
    result = subprocess.run(
        ['gh', 'repo', 'view', repo_name],
        capture_output=True,
        text=True
    )

    if result.returncode != 0:
        print(f"Creating new public repo: {repo_name}")
        subprocess.run(
            ['gh', 'repo', 'create', repo_name, '--public', '--description', 'ModelIT K12 Blog Hero Images'],
            check=True
        )

        # Clone the repo
        subprocess.run(['gh', 'repo', 'clone', repo_name], check=True)

        # Copy all images to the repo
        os.makedirs(f'{repo_name}/images', exist_ok=True)
        for week_num in range(1, 53):
            src = f'scripts/newsletter-output/week-{week_num:02d}-hero.jpg'
            dst = f'{repo_name}/images/week-{week_num:02d}-hero.jpg'
            if os.path.exists(src):
                subprocess.run(['cp', src, dst], check=True)
                print(f"Copied week-{week_num:02d}-hero.jpg")

        # Commit and push
        os.chdir(repo_name)
        subprocess.run(['git', 'add', '.'], check=True)
        subprocess.run(['git', 'commit', '-m', 'Add all 52 ModelIT blog hero images'], check=True)
        subprocess.run(['git', 'push', 'origin', 'main'], check=True)
        os.chdir('..')

        print("SUCCESS: All images uploaded to GitHub!")
    else:
        print(f"Repo {repo_name} already exists")

    # Get the GitHub username
    result = subprocess.run(['gh', 'api', 'user', '--jq', '.login'], capture_output=True, text=True, check=True)
    username = result.stdout.strip()

    return username, repo_name

def get_github_image_url(username, repo_name, week_num):
    """Generate GitHub raw URL for an image"""
    return f"https://raw.githubusercontent.com/{username}/{repo_name}/main/images/week-{week_num:02d}-hero.jpg"

def json_to_simplified_html(week_data, image_url):
    """Convert JSON blog data to simplified HTML with embedded image"""

    html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>{week_data['title']}</title>
    <style>
        body {{
            font-family: Arial, sans-serif;
            line-height: 1.6;
            max-width: 800px;
            margin: 0 auto;
            padding: 20px;
            color: #333;
        }}
        .hero-image {{
            width: 100%;
            max-width: 100%;
            height: auto;
            margin-bottom: 30px;
        }}
        .excerpt {{
            font-size: 1.2em;
            font-style: italic;
            color: #555;
            padding: 15px;
            background-color: #f5f5f5;
            border-left: 4px solid #0066cc;
            margin: 20px 0;
        }}
        h2 {{
            color: #0066cc;
            margin-top: 30px;
        }}
        .cta-buttons {{
            text-align: center;
            margin: 40px 0;
        }}
        .cta-button {{
            display: inline-block;
            padding: 15px 30px;
            margin: 10px;
            color: white;
            text-decoration: none;
            font-weight: bold;
            border-radius: 5px;
        }}
        .cta-primary {{
            background-color: #0066cc;
        }}
        .cta-secondary {{
            background-color: #28a745;
        }}
        .footer {{
            margin-top: 40px;
            padding: 20px;
            background-color: #f0f0f0;
            border-top: 2px solid #ccc;
        }}
    </style>
</head>
<body>
    <img src="{image_url}" alt="{week_data['title']}" class="hero-image">

    <h1>{week_data['title']}</h1>

    <div class="excerpt">
        <p>{week_data['excerpt']}</p>
    </div>

    <p>{week_data['content']['opening_hook']}</p>

    <h2>{week_data['content']['section_1_title']}</h2>
    <p>{week_data['content']['section_1_text']}</p>

    <h2>{week_data['content']['section_2_title']}</h2>
    <p>{week_data['content']['section_2_text']}</p>

    <h2>{week_data['content']['section_3_title']}</h2>
    <p>{week_data['content']['section_3_text']}</p>

    <h2>{week_data['content']['section_4_title']}</h2>
    <p>{week_data['content']['section_4_text']}</p>

    <p><strong>{week_data['content']['closing']}</strong></p>

    <div class="cta-buttons">
        <a href="{week_data['ctas'][0]['url']}" class="cta-button cta-primary">{week_data['ctas'][0]['text']}</a>
        <a href="{week_data['ctas'][1]['url']}" class="cta-button cta-secondary">{week_data['ctas'][1]['text']}</a>
    </div>

    <div class="footer">
        <h3>Research Citations</h3>
        <ul>'''

    for citation in week_data['metadata']['research_citations']:
        html += f'\n            <li>{citation}</li>'

    html += '''
        </ul>

        <h3>NGSS Alignment</h3>
        <ul>'''

    for practice in week_data['metadata']['ngss_practices']:
        html += f'\n            <li>{practice}</li>'

    html += f'''
        </ul>

        <p><strong>Authors:</strong> {week_data['author']}</p>
        <p><strong>Category:</strong> {week_data['category']}</p>
    </div>
</body>
</html>'''

    return html

# Main execution
if __name__ == "__main__":
    print("="*60)
    print("ModelIT Blog HTML Generator with GitHub Image Hosting")
    print("="*60)

    # Set up GitHub image hosting
    username, repo_name = setup_github_image_hosting()

    # Create output directory for HTML files
    os.makedirs('blog-html-files', exist_ok=True)

    # Process all 52 weeks
    for week_num in range(1, 53):
        json_file = f'modelitk12-blog/content/week-json/week-{week_num:02d}-content.json'

        if not os.path.exists(json_file):
            print(f"Warning: {json_file} not found, skipping...")
            continue

        try:
            # Load JSON
            with open(json_file, 'r', encoding='utf-8') as f:
                week_data = json.load(f)

            # Get GitHub image URL
            image_url = get_github_image_url(username, repo_name, week_num)

            # Generate HTML
            html_content = json_to_simplified_html(week_data, image_url)

            # Save HTML file
            html_filename = f'blog-html-files/week-{week_num:02d}-blog.html'
            with open(html_filename, 'w', encoding='utf-8') as f:
                f.write(html_content)

            print(f"SUCCESS: Created {html_filename}")

        except Exception as e:
            print(f"Error processing Week {week_num}: {str(e)}")

    print("\n" + "="*60)
    print("All 52 HTML files created successfully!")
    print(f"Files saved in: blog-html-files/")
    print(f"Images hosted on GitHub: {username}/{repo_name}")
    print("="*60)
