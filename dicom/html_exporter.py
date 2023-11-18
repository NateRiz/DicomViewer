import os


class HTMLExporter:
    def export(self, directory, index):
        group = f"group{index}"
        group_tag = f"imggrp{index}"
        template = ""
        series = os.path.basename(directory)
        study = os.path.basename(os.path.dirname(directory))
        with open("template.txt", "r") as file:
            template = file.read()
        template = template.replace("$grouptag", group_tag)
        template = template.replace("$group", group)
        series_path = os.path.join(study, series)
        template = template.replace("$seriespath", series_path)
        img_tag_template = '\n\t<img class="{}" src="{}">'
        img_tags = ""
        for i in os.listdir(directory):
            if not i.endswith(".png"):
                return

            file_path = os.path.join(series_path, i)
            img_tags+=img_tag_template.format(group, file_path)

        template = template.replace("$imgtags", img_tags)
        with open(os.path.join(directory, f"group_{index}.html"), "w") as file:
            file.write(template)
