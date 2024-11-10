// static/terminal.js
document.addEventListener('DOMContentLoaded', function() {
    var term = new Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Welcome to the SSH Terminal\n');

    let commandHistory = [];
    let commandIndex = -1;

    term.onKey(e => {
        // Check if Enter key is pressed
        if (e.domEvent.key === 'Enter') {
            e.preventDefault();
            let command = term._core.buffer.xterm.rows[term._core.buffer.ybase + term._core.buffer.y].translateToString(true);
            commandHistory.push(command);
            commandIndex = commandHistory.length;
            term.write('\r\n');
            
            // Send command to server
            sendCommand(command);
        } else if (e.domEvent.key === 'ArrowUp') {
            e.preventDefault();
            if (commandIndex > 0) {
                commandIndex--;
                term.write('\x1b[2K\r' + commandHistory[commandIndex]);
            }
        } else if (e.domEvent.key === 'ArrowDown') {
            e.preventDefault();
            if (commandIndex < commandHistory.length - 1) {
                commandIndex++;
                term.write('\x1b[2K\r' + commandHistory[commandIndex]);
            } else {
                term.write('\x1b[2K\r');
            }
        } else {
            term.write(e.key);
        }
    });

    function sendCommand(command) {
        let hostname = document.getElementById('hostname').value;
        let username = document.getElementById('username').value;
        let password = prompt("Enter your password:");

        fetch('/command', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({
                'command': command,
                'hostname': hostname,
                'username': username,
                'password': password
            })
        }).then(response => response.json())
          .then(data => {
              if (data.status === "success") {
                  term.write(data.output);
                  if (data.error) {
                      term.write(data.error);
                  }
              } else {
                  term.writeln('Error: ' + data.message);
              }
              term.write('\r\n');
              term.write('$ ');
          });
    }

    term.write('$ ');
});