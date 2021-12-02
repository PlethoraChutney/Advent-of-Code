// I also want to use the early, easy puzzles to practice javascript
// I'm running this in node, not a browser window

// Load in the FileSystem module to read files
const { dir } = require('console');
var fs = require('fs');

let input = fs.readFileSync('input.txt', 'utf8');

input = input.split('\n');

// part one

let pos = 0;
let depth = 0;
let aim = 0;
let aim_depth = 0;

for (let i = 0; i < input.length; i++) {
    let line = input[i].split(' ');
    if (line[0] == '') {
        // it seems that js reads in the terminal newline
        continue;
    }
    let direction = line[0];
    let dist = parseInt(line[1]);
    
    switch (direction.charAt(0)) {
        case 'f':
            pos += dist;
            aim_depth += dist * aim;
            break;
        case 'd':
            depth += dist;
            aim += dist;
            break;
        case 'u':
            depth -= dist;
            aim -= dist;
            break;
    }
    
}

console.log(pos * depth);
console.log(pos * aim_depth);