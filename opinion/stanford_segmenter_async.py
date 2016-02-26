from nltk import compat
from nltk.internals import find_jar, config_java, java, _java_options

from nltk.tokenize.api import TokenizerI
import tempfile
import os
import json
from subprocess import PIPE
import threading
import Queue
import time


class AsynchronousFileReader(threading.Thread):
    """
    Helper class to implement asynchronous reading of a file
    in a separate thread. Pushes read lines on a queue to
    be consumed in another thread.
    """

    def __init__(self, fd, queue):
        assert isinstance(queue, Queue.Queue)
        assert callable(fd.readline)
        threading.Thread.__init__(self)
        self._fd = fd
        self._queue = queue

    def run(self):
        """The body of the tread: read lines and put them on the queue."""
        for line in iter(self._fd.readline, u''):
            self._queue.put(line)

    def eof(self):
        """Check whether there is no more content to expect."""
        return not self.is_alive() and self._queue.empty()


class StanfordSegmenter(TokenizerI):
    _JAR = 'stanford-segmenter.jar'

    def __init__(self, path_to_jar=None,
                 path_to_sihan_corpora_dict=None,
                 path_to_model=None, path_to_dict=None,
                 encoding='UTF-8', options=None,
                 verbose=False, java_options='-mx2g'):
        self._stanford_jar = find_jar(
            self._JAR, path_to_jar,
            env_vars=('STANFORD_SEGMENTER',),
            searchpath=(),
            verbose=verbose
        )
        self._sihan_corpora_dict = path_to_sihan_corpora_dict
        self._model = path_to_model
        self._dict = path_to_dict

        self._encoding = encoding
        self.java_options = java_options
        options = {} if options is None else options
        self._options_cmd = ','.join('{0}={1}'.format(key, json.dumps(val)) for key, val in options.items())

    def segment_file(self, input_file_path):
        """
        """
        cmd = [
            'edu.stanford.nlp.ie.crf.CRFClassifier',
            '-sighanCorporaDict', self._sihan_corpora_dict,
            '-textFile', input_file_path,
            '-sighanPostProcessing', 'true',
            '-keepAllWhitespaces', 'false',
            '-loadClassifier', self._model,
            '-serDictionary', self._dict
        ]

        stdout = self._execute(cmd)

        return stdout

    def segment(self, tokens):
        return self.segment_sents([tokens])

    def segment_sents(self, sentences):
        """
        """
        encoding = self._encoding
        # Create a temporary input file
        _input_fh, self._input_file_path = tempfile.mkstemp(text=True)

        # Write the actural sentences to the temporary input file
        _input_fh = os.fdopen(_input_fh, 'wb')
        _input = '\n'.join((' '.join(x) for x in sentences))
        if isinstance(_input, compat.text_type) and encoding:
            _input = _input.encode(encoding)
        _input_fh.write(_input)
        _input_fh.close()

        cmd = [
            'edu.stanford.nlp.ie.crf.CRFClassifier',
            '-sighanCorporaDict', self._sihan_corpora_dict,
            '-textFile', self._input_file_path,
            '-sighanPostProcessing', 'true',
            '-keepAllWhitespaces', 'false',
            '-loadClassifier', self._model,
            '-serDictionary', self._dict
        ]

        stdout = self._execute(cmd)

        # Delete the temporary file
        os.unlink(self._input_file_path)

        return stdout

    def _execute(self, cmd, verbose=False):
        encoding = self._encoding
        cmd.extend(['-inputEncoding', encoding])
        _options_cmd = self._options_cmd
        if _options_cmd:
            cmd.extend(['-options', self._options_cmd])

        default_options = ' '.join(_java_options)

        # Configure java.
        config_java(options=self.java_options, verbose=verbose)

        p = java(cmd, classpath=self._stanford_jar, stdout=PIPE, stderr=PIPE, blocking=False)
        stdout_queue = Queue.Queue()
        stdout_reader = AsynchronousFileReader(p.stdout, stdout_queue)
        stdout_reader.start()

        result = ""

        while not stdout_reader.eof():
            while not stdout_queue.empty():
                result += stdout_queue.get().decode('utf-8');
            time.sleep(1)

        stdout_reader.join()

        # Return java configurations to their default values.
        config_java(options=default_options, verbose=False)

        return result

    def setup_module(module):
        from nose import SkipTest

        try:
            StanfordSegmenter()
        except LookupError:
            raise SkipTest(
                'doctests from nltk.tokenize.stanford_segmenter are skipped because the stanford segmenter jar doesn\'t exist')
