# -*- coding: utf-8 -*

from jinja2 import Environment, PackageLoader
import jinja2


def create_output_html(list_of_links):
    print list_of_links
    templateVars = { "title" : "Test Example",
                     "description" : "A simple inquiry of function.",
                     "list_of_links" : list_of_links
                   }

    templateLoader = jinja2.FileSystemLoader( searchpath="." )
    templateEnv = jinja2.Environment( loader=templateLoader )
    TEMPLATE_FILE = "template.html"

    template = templateEnv.get_template( TEMPLATE_FILE )
    return template.render(templateVars)

