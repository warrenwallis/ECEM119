const { exec } = require('child_process');

exec('python json.py', (error, stdout, stderr) => {
    console.log('1', stdout, '2');
    console.log('after');
});
