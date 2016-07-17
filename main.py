import fontforge
import json
import sys
import os

class Ff:
    def __init__(self, code_base=1):
        f = fontforge.font()
        f.encoding = 'UnicodeFull'
        f.design_size = 16
        f.em = 512
        f.ascent = 448
        #  f.design_sizescent = 64

        self.f = f
        self.char_code = code_base


    def create_char_from_file(self, char_code, file_path, name=''):
        if char_code in self.f:
            print("[debug]: char_code", hex(char_code), "is already exist.")
            return

        glyph = self.f.createChar(char_code, name)
        glyph.importOutlines(file_path)


    def add_char(self, name, svg_path="."):
        #  find a place
        while self.char_code in self.f:
            self.char_code += 1

        file_path = os.path.join(svg_path, name+".svg")
        self.create_char_from_file(self.char_code, file_path, name)


    def add_svg_dir(self, svg_path):
        for pwd, dir_names, file_names in os.walk(svg_path):
            for file_name in file_names:
                name,_ = os.path.splitext(file_name)
                self.add_char(name, svg_path)


    def create_font_file(self, file_name):
        self.f.generate(file_name)


    def create_files(self, ttf_path=None, json_path=None):
        if ttf_path is not None:
            self.create_font_file(ttf_path)

        if json_path is not None:
            json_obj = [
                {"name":name, "code":self.f[name].unicode}
            for name in self.f
            ]
            json.dump(json_obj, open(json_path, 'w'))


    def webkit_pathch(file_name):
        svgfile = open(file_name, 'r+')
        svgtext = svgfile.read()
        svgfile.seek(0)
        svgfile.write(svgtext.replace('''<svg>''', '''<svg xmlns="http://www.w3.org/2000/svg">'''))
        svgfile.close()


def debug_run():
    f = Ff()
    f.add_svg_dir("node_modules/open-iconic/svg")
    f.create_files("out/out.ttf", "out/out.json")
    print("created file: out/out.ttf out/out.json")


if __name__=="__main__":
    if len(sys.argv) < 4:
        debug_run()
    else:
        svg_path = sys.argv[1]
        ttf_file = sys.argv[2]
        json_file = sys.argv[3]
        export_list_file = None

        if len(sys.argv) > 4:
            export_list_file = sys.argv[4]

        f = Ff()

        if export_list_file is None:
            f.add_svg_dir(svg_path)
        else:
            for line in open(export_list_file, 'r'):
                f.add_char(line, svg_path)

        f.create_files(ttf_file, json_file)
        print("created file:", ttf_file, json_file)

