from jinja2 import Environment, PackageLoader
import jinja2


def create_output_html(list_of_links, rooturl):
    print(list_of_links)
    templateVars = { "title" : "Results of 404 finder",
                     "description" : "A simple inquiry of function.",
                     "list_of_links" : list_of_links,
                     "rooturl": rooturl
                   }

    templateLoader = jinja2.FileSystemLoader( searchpath="." )
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = "template.html"

    template = templateEnv.get_template( TEMPLATE_FILE )
    return template.render(templateVars)

