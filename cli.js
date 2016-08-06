#!/usr/bin/env node
# -*- mode: js -*-

const spawn = require('child_process').spawn
const args  = process.argv.slice(2)
const bin = require('./')


// Call.
spawn(bin, args, { stdio: 'inherit' }).on('exit', process.exit)
