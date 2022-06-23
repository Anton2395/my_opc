<template>
    <div class="but" v-if="!ChangeMode" @click="ChangeModeMethod">
            <p id="add-icon"><img src="@/assets/img/add_icon.png"></p>
    </div>
    
    
    <div class="connection" v-if="ChangeMode">
    <connection-loading v-if="ShowLoading" />
    <v-if v-if="!ShowLoading" >
        <div class="name-connection-area">
            <div class="name-connection">
                <p class="value-pole"><input type="text" v-model="newConnect.name"></p>
            </div>
            <div class="status-area"></div>
        </div>
        <div class="parametr-area">
            <table class="table-param">
                <tr class="line-param">
                    <td class="name-pole">IP: </td>
                    <td class="value-pole"><input type="text" v-model="newConnect.ip_addres"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">port: </td>
                    <td class="value-pole"><input type="text" v-model="newConnect.port"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Driver: </td>
                    <td class="value-pole">
                        <select name="asd" v-model="newConnect.driver">
                            <option value="Snap7" checked>Snap7</option>
                        </select>
                    </td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Slot: </td>
                    <td class="value-pole"><input type="text" v-model="newConnect.slot"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Rack: </td>
                    <td class="value-pole"><input type="text" v-model="newConnect.rack"></td>
                </tr>
            </table>
        </div>
        <div class="button-area">
            <button class="button change" @click="ChangeModeMethod">Сancel</button>
            <button class="button update" @click="AddCon">Save</button>
        </div>
    </v-if>
    </div>
</template>

<script>
import axios from "axios";
import ConnectionLoading from './ConnectionLoading'

export default {
    data() {
        return {
            ShowLoading:false,
            newConnect: {
                name:'',
                ip_addres:'',
                port:'',
                driver:'',
                slot:'',
                rack:''
            },
            ChangeMode: false
        };
    },
    emits: ['addconn'],
    methods: {
        ChangeModeMethod() {
            // console.log(1)
            this.ChangeMode = !this.ChangeMode
        },
        AddCon() {
            console.log(this.newConnect)
            this.ShowLoading = true
            axios.post('http://localhost:8000/connections', this.newConnect)
                .then(response => {
                    console.log(response)
                    this.$emit('addconn', this.newConnect)
                    this.newConnect = {
                        name:'',
                        ip_addres:'',
                        port:'',
                        driver:'',
                        slot:'',
                        rack:''
                    }
                    this.ShowLoading = false
                    this.ChangeMode = !this.ChangeMode
                })
                .catch(error => {
                    console.log(error.response.status)
                    this.ShowLoading = false
                })
            
            
        }
    },
    components: {
        ConnectionLoading
    }
}
</script>

<style scoped>
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

.cancel {
    border: 2px solid #aaff71;
    background-color: #cf662e80;
    color: white;
}
.update {
    border: 2px solid #aaff71;
    background-color: #aaff7150;
    color: white;
    
}
.but {
    border: 2px solid #8e8d96;
    border-radius: 5px;
    float: left;
    height: 215px;
    width: 300px;
    background-color: #8e8d96;
    margin: 5px;
    transition: background-color .3s, border-color .3s, box-shadow .2s;
    -moz-user-select: none;
    user-select: none;
}

.but p {
    display: table-cell;
    height: 200px;
    width: 300px;
    vertical-align: middle;
}

.but img {
    margin: auto;
    width: 30%;
    height: 40%;
    opacity: 0.2;
    display: block;
    pointer-events: none;
}

.but:hover {
    /* background-color: #3B3A3D; */
    box-shadow: 0px 0px 10px white;
}

.but:active {
    border-color: #68676b;
    background-color: #4e4d52;
    box-shadow: 0px 0px 3px #9c9aa7;
    ;
}
</style>