from polls.messaging.handlers.choice_handlers import ChoiceUpdatedHandler, ChoiceVotedHandler, QuestionCreatedHandler
from polls.messaging.handlers.question_handlers import QuestionUpdatedHandler , QuestionDeletedHandler
from polls.messaging.handlers.stats_handlers import ChoiceVotedHandler
from polls.messaging.handlers.user_handlers import UserCreatedHandler, UserUpdatedHandler, UserDeletedHandler


class HandlerRegistry:
    def __init__(self):
        self._handlers = []
    
    def register(self, handler):
        self._handlers.append(handler)
    
    def get_handler(self, event_type):
        for handler in self._handlers:
            if handler.can_handle(event_type):
                return handler
        return None
    
    
#create registries for different services
choice_registry = HandlerRegistry()
choice_registry.register(QuestionCreatedHandler())
choice_registry.register(ChoiceVotedHandler())
choice_registry.register(ChoiceUpdatedHandler())

question_registry = HandlerRegistry()
question_registry.register(QuestionCreatedHandler())
question_registry.register(QuestionUpdatedHandler())
question_registry.register(QuestionDeletedHandler())

stats_registry = HandlerRegistry()
stats_registry.register(ChoiceVotedHandler())

user_registry = HandlerRegistry()
user_registry.register(UserCreatedHandler())
user_registry.register(UserUpdatedHandler())
user_registry.register(UserDeletedHandler())


