import os
from jinja2 import Environment, FileSystemLoader

src_filenames = os.listdir("jinja/srcs")
# print(src_filenames)

environment = Environment(loader=FileSystemLoader("jinja/templates/"))
template = environment.get_template("proj_template.html")


for filename in src_filenames:
    print(filename)
    parts = {}
    with open(os.path.join("jinja/srcs", filename), "r") as infile:
        line = infile.readline().strip()
        while line:
            if line[0] == 't':
                parts["title"] = line[1:]
            elif line[0] == 'g':
                parts["github"] = line[1:]
            elif line[0] == 'd':
                parts["description"] = line[1:]
            elif line[0] == 'l':
                link = infile.readline().strip()
                if not "links" in parts:
                    parts["links"] = []
                parts["links"].append({"name":line[1:], "link":link})
            elif line[0] == 'r':
                roadmap_list = line[1:].split(',')
                roadmap_list = [{"tag":(0 if elem[0] == 'd' else 1), "item":elem[1:]} for elem in roadmap_list]
                parts["roadmap"] = roadmap_list
            elif line[0] == 's':
                section = infile.readline().strip()
                if not "sections" in parts:
                    parts["sections"] = []
                parts["sections"].append({"title":line[1:], "text":section})
            line = infile.readline().strip()
            
            # write output HTML file
            with open("pages/" + filename.rsplit('.', 1)[0] + ".html", "w") as outfile:
                outfile.write(template.render(parts))
# print(parts)





