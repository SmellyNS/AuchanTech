"""
Основная программа:

Вариант с допущением, что это не тестовое задание, а промышленная задача.
Постарался учесть неправильный ввод пользователем и предусмотреть дальнейшее масштабирование проекта.

Так были созданы 3 основных класса:

DefaultVars - для обозначения корневых и результативных директорий. Можно расширить при появлении новых глобальных вводных.
ErrorsClass - описывает возможные ошибки и может быть расширен при появлении новых кейсов
ReaderClass - содержит всю необходимую информацию о читаемых файлах и в нём реализованы основные методы. Может быть расширен новым функционалом и атрибутами

Допущения:
- Результирующий файл для каждого исходного генерируется в том же формате, что исходный;
- Входные данные в файлах разделяются запятой
- Интервалы указываются в формате MININT-MAXINT с вхождением в интервал обоих значений
- Во входных данных могут быть только целые числа.
- Дополнительные символы в исходных файлах, помимо символов "-","," и цифр, могут находиться только в начале и конце файла, и это могут быть лишь двойные кавычки (")
  Данные символы считаются не несущими информации и игнорируются при обработке.
- В случае ошибки при обработке файла генерируется файл по маске "TEST_AUCHAN_error*" c описанием ошибки внутри

Протестировано заменой в файле TEST_AUCHAN_2.txt входных данных на:
"001,2,3,0а16,75,095-130,17,65"
"001,2,3,016,75,195-130,17,65"

В процессе обработки исключений в данном случае намеренно не роняю приложение, для наглядности.
В рядовом случае каждая ошибка отбрасывала бы своё исключение,
чтобы можно было заметить сбой в дашборде, сняться с расписания и отследить ошибку по стектрейсу.

"""
import fnmatch
import os


class DefaultVars:
    def __init__(self):
        self.rootdir = "C:/Users/Дмитрий/PycharmProjects/pythonProject/"
        self.resultdir = "C:/Users/Дмитрий/PycharmProjects/pythonProject/Result/"


class ErrorsClass:

    def __init__(self, err_code):

        self.err_code = err_code
        if err_code == 0:
            self.error_name = "Success"
            self.error_description = "NoDescription"
            self.global_error = False
        if err_code == 1:
            self.error_name = "NoFilesToReadError"
            self.error_description = "[Error] NoFilesToReadError: Не было найдено файлов, доступных для чтения."
            self.global_error = True
        elif err_code == 2:
            self.error_name = "InvalidInputError"
            self.error_description = "[Error] InvalidInputError: Входные данные содержат недопустимые символы"
            self.global_error = False
        elif err_code == 3:
            self.error_name = "InvalidIntervalDefinition"
            self.error_description = ("[Error] InvalidIntervalDefinition: Интервал должен быть указан в формате "
                                      "\"минимум-максимум\"")
            self.global_error = False
        else:
            self.error_name = "UnknownError"
            self.error_description = "[Error] UnknownError: Произошла неизвестная ошибка"
            self.global_error = True

    def printError(self, ReaderInstanse):
        if self.global_error:
            ReaderInstanse.writeResultToFile(

                ReaderInstanse.default_vars.resultdir +
                "TEST_AUCHAN_error_global.txt",

                self.error_description)
        else:
            ReaderInstanse.writeResultToFile(

                ReaderInstanse.default_vars.resultdir +
                "TEST_AUCHAN_error" +
                ReaderInstanse.filename[5:],

                self.error_description)


class ReaderClass:

    def __init__(self, filename, filepath, default_vars):
        self.filename = filename
        self.filepath = filepath
        self.default_vars = default_vars
        self.result_string = self.getResultStringFromFile()

    def writeResultToFile(self, filepath, result):  # Записать результат
        if result is None:
            return 23
        with open(filepath, "w") as currentFile:
            currentFile.write(result)

    def getResultStringFromFile(self):  # Получить результирующую строку на основании переданного файла
        with open(self.filepath, "r") as currentFile:
            currentFileText = currentFile.read()
            if len(currentFileText) == 0:
                return ""

            currentFileText = currentFileText[1:-1] if currentFileText[0] == '"' and currentFileText[
                -1] == '"' else currentFileText

            resultArray = []

            # Думал о том, что эффективно было бы вставлять элементы при формировании сразу на свои места,
            # но пришёл к выводу, что в худшем случае по ходу составления списка каждый раз придётся проходить по нему
            # от начала до конца, что даст приблизительную сложность nlogn. Такая же заявленная сложность у стандартного
            # в python Timsort, поэтому оставил смешанный массив с последующей отдельной сортировкой

            for elem in currentFileText.split(","):  # Итерируем входную строку в виде списка

                if elem.__contains__(
                        "-"):  # Период во всех случаях указан в формате MinInt-MaxInt, поэтому мы можем получить границы интервала, разделив значение по символу "-"
                    try:
                        x1 = int(elem.split("-")[0])
                        x2 = int(elem.split("-")[1])
                    except ValueError:
                        ErrorsClass(2).printError(self)
                        return None
                    if x1 > x2:
                        ErrorsClass(3).printError(self)
                        return None

                    resultArray += [str(i) for i in list(range(x1, x2 + 1))]

                else:
                    try:
                        int(elem)
                    except ValueError:
                        ErrorsClass(2).printError(self)
                        return None
                    resultArray.append(str(int(elem)))

            ## В одном из файлов числа дублируются (хоть и в невалидном по названию).
            ## Задачи дедублицировать не было,
            ## поэтому проигнорировал их наличие.
            ## В случае необходимости дедублицировать достаточно добавить
            ## resultArray = list(set(resultArray))
            return "\n".join(sorted(resultArray, key=lambda a: int(
                a))) + "\n"  # Лямбда-функция позволяет отсортировать итоговый список в порядке возрастания чисел, а не в алфавитном порядке




def getFilesPaths(rootdir):  #Получить список всех полных путей файлов-источников
    filesList = []
    for root, dirnames, filenames in os.walk(rootdir):
        if not root.startswith(rootdir + "Result"):
            for fname in fnmatch.filter(filenames, 'TEST_*'):
                filesList.append(ReaderClass(filename=fname, filepath=root + "/" + fname, default_vars=default_vars))
    if len(filesList) == 0:
        ErrorsClass(1).printError(ReaderClass(filename=None, filepath=None, default_vars=default_vars))
        return None
    else:
        return filesList


def main():
    try:
        for i in getFilesPaths(default_vars.rootdir):  # Записываем результат для каждого найденного файла
            i.writeResultToFile(
                i.default_vars.resultdir +
                "TEST_AUCHAN_success" +
                i.filename[5:], i.result_string)
    except TypeError:
        return 1


if __name__ == "__main__":
    default_vars = DefaultVars()
    main()
