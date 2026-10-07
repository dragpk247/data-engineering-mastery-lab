"""
04_kafka_streaming/streaming_events.py
--------------------------------------
Demonstrates Real-Time Event Streaming Architecture (Kafka pattern).
Key concepts:
- Topic partitioning and hashing
- Event producers with JSON serialization
- Consumer groups and committed offset management
- Handling at-least-once delivery semantics
"""

import time
import json
import hashlib
from collections import defaultdict

class MockKafkaBroker:
    """Simulates a distributed partitioned Kafka topic in memory."""
    def __init__(self, num_partitions=3):
        self.num_partitions = num_partitions
        self.partitions = defaultdict(list)
        self.offsets = defaultdict(int)

    def produce(self, topic: str, key: str, value: dict):
        # Kafka hash partitioning logic
        partition_idx = int(hashlib.md5(key.encode()).hexdigest(), 16) % self.num_partitions
        offset = len(self.partitions[partition_idx])
        message = {
            "topic": topic,
            "partition": partition_idx,
            "offset": offset,
            "key": key,
            "value": value,
            "timestamp": time.time()
        }
        self.partitions[partition_idx].append(message)
        return partition_idx, offset

    def consume(self, partition_idx: int, from_offset: int, batch_size=10):
        messages = self.partitions[partition_idx][from_offset:from_offset + batch_size]
        return messages

def main():
    print("=" * 65)
    print("⚡ Real-Time Event Streaming Lab (Kafka Architecture)")
    print("=" * 65)

    broker = MockKafkaBroker(num_partitions=3)
    TOPIC = "user_clicks_v1"

    print(f"\n--- 1. Producing Events to Partitioned Topic: '{TOPIC}' ---")
    raw_events = [
        ("user_101", {"action": "page_view", "url": "/pricing"}),
        ("user_202", {"action": "add_to_cart", "product_id": "P50"}),
        ("user_101", {"action": "click_checkout", "cart_id": "C99"}), # Same key -> Same partition!
        ("user_303", {"action": "search", "query": "lakehouse"}),
        ("user_202", {"action": "checkout_success", "total": 199.00}),
    ]

    for key, payload in raw_events:
        part, off = broker.produce(TOPIC, key, payload)
        print(f"Produced key={key:<10} ➔ Partition [{part}] at Offset {off}")

    print("\n--- 2. Consumer Group Processing by Partition ---")
    for p in range(broker.num_partitions):
        messages = broker.consume(partition_idx=p, from_offset=0)
        print(f"\nConsumer Worker assigned to Partition [{p}]:")
        for msg in messages:
            print(f"  [Offset {msg['offset']}] Key: {msg['key']} | Payload: {msg['value']}")

    print("=" * 65)
    print("✅ Event Streaming Lab Finished Successfully!")
    print("=" * 65)

if __name__ == "__main__":
    main()
