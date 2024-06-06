"""Class for tracking ratelimits on a per-route basis."""

from dataclasses import dataclass


@dataclass
class Bucket:
    """Data for specific bucket."""

    name: str
    """Name of the route."""

    count: int
    """Number of requests made to the route."""

    reset: float
    """Time at which the bucket resets."""

    reset_after: float
    """Time in seconds until the bucket resets."""

    limit: int
    """Number of requests allowed per bucket."""

    internal_retry_count: int
    """Number of retries made by the client."""


class BucketTrack:
    """Class for tracking ratelimits on a per-route basis."""

    def __init__(
        self,
        buckets: dict[str, Bucket] | None = None,
    ) -> None:
        """Initialize the bucket tracker."""
        self.buckets = buckets or {}

    def increment(self, bucket: Bucket) -> None:
        """Increment the number of requests made to a route."""
        if bucket.name in self.buckets:
            self.buckets[bucket.name].count += 1
        else:
            self.buckets[bucket.name] = bucket

    def update(self, bucket: Bucket) -> None:
        """Update the bucket for a specific route."""
        self.buckets[bucket.name] = bucket
