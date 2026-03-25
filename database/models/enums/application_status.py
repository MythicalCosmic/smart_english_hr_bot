import enum



class GenderEnum(enum.Enum):
    male = "male"
    female = "female"


class ApplicationStatusEnum(enum.Enum):
    draft = "draft"
    pending = "pending"
    under_review = "under_review"
    interview_scheduled = "interview_scheduled"
    accepted = "accepted"
    rejected = "rejected"
    withdrawn = "withdrawn"

class LevelEnum(str, enum.Enum):
    secondary = "secondary"
    specialized_secondary = "specialized_secondary"
    incomplete_higher = "incomplete_higher"
    bachelor = "bachelor"
    master = "master"
    # English proficiency levels
    past = "past"
    ortacha = "ortacha"
    ilgor = "ilgor"