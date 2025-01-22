
# Алгоритм проверки гипотез

Гипотезы, которые необходимо проверить, имеют следующий формат: _Фотографии с погодными условиями_ **target_weather** _имеют_ **compare** _значение_ **target_value**.

- **target_value** — измеряемая характеристика фотографии (например, размытость, контрастность).
- **compare** — знак сравнения («больше» или «меньше»).
- **target_weather** — тип погодных условий (например, снежные, туманные, морозные).

## Процесс проверки гипотез

Для проверки гипотезы сравнивается распределение значений **target_value** в выборке с условиями **target_weather** с соответствующими выборками из двух других типов погодных условий.

### 1. Проверка нормальности распределения

Сначала определяется, имеют ли выборки нормальное распределение. Для этого используются критерии:

- **Критерий Шапиро–Уилка (Shapiro-Wilk test)**
- **Критерий Д’Агостино–Пирсона (D'Agostino-Pearson test)**

Если p-значение обоих тестов больше 0,05, выборка считается нормально распределённой.

### 2. Сравнение выборок

Далее выборки **target_weather** и **other_weather** сравниваются с использованием следующих статистических тестов:

- **Двухвыборочный критерий Колмогорова–Смирнова (Two-sample Kolmogorov-Smirnov test)** — для всех случаев.
- **Двухвыборочный t-критерий (Two-sample t-test)** — применяется, если обе выборки имеют нормальное распределение.
- **Критерий Манна–Уитни (Mann-Whitney U test)** — используется, если хотя бы одна из выборок не является нормально распределённой.

### 3. Интерпретация результатов

Во всех тестах проверяется односторонняя альтернатива в соответствии с направлением сравнения (**compare**), таким образом, чтобы подтверждалась изначальная гипотеза.

- Если во всех тестах p-значение меньше 0,05, гипотеза считается подтверждённой для данной пары выборок (так как принимаются подтверждающие её альтернативы).
- Гипотеза принимается окончательно, если она подтвердится при сравнении выборки **target_weather** с **двумя** другими выборками (**other_weather1** и **other_weather2**).
- В противном случае гипотеза отвергается.

## Результаты эксперимента

В рамках эксперимента была реализована автоматизированная система проверки гипотез. По итогам проверки **9 из 10 гипотез** были подтверждены.

Единственная гипотеза, которая была отклонена, — **«Фотографии с морозом имеют большую яркость»**. Причём это наблюдение осталось неизменным в обеих реализациях гипотезы, использующих разные способы вычисления метрики.


### Детальные результаты


#### Analyze result for proc 'ImageBlurrinessProcessor'

##### Analyze 'fogsmog' less 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(50808.0), pvalue=np.float64(1.313723815467668e-154))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.6557685009487666), pvalue=np.float64(6.628088153970775e-135), statistic_location=np.float64(658.2895143928804), statistic_sign=np.int8(1))

##### Analyze 'fogsmog' less 'frost'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(41892.0), pvalue=np.float64(4.442764865894223e-127))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.6239009287925696), pvalue=np.float64(5.3665958734277033e-104), statistic_location=np.float64(588.3873851950915), statistic_sign=np.int8(1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageBlurrinessProcessor is accepted.

#### Analyze result for proc 'ImageLuminanceProcessor'

##### Analyze 'frost' greater 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: failed
MannwhitneyuResult(statistic=np.float64(42568.0), pvalue=np.float64(1.0))

###### Two-sample Kolmogorov-Smirnov: failed
KstestResult(statistic=np.float64(0.0), pvalue=np.float64(1.0), statistic_location=np.float64(229.40792609869513), statistic_sign=np.int8(-1))

##### Analyze 'frost' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: failed
MannwhitneyuResult(statistic=np.float64(85936.0), pvalue=np.float64(1.0))

###### Two-sample Kolmogorov-Smirnov: failed
KstestResult(statistic=np.float64(0.0), pvalue=np.float64(1.0), statistic_location=np.float64(229.23920996721313), statistic_sign=np.int8(-1))

##### Conclusion
Some tests failed. The hypothesis of ImageProcessor ImageLuminanceProcessor is rejected.

#### Analyze result for proc 'ImageLuminanceProcessor' (through brightness)

##### Analyze 'frost' greater 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: failed
MannwhitneyuResult(statistic=np.float64(57569.0), pvalue=np.float64(1.0))

###### Two-sample Kolmogorov-Smirnov: failed
KstestResult(statistic=np.float64(0.0), pvalue=np.float64(1.0), statistic_location=np.float64(234.5027208108016), statistic_sign=np.int8(-1))

##### Analyze 'frost' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: failed
MannwhitneyuResult(statistic=np.float64(118934.0), pvalue=np.float64(1.0))

###### Two-sample Kolmogorov-Smirnov: failed
KstestResult(statistic=np.float64(0.0), pvalue=np.float64(1.0), statistic_location=np.float64(233.77611525086934), statistic_sign=np.int8(-1))

##### Conclusion
Some tests failed. The hypothesis of ImageProcessor ImageLuminanceProcessor is rejected.

#### Analyze result for proc 'ImageContrastProcessor'

##### Analyze 'fogsmog' less 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(147192.0), pvalue=np.float64(9.29137670766265e-48))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.3471157495256167), pvalue=np.float64(2.176117514937807e-38), statistic_location=np.float64(1683.7204489349128), statistic_sign=np.int8(1))

##### Analyze 'fogsmog' less 'frost'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(100813.0), pvalue=np.float64(5.109202117662816e-52))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.4143034055727554), pvalue=np.float64(2.5497484689240907e-46), statistic_location=np.float64(1725.4043885516378), statistic_sign=np.int8(1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageContrastProcessor is accepted.

#### Analyze result for proc 'ImageSaturationProcessor'

##### Analyze 'fogsmog' less 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(213587.0), pvalue=np.float64(2.646969993778402e-10))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.17802656546489565), pvalue=np.float64(1.1418893337420746e-10), statistic_location=np.float64(13.197056603773586), statistic_sign=np.int8(1))

##### Analyze 'fogsmog' less 'frost'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(42368.0), pvalue=np.float64(2.4102384376055644e-126))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.6520743034055727), pvalue=np.float64(1.5994984846435724e-113), statistic_location=np.float64(36.62994855967078), statistic_sign=np.int8(1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageSaturationProcessor is accepted.

#### Analyze result for proc 'ImageWhiteGradientProcessor'

##### Analyze 'snow' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(438663.0), pvalue=np.float64(1.3285700006299928e-105))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.5398861480075902), pvalue=np.float64(1.0330183354547507e-91), statistic_location=np.float64(58776.724466542495), statistic_sign=np.int8(-1))

##### Analyze 'snow' greater 'frost'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(165627.0), pvalue=np.float64(0.00019758838449943786))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.12524617996604415), pvalue=np.float64(0.00019209206472779316), statistic_location=np.float64(136864.9147619451), statistic_sign=np.int8(-1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageWhiteGradientProcessor is accepted.

#### Analyze result for proc 'ImageWhitenessProcessor'

##### Analyze 'snow' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(367453.5), pvalue=np.float64(1.4319539189950012e-38))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.31309297912713474), pvalue=np.float64(2.2193070960182266e-31), statistic_location=np.float32(0.08771063), statistic_sign=np.int8(-1))

##### Analyze 'snow' greater 'frost'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(231406.0), pvalue=np.float64(1.6377037960549801e-59))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.5262988115449915), pvalue=np.float64(1.1875975513668218e-65), statistic_location=np.float32(0.18236656), statistic_sign=np.int8(-1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageWhitenessProcessor is accepted.

#### Analyze result for proc 'ImageColdnessProcessor'

##### Analyze 'frost' less 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(94320.0), pvalue=np.float64(9.352550866029234e-25))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.40974533106960953), pvalue=np.float64(4.0678930978300085e-40), statistic_location=np.float32(-0.021914005), statistic_sign=np.int8(1))

##### Analyze 'frost' less 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(149731.0), pvalue=np.float64(2.932025304001386e-15))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.34142414860681114), pvalue=np.float64(1.0293554082054872e-31), statistic_location=np.float32(-0.014072556), statistic_sign=np.int8(1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageColdnessProcessor is accepted.

#### Analyze result for proc 'ImageEdgeDensityProcessor'

##### Analyze 'frost' greater 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(175608.0), pvalue=np.float64(2.2785946952454237e-08))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.17903225806451614), pvalue=np.float64(2.74148371023458e-08), statistic_location=np.float32(0.06655714), statistic_sign=np.int8(-1))

##### Analyze 'frost' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(389086.0), pvalue=np.float64(3.69164923755004e-173))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.7894117647058824), pvalue=np.float64(5.655648887448089e-166), statistic_location=np.float32(0.018665342), statistic_sign=np.int8(-1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageEdgeDensityProcessor is accepted.

#### Analyze result for proc 'ImageSegmentsSharpnessProcessor'

##### Analyze 'snow' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(455254.5), pvalue=np.float64(1.254998094676556e-126))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.5915559772296015), pvalue=np.float64(6.143470715031613e-110), statistic_location=np.float32(0.14574899), statistic_sign=np.int8(-1))

##### Analyze 'snow' greater 'frost'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(170993.0), pvalue=np.float64(2.3475168867729748e-06))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.14707979626485568), pvalue=np.float64(7.681609015017876e-06), statistic_location=np.float32(0.4365325), statistic_sign=np.int8(-1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageSegmentsSharpnessProcessor is accepted.

#### Analyze result for proc 'ImageBrightSpotsProcessor'

##### Analyze 'frost' greater 'snow'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(176766.0), pvalue=np.float64(6.31280016592005e-09))
/home/user1/github/university/sno-fo-fro/.venv/lib/python3.12/site-packages/scipy/stats/_axis_nan_policy.py:586: RuntimeWarning: ks_2samp: Exact calculation unsuccessful. Switching to method=asymp.
  res = hypotest_fun_out(*samples, **kwds)

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.17760611205432938), pvalue=np.float64(3.6090625919488726e-08), statistic_location=np.float64(0.1493270475134036), statistic_sign=np.int8(-1))

##### Analyze 'frost' greater 'fogsmog'
Both samples have not a normal distribution.

###### Mann-Whitney U test: passed
MannwhitneyuResult(statistic=np.float64(391138.0), pvalue=np.float64(6.355651489142776e-177))

###### Two-sample Kolmogorov-Smirnov: passed
KstestResult(statistic=np.float64(0.831640866873065), pvalue=np.float64(4.1444722522067324e-184), statistic_location=np.float64(0.05342881944444444), statistic_sign=np.int8(-1))

##### Conclusion
All tests passed. The hypothesis of ImageProcessor ImageBrightSpotsProcessor is accepted.