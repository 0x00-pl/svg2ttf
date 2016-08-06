var cli = require("cli")
var child_process = require("child_process")

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

function call_cmd(svg_path, ttf_file, json_file, name_list){
    var cmd = "python3 main.py"+
        " "+svg_path+
        " "+ttf_file+
        " "+json_file

    if(name_list){
        cmd = cmd + " "+name_list
    }
    child_process.exec(cmd, (error, stdout, stderr) => {
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

function call_pipe(config, cb){
    var conf = Object.assign({
        out_ttf: 'out/out.ttf',
        out_json: 'out/out.json',
        svg_path: 'node_modules/open-iconic/svg'
    }, config)
    var conf_json = JSON.stringify(conf)
    var proc = child_process.spwan("python3 main.py")
    proc.stdin.write(conf_json)
    proc.on('close', code=>{
        console.log('proc exit code:', code)
        cb()
    })
}

export.default = call_pipe
