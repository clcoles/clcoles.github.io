#!/bin/env python3

import mistune, os, collections

with open('index-template.html') as f:
    index_template = f.read()

post_path = 'Entries'
posts = collections.OrderedDict()

for directory in reversed(sorted([f for f in os.listdir(post_path) if os.path.isdir(os.path.join(post_path, f))])):
    post_dir = os.path.join(post_path, directory)
    markdown_files = [f for f in os.listdir(post_dir) if f.endswith('.md')]
    if len(markdown_files) > 0:
        contents = open(os.path.join(post_dir, markdown_files[0])).read()
        html = mistune.markdown(contents)
        final = html.replace('src="./', 'src="'+post_dir+'/')
        posts[directory] = final
    else:
        print("Error! No md file in the {} directory.".format(post_dir))

final = index_template.replace('{{main_text}}', "\n".join(posts.values()))

with open('index.html', 'w') as f:
    f.write(final)
