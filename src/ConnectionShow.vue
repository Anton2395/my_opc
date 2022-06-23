<template>
    <div class="name-connection-area">
        <div class="name-connection">
            <p class="value-pole">{{connect.name}}</p>
        </div>
        <div class="status-area" v-bind:class="{ connectdone: status}"></div>
    </div>
    <div class="parametr-area">
        <table class="table-param">
            <tr class="line-param">
                <td class="name-pole">IP: </td>
                <td class="value-pole">{{connect.ip_addres}}</td>
            </tr>
            <tr class="line-param">
                <td class="name-pole">port: </td>
                <td class="value-pole">{{connect.port}}</td>
            </tr>
            <tr class="line-param">
                <td class="name-pole">Driver: </td>
                <td class="value-pole">{{connect.driver}}</td>
            </tr>
            <tr class="line-param">
                <td class="name-pole">Slot: </td>
                <td class="value-pole">{{connect.slot}}</td>
            </tr>
            <tr class="line-param">
                <td class="name-pole">Rack: </td>
                <td class="value-pole">{{connect.rack}}</td>
            </tr>
        </table>
    </div>
    <div class="button-area">
        <div class="switcher-area">
            <input class="switcher" type="checkbox" id="switcher-run" v-model="runCon" @click="MethodCon">
            <label for="toggle"></label>
        </div>
        <button class="button change" @click="changeModeConnect">Change param</button>
        <button class="button change">Area</button>
    </div>
</template>

<script>
import axios from "axios";

export default {
    props: ['connect', 'status'],
    data() {
        return {
            runCon: false,
        }
    },
    created() {
        this.runCon = this.connect.switchr
    },
    emits: ['clickbut'],
    methods: {
        changeModeConnect() {
            this.$emit('clickbut')
        },
        async MethodCon (event) {
            console.log(1, this.runCon, event.target.checked)
            let count = 0
            if (event.target.checked) {
                while (count<=4) {
                    await axios.post('http://127.0.0.1:8000/start',{
                                id: this.connect.id,
                                name: this.connect.name
                                }, { timeout: 2000 }).then(
                    response => {
                        count = 5;
                        console.log(response.data.status);
                        this.runCon = true;
                    }
                    ).catch( () => {
                        count = count + 1;
                        this.runCon = false;
                    })
                }
            } else {
                while (count<=4) {
                    await axios.post('http://127.0.0.1:8000/stop', {
                                    id: this.connect.id,
                                    name: this.connect.name
                                    }, { timeout: 2000 }).then(
                        response => {
                            count = 5;
                            console.log(response.data.status);
                            this.runCon = false;
                        }
                    ).catch( () => {
                        count = count + 1;
                        this.runCon = true;
                    })
                }
            }
        }
    }
}
</script>

<style>
.name-connection-area {
    /*поля имени и статуса*/
    width: 100%;
    margin: 0 auto;
    /*центрируем ее*/
    height: 30px;
    /*Задаем высоту обертки*/
    border-radius: 5px;
}
.name-connection {
    /*Поле имени*/
    border-radius: 5px;
    height: 10px;
    position: relative;
    float: left;
    /*Задаем обтекание*/
    height: 100%;
    font-size: 16px;
    color: white;
    width: 80%;
    /*Фиксируем ширину блока*/
    text-align: center;
    /*Центрируем текст по горизонтали*/
}

.name-connection p {
    position: absolute;
    top: 50%;
    left: 50%;
    margin-right: -50%;
    transform: translate(-50%, -50%);
}

.status-area {
    /*поле статуса*/
    float: left;
    /*Задаем обтекание*/
    width: 10%;
    height: 80%;
    margin: 3px;
    background: #c34c4c;
    border-radius: 3px;
    box-shadow: 0px 0px 6px #c34c4c;
    transition: box-shadow .3s, background .3s;
}

.connectdone{
    background: #86b959;
    box-shadow: 0px 0px 6px #86b959;
}

.parametr-area {
    padding-top: 2%;
    color: white;
    font-size: 14px;
    margin-bottom: 5px;
}

.parametr {
    /*Параметры*/
    padding-left: 2%;
    font-size: 14px;
    margin-top: 5%;
}

.table-param {
    width: 100%;
}

.name-pole {
    border: 0;
    margin: 0;
    width: 20%;
    padding-top: 5px;
    padding-left: 2%;
    padding-bottom: 5px;
    vertical-align: middle;
    text-align: right;
}

.value-pole {
    border: 0;
    width: 50%;
    margin: 0;
    padding: 0;
    padding-left: 15px;
}

.value-pole input {
    width: 95%;
    height: 100%;
    padding: 0;
    border: none;
    background: none;
    outline: none;
    padding: 0;
    padding-left: 5px;
    color: white;
    font-family: 'newfont';
    font-size: 14px;
    background-color: #605f69;
    border-radius: 3px;
}

.value-pole input:focus {
    background-color: black;
    border: 1px solid;
}

.button-area {
    display: flex;
    margin: 7px;
    align-items: center;
    justify-content: space-around;
}

.switcher-area {
    display: flex;
    align-items: center;
    justify-content: center;
}
input[type="checkbox"] {
    float: left;
    width: 20px;
    height: 10px;
    -webkit-appearance: none;
    -moz-appearance: none;
    background: #ff6d6d;
    outline: none;
    border-radius: 50px;
    box-shadow: inset 0 0 5px rgba(0, 0, 0, .2);
    transition: 0.5s;
    position: relative;
}

input:checked[type="checkbox"] {
    background: #59d663;
}

input[type="checkbox"]::before {
    content: '';
    position: absolute;
    width: 10px;
    height: 10px;
    border-radius: 50%;
    top: 0;
    left: 0;
    background: #fff;
    transform: scale(1.1);
    box-shadow: 0 2px 5px rgba(0, 0, 0, .2);
    transition: 0.3s;
}

input:checked[type="checkbox"]::before {
    left: 10px;
}

.button {
    width: 32%;
    height: 18px;
    -moz-user-select: none;
    -ms-user-select: none;
    -o-user-select: none;
    -webkit-user-select: none;
    user-select: none;
    float: left;
    border-radius: 2px;
    font-size: 10px;
    text-align: center;
    text-transform: uppercase;
    -webkit-transition: all 150ms ease-in-out;
    transition: all 150ms ease-in-out;
}

.change {
    background-color: transparent;
    border: 2px solid #aaff7170;
    color: #fff;
    box-shadow: 0 0 40px 40px #aaff7100 inset, 0 0 0 0 #aaff7100;
}

.button:hover {
    box-shadow: 0 0 4px 0 #3498db00 inset, 0 0 4px 4px #aaff7196;
}

.button:active {
    box-shadow: 0 0 3px 0 #3498db00 inset, 0 0 3px 3px #aaff7196;
}
</style>