import sys
import asyncio
import os
import lorem

from wws_wrap import StreamSource, StreamOperator, wws_start


class ConversationSource(StreamSource):

    def __init__(self, routing_key, delay=0):
        StreamSource.__init__(self, routing_key)
        self._delay = delay

    async def produce(self):
        while True:
            data = lorem.sentence()
            yield data
            if self._delay:
                await asyncio.sleep(self._delay)

class ConversationTranscript(StreamOperator):

    block_type = 'Transcript'
    function_name = 'transcribe'
    input_ports = [('person1', str), ('person2', str)]
    output_ports = [('transcript', str), ('count1', int), ('count2', int)]
    version = '1.0.0'

    def __init__(self, inputs, outputs, name1: str, name2: str, **kwargs) -> None:
        super(ConversationTranscript, self).__init__(inputs, outputs)
        self._count1 = 0
        self._count2 = 0
        self._name1 = name1
        self._name2 = name2

    def process(self, data, key=None) -> Iterator[Tuple[str, Any]]:
        if key == 'person1':
            self._count1 += 1
            yield 'count1', self._count1
            yield 'transcript', '%s said:\n%s' % (self._name1, data)
        elif key == 'person2':
            self._count2 += 1
            yield 'count2', self._count2
            yield 'transcript', '%s said:\n%s' % (self._name2, data)
        else:
            pass  # unknown input


if __name__ == '__main__':
    ConversationSource('person.one', 1)
    ConversationSource('person.two', 1)
    wws_start()