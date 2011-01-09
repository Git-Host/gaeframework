import re

class Wiki:
    '''
    Parse wiki markup and return html.
    
    Using:
      Wiki().parse(raw_data)
    '''
    rules = {
            # link
            r"((https?|ftp|nntp|news|mailto)://([a-zA-Z0-9_-]+[a-zA-Z0-9._-]*\.[a-zA-Z0-9_-]{2,4})([^ ]*))":
                "<a href='\\1'>\\3</a>",
            # email
            r"([a-zA-Z0-9_-]+[a-zA-Z0-9._-]*\@([a-zA-Z0-9_-]+[a-zA-Z0-9._-]*\.[a-zA-Z0-9_-]{2,4}))":
                "<a href='mailto:\\1'>\\1</a>",
            # TODO: generate TOC (table of contents)
            r"^\[TOC\ h([1-6])-h([2-6])]$":
                "TOC - table of contents",
            }

    def __init__(self):
        self.in_p = False
        self.in_pre = False
        self.in_code = False
        self.result = []

    def parse(self, text):
        '''
        Parce wiki text and return html.
        '''
        lines = text.splitlines()
        self.result = []
        # transform wiki text to html
        for line in lines:
            # delete white spaces
            line = line.strip()
            # processing lines
            line = self.parse_line(line)
            # processing blocks
            line = self.parse_block(line)
        # post processing (close tags)
        if self.in_p:
            last = self.result.pop()
            self.result.append("</p>")
            self.result.append(last)
        return "".join(self.result)

    def parse_block(self, line):
        # separator
        if re.match(r"^-{3,}$", line):
            line = "<hr>"
        # header
        elif line.startswith("="):
            depth = line.count("=", 0, 6)
            line = "<h%s>%s</h%s>" % (depth, line.lstrip("= "), depth)
        # paragraph
        elif not self.in_p and line:
            self.in_p = True
            self.result.append("<p>")
        elif self.in_p and line == "":
            self.in_p = False
            self.result.pop()
            self.result.append("</p>")
        elif self.in_p:
            last = self.result.pop()
            self.result.append("<br/>")
            self.result.append(last)
        elif line == "":
            self.result.pop()
        # set value and new line
        self.result.append(line)
        self.result.append("\n")

    def parse_line(self, line):
        # replace rules
        for (key, value) in self.rules.items():
            line = re.sub(key, value, line);
        # return changed line
        return line
