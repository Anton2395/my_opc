let status_connections_area = {}
let timer_list = {}

function create_button_add(id) {
    $('.area-connections').append(`
    <div id="button-add-connect">
        <p id="add-icon"><img src="/static/img/add_icon.png"></p>
    </div>
    `)
    $('#button-add-connect').click(function () {
        this.remove()
        AddNewConnection()
    });
};

function AddNewConnection() {
    last_id = last_id + 1
    id = last_id
    $('.area-connections').append(`
    <div id="connections`+ id + `" class="connections">
        <div class="name-connection-area">
            <div class="name-connection">
                <p id="name`+ id + `" class="value-pole"><input id="input-name` + id + `" type="text" placeholder="Name"></p>
            </div>
            <div id="status`+ id + `" class="status-area"></div>
        </div>
        <div class="parametr-area">
            <table class="table-param">
                <tr class="line-param">
                    <td class="name-pole">IP: </td>
                    <td class="value-pole" id="ip`+ id + `"><input id="input-ip` + id + `" type="text" placeholder="123.123.123.123"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">port: </td>
                    <td class="value-pole" id="port` + id + `"><input id="input-port` + id + `" type="text" placeholder="102"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Driver: </td>
                    <td class="value-pole" id="driver`+ id + `"><input id="input-driver` + id + `" type="text" placeholder="Snap7"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Slot: </td>
                    <td class="value-pole" id="slot`+ id + `">
                        <input id="input-slot`+ id + `" type="text" placeholder="0">
                    </td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Rack: </td>
                    <td class="value-pole" id="rack`+ id + `"><input id="input-rack` + id + `" type="text" placeholder="1"></td>
                </tr>
            </table>
        </div>
        <div class="button-area" id="button-area`+ id + `">
            <input type="checkbox" id="switcher-run`+ id + `">
            <label for="toggle">
            <button class="button-change" id="save`+ id + `">Save</button>
        </div>
    </div>
    `);
    $('#save' + id).css('border', '2px solid #aaff71')
    $('#save' + id).css('background-color', '#aaff7150')
    $('#save' + id).css('color', 'black')
    $('#switcher-run' + id).prop("disabled", true);
    $('#save' + id).click(function () {
        method_save_connections(id, this);
    });
};

function method_save_connections(id, button_save) {
    data = {
        id: id,
        name: $('#input-name' + id).val(),
        ip: $('#input-ip' + id).val(),
        driver: $('#input-driver' + id).val(),
        slot: $('#input-slot' + id).val(),
        rack: $('#input-rack' + id).val()
    }
    $.post("add_connection", data, function (data, status) {
        if (status == "success") {
            if (data.status) {
                ChangeInputToText(data.connection);
                change_method_front_save(id);
                button_save.remove();
                create_button_add();
            }
            else {
                alert(data.text)
            }
        }
    });
}

function change_method_front_save(id) {
    $('#button-area' + id).append(`
        <button class="button-change" id="change`+ id + `">Change param</button>
        `);
    $('#switcher-run' + id).prop("disabled", false);
    $('#switcher-run' + id).click(function () {
        switcher_background(id, this)
    });
    $('#change' + id).click(function () {
        change_to_form_and_back(id);
    });
};

function switcher_background(id, object) {
    if ($(object).is(':checked')) {
        $('#connections' + id).css("background-color", "#7AA899")
        start_process(id)
        start_check_status_process(id)
    } else {
        stop_check_status_process(id)
        stop_process(id)
        $('#connections' + id).css("background-color", "#6E6C78")
    }
};

function change_to_form_and_back(id) {
    if ($('#change' + id).html() == "Change param") {
        $('#change' + id).html('Update')
        $('#name' + id).html('<input id="input-name' + id + '" type="text" value="' + $('#name' + id).html() + '">')
        $('#ip' + id).html('<input id="input-ip' + id + '" type="text" value="' + $('#ip' + id).html() + '">')
        $('#port' + id).html('<input id="input-port' + id + '" type="text" value="' + $('#port' + id).html() + '">')
        $('#driver' + id).html('<input id="input-driver' + id + '" type="text" value="' + $('#driver' + id).html() + '">')
        $('#rack' + id).html('<input id="input-rack' + id + '" type="text" value="' + $('#rack' + id).html() + '">')
        $('#slot' + id).html('<input id="input-slot' + id + '" type="text" value="' + $('#slot' + id).html() + '">')
        $('#change' + id).html('Update')
        $('#change' + id).css('border', '2px solid #aaff71')
        $('#change' + id).css('background-color', '#aaff7150')
        $('#change' + id).css('color', 'black')
    } else if ($('#change' + id).html() == "Update") {
        $('#name' + id).html($('#input-name' + id).val())
        $('#ip' + id).html($('#input-ip' + id).val())
        $('#port' + id).html($('#input-port' + id).val())
        $('#driver' + id).html($('#input-driver' + id).val())
        $('#rack' + id).html($('#input-rack' + id).val())
        $('#slot' + id).html($('#input-slot' + id).val())
        $('#change' + id).html('Change param')
        $('#change' + id).css('border', '2px solid #aaff7170')
        $('#change' + id).css('background-color', 'transparent')
        $('#change' + id).css('color', '#fff')
    } else {
        alert("что-то пошло не так")
    };
};


function ChangeInputToText(connection) {
    $('#name' + connection.id).html(connection.name)
    $('#ip' + connection.id).html(connection.ip_addres)
    $('#port' + connection.id).html(connection.port)
    $('#driver' + connection.id).html(connection.driver)
    $('#rack' + connection.id).html(connection.rack)
    $('#slot' + connection.id).html(connection.slot)
};


function start_check_status_process(id) {
    timer_list[id] = setTimeout(function run() {
        getStatus($('#name'+id).html(), id);
        timer_list[id] = setTimeout(run, 3000);
    }, 3000);
};

function stop_check_status_process(id) {
    clearTimeout(timer_list[id])
};

function start_process(id) {
    $.post('/start/' + $('#name'+id).html())
};

function stop_process(id) {
    $.post('/stop/' + $('#name'+id).html())
};

function getStatus(name_connection, id) {
    $.get('/status/' + name_connection, function(data){
        if (data.process == true) {
            $('#connections' + id).css("background-color", "#7AA899")
        } else {
            $('#connections' + id).css("background-color", "#FF9898")
        }
    });
};