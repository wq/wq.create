import { modules } from './wq.js';

const { react: React } = modules;

const { '@wq/react': react } = modules;

const { '@wq/material': material } = modules;

function Test() {
    const state = react.usePluginState('myPlugin');
    return /*#__PURE__*/ React.createElement(
        material.List,
        null,
        state.values.map(value =>
            /*#__PURE__*/ React.createElement(
                material.ListItem,
                {
                    key: value.id
                },
                value.label
            )
        )
    );
}

var input = {
    name: 'myPlugin',
    actions: {
        setValues(payload) {
            return {
                type: 'MYPLUGIN_SET_VALUES',
                payload
            };
        }
    },

    reducer(state, action) {
        switch (action.type) {
            case 'MYPLUGIN_SET_VALUES':
                return {
                    values: action.payload
                };

            default:
                return (
                    state || {
                        values: []
                    }
                );
        }
    },

    components: {
        Test
    }
};

export default input;
