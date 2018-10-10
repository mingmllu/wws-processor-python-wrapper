from wws_wrap import StreamOperator, wws_start

class JsonHelloWorldOperator(StreamOperator):

    block_type = 'pywrap_json_hello_world'
    input_ports = [('in', str)]
    output_ports = [('out', str)]

    def __init__(self, inputs, outputs, **kwargs):
        StreamOperator.__init__(self, inputs, outputs)

    def process(self, data, key=None):
        yield 'out', 'Hello World'

if __name__ == '__main__':
    wws_start()
