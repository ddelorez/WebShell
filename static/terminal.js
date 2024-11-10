// static/terminal.js
document.addEventListener('DOMContentLoaded', function() {
    var term = new Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Welcome to the SSH Terminal\n');

    // Here you would implement the logic for SSH command execution and output display
    term.onKey(e => {
        term.write(e.key);
        // Implement SSH command sending here
    });
});