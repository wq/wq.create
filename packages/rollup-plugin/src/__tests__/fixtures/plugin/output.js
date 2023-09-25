import { modules } from "./wq.js";

const { "@wq/react": react } = modules;
const { usePluginState } = react;

const { "@wq/material": material } = modules;
const { List } = material;
const { ListItem } = material;

const { "@mui/material": muiMaterial } = modules;
const { Grid } = muiMaterial;

const { "react/jsx-runtime": jsxRuntime } = modules;
const { jsx } = jsxRuntime;
const { jsxs } = jsxRuntime;

function Test() {
    const state = usePluginState("myPlugin");
    return /*#__PURE__*/ jsxs(List, {
        children: [
            state.values.map((value) =>
                /*#__PURE__*/ jsx(
                    ListItem,
                    {
                        children: value.label,
                    },
                    value.id
                )
            ),
            /*#__PURE__*/ jsx(ListItem, {
                children: /*#__PURE__*/ jsx(Grid, {}),
            }),
        ],
    });
}

var input = {
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
                return {
                    values: action.payload,
                };
            default:
                return (
                    state || {
                        values: [],
                    }
                );
        }
    },
    components: {
        Test,
    },
};

export { input as default };
