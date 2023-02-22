import Test from "./Component";

export default {
    name: "myPlugin",
    actions: {
        setValues(payload) {
            return {
                type: "MYPLUGIN_SET_VALUES",
                payload,
            };
        },
    },
    reducer(state, action) {
        switch (action.type) {
            case "MYPLUGIN_SET_VALUES":
                return { values: action.payload };
            default:
                return state || { values: [] };
        }
    },
    components: {
        Test,
    },
};
