const config = {
    store: {
        service: "https://example.com/",
    },
    material: {
        theme: {
            primary: "#7500ae",
            secondary: "#0088bd",
        },
    },
    map: {
        bounds: [
            [-180, -70],
            [180, 70],
        ],
    },
    pages: {
        index: {
            verbose_name: "Home",
            url: "",
            show_in_index: false,
        },
        login: {
            url: "login",
        },
        logout: {
            url: "logout",
        },
        item: {
            url: "items",
            list: true,
            form: [
                {
                    name: "date",
                    label: "Date",
                    hint: "The date when the observation was taken",
                    type: "date",
                },
                {
                    name: "category",
                    label: "Category",
                    hint: "Observation type",
                    type: "select one",
                    "wq:ForeignKey": "category",
                    "wq:related_name": "observation_set",
                },
                {
                    name: "geometry",
                    label: "Location",
                    bind: {
                        required: true,
                    },
                    hint: "The location of the observation",
                    type: "geopoint",
                },
                {
                    name: "photo",
                    label: "Photo",
                    hint: "Photo of the observation",
                    type: "image",
                },
                {
                    name: "notes",
                    label: "Notes",
                    hint: "Field observations and notes",
                    type: "text",
                    multiline: true,
                },
            ],
            verbose_name: "observation",
            verbose_name_plural: "observations",
            ordering: ["-date"],
            label_template: "{{date}}",
        },
        category: {
            cache: "all",
            background_sync: false,
            name: "category",
            url: "categories",
            list: true,
            form: [
                {
                    name: "name",
                    label: "Name",
                    bind: {
                        required: true,
                    },
                    "wq:length": 255,
                    type: "string",
                },
                {
                    name: "description",
                    label: "Description",
                    type: "text",
                },
            ],
            verbose_name: "category",
            verbose_name_plural: "categories",
            label_template: "{{name}}",
        },
    },
};

export default config;
