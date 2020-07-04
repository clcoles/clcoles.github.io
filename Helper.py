#!/bin/env python3

import mistune, os, collections

with open('index-template.html') as f:
    index_template = f.read()

post_path = 'Entries'
posts = []

for directory in reversed(sorted([f for f in os.listdir(post_path) if os.path.isdir(os.path.join(post_path, f))])):
    post_dir = os.path.join(post_path, directory)
    markdown_files = [f for f in os.listdir(post_dir) if f.endswith('.md')]
    if len(markdown_files) > 0:
        contents = open(os.path.join(post_dir, markdown_files[0])).read()
        html = mistune.markdown(contents)
        posts.append({
            "html": html,
            "post_dir": directory,
            "post_name": os.path.join('posts', directory + ".html")
        })
    else:
        print("Error! No md file in the {} directory.".format(post_dir))

with open('index.html', 'w') as f:
    posts_html = [post['html'].replace('src="./', 'src="'+post['post_dir']+'/') for post in posts]
    f.write(index_template.replace('{{main_text}}', "\n".join(posts_html)))

for post in posts:
    with open(post['post_name'], 'w') as f:
        post_html = post['html'].replace('src="./', 'src="../'+post_path+"/"+post['post_dir']+'/')
        f.write(index_template.replace('{{main_text}}', post_html).replace('./HTML/', './../HTML/'))
