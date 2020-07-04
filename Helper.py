#!/bin/env python3

import mistune

with open('index-template.html') as f:
    index_template = f.read()
with open('Posts/2020-04-29-SweetAndSourTofu/Sweet and Sour Tofu.md') as f:
    post_md = f.read()


final = index_template.replace('{{main_text}}', mistune.markdown(post_md))
final = final.replace('src="./', 'src="Posts/2020-04-29-SweetAndSourTofu/')
with open('index.html', 'w') as f:
    f.write(final)
