#  Copyright 2023 Synnax Labs, Inc.
#
#  Use of this software is governed by the Business Source License included in the file
#  licenses/BSL.txt.
#
#  As of the Change Date specified in that file, in accordance with the Business Source
#  License, use of this software will be governed by the Apache License, Version 2.0,
#  included in the file licenses/APL.txt.
#
#  Use of this software is governed by the Business Source License included in the file
#  licenses/BSL.txt.
#
#  As of the Change Date specified in that file, in accordance with the Business Source
#  License, use of this software will be governed by the Apache License, Version 2.0,
#  included in the file licenses/APL.txt.

import numpy as np
import pandas as pd

from synnax import telem
from synnax.channel.registry import ChannelRegistry
from synnax.telem import NumpyArray, TimeRange, UnparsedTimeStamp
from synnax.transport import Transport

from . import iterator
from .iterator import AUTO_SPAN, NumpyIterator
from .writer import DataFrameWriter


class FramerClient:
    """SegmentClient provides interfaces for reading and writing segmented
    telemetry from a Synnax Cluster. SegmentClient should not be instantiated
    directly, but rather used through the synnax.Synnax class.
    """

    _transport: Transport
    _channels: ChannelRegistry

    def __init__(self, transport: Transport, registry: ChannelRegistry):
        self._transport = transport
        self._channels = registry

    def new_writer(self, start: UnparsedTimeStamp, keys: list[str]) -> DataFrameWriter:
        """Opens a new writer on the given channels.

        :param keys: A list of channel keys that the writer will write to. A writer
        cannot write to keys not provided in this list. See the NumpyWriter documentation
        for more.
        :returns: A NumpyWriter that can be used to write telemetry to the given channels.
        """
        npw = DataFrameWriter(client=self._transport.stream, registry=self._channels)
        npw.open(start, keys)
        return npw

    def new_iterator(
        self,
        keys: list[str],
        tr: TimeRange,
        aggregate: bool = False,
    ) -> NumpyIterator:
        """Opens a new iterator over the given channels within the provided time range.

        :param keys: A list of channel keys to iterator over.
        :param tr: A time range to iterate over.
        :param aggregate:  Whether to accumulate iteration results or reset them on every
        iterator method call.
        :returns: A NumpyIterator over the given channels within the provided time
        range. See the NumpyIterator documentation for more.
        """
        npi = iterator.NumpyIterator(
            transport=self._transport.stream,
            channels=self._channels,
            aggregate=aggregate,
        )
        npi.open(keys, tr)
        return npi

    def write(self, to: str, start: UnparsedTimeStamp, data: np.ndarray):
        """Writes telemetry to the given channel starting at the given timestamp.

        :param to: The key of the channel to write to.
        :param start: The starting timestamp of the first sample in data.
        :param data: The telemetry to write to the channel.
        :returns: None.
        """
        _writer = self.new_writer(start, [to])
        try:
            _writer.write(pd.DataFrame({to: data}))
            _writer.commit()
        finally:
            _writer.close()

    def read(
        self, from_: str, start: UnparsedTimeStamp, end: UnparsedTimeStamp
    ) -> np.ndarray:
        """Reads telemetry from the channel between the two timestamps.

        :param from_: THe key of the channel to read from.
        :param start: The starting timestamp of the range to read from.
        :param end: The ending timestamp of the range to read from.
        :returns: A numpy array containing the retrieved telemetry.
        :raises ContiguityError: If the telemetry between start and end is non-contiguous.
        """
        return self.read_array(from_, start, end)

    def read_array(
        self, from_: str, start: UnparsedTimeStamp, end: UnparsedTimeStamp
    ) -> NumpyArray:
        """Reads a Segment from the given channel between the two timestamps.

        :param from_: The key of the channel to read from.
        :param start: The starting timestamp of the range to read from.
        :param end: The ending timestamp of the range to read from.
        :returns: A NumpySegment containing the read telemetry.
        :raises ContiguityError: If the telemetry between start and end is non-contiguous.
        """
        _iterator = self.new_iterator([from_], TimeRange(start, end), aggregate=True)
        try:
            _iterator.seek_first()
            while _iterator.next(AUTO_SPAN):
                pass
            frame = _iterator.value
        finally:
            _iterator.close()
        return frame[from_]
