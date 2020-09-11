class ProcessLine(object):
    def __init__(self, processors):
        self.processors = processors

    def process_column(self, column):
        result_column = column
        for processor in self.processors:
            result_column = processor.process_column(result_column)
        return result_column

    def process(self, stock):
        result_stock = stock
        for processor in self.processors:
            result_stock = processor.process(result_stock)
        return result_stock
