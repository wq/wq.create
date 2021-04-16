import wqConfig from './data/config';

const config = {
    ...wqConfig,
    router: {
        'base_url': ''
    },
    store: {
	'service': '',
	'defaults': {'format': 'json'}
    },
    material: {
        theme: {
            primary: '#7500ae',
            secondary: '#0088bd'
        }
    },
    map: {
	bounds: [[-93.6, 44.7], [-92.8, 45.2]]
    }
}

export default config;
