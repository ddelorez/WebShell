// static/main.js
window.addEventListener('load', function() {
    var term = new Terminal();
    term.open(document.getElementById('terminal'));
    term.write('Web SSH Terminal\n');

    document.getElementById('connectForm').addEventListener('submit', function(e) {
        e.preventDefault();
        fetch('/connect', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        }).then(response => response.json())
          .then(data => {
              if (data.status === "connected") {
                  term.writeln("Connected to SSH server!");
              } else {
                  term.writeln("Error: " + data.message);
              }
          });
    });
});