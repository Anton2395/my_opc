<template>
    <div class="main-body">
        <div class="connection-area">
            <ConnectionList></ConnectionList>
        </div>
    </div>
</template>


<script>
import ConnectionList from './ConnectionList'

export default {
    components: { ConnectionList }
}
</script>

<style>
* {
    margin: 0;
    padding: 0;
    box-sizing: border-box;
}
</style>