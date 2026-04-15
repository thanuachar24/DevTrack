from abc import ABC, abstractmethod


class BaseEntity(ABC):
    @abstractmethod
    def validate(self):
        pass

    def to_dict(self):
        return {
            key: value
            for key, value in self.__dict__.items()
        }
    
    def describe(self):
        pass

class Reporter(BaseEntity):
    def __init__(self, id, name, email, team):
        self.id = id
        self.name = name
        self.email = email
        self.team = team

    def validate(self):
        if not self.name:
            raise ValueError('Name cannot be empty')

        if '@' not in self.email:
            raise ValueError('Invalid email')

        if not self.team:
            raise ValueError('Team cannot be empty')

class Issue(BaseEntity):
    def __init__(self, id, title, description, status, priority, reporter_id, created_at=None):
        self.id = id
        self.title = title
        self.description = description
        self.status = status
        self.priority = priority
        self.reporter_id = reporter_id
        self.created_at = created_at
    
    def validate(self):
        if self.reporter_id is None:
            raise ValueError('Reporter-ID cannot be empty')
        
        if not self.title:
            raise ValueError('Title cannot be empty')

        allowed_status = ["open", "in_progress", "resolved", "closed"]
        
        if self.status not in allowed_status:
            raise ValueError('Invalid status')

        allowed_priority = ["low", "medium", "high", "critical"]

        if self.priority not in allowed_priority:
            raise ValueError('Invalid priority')

    def describe(self):
        return f"{self.title} [{self.priority}]"


class CriticalIssue(Issue):
    def describe(self):
        return f"[URGENT] {self.title} - needs immediate attention!"

class LowPriorityIssue(Issue):
    def describe(self):
        return f"{self.title} — low priority, handle when free"