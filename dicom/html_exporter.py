import os


class HTMLExporter:
    def export(self,directory,index):
        group=f"group{index}"
        group_tag=f"<imggrp{index}>"
        template=""
        with open("template.txt","r") as file:
            template=file.read()
        template=template.replace("$grouptag",group_tag)
        template=template.replace("$group",group)
        with open(os.path.join(directory,f"group_{index}.html"),"w") as file:
            file.write(template)
