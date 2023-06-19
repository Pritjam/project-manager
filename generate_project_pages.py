import os
from jinja2 import Environment, FileSystemLoader

# Loads a template from templates/
# Uses that template and the text sources in srcs/ to generate
# content pages, with the Jinja templating engine.

def parse_md_link(md_link):
    # accepts a markdown link of the form `[visible text](https://url)`
    # returns the visible text and the url as 2 strings
    bracket_num = 0
    closing_bracket_idx = 0
    for char in md_link:
        if char == '[':
            bracket_num += 1
        elif char == ']':
            bracket_num -= 1
        if bracket_num == 0:
            break
        closing_bracket_idx += 1
    
    visible_text = md_link[1:closing_bracket_idx]
    url = md_link[closing_bracket_idx + 2:-1]
    return visible_text, url
        

def process_file(filepath):
    components = {}
    with open(filepath, 'r') as input_file:
        line = "initial value"
        while line:
            line = input_file.readline().strip()
            toks = line.split(':', 1)
            key = toks[0].strip()
            # Decide what to do based on token

            # unique components such as title, description, etc
            if key in ['title', 'description', 'roadmap', 'github']:
                content = toks[1].strip()
                components[key] = content
                # roadmap_list = line[1:].split(',')
                # roadmap_list = [{"tag":(0 if elem[0] == 'd' else 1), "item":elem[1:]} for elem in roadmap_list]
                # parts["roadmap"] = roadmap_list
            # non-unique components, there can be multiple of each of these. Often will span multiple lines.
            elif key == 'paragraph':
                # paragraph of text, this first line is a title
                title = toks[1].strip()
                paragraph_content = input_file.readline().strip()
                # ensure we have a part in the components for this
                if not "paragraphs" in components:
                    components["paragraphs"] = []
                # Add this paragraph
                paragraph = {'title' : title, 'text' : paragraph_content}
                components["paragraphs"].append(paragraph)
            elif key == 'link':
                # link to another site or source, formatted as a Markdown link
                md_link = toks[1].strip()
                visible_text, url = parse_md_link(md_link)
                if not "links" in components:
                    components["links"] = []
                link = {'visible' : visible_text, 'url' : url}
                components["links"].append(link)
    
    return components



print("Using file 'templates/proj_template.html' as jinja2 template.\nUsing 'srcs' as project description inputs.")

src_filenames = os.listdir("srcs")

environment = Environment(loader=FileSystemLoader("templates/"))
template = environment.get_template("proj_template.html")

for filename in src_filenames:
    filepath = os.path.join("srcs", filename)
    print("Parsing file at path %s now" % filepath)
    components = process_file(filepath)

    # get output path
    out_filename = os.path.splitext(filename)[0]
    out_filename += '.html'
    out_path = os.path.join('out', out_filename)
    # write output HTML file
    with open(out_path, "w") as outfile:
        outfile.write(template.render(components))
# print(parts)





