from dataclasses import dataclass, asdict
from typing import Dict, Type


@dataclass


class InfoMessage:
    """Информационное сообщение о тренировке."""

    training_type: str
    duration: float
    distance: float
    speed: float
    calories: float

    def get_message(self) -> str:
        template = ('Тип тренировки: {training_type}; '
                    'Длительность: {duration:.3f} ч.; '
                    'Дистанция: {distance:.3f} км; '
                    'Ср. скорость: {speed:.3f} км/ч; '
                    'Потрачено ккал: {calories:.3f}.')
        return template.format(**asdict(self))


class Training:
    """Базовый класс тренировки."""
    M_IN_KM: int = 1000
    LEN_STEP: float = 0.65
    ONE_HOUR: int = 60
    
    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float) -> None:
        self.action = action
        self.duration_h = duration
        self.weight_kg = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance() / self.duration_h

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        raise NotImplementedError("get_spent_calories не переопределен")

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration_h,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CALORIES_MEAN_SPEED_MULTIPLIER: int = 18
    CALORIES_MEAN_SPEED_DIFFERENCE: int = 20

    def __init__(self, action: int, duration: float, weight: float) -> None:
        super().__init__(action, duration, weight)

    def get_spent_calories(self) -> float:
        return(((self.CALORIES_MEAN_SPEED_MULTIPLIER * self.get_mean_speed()
                 - self.CALORIES_MEAN_SPEED_DIFFERENCE) * self.weight_kg)
               / self.M_IN_KM * self.duration_h * self.ONE_HOUR)


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""
    CALORIES_WEIGHT_MULTIPLIER_1: float = 0.035
    CALORIES_WEIGHT_MULTIPLIER_2: float = 0.029
    
    def __init__(self, action: int, duration: float,
                 weight: float, height: float) -> None:
        super().__init__(action, duration, weight)
        self.height_m = height

    def get_spent_calories(self) -> float:
        return((self.CALORIES_WEIGHT_MULTIPLIER_1 * self.weight_kg
                + (self.get_mean_speed() ** 2 // self.height_m)
                * self.CALORIES_WEIGHT_MULTIPLIER_2 * self.weight_kg)
               * (self.duration_h * self.ONE_HOUR))


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP: float = 1.38
    CALORIES_MEAN_SPEED_SUMMAND: float = 1.1
    CALORIES_WEIGHT_MULTIPLIER: int = 2

    def __init__(self, action: int, duration: float, weight: float,
                 length_pool: float, count_pool: float) -> None:
        super().__init__(action, duration, weight)
        self.length_pool_m = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self) -> float:
        return(self.length_pool_m * self.count_pool
               / self.M_IN_KM / self.duration_h)

    def get_spent_calories(self) -> float:
        return((self.get_mean_speed() + self.CALORIES_MEAN_SPEED_SUMMAND)
               * self.CALORIES_WEIGHT_MULTIPLIER * self.weight_kg)


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    workouts: Dict[str, Type[Training]] = {
        'SWM': Swimming, 'RUN': Running, 'WLK': SportsWalking}
    if workout_type not in workouts:
        raise ValueError('Неизвестная тренировка')
    training = workouts[workout_type](*data)
    return training


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())
if __name__ == '__main__':

    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]
    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)