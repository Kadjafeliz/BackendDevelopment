class InfoMessage:
    """Информационное сообщение о тренировке."""

    def __init__(self,
                 training_type: str,
                 duration: float,
                 distance: float,
                 speed: float,
                 calories: float
                 ) -> None:
        self.training_type = training_type
        self.duration = duration
        self.distance = distance
        self.speed = speed
        self.calories = calories

    def get_message(self):
        message = (f'Тип тренировки: {self.training_type};\n'
                   f'Длительность: {self.duration:.3f} ч.; \n'
                   f'Дистанция: {self.distance:.3f} км;\n'
                   f'Ср. скорость: {self.speed:.3f} км/ч;\n'
                   f'Потрачено ккал: {self.calories:.3f}.\n\n')
        return message


class Training:
    """Базовый класс тренировки."""
    M_IN_KM = 1000
    LEN_STEP = 0.65
    CALORIES_MEAN_SPEED_MULTIPLIER = 18
    CALORIES_MEAN_SPEED_SHIFT = 1.79
    MINUTES_IN_HOUR = 60

    def __init__(self,
                 action: int,
                 duration: float,
                 weight: float,
                 ) -> None:
        self.action = action
        self.duration = duration
        self.weight = weight

    def get_distance(self) -> float:
        """Получить дистанцию в км."""
        dist = self.action * self.LEN_STEP / self.M_IN_KM
        return dist

    def get_mean_speed(self) -> float:
        """Получить среднюю скорость движения."""
        mean_speed = self.get_distance() / self.duration
        return mean_speed

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        pass

    def show_training_info(self) -> InfoMessage:
        """Вернуть информационное сообщение о выполненной тренировке."""
        return InfoMessage(self.__class__.__name__, self.duration,
                           self.get_distance(), self.get_mean_speed(),
                           self.get_spent_calories())


class Running(Training):
    """Тренировка: бег."""
    CONST1 = 18
    CONST2 = 1.79

    def get_spent_calories(self) -> float:
        """Получить количество затраченных калорий."""
        var1 = (self.CONST1 * self.get_mean_speed() + self.CONST2)
        var2 = (self.weight / self.M_IN_KM * self.duration
                * self.MINUTES_IN_HOUR)
        calories = var1 * var2
        return calories


class SportsWalking(Training, ):
    """Тренировка: спортивная ходьба."""

    WK_CONST1 = 0.035
    WK_CONST2 = 0.029
    KM_HOUR_RATIO = 0.278
    EOTK_2 = 100

    def __init__(self, action, duration, weight, height):
        super().__init__(action, duration, weight)
        self.height = height

    def get_spent_calories(self) -> float:
        mean_square = ((self.get_mean_speed()
                        * self.KM_HOUR_RATIO) ** 2)
        speed_ht = mean_square / (self.height / self.EOTK_2)
        calories = ((self.WK_CONST1 * self.weight + (speed_ht * self.WK_CONST2
                    * self.weight)) * self.duration
                    * self.MINUTES_IN_HOUR)
        return calories


class Swimming(Training):
    """Тренировка: плавание."""
    LEN_STEP = 1.38
    SW_CONST1 = 1.1
    SW_CONST2 = 2

    def __init__(self, action, duration, weight, length_pool, count_pool):
        super().__init__(action, duration, weight)
        self.length_pool = length_pool
        self.count_pool = count_pool

    def get_mean_speed(self):
        mean_speed = (self.length_pool * self.count_pool / self.M_IN_KM
                      / self.duration)
        return mean_speed

    def get_spent_calories(self):

        calories = ((self.get_mean_speed() + self.SW_CONST1) * self.SW_CONST2
                    * self.weight * self.duration)
        return calories


def read_package(workout_type: str, data: list) -> Training:
    """Прочитать данные полученные от датчиков."""
    train = {'RUN': Running,
             'WLK': SportsWalking,
             'SWM': Swimming}
    if workout_type not in train:
        return 'Empty'
    return train[workout_type](*data)


def main(training: Training) -> None:
    """Главная функция."""
    if training == 'Empty':
        print("Такого типа тренировки нет, попробуйте еще раз!")
    else:
        calc = training.show_training_info()
        print(calc.get_message())


if __name__ == '__main__':

    print("""
Прежде чем перейти к вводу значений, рекомендую 
ознакомиться с инструкцией в файле README.\n""")
    workout_type = input("Введите тип тренировки: \n")
    input_string = input("Введите значения тренировки, разделённые пробелами: \n")
    data = list(map(int, input_string.split()))
    training = read_package(workout_type, data)
    main(training)

