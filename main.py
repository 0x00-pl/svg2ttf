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


    def add_char(self, name, svg_path=".", char_code=None):
        #  find a place
        while char_code is None or char_code in self.f:
            char_code = self.char_code
            self.char_code += 1

        file_path = os.path.join(svg_path, name+".svg")
        self.create_char_from_file(char_code, file_path, name)


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

def read_config_form_stdin():
    try:
        config = json.loads(sys.stdin.read())
    except ValueError:
        config = {}

    outttf = config.get('out_ttf', 'out/out.ttf')
    outjson = config.get('out_json', 'out/out.json')

    svg_path = config.get('svg_path', 'node_modules/open-iconic/svg')
    name_list = config.get('name_list', None)

    ff = Ff()
    if name_list is None:
        ff.add_svg_dir(svg_path)
    else:
        for svg_conf in name_list:
            name = svg_conf.get('name', '')
            char_code = svg_conf.get('code', None)
            if char_code is not None:
                char_code = int(char_code, 16)
            ff.add_char(name, svg_path)

    ff.create_files(outttf, outjson)
    print("created file:", outttf, outjson)


if __name__=="__main__":
    if len(sys.argv) < 4:
        #debug_run()
        read_config_form_stdin()
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
                name = line.strip()
                f.add_char(name, svg_path)

        f.create_files(ttf_file, json_file)
        print("created file:", ttf_file, json_file)

