class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_mesage(self):
        print(f'Тип тренировки: {self.training_type}')
        print(f'Длительность: {self.duration} ч')
        print(f'Дистанция: {self.distance} км')
        print(f'Средняя скорость: {self.speed} км/ч')
        print(f'Потрачено каллорий: {self.calories}')
    pass


class Training:
    """Базовый класс тренировки."""

    LEN_STEP: float = 0.65
    M_IN_KM: float = 1000.0

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action,
        self.duration = duration,
        self.weight = weight
        pass

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        return self.action * self.LEN_STEP / self.M_IN_KM
        pass

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        return self.get_distance / self.duration
        pass

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(type(self).__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())
        pass


class Running(Training):
    """Тренировка: бег."""

    def get_spent_calories(self) -> float:
        Coeff_caloriea_1: int = 18
        Coeff_caloriea_2: int = 20
        One_hour: int = 60

        return (((Coeff_caloriea_1 * self.get_mean_speed() - Coeff_caloriea_2)
                * self.weight) / self.M_IN_KM * self.duration * One_hour)
    pass


class SportsWalking(Training):
    """Тренировка: спортивная ходьба."""

    def __init__(self,
                 weight: float,
                 growth: float
                 ) -> None:
        self.weight = weight
        self.growth = growth

    def get_mesage(self):

        print(f'Тип тренировки: {self.training_type}')
        print(f'Длительность: {self.duration} ч')
        print(f'Дистанция: {self.distance} км')
        print(f'Средняя скорость: {self.speed} км/ч')
        print(f'Потрачено каллорий: {self.calories}')

    def get_spent_calories(self) -> float:
        Coeff_caloriea_1: int = 0.035
        Coeff_caloriea_2: int = 0.029
        One_hour: int = 60

        return ((Coeff_caloriea_1 * self.weight
                 + (self.get_mean_speed**2 // self.growth)
                 * Coeff_caloriea_2 * self.weight) * One_hour)
    pass


class Swimming(Training):
    """Тренировка: плавание."""

    LEN_STEP: float = 1.38
    M_IN_KN: float = 1000.0

    def __init__(self,
                 length_pool: float,
                 count_pool: float,
                 weight: float,
                 duration: float
                 ) -> None:
        self.length_pool = length_pool
        self.count_pool = count_pool
        self.weight = weight
        self.duration = duration

    def get_mesage(self):
        print(f'Тип тренировки: {self.training_type}')
        print(f'Длительность: {self.duration} ч')
        print(f'Потрачено каллорий: {self.calories}')
        print(f'Длина бассейна: {self.length_pool}м ')
        print(f'Сколько раз пользователь переплыл бассейн: {self.count_pool}')
        print(f'Средняя скорость: {self.speed} км/ч')

    def get_mean_speed(self) -> float:

        return((self.length_pool * self.count_pool
                / self.M_IN_KM / self.duration))

    def get_spent_calories(self) -> float:

        return((self.speed + 1.1) * 2 * self.weight)
    pass


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""

    workout_type_and_class = {
        'SWM': Swimming,
        'RUN': Running,
        'WLK': SportsWalking}
    training = workout_type_and_class[workout_type](*data)
    return training
    pass


def main(training: Training) -> None:
    """Главная функция."""

    info = training.show_training_info()
    print(info.get_message())
    pass


if __name__ == '__main__':
    packages = [
        ('SWM', [720, 1, 80, 25, 40]),
        ('RUN', [15000, 1, 75]),
        ('WLK', [9000, 1, 75, 180]),
    ]

    for workout_type, data in packages:
        training = read_package(workout_type, data)
        main(training)
