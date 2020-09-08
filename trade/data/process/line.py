class ProcessLine(object):
    def __init__(self, processors):
        self.processors = processors

    def process(self, stock):
        result_stock = stock
        for processor in self.processors:
            result_stock = processor.process(result_stock)
        return result_stock
