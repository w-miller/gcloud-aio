from __future__ import annotations

from typing import Any

from gcloud.aio.auth import BUILD_GCLOUD_REST

if BUILD_GCLOUD_REST:
    pass
else:
    from aioprometheus import Counter, Histogram  # type: ignore[attr-defined]

    _NAMESPACE = 'gcloud_aio'
    _SUBSYSTEM = 'pubsub'

    class _AioShim:
        def __init__(self, cls: type[Counter | Histogram],
                     name: str, doc: str, **kwargs: Any) -> None:
            self._wrapped = cls(name=self._full_name(name), doc=doc, **kwargs)
            self._labels: dict[str, str] = {}

        @staticmethod
        def _full_name(name: str, unit: str = '') -> str:
            return '_'.join(part for part in (
                _NAMESPACE, _SUBSYSTEM, name, unit) if part)

        def __getattr__(self, item: Any) -> Any:
            attr = getattr(self._wrapped, item)
            if callable(attr):
                return lambda *args, **kwargs: attr(
                    self._labels, *args, **kwargs)
            return attr

        def labels(self, **labels: str) -> _AioShim:
            self._labels.update(labels)
            return self

    BATCH_SIZE = _AioShim(
        Histogram,
        'subscriber_batch',
        'Histogram of number of messages pulled in a single batch',
        buckets=(
            0, 1, 5, 10, 25, 50, 100, 150, 250, 500, 1000, 1500, 2000,
            5000, float('inf'),
        ),
    )

    CONSUME = _AioShim(
        Counter,
        'subscriber_consume',
        'Counter of the outcomes of PubSub message consume attempts',
    )

    CONSUME_LATENCY = _AioShim(
        Histogram,
        'subscriber_consume_latency',
        'Histogram of PubSub message consume latencies',
        buckets=(.01, .1, .25, .5, 1.0, 2.5, 5.0, 7.5, 10.0, 20.0,
                 30.0, 60.0, 120.0, float('inf')),
    )

    BATCH_STATUS = _AioShim(
        Counter,
        'subscriber_batch_status',
        'Counter for success/failure to process PubSub message batches',
    )

    MESSAGES_PROCESSED = _AioShim(
        Counter,
        'subscriber_messages_processed',
        'Counter of successfully acked/nacked messages',
    )

    MESSAGES_RECEIVED = _AioShim(
        Counter,
        'subscriber_messages_received',
        'Counter of messages pulled from subscription',
    )
