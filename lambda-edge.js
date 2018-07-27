exports.handler = async (event, context, callback) => {
    const response = event.Records[0].cf.response
    const requestUri = event.Records[0].cf.request.uri

    const key = 'x-amz-meta-cloudfront-prefetch'
    const value = '{"prefetch-urls":["' +requestUri+ '"],"/prefetch-manifest":"/manifest.json"}'

    response.headers['x-amz-meta-cloudfront-prefetch'] = [{key:key, value:value}]

    console.log(response.headers['x-amz-meta-cloudfront-prefetch'])

    callback(null, response)
};