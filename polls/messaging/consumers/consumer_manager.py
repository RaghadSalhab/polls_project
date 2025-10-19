import threading
import time
from polls.messaging.messaging_setup import setup_all
from polls.messaging.consumers.choice_consumer import consume_choice_queue
from polls.messaging.consumers.question_consumer import consume_question_queue
from polls.messaging.consumers.user_consumer import consume_user_queue
from polls.messaging.consumers.stats_consumer import consume_stats_queue

def run_all_consumers():
    setup = setup_all()

    threads = [
        threading.Thread(target=consume_question_queue, daemon=True),
        threading.Thread(target=consume_choice_queue, daemon=True),
        threading.Thread(target=consume_user_queue, daemon=True),
        threading.Thread(target=consume_stats_queue, daemon=True),]

    for t in threads:
        t.start()

    print("🎉 All consumers started. Running in background...")
    try:
        while True:
            time.sleep(10)
    except KeyboardInterrupt:
        print("🛑 Stopping consumers...")