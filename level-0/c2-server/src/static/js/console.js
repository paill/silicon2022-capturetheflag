$(function () {
    $('#terminal').terminal({
        help: function() {
            this.echo(`Commands:
              help: print this help output
              beacons: list beacons on hosts
              exec <beacon-id> command: get current user on host
              exec <beacon-id> ls [path]: list files on host
              exec <beacon-id> download [file]: download file from host
              exec <beacon-id> upload [file]: upload file to host
              exec <beacon-id> echo [file]: output contents of file or variable on host
            `);
        },
        beacons: function () {
            $.ajax({
                url: "/beacons",
                success: (response_data) => {
                    var ouput = JSON.stringify(response_data, null, 2)
                    this.echo(ouput);
                },
                error: (response) => {
                    this.echo("error fetching beacons: " + response)
                }
            });
        },
        exec: function (beacon_id, command, ...args) {
            console.log(...args)
            $.ajax({
                url: "/command",
                type: 'POST',
                data: JSON.stringify({ beacon_id: beacon_id, command: command, arg: args}),
                contentType: "application/json; charset=utf-8",
                success: (response_data) => {
                    var ouput = JSON.stringify(response_data, null, 2)
                    this.echo(ouput);
                },
                error: (response) => {
                    this.echo("error running command: " + response)
                },
                xhrFields: {
                    withCredentials: true
                }
            });                
        }
    },
    {
        greetings: greetings.innerHTML,
        checkArity: false
    });
});