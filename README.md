# sno-fo-fro
<img src=https://github.com/user-attachments/assets/177846f6-5e40-40db-9384-a0e67ac2de2f alt="logo" width="100" align="right">

**Sno-fo-fro** (**sno**w-**fo**g-**fro**st) — это приложение, которое поможет вам определить, какая погода на улице: снежная, туманная или морозная, просто по фотографии. Больше не нужно гадать, глядя в окно!

## Быстрый старт

Начальная настройка
```python
rye sync
```

Запуск
```python
rye run python -m src.sno_fo_fro.app
```

## Интерфейс приложения
![demo](https://github.com/user-attachments/assets/ee7843fa-5ee5-4570-af4d-8eddada99339)


## Гипотезы

На начальном этапе разработки были сформулированы следующие гипотезы. На их основе были разработаны метрики, которые впоследствии использовались для построения классификатора.

1. **Фотографии с туманом имеют меньшую насыщенность.**  **Способ проверки:** посчитать среднюю насыщенность фотографий
2. **Фотографии с туманом имеют меньшую контрастность.** **Способы проверки:** почитать контрастность фотографии как RMS contrast или Michelson contrast
3. **Фотографии с туманом более размытые.** **Способы проверки:** Формула предложенная в [статье](https://pyimagesearch.com/2015/09/07/blur-detection-with-opencv/). Или отслеживание величины изменений после размытия.
4. **Фотографии с морозом имеют большую яркость** (отклонена). **Способы проверки:**  посчитать среднюю яркость изображения как luminance (освещенность) или получить среднее значение value из HSV.
5. **Снежные фотографии имеют наиболее распределённую резкость**: часть изображения с низкой резкостью (снег, снежные шапки) и часть изображения с высокой резкостью (различные объекты) наиболее равны по размерам. В отличие от тумана (где преобладает низкая резкость) и мороза (где большой высокой резкости, так как меньше цвето однородных областей). **Способ проверки:** поделить изображение на отдельные сегменты, в каждом из сегментов оценить резкость и поделить их на группы в зависимости от полученного значения.
6. **Снежные фотографии имеют больше белого цвета.** **Способы проверки:** Задать нижнюю границу белого цвета и считать все остальные пиксели белыми. Если не получится, считать за белый цвет в зависимости от цветов на картинке (провести "баланс белого" перед).
7.  **Снежные фотографии имеют наибольшие перепады в изменении "белизны" цвета.** Снежинки создают резкое изменение цвета (если объект за ними не белый) своим наличием. Но при этом части на фото также могут быть части, где цвет почти не меняется. **Способы проверки:** получение градиента "белизны" цвета через значения Saturation и Value из HSV и расчёт его стандартного отклонения. Если не получится, то модификация формулы с учётом особенностей фотографий.
8. **Показатель "плотность краев" выше для фотогафий с морозом.** **Для проверки гипотезы** (и собственно обнаружения краев) используем алгоритм Сanny.
9. **Фотографии с морозом имеют более холодные цвета, чем снежные фотографии.** **Способ проверки:** Оцениваем преобладание синего (холодного) цвета над красным (тёплого)
10. **Фотографии с морозом чаще содержат небольшие, но яркие блики (от инея, льда), чем фотографии со снегом и туманом.** **Способ проверки:** Изображение переводится в цветовое пространство HSV, где выделяется канал яркости (V). Затем, с помощью локального усреднения и порогового значения, определяются яркие области, отличающиеся от локального окружения, и вычисляется их доля от общего количества пикселей.

## Разработчикам

### Начальная настройка
```python
rye sync && rye run pre-commit install
```

### Запуск тестов
```python
rye test
```

### Запуск эксперимента для проверки гипотез

```python
rye run python -m src.sno_fo_fro.experiment
```

### Обучение модели на датасете `weather-data`

1. Скачать [датасет с изображениями](https://drive.usercontent.google.com/download?id=1DgfRxGJRhEGTGR7H1HbuifFz0TUlbBaG&export=download) и распаковать в корне проекта в папку `weather-data`
2. Запустить `rye run python -m src.sno_fo_fro.scripts.generate_csv` для генерации датасета с метриками `metrics_table.csv`
3. Запустить `ml.ipynb` и дождаться окончания обучения модели (около 10 минут)
4. В директории `pretrained` появится готовая модель
5. По желанию, передать в H2OMLClassifier путь до готовой модели

## Лицензия

Код распространяется под лицензией MIT. Подробнее в файле [LICENCE](LICENCE).
