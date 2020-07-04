#!/bin/env python3

import mistune, os, collections, re

with open('index-template.html') as f:
    index_template = f.read()

post_path = 'Entries'
posts = []

footnotes = """
[^url]
"""

class MyRenderer(mistune.Renderer):
    def __init__(self):
        self.metatags = {}
        super().__init__()
    def header(self, text, level, raw=None):
        if level == 1:
            return '<a href={{mainlink}} class="entry-title"><h%d>%s</h%d></a>\n' % (level, text, level)
        return '<h%d>%s</h%d>\n' % (level, text, level)
    def footnote_ref(self, key, index):
        return ''
    def footnote_item(self, key, text):
        notags = re.compile('<.*?>')
        self.metatags[key] = re.sub(notags, '', text).strip()
        return ''
    def footnotes(self, text):
        return ''


for directory in reversed(sorted([f for f in os.listdir(post_path) if os.path.isdir(os.path.join(post_path, f))])):
    post_dir = os.path.join(post_path, directory)
    markdown_files = [f for f in os.listdir(post_dir) if f.endswith('.md')]
    if len(markdown_files) > 0:
        contents = footnotes + open(os.path.join(post_dir, markdown_files[0])).read() 
        r = MyRenderer()
        md = mistune.Markdown(escape=True, renderer=r)
        html = md(contents)
        posts.append({
            "html": html,
            "post_dir": directory,
            "post_file": directory + ".html",
            "post_name": os.path.join('posts', (r.metatags['url'] if 'url' in r.metatags else directory) + ".html"),
            "meta": r.metatags,
        })
    else:
        print("Error! No md file in the {} directory.".format(post_dir))

with open('index.html', 'w') as f:
    posts_html = [post['html'].replace('src="./', 'src="'+post_path+"/"+post['post_dir']+'/')
                              .replace('{{mainlink}}', post['post_name']) for post in posts]
    f.write(index_template.replace('{{main_text}}', "\n".join(posts_html))
                          .replace('{{toplink}}', ""))
                          

for post in posts:
    with open(post['post_name'], 'w') as f:
        print(post['post_name'], post['meta'])
        post_html = post['html'].replace('src="./', 'src="../'+post_path+"/"+post['post_dir']+'/') \
                                .replace('{{mainlink}}', post['post_file']) 
        f.write(index_template.replace('{{main_text}}', post_html).replace('./HTML/', './../HTML/')
                              .replace('{{toplink}}', "../index.html"))
