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

    limit: int
    """Number of requests allowed per bucket."""


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

    def get(self, name: str) -> Bucket | None:
        """Get the bucket for a specific route."""
        return self.buckets.get(name)

    def decrement(self, name: str) -> None:
        """Decrement the number of requests made to a route."""
        if name in self.buckets:
            self.buckets[name].count -= 1

    def reset(self, name: str) -> None:
        """Reset the bucket for a specific route."""
        if name in self.buckets:
            self.buckets[name].count = 0

    def set_bucket(self, bucket: Bucket) -> None:
        """Set the bucket for a specific route."""
        self.buckets[bucket.name] = bucket
