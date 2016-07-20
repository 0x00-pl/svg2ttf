var cli = require("cli")


cli.parse({
    name_list: ["l", "only export name in list", "file"],
    svg_path: ["arg0", "svg path", "path"],
    ttf_file: ["arg1", "output ttf file", "path"],
    json_file: ["arg2", "output json file", "path"],
})

cli.main(function(args, options){
    if(args.length < 3){
        cli.getUsage(-1)
    }

    options.svg_path = args[0]
    options.ttf_file = args[1]
    options.json_file = args[2]

    call_cmd(options.svg_path, options.ttf_file, options.json_file, options.name_list)
})


export default function call_cmd(svg_path, ttf_file, json_file, name_list){
    var cmd = "python3 main.py"+
        " "+svg_path+
        " "+ttf_file+
        " "+json_file

    if(name_list){
        cmd = cmd + " "+name_list
    }
    require('child_process')
        .exec(cmd, (error, stdout, stderr) => {
            if (error) {
                console.error(`exec error: ${error}`);
                return;
            }
            console.log(stdout);
            if(stderr){
                console.log(`stderr: ${stderr}`);
            }
        })
}
