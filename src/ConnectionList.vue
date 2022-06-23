<template>
    <!-- <transition name="fade">
    <div 
        v-show="RClickMenu.status"
        style="position: absolute; z-index:1; height: 100%; width: 100%;"
        @click="RClickMenu.status = false"
        >
    <div  class="menuRclick" :style="'left: '+RClickMenu.x+'px; top: '+RClickMenu.y+'px;'">
        asdasd
    </div>
    </div>
    </transition> -->
    <div
        class="connection"
        @contextmenu.prevent="ShowRClick(item.id, $event)"
        v-for="item, index in Connections" :key="item.name"
        v-bind:class="{ workproc: statusProc[item.name]}"
    >
    <connection-show
        @clickbut="changeModeConnect(index)"
        v-if="!item.statusChange"
        :connect="item"
        :status="statusConn[item.name]"
        @contextmenu.prevent="Test"
    />
    <connection-change
        @cancel="changeModeConnect(index)"
        @update="changeModeConnect(index)"
        v-if="item.statusChange"
        :connect="item"
        :index="index"
    />
    </div>
    <add-button
        v-if="!addFormShow"
        @click="Check"
        @addconn="AddCon"
    />

</template>


<script>
import AddButton from './AddButton';
import ConnectionShow from './ConnectionShow';
import ConnectionChange from './ConnectionChange';
import axios from "axios";

export default {
    data() {
        return {
            addFormShow: false,
            Connections: [],
            RClickMenu: {
                status: false,
                x: 110,
                y: 110
            },
            statusProc: {},
            statusConn: {}
        };
    },
    components: {
        AddButton,
        ConnectionShow,
        ConnectionChange,
    },
    methods: {
        AddCon(Conn) {
            this.addFormShow = false
            this.Connections.push({
                    id: 2,
                    name: Conn.name,
                    status: 0,
                    ip_addres: Conn.ip_addres,
                    port: Conn.port,
                    driver: Conn.driver,
                    slot: Conn.slot,
                    rack: Conn.rack,
                    statusChange:false
                });
        },
        changeModeConnect: function(index) {
            // console.log(index)
            this.Connections[index].statusChange = !this.Connections[index].statusChange
        },
        Check: function() {
            this.addFormShow = !this.addFormShow
        },
        ShowRClick(idConnection, event) {
            console.log(idConnection);
            console.log(event)
            this.RClickMenu.x = event.x + 10
            this.RClickMenu.y = event.y + 10
            this.RClickMenu.status = true
        },
        async getStatusData() {
            let response = await axios.get('http://127.0.0.1:8000/status/proc');
            this.statusProc = response.data;
            response = await axios.get('http://127.0.0.1:8000/status/conn');
            this.statusConn = response.data;
        }
    },
    created() {
        let getStatusData = this.getStatusData
        axios.get('http://127.0.0.1:8000/connections/').then(
            response => {
                console.log(response)
                this.Connections = response.data
            }
        );
        setInterval(function() {
                getStatusData()
            }, 3000);

    },
}

// async function getStatusData() {
//     let response = await axios.get('http://127.0.0.1:8000/status/proc')
//     return response.data
// }
</script>


<style>

.menuRclick {
    position: absolute;
    z-index: 10;
    height: 50px;
    width: 200px;
    background-color: yellow;
}

.fade-enter-active, .fade-leave-active {
  transition: opacity .3s;
}
.fade-enter, .fade-leave-to /* .fade-leave-active до версии 2.1.8 */ {
  opacity: 0;
}
.connection {
    /*поле одного соединения*/

    border-radius: 5px;
    float: left;
    background-color: #6E6C78;
    margin: 5px;
    height: 215px;
    width: 300px;
    /*Фиксируем ширину блока*/
    transition: box-shadow .3s, background .3s;
}

.connection:hover {
    box-shadow: 0px 0px 5px #9c9aa7;
}

.workproc {
    background-color: rgb(122, 168, 153);
}
</style>