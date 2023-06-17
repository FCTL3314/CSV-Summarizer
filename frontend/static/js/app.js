new Vue({
    el: '#app-container',
    data: {
        activeTasksCount: null,
        taskIds: [],
        taskResults: [],
    },
    created: function () {
        const vm = this;

        setInterval(function () {
            axios.get('/api/v1/csv/active-tasks/')
                .then(function (response) {
                    vm.activeTasksCount = response.data.count
                })
                .catch(function (error) {
                    console.error(error);
                });
        }, 1000);
    },
    methods: {
        uploadFile() {
            const vm = this;
            const fileInput = this.$refs.fileinput;
            const formData = new FormData();
            formData.append('file', fileInput.files[0]);

            axios.post('/api/v1/csv/upload/', formData, {
                headers: {
                    'Content-Type': 'multipart/form-data',
                }
            })
                .then(function (response) {
                    console.log(response)
                    if (response.status === 201) {
                        vm.taskIds.push(response.data.task_id);
                    }
                    console.log(response.data);
                })
                .catch(function (error) {
                    console.error(error);
                });
        },
        getTaskResult() {
            const vm = this;
            const taskIdInput = this.$refs.taskidinput;

            axios.get(`/api/v1/csv/result/${taskIdInput.value}/`)
                .then(function (response) {
                    if (response.status === 200) {
                        vm.taskResults.push(response.data.result);
                    } else if (response.status === 202) {
                        vm.taskResults.push(response.data.detail);
                    }
                    console.log(response.data);
                })
                .catch(function (error) {
                    console.error(error);
                })
                .finally(function () {
                    taskIdInput.value = '';
                });
        },
    }
})