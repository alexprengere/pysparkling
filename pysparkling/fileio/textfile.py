from __future__ import absolute_import, unicode_literals

import logging
from io import StringIO

from . import codec
from .file import File

log = logging.getLogger(__name__)


class TextFile(File):
    """
    Derived from :class:`pysparkling.fileio.File`.

    :param file_name:
        Any text file name. Supports the schemes ``http://``, ``s3://`` and
        ``file://``.

    """

    def __init__(self, file_name):
        File.__init__(self, file_name)

    def load(self, encoding='utf8'):
        """
        Load the data from a file.

        :param encoding: (optional)
            The character encoding of the file.

        :returns:
            An ``io.StringIO`` instance. Use ``getvalue()`` to get a string.

        """
        if type(self.codec) == codec.Codec and \
           getattr(self.fs, 'load_text'):
            print(self.codec)
            stream = self.fs.load_text()
        else:
            stream = self.fs.load()
            stream = StringIO(
                self.codec.decompress(stream).read().decode(encoding)
            )
        return stream

    def dump(self, stream=None, encoding='utf8'):
        """
        Writes a stream to a file.

        :param stream:
            An ``io.StringIO`` instance.

        :param encoding: (optional)
            The character encoding of the file.

        :returns:
            self

        """
        if stream is None:
            stream = StringIO()

        stream = self.codec.compress(stream.read().encode(encoding))
        self.fs.dump(stream)

        return self