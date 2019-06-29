<template>
    <Row align="middle" type="flex">
        <Col span="4"> {{labelContent}}</Col>
        <Col><Input class="register-input" @input="handleInput" :value="textContent" :disabled="disabled" :type="inputType"></Input></Col>
    </Row>
</template>

<script>
    export default {
        name: "InputWithLabel",
        model:{
            prop: 'textContent',
            event: 'input'
        },
        props: [
            'textContent',
            'labelContent',
            'disabled',
            'inputType'
        ],
        methods:{
            handleInput(){
                this.$emit('input',event.target.value)
            },
        },
    }
</script>

<style scoped>
    .register-input{
        width: 300px;
    }
</style>