# polls/messaging/core/config.py
from dataclasses import dataclass
from typing import Dict, List, Optional 

@dataclass
class QueueConfig:
    name: str
    dlq_name: Optional[str] = None
    filter_policy: Optional[Dict] = None

@dataclass
class TopicConfig:
    name: str
    queues: List[QueueConfig]

MESSAGING_CONFIG = {
    "question": TopicConfig(
        name="question-topic",
        queues=[
            QueueConfig(name="question-queue", dlq_name="question-dlq"),
            QueueConfig(
                name="choice-queue", 
                dlq_name="choice-dlq",
                filter_policy={"event_type": ["QUESTION_CREATED", "QUESTION_UPDATED"]}
            )
        ]
    ),
    "choice": TopicConfig(
        name="choice-topic",
        queues=[
            QueueConfig(name="choice-queue", dlq_name="choice-dlq"),
            QueueConfig(
                name="stats-queue",
                dlq_name="stats-dlq", 
                filter_policy={"event_type": ["CHOICE_VOTED"]}
            )
        ]
    ),
    "user": TopicConfig(
        name="user-topic",
        queues=[
            QueueConfig(name="user-queue", dlq_name="user-dlq")
        ]
    ),
    "stats": TopicConfig(
        name="stats-topic",
        queues=[
            QueueConfig(name="stats-queue", dlq_name="stats-dlq")
        ]
    )
}