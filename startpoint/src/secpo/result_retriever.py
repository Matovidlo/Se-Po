""" This module is created by Martin Vasko.
    Output of the finished container or VM task is result.
    It is expected to retrieve this result by copying it back to host OS.
    On this result can be applied filter or highlighter because of
    possible false positives, true negatives etc.
"""

import functools


class ResultRetriever:
    def __init__(self, result_highlighter=None):
        """ Initialize """
        self.security_results = None
        self.portability_results = None
        if result_highlighter and isinstance(result_highlighter,
                                             ResultHighlighter):
            self.highlighter = result_highlighter
        else:
            self.highlighter = ResultHighlighter()

    def retrieve(self):
        """
        Retrieve results from docker container. Copy files from execution of
        external tools.
        :return:
        """
        pass

    def perform_filter(self):
        """
        Perform filtering using ResultHighlighter and custom driven function.
        :return:
        """
        self.highlighter.highlight()


class ResultHighlighter:
    def __init__(self, user_function=None, *args, **kwargs):
        """ Initialize """
        self.user_function = self._config
        if user_function:
            self.user_function = user_function
        self.args = args
        self.kwargs = kwargs

    def _config(self, *args, **kwargs):
        """
        User driven function for pre configuration of highlighting.
        This function should be blank and custom user function
        should be implemented in order to highlight.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def _highlight(self, *args, **kwargs):
        """
        Common highlight function of retrieved result.
        :param args:
        :param kwargs:
        :return:
        """
        pass

    def highlight(self):
        @functools.wraps(self.user_function)
        def run(*args, **kwargs):
            self.user_function(*args, **kwargs)
            self._highlight(*args, **kwargs)
        return run(*self.args, **self.kwargs)


def my_highlight(config):
    print(config)
    pass


if __name__ == '__main__':
    highlighter = ResultHighlighter(my_highlight, ['file'])
    result = ResultRetriever(highlighter)
    result.perform_filter()