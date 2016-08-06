var cli = require("cli")
var child_process = require("child_process")

cli.parse({
    svg_path: ["arg0", "svg path", "path"],
    out_ttf: ["arg1", "output ttf file", "path"],
    out_json: ["arg2", "output json file", "path"],
    name_list: ["l", "only export name in list", "file"],
})

cli.main(function(args, options){
    if(args.length < 3){
        cli.getUsage(-1)
    }
    // set untaged argds to options
    options.svg_path = args[0]
    options.out_ttf = args[1]
    options.out_json = args[2]
    // call_cmd(options.svg_path, options.ttf_file, options.json_file, options.name_list)
    call_pipe(options)
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
        svg_path: 'node_modules/open-iconic/svg',
        out_ttf: 'out/out.ttf',
        out_json: 'out/out.json',
        name_list: undefined,
    }, config||{})
    var conf_json = JSON.stringify(conf)
    var proc = child_process.spawn("python3", ["main.py"])
    console.log('======')
    proc.stdin.end(conf_json)
    proc.stdout.pipe(process.stdout)
    proc.on('close', code=>{
        console.log('======')
        console.log('proc exit code:', code)
        cb&&cb()
    })
}

exports.default = call_pipe
