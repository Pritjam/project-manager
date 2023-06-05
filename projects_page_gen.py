import os
from jinja2 import Environment, FileSystemLoader

environment = Environment(loader=FileSystemLoader("jinja/templates/"))
template = environment.get_template("projects_template.html")

parts = {"projects":[]}
with open("jinja/all_projs.txt", "r") as infile:
    proj_name = infile.readline().strip()
    while proj_name:
        proj_link = "pages/" + infile.readline().strip()
        proj_desc = infile.readline().strip()
        parts["projects"].append({"title":proj_name, "link":proj_link, "description":proj_desc})
        proj_name = infile.readline().strip()
        
        # write output HTML file
    with open("projects.html", "w") as outfile:
        outfile.write(template.render(parts))
# print(parts)





