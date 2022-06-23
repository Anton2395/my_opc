<template>
    <connection-loading v-if="LoadingFlag" />
    <div v-if="!LoadingFlag">
        <div class="name-connection-area">
            <div class="name-connection">
                <p class="value-pole"><input type="text" v-model="locCon.name"></p>
            </div>
        </div>
        <div class="parametr-area">
            <table class="table-param">
                <tr class="line-param">
                    <td class="name-pole">IP: </td>
                    <td class="value-pole"><input type="text" v-model="locCon.ip_addres"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">port: </td>
                    <td class="value-pole"><input type="text" v-model="locCon.port"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Driver: </td>
                    <td class="value-pole">
                        <select name="asd" v-model="locCon.driver">
                            <option value="Snap7">Snap7</option>
                            <option value="other">Other</option>
                        </select>
                    </td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Slot: </td>
                    <td class="value-pole"><input type="text" v-model="locCon.slot"></td>
                </tr>
                <tr class="line-param">
                    <td class="name-pole">Rack: </td>
                    <td class="value-pole"><input type="text" v-model="locCon.rack"></td>
                </tr>
            </table>
        </div>
        <div class="button-area">
            <transition name="fade">
            <div class="switcher-area" style="width:20px">
            </div>
            </transition>
            <button class="button cancel" @click="cancelClick">Сancel</button>
            <button class="button update" @click="updateClick">Update</button>
        </div>
    </div>
</template>

<script>
import ConnectionLoading from './ConnectionLoading';
import { ElMessage } from 'element-plus';
// import axios from "axios";

export default {
    created() {
        this.locCon = this.connect
    },
    props: ['connect', 'index'],
    data() {
        return {
            locCon: {},
            LoadingFlag: false
        }
    },
    methods: {
        cancelClick() {
            ElMessage('this is a message.')
            this.$emit('cancel')
        },
        async updateClick() {
            // this.LoadingFlag = true
            // let count = 0;
            // let statusStop = false
            // let data = {
            //     name: this.locCon.name,
            //     driver: this.locCon.driver,
            //     ip_addres: this.locCon.ip_addres,
            //     port: this.locCon.port,
            //     slot: this.locCon.slot,
            //     rack: this.locCon.rack,
            //     switchr: false,
            // };
            // if (this.locCon.switchr) {
            //     while (count<=4) {
            //             await axios.post('http://127.0.0.1:8000/stop', {
            //                             id: this.locCon.id,
            //                             name: this.locCon.name
            //                             }, { timeout: 2000 }).then(
            //                 response => {
            //                     if (response.data.status) {
            //                         statusStop = true
            //                         this.locCon.switchr = false
            //                     }
            //                     count = 5;
            //             }).catch( () => {
            //                 count = count + 1;
            //             });
            //     };
            // };
            // if (statusStop) {
            //     try {
            //         let response = await axios.put('http://127.0.0.1:8000/connections/'+this.locCon.id, data);

                    this.$emit('update');
            //         this.LoadingFlag = false
            //     } catch {
            //         this.LoadingFlag = false
            //     }
                
            // }
            
            
            
        }
    },
    components: {
        ConnectionLoading,
    }
}
</script>

<style scoped>

.fade-enter-active, .fade-leave-active {
  transition: opacity .1s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
  opacity: 0;
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