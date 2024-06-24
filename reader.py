"""
Основная программа:

Простой вариант, без учета эффективности, ошибок пользователя и т.д.

Ввиду простоты программы и отсутствия необходимости дальнейшего масштабирования
выполнена без чёткого следования каким-либо парадигмам, но ближе к структурной. с использованием 3 методов


Реализовано 3 функции:

getFilesPaths(rootdir=str()) - Получить список всех полных путей файлов-источников
getResultStringFromFile(filepath=str()): - Получить результирующую строку на основании переданного файла
writeResultToFile(filepath=str(),result=str()) - Записать результат

"""
import fnmatch
import os

# Корневой путь, где находятся директории источников и Result
rootdir = "C:/Users/Дмитрий/PycharmProjects/pythonProject/"

resultdir = rootdir + "Result/"


def getFilesPaths(root_dir):  #Получить список всех полных путей файлов-источников
    filespath = []
    for root, dirnames, filenames in os.walk(root_dir):
        if not root.startswith(root_dir + "Result"):
            for fname in fnmatch.filter(filenames, 'TEST_*'):
                filespath.append(root + "/" + fname)
    return filespath


def getResultStringFromFile(filepath):  # Получить результирующую строку на основании переданного файла
    with open(filepath, "r") as currentFile:
        currentFileText = currentFile.read()[1:-1]  # Во всех файлах содержимое обёрнуто в кавычки. Избавляемся от них.
        resultArray = []
        for elem in currentFileText.split(","):  # Итерируем входную строку в виде списка
            if elem.__contains__(
                    "-"):  # Период во всех случаях указан в формате MinInt-MaxInt, поэтому мы можем получить границы
                # интервала, разделив значение по символу "-"
                x1 = int(elem.split("-")[0])
                x2 = int(elem.split("-")[1])
                resultArray += [str(i) for i in list(range(x1, x2 + 1))]
            else:
                resultArray.append(str(int(elem)))
        ## В одном из файлов числа дублируются (хоть и в невалидном по названию).
        ## Задачи дедублицировать не было,
        ## поэтому проигнорировал их наличие.
        ## В случае необходимости дедублицировать достаточно добавить
        ## resultArray = list(set(resultArray))
        return "\n".join(sorted(resultArray, key=lambda a: int(
            a))) + "\n"  # Лямбда-функция позволяет отсортировать итоговый список в порядке возрастания чисел,
        # а не в алфавитном порядке


def writeResultToFile(filepath, result):  # Записать результат
    with open(filepath, "w") as currentFile:
        currentFile.write(result)


def main():
    for i in getFilesPaths(rootdir):  # Записываем результат для каждого найденного файла
        writeResultToFile(resultdir + "TEST_AUCHAN_success" + i.split("/")[-1][5:], getResultStringFromFile(i))


if __name__ == "__main__":
    main()
