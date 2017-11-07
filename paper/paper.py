# paper.py
# by James Fulford

import docx

IGNORE_STARTS = [".", "_", "-"]


def write(paper_ob, variables, **kwargs):
    """"""

    #
    # Prepare variables
    #
    ready = {}
    for kw in kwargs:
        ready[unicode(kw)] = kwargs[kw]
    for var in variables.keys():
        ready[unicode(var)] = variables[var]

    #
    # Iterate over paragraphs
    #
    doc = docx.Document(paper_ob)
    for p in doc.paragraphs:
        p.text = p.text.format(**ready)

    #
    # Save
    #
    doc.save("Output.docx")


vari = {
    "intro": "IT WORKED"
}


print write(open("Sample.docx"), vari)
