from models.user import User


def caluclate_bmi(user: User) -> float:
    height_m = user.height / 100
    return round(user.weight / (height_m**2))
