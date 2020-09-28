import config from './data/config';

export default {
    ...config,
    router: {
        'base_url': ''
    },
    store: {
	'service': '',
	'defaults': {'format': 'json'}
    },
    material: {
        theme: {
            primary: '#550099',
            secondary: '#0dccb1'
        }
    },
    map: {
	bounds: [[44.7, -93.6], [45.2, -92.8]]
    }
}
