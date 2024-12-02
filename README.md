[![Get MOEX data](https://github.com/ruslanbay/moex/actions/workflows/getMoexData.yml/badge.svg?branch=main&event=schedule)](https://github.com/ruslanbay/moex/actions/workflows/getMoexData.yml)
[![Get currency exchange rate](https://github.com/ruslanbay/moex/actions/workflows/getCurrency.yml/badge.svg?branch=main&event=schedule)](https://github.com/ruslanbay/moex/actions/workflows/getCurrency.yml)
[![Update history.tsv](https://github.com/ruslanbay/moex/actions/workflows/updateHistoryTsv.yml/badge.svg?branch=main&event=schedule)](https://github.com/ruslanbay/moex/actions/workflows/updateHistoryTsv.yml)
[![Update Ticket List](https://github.com/ruslanbay/moex/actions/workflows/updateTicketList.yml/badge.svg?branch=main&event=schedule)](https://github.com/ruslanbay/moex/actions/workflows/updateTicketList.yml)

# Визуализация данных Мосбиржи. Как российский фондовый рынок изменился за последние 10 лет

Данная визуализация показывает объём торгов по стоимости и количеству сделок, капитализацию рынка. Доступно два типа визуализации: в динамике (histogram) и в разрезе (treemap). Все графики интерактивные, можно кликать, зумить. Экспериментируйте! :)


<details>
  <summary>PATHBAR ДЛЯ УДОБНОЙ НАВИГАЦИИ</summary>
  <img src="images/article/treemap_pathbar.gif" />
</details>

<details>
  <summary>SEARCHBOX ДЛЯ БЫСТРОГО ПОИСКА ПО ТИКЕРАМ</summary>
  <img src="images/article/treemap_searchbox.gif" />
</details>

<details>
  <summary>ФИЛЬТР ЦЕННЫХ БУМАГ</summary>
  Чтобы на treemap отобразить только выбранные бумаги, перечислите их тикеры и сохраните в txt файл. После этого кликните по кнопке 🛄 и выберете ваш файл. Все данные обрабатываются на вашем устройстве, на сервер ничего не отправляется. Пример содержимого файла portfolio.txt:

```
ticker
GAZP
PLZL
YDEX
```
  <img src="images/article/treemap_filter.gif" />
</details>

<details>
  <summary>СБРОСИТЬ ФИЛЬТР</summary>
  <img src="images/article/treemap_erase_filter.gif" />
</details>

 
<details>
  <summary>ОТКРЫТЬ ГИСТОГРАММУ</summary>
  <img src="images/article/histogram.gif" />
</details>

<details>
  <summary>СКРЫТЬ ЭЛЕМЕНТ НА ГРАФИКЕ</summary>
  Кликните по элементу легенды, чтобы его скрыть. Кликните дважды, чтобы скрыть всё кроме выбранного элемента
  <img src="images/article/histogram_legend.gif" />
</details>

<details>
  <summary>ВЫБРАТЬ ВРЕМЕННОЙ ОТРЕЗОК НА ГИСТОГРАММЕ</summary>
  Чтобы выбрать период, за который вы хотите посмотреть данные, можете использовать кнопки `1 year`, `6 months`, `1 month`, либо выделить часть графика

  <img src="images/article/histogram_rangeselector.gif" /> <img src="images/article/histogram_zoom.gif" />
</details>

<details>
  <summary>УСТАНОВИТЬ ПРИЛОЖЕНИЕ</summary>
  Чтобы установить приложение нажмите кнопку `Install` в нижней части экрана

  <img src="images/article/install.jpg" />
</details>

<details>
  <summary>УСТАНОВИТЬ НА IPHONE ИЛИ IPAD</summary>

  <img src="images/article/install_ios.gif" />
</details>


<details>
  <summary>УСТАНОВИТЬ В FIREFOX</summary>

  <img src="images/article/install_firefox.gif" />
</details>

<details>
  <summary>БЫСТРЫЕ ССЫЛКИ</summary>
  В Windows по правый клик на ярлык приложения вызывает меню с быстрыми ссылками на Treemap, History и Listings

  <img src="images/article/windows_shortcuts.jpg" />
</details>

<details>
  <summary>ПОДЕЛИТЬСЯ</summary>
  
  Пожалуйста, расскажите о проекте друзьям и коллегам!

  <img src="images/article/share.gif" />
</details>

Ниже пример использования для анализа данных Мосбиржи.

Мосбиржа предоставляет данные с декабря 2011 года. За прошедшие 13 лет общая рублёвая капитализация компаний, представленных на бирже, удвоилась: с 24 до 50 триллионов. Если посмотреть этот же график в других валютах, увидим что рубль потерял 2/3 стоиомсти, а общая капитализация рынка снизилась примерно на четверть.

![](images/article/history-total-rub.jpeg)

![](images/article/history-rub-vs-usd.jpeg)

![](images/article/history-total-usd.jpeg)

![](images/article/treemap-cap-2011-12-19.jpeg)

![](images/article/treemap-cap-2024-10-10.jpeg)

Число отечественных компаний, представленных на бирже, достигло пика в ноябре 2012 года и с тех пор снижается.

![](images/article/listing-total.jpeg)

![](images/article/listing-new.jpeg)

Ниже таблица с распределением секторов в общей капиталазации рынка.

|Сектор                    |2011-12-19|2024-11-14|
|--------------------------|----------|----------|
|Нефть, газ                |52%       |44%       |
|Финансы                   |12%       |19%       |
|Металлы                   |12%       |15%       |
|Информационные технологии |0.04%     |4.1%      |
|Электроэнергетика         |9%        |3.8%      |
|Химпром и нефтехимия      |4%        |3.4%      |
|Промышленность            |1.1%      |3%        |
|Транспорт                 |0.85%     |2%        |
|Потребительский сектор    |2.7%      |2%        |
|Телекоммуникации          |3.8%      |1.6%      |
|Строительство             |0.37%     |1.1%      |
|Холдинги                  |0.96%     |0.68%     |
|Здравоохранение           |0.33%     |0.58%     |

Из-за большой доли нефтегазовых компаний-экспортёров, курс рубля и капитализация рынка коррелируют со стоимостью нефти.

![](images/article/history-cap-usd-vs-brent.jpeg)
![](images/article/rub-vs-oil.jpeg)

В 2017 году ЦБР начал применять бюджетное правило, согласно которому бюджет формировался исходя из ожидаемой стоимости Urals в 40 USD, "излишки" в виде иностранной валюты и драгметаллов направлялись в ФНБ. Последующие три года, благодаря этой мере, несмотря на дорожавшую нефть, рубль оставался стабильным. Дешёвый по отношению к нефти рубль помог компаниям-экспортёрам снизить издержки и принёс им дополнительную прибыль.

![](images/article/rub-vs-oil-export.jpeg)

По объёмам торгов я заметил растущую популярность ETF денежного рынка. Они появились почти одновременно - в середине 2022 года и с тех пор их доля в объёме торгов выросла с 0.8% до 12% или с 0.45 до 19 млрд. рублей. Насколько понимаю, это связано с ростом ключевой ставки и доходности облигаций.

![](images/article/tqtf-etf-value-histogram.jpeg)
![](images/article/tqtf-etf-value-treemap-2022-07-22.jpeg)
![](images/article/tqtf-etf-value-treemap-2024-11-13.jpeg)

Объём торгов ETF денежного рынка сравним с объёмами торгов нескольких отраслей вместе взятых. Из-за высокой ключевой ставки рынок долговых бумаг выглядит привлекательнее инвестиций в акции:

![](images/article/tqtf-etf-value-histogram-compare.jpeg)

Посмотреть графики можно на странице [ruslanbay.github.io/moex](http://ruslanbay.github.io/moex). Данные обновляются ежедневно.

JS - не моя стихия, не судите код строго, он просто работает =)
