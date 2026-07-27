# Travel — China 2026 Operations Canon

Операционный маршрут на **28.08–14.09.2026**:
**Шанхай → Чунцин → Фужун → Чжанцзяцзе → Гуйлинь/Яншо → Шэньчжэнь → Пекин**.

Последняя проверка источников: **27.07.2026**. Репозиторий подключён к
[`samuraiIT/Travel`](https://github.com/samuraiIT/Travel), ветка `master`.

Релиз **1.0.4** запускает owner-only Telegram Travel Agent
`@travel_samurai_bot` на NousResearch Hermes Agent. Live-профиль использует
быстрый OmniRoute combo `travel-fast` (Codex Spark → строгий
`codex-review` fallback) и только семь релевантных Travel skills. SOUL задаёт
естественный, короткий и контекстный Telegram-диалог без притворства
человеком; safety и approval gates не изменены. Токены и другие секреты
хранятся только во внешнем runtime-профиле и никогда не входят в Git.

> **Главный вывод:** маршрут укладывается в 18 календарных дат и 16 ночей в
> Китае. Бадалин 13 сентября не является частью обязательного маршрута:
> после HU7706 это только `Backup`, а шанс успеть на канатную дорогу низкий.

## Статусы и база расчёта

| Статус | Значение |
|---|---|
| `Confirmed` | Подтверждено билетом/скриншотом или актуальным официальным источником |
| `Book` | Выбрано, но ещё не забронировано; цена/время могут измениться |
| `Backup` | Необязательный или условный вариант; маршрут не зависит от него |

- Курс планирования: **¥1 = ₽11,5025**, официальный курс Банка России на
  25.07.2026. В таблицах RUB округлены примерно до ₽10.
- Дневная стоимость: транспорт + входы **на человека**; отель указан отдельно
  **за номер/ночь**. Питание — отдельная статья.
- Оплаченные суммы сохраняются в RUB: CZ656+CZ3571 — **₽20 546**,
  PN6438 — **₽6 779**. Цена пакета HU7706+HU7985 на скриншоте не видна.
- Точные номера поездов нельзя подтвердить до открытия продаж. Официальное
  окно 12306 — 15 дней, включая день поездки.

## Неприкосновенные билеты

| Status | Дата/время | Рейс | Маршрут | Подтверждение |
|---|---|---|---|---|
| `Confirmed` | 28.08 21:15 → 29.08 11:40 | CZ656 | SVO → CAN | `China/image.png` |
| `Confirmed` | 29.08 15:00–17:25 | CZ3571 | CAN → SHA | `China/image.png` |
| `Confirmed` | 31.08 12:35–15:25 | PN6438 | PVG → CKG | `China/image.png` |
| `Confirmed` | 13.09 13:10–16:15 | HU7706 | SZX T3 → PEK T2 | local-only `China/image copy.png`; public facts in `China/EVIDENCE_POLICY.md` |
| `Confirmed` | 14.09 14:25–18:05 | HU7985 | PEK T2 → SVO C | local-only `China/image copy.png`; public facts in `China/EVIDENCE_POLICY.md` |

Скриншот Hainan требует получить и повторно зарегистрировать багаж. Публичный
список through-check Hainan на сезон 29.03–24.10.2026 содержит
HU7702→HU7985, но **не** HU7706→HU7985. Поэтому сквозной багаж не предполагаем;
ярлык всё равно проверить у стойки в SZX.

## Маршрут по дням

| Status | Дата, время | Место / адрес или станция | Транспорт и длительность | Стоимость CNY / RUB | Нагрузка и резерв | Бронь / дедлайн |
|---|---|---|---|---|---|---|
| `Confirmed` | **28.08, 18:15–21:15** | SVO, терминал перепроверить в boarding pass | Аэропорт 3ч; CZ656, ночной перелёт | Пакет CZ: **¥1 786 / ₽20 546**, оплачен, на человека | **Переезд**; целевой приезд за 3ч | Online check-in / **27.08** |
| `Confirmed` | **29.08, 11:40–20:00** | CAN → SHA; отель `Book` у People’s Square/Jing’an, точный адрес после брони | Стыковка 3ч20; CZ3571 2ч25; до отеля 45–75м | Локально **¥80–160 / ₽920–1 840**; отель **¥300–500 / ₽3 450–5 750** за номер | **Переезд**; 2ч35 до вылета после посадки, 45м дорожный резерв | Отель / **31.07**; Бунд вечером только `Backup` |
| `Book` | **30.08, 08:30–21:00** | 豫园, 上海市黄浦区安仁街218号 → 外滩, 中山东一路 | Метро/пешком; 8–10ч с 2ч отдыха; башня **или** круиз | **¥220–340 / ₽2 530–3 910**; отель **¥300–500 / ₽3 450–5 750** | **Активный**; 2ч на жару/толпу | Yu Garden + башня/круиз / **27.08** |
| `Confirmed` | **31.08, 08:30–18:30** | PVG → CKG; отель `Book` в Jiefangbei | Airport Link/метро 40–75м; PN6438 2ч50; от CKG 60–90м | PN+локально **¥659–709 / ₽7 580–8 160**; отель **¥200–350 / ₽2 300–4 030** | **Переезд**; прибыть PVG к 10:00, 45м после CKG | Отель / **31.07**; Hongyadong только `Backup` |
| `Book` | **01.09, 08:30–21:00** | 李子坝观景台, 渝中区李子坝正街39号 → 长江索道 → 南滨路 | Метро/пешком/канатная дорога; 8–10ч | **¥80–160 / ₽920–1 840**; отель **¥200–350 / ₽2 300–4 030** | **Активный**; +20м из-за работ Liziba, +90м очередь/погода | Слот 长江索道 / **30.08** |
| `Book` | **02.09, 09:00–20:30** | 磁器口古镇, 重庆市沙坪坝区; 洪崖洞 `Backup` | Метро/пешком; 6–8ч | **¥40–100 / ₽460–1 150**; отель **¥200–350 / ₽2 300–4 030** | **Лёгкий**; 3ч отдых/сборы | Перепроверить режим / **31.08** |
| `Book` | **03.09, 07:00–15:00** | 重庆东站 → 张家界西站 → 芙蓉镇站 | Высокоскоростной поезд + пересадка + отель; 3,5–5ч door-to-door | **¥260–350 / ₽2 990–4 030**; отель **¥150–300 / ₽1 730–3 450** | **Переезд**; 60–90м в 重庆东, 45м на пересадку | 12306 / продажи с **20.08** |
| `Book` | **04.09, 08:00–20:00** | 芙蓉镇景区 → 红石林国家地质公园 | Пешком + заранее заказанное авто; 7–9ч | **¥220–320 / ₽2 530–3 680**; отель **¥150–300 / ₽1 730–3 450** | **Средний**; 2ч на дождь/дорогу | Оба входа + авто / **01.09** |
| `Book` | **05.09, 08:00–14:00** | 芙蓉镇站 → 张家界西站 → 武陵源标志门 | Поезд около 23м; весь путь 2–2,5ч | **¥80–150 / ₽920–1 730**; отель **¥220–380 / ₽2 530–4 370** | **Переезд**; 60м станция + 60м дорога | 12306 / продажи с **22.08**; парк вечером только `Backup` |
| `Book` | **06.09, 07:00–18:00** | 武陵源东门, 张家界市武陵源区金鞭路279号; Yuanjiajie/Tianzi | Шаттл парка + лифт/канатка + пешком; 9–11ч | **¥300–390 / ₽3 450–4 490**; отель **¥220–380 / ₽2 530–4 370** | **Высокий**; 90м на очередь/погоду | `张家界一机游` timeslot / **27.08** |
| `Book` | **07.09, 08:00–17:30** | 武陵源东门; Ten-Mile Gallery **или** Huangshi Village | Шаттл + пешком; 7–9ч | **¥70–180 / ₽810–2 070**; отель **¥220–380 / ₽2 530–4 370** | **Средний**; 2ч восстановление/погода | Подтвердить многодневность входа и внутренний транспорт / **27.08** |
| `Book` | **08.09, 07:30–17:30** | 天门山, 张家界市永定区大庸中路11号 | Пакет канатка/автобус + пешком; 8–10ч | **¥258–350 / ₽2 970–4 030**; городской отель **¥180–300 / ₽2 070–3 450** | **Высокий**; 90м погода/очередь | Tianmen timeslot + отель / **29.08** |
| `Book` | **09.09, 07:00–17:00** | 张家界西站 → 桂林北站 | Целевой прямой поезд около 7ч + 30–45м до отеля | **¥370–430 / ₽4 260–4 950**; отель **¥220–380 / ₽2 530–4 370** | **Переезд**; 75м станция + 45м прибытие | 12306 / продажи с **26.08**; Two Rivers вечером только `Backup` |
| `Book` | **10.09, 08:30–20:30** | 桂林 → 阳朔 → 遇龙河: точный причал только из voucher | Авто/автобус + bamboo raft + велосипед; 7–9ч | **¥300–450 / ₽3 450–5 180**; отель **¥220–380 / ₽2 530–4 370** | **Средний**; 2ч дождь/закрытие реки | Yangshuo + raft / **03.09** |
| `Book` | **11.09, 08:00–19:30** | 兴坪古镇 / 漓江; Longji — альтернатива, не второй маршрут того же дня | Авто/автобус + пешком/лодка; 8–10ч | **¥200–350 / ₽2 300–4 030**; отель **¥220–380 / ₽2 530–4 370** | **Средний**; 2ч погода/трафик | Выбрать Xingping/Li River supplier / **04.09** |
| `Book` | **12.09, 07:00–17:30** | 桂林北站 **или** 桂林西站 → 深圳北站 → отель с доступом к SZX | Авто + поезд 2ч45–4ч + метро/такси | **¥300–360 / ₽3 450–4 140**; отель **¥300–500 / ₽3 450–5 750** | **Переезд**; 90м станция + 60м Shenzhen | 12306 / продажи с **29.08**; Shenzhen Bay только `Backup` |
| `Confirmed` | **13.09, 09:30–19:00** | 深圳宝安机场T3 → 北京首都机场T2 → airport hotel | Метро/такси + HU7706 3ч05 + багаж/выход 60–100м | Локально **¥100–250 / ₽1 150–2 880**; HU оплачен, сумма неизвестна; отель **¥200–450 / ₽2 300–5 180** | **Переезд**; приехать SZX к 11:00; Бадалин только `Backup` | PEK T2 hotel / **31.07**; private driver / **10.09** |
| `Confirmed` | **14.09, 10:30–18:05** | 北京首都机场T2 → SVO C | Shuttle + HU7985; аэропорт 3ч, полёт 7ч40 | **¥0–100 / ₽0–1 150** локально; HU оплачен, сумма неизвестна | **Переезд**; быть в PEK T2 к 11:25; экскурсий нет | Online check-in, recheck багажа / **13.09** |

## Критический разбор Бадалина после HU7706

### Что подтверждено

- HU7706 садится в **PEK T2 в 16:15**, если идёт по расписанию.
- Багаж моделируется как получение в PEK; through-check не подтверждён.
- Расстояние PEK→Badaling у route provider — около **73,6 км**; это не гарантия
  времени в трафике.
- Официальный сезон Night Great Wall действует до 06.10.2026:
  вход **18:30–21:00**, подсветка **19:20–22:00**.
- Южная наземная канатная дорога принимает на подъём **17:30–19:30**.
- Официальный автобус PEK→Badaling отправляется только в 06:00 и 08:00;
  после HU7706 он бесполезен. Нужен заранее заказанный автомобиль.

### Временная модель

| Сценарий | Выход/встреча в PEK | Дорога 74 км | Прибытие | Канатка до 19:30 | Ночной вход до 21:00 |
|---|---:|---:|---:|---|---|
| Best: on-time, carry-on, водитель ждёт | 16:50–17:05 | 75–90м | 18:05–18:35 | Возможно | Вероятно |
| Base: on-time, зарегистрированный багаж | 17:15–17:35 | 90–110м | 18:45–19:25 | На грани | Вероятно |
| Adverse: задержка/багаж/трафик | после 17:40 | 110–140м | после 19:30 | Нет | Условно |

Это не статистика авиакомпании, а консервативная операционная оценка:

| Цель | Плановая вероятность | Verdict |
|---|---:|---|
| Групповой тур с отправлением 16:20 | **0%** | `Backup` / фактически невозможен |
| Канатка, с зарегистрированным багажом | **20–35%** | `Backup`, не покупать невозвратный пакет ради неё |
| Канатка, только ручная кладь + водитель | **40–55%** | Всё ещё `Backup` |
| Ночной вход, багаж + водитель | **60–75%** | Реалистичнее, но зависит от рейса/трафика |
| Ночной вход, только ручная кладь + водитель | **75–85%** | Возможен при on-time рейсе |

**Hard abort:** если машина не выехала из PEK до **17:20**, канатную дорогу
снять с плана; если ETA к Badaling позже **20:30**, ехать в airport hotel.
Даже приезд в 19:25 не оставляет безопасного времени на парковку, входной
контроль и поиск посадки, поэтому рабочий cutoff для канатки — **19:15**.

Рекомендуемый основной план 13.09: багаж → airport hotel → ужин/сон.
Бадалин активировать только утром 13.09 по фактическому статусу рейса,
возвратности билета, погоде и подтверждённому водителю.

## Реестр бронирований

| Status | Что | Когда открывается / крайний срок | Канал |
|---|---|---|---|
| `Book` | Все 16 ночей с бесплатной отменой | **31.07** | Agoda/Trip.com/отель; точный адрес сохранить по-китайски |
| `Book` | 重庆东→张家界西→芙蓉镇, 03.09 | **20.08** | Официальный 12306 |
| `Book` | 芙蓉镇→张家界西, 05.09 | **22.08** | Официальный 12306 |
| `Book` | 张家界西→桂林北, 09.09 | **26.08** | Официальный 12306 |
| `Book` | 桂林北/西→深圳北, 12.09 | **29.08** | Официальный 12306 |
| `Book` | Zhangjiajie Park 06–07.09 | **27.08** operational cutoff | `张家界一机游` |
| `Book` | Tianmen Mountain 08.09 | **29.08** operational cutoff | Официальный канал/поставщик |
| `Book` | Yulong raft 10.09 | **03.09** | Поставщик; причал только из voucher |
| `Backup` | Badaling Night + refundable driver | Проверить **29.08**, финализировать **10.09** | `长城内外旅游` + licensed driver |
| `Confirmed` | Online check-in и документы | За 24–48ч до каждого рейса | Авиакомпания |

Для 12306 дата открытия рассчитана как дата поездки минус 14 дней. Точное время
начала продаж зависит от станции; в день открытия проверять официальный канал,
не подменять его неофициальным MCP.

## Ночёвки и бюджет

| Локация | Ночей | Диапазон за номер/ночь | Подытог CNY / RUB |
|---|---:|---:|---:|
| Shanghai | 2 | ¥300–500 | ¥600–1 000 / ₽6 900–11 500 |
| Chongqing | 3 | ¥200–350 | ¥600–1 050 / ₽6 900–12 080 |
| Furong | 2 | ¥150–300 | ¥300–600 / ₽3 450–6 900 |
| Wulingyuan | 3 | ¥220–380 | ¥660–1 140 / ₽7 590–13 110 |
| Zhangjiajie City | 1 | ¥180–300 | ¥180–300 / ₽2 070–3 450 |
| Guilin | 1 | ¥220–380 | ¥220–380 / ₽2 530–4 370 |
| Yangshuo | 2 | ¥220–380 | ¥440–760 / ₽5 060–8 740 |
| Shenzhen | 1 | ¥300–500 | ¥300–500 / ₽3 450–5 750 |
| PEK T2 | 1 | ¥200–450 | ¥200–450 / ₽2 300–5 180 |
| **Итого** | **16** |  | **¥3 500–6 180 / ₽40 260–71 090 за номер** |

| Категория | Оценка | Примечание |
|---|---:|---|
| Уже известные авиабилеты | **₽27 325** | CZ-пакет + PN6438; HU-сумма неизвестна |
| Межгородские поезда | **¥892–1 021 / ₽10 260–11 740 на человека** | До открытия продаж |
| Локальный транспорт + активности | **¥2 056–3 539 / ₽23 650–40 710 на человека** | Без поездов, известных авиабилетов и Badaling private car |
| Питание | **¥1 700–3 060 / ₽19 550–35 200 на человека** | ¥100–180 × 17 дней в Китае |
| Жильё | **¥3 500–6 180 / ₽40 260–71 090 за номер** | Делится между жильцами номера |
| Badaling `Backup` | **¥700–1 300 / ₽8 050–14 950 за машину/входы** | Перепроверить live price и возвратность |
| Страховка | **TBD** | Получить полис с Китаем и активностями |

Итог нельзя честно закрыть до появления цены HU, состава путешественников,
реальных hotel rates и поездов. Для одного человека в одном номере рабочий
остаток без HU/страховки/Badaling — примерно **¥8 148–13 800**
(около **₽93 720–158 730**) плюс уже оплаченные ₽27 325.

## Операционные риски

| Риск | Триггер | Действие |
|---|---|---|
| Тайфун/ливень/жара | Официальный прогноз за 7–10 дней | Переставить outdoor в буфер, не выдавать климатическую норму за прогноз |
| Работы на Liziba | 01.09 действует частичное ограничение | +20м, следовать навигации персонала |
| Tianmen East Glass Walkway закрыт | Нет официального reopening notice | Не обещать; использовать West/Panlong, перепроверить за 72ч |
| Yulong rafting закрыт из-за воды | Нет подтверждения поставщика утром | Возвратный билет; заменить dry-land Yangshuo route |
| Поезд не появился/нет мест | 12306 sale day | Искать официальную пересадку; не ломать ночёвки молча |
| Багаж HU не through-check | Ярлык в SZX не до SVO | Получить в PEK, сохранить receipt, зарегистрировать 14.09 |
| Perplexity Space недоступен | Cloudflare verification | Не считать его импортированным; использовать экспорт владельца |

## Источники

Материальные спорные утверждения проверены официальным источником или
поставщиком:

1. [Bank of Russia: CNY rate on 25.07.2026](https://www.cbr.ru/eng/currency_base/daily/?UniDbQuery.Posted=True&UniDbQuery.To=25.07.2026)
2. [12306: 15-day presale window](https://passport.12306.cn/otnyt/gonggao/gsggp.html)
3. [Chinese Embassy in Russia: visa-free entry up to 30 days through 31.12.2027](https://ru.china-embassy.gov.cn/rus/lsfw_143010/zytz_142816/202605/t20260520_11914284.htm) — применимо только к обычным российским паспортам и допустимой цели поездки
4. [Shanghai Government: Airport Link SHA T2↔PVG, 40 minutes, ¥26](https://english.shanghai.gov.cn/en-Transportation/20241231/f66f14bbd4b549ab88e6f3aec375790c.html)
5. [Yu Garden official closure notice](https://www.yugarden.com.cn/page/articleview/message.html)
6. [Chongqing official Yangtze Cableway price decision](https://fzggw.cq.gov.cn/zwgk/zfxxgkml/jgxx/jgzc/202503/t20250324_14434363.html)
7. [Chongqing official Liziba works from 01.09.2026](https://www.cq.gov.cn/ywdt/jrcq/202606/t20260613_15751500_app.html)
8. [Chongqing official Liziba address](https://www.cqyz.gov.cn/zjyz/lyyz/rmdkd/202210/t20221005_11164443.html)
9. [Hunan Government: Zhangjiajie park booking/hours/address](https://www.enghunan.gov.cn/hneng/SP/sp2023/2023MayDay/202304/t20230426_29324679.html)
10. [Hunan Government: Tianmen current East Glass Walkway closure](https://enghunan.gov.cn/hneng/Tourism/WhatGoingon/202605/t20260513_33976257.html)
11. [Hunan Government: Tianmen hours/address](https://enghunan.gov.cn/hneng/SP/sp2023/2023MayDay/202304/t20230426_29324673.html)
12. [Trip.com supplier: Yulong raft products/prices](https://us.trip.com/travel-guide/attraction/yangshuo/yulong-river-rafting-10758988/)
13. [Klook supplier: Yulong voucher/wharf process](https://www.klook.com/zh-CN/activity/155144-guilin-yangshuo-the-li-river-and-yulong-rive-2-days-private-tour/)
14. [Beijing Government: Badaling Night 2026 hours and cableway](https://english.beijing.gov.cn/travellinginbeijing/events/202604/t20260424_4608135.html)
15. [Beijing Government: official Badaling booking channel](https://english.beijing.gov.cn/consuminginbeijing/onedayinbeijing/sleeplessinbeijing/updatesofnighttimeconsumption/202602/t20260209_4502618.html)
16. [Beijing Government: PEK–Badaling bus departures](https://english.beijing.gov.cn/livinginbeijing/transportation/bus/202602/t20260211_4507827.html)
17. [Hainan through-check lookup](https://new.hnair.com/hainanair/ibe/common/throughCheckIn.do)
18. [Route-provider estimate PEK→Badaling](https://www.rome2rio.com/zh/s/%E5%8C%97%E4%BA%AC%E9%A6%96%E9%83%BD%E5%9B%BD%E9%99%85%E6%9C%BA%E5%9C%BA-PEK/Badaling-Great-Wall)

Furong/Red Stone Forest, конкретные отели, точные train times и часть внутренних
цен пока имеют статус `Book`: их нельзя повышать до `Confirmed` до проверки
официального inventory/поставщика в окне продажи.

## Роли и skills

| Роль | Ответственность |
|---|---|
| China Travel Operations Lead | Канон, конфликты, go/no-go и итоговый handoff |
| Rail & Airport Operations Planner | 12306, терминалы, багаж, стыковки, buffers |
| China Grounding Researcher | Официальные адреса, режимы, закрытия, suppliers |
| Budget & Booking Controller | Курс, cost basis, дедлайны, refundable inventory |
| Travel Risk Manager | Best/base/adverse, abort triggers, weather and fatigue |

Интегрированы skills:

- `travel-agent-skill` — календарь, ночи, бюджет и booking register;
- `travel-concierge` — grounded addresses/routes без выдуманных Place IDs;
- `travel-day-optimizer` — таймлайны, буферы и contingency;
- `china-travel-operations` — объединяющий workspace skill и валидатор.

Оригинальные upstream snapshots и provenance сохранены в
`.agents/skills/<skill>/references/`. Deprecated Google ADK sample не запускается
как будто его map-tools доступны.

## Структура и обслуживание

```text
Travel/
├── README.md                         # этот human canon
├── AGENTS.md                         # project-local правила
├── China/                            # исходные планы и ticket evidence
├── config/hermes/                    # safe profile policy, no secrets
├── deploy/systemd/                   # dedicated Hermes user unit
├── data/china-2026.json              # machine-checkable facts
├── prompts/                          # CLI and Telegram agent prompts
├── scripts/                          # deploy/provision/verify/validators
├── tests/                            # release/security config tests
├── supabase/schema.sql               # optional, not deployed
└── docs/                             # architecture, tools, roadmap
```

`China/image copy.png` содержит booking reference, поэтому остаётся
immutable local-only evidence и исключён из Git. Политика:
[`China/EVIDENCE_POLICY.md`](China/EVIDENCE_POLICY.md).

Проверка:

```bash
python3 /opt/project_llm/projects/Travel/scripts/validate_itinerary.py
```

Перед каждым booking-днём обновить live inventory, затем синхронно изменить
`README.md` и `data/china-2026.json` и снова запустить валидатор.

## Telegram Travel Agent

Архитектура, threat model и rollback:
[`docs/HERMES_TELEGRAM_ARCHITECTURE.md`](docs/HERMES_TELEGRAM_ARCHITECTURE.md).
Roadmap и статус приёмки: [`docs/ROADMAP.md`](docs/ROADMAP.md).
Research/OSS/MCP/skills matrix:
[`docs/RESEARCH_AND_SELECTION.md`](docs/RESEARCH_AND_SELECTION.md).
Exact live state and activation handoff:
[`docs/OPERATIONS_HANDOFF.md`](docs/OPERATIONS_HANDOFF.md).

Идемпотентное обновление профиля; при `--start` активный gateway будет
перезапущен только после resource/config checks:

```bash
/opt/project_llm/projects/Travel/scripts/install_travel_bot.sh
/opt/project_llm/projects/Travel/scripts/install_travel_bot.sh --start
```

Live unit уже provisioned и active. При следующей ротации токена выполнить из
интерактивного терминала:

```bash
/opt/project_llm/projects/Travel/scripts/ensure_travel_resources.sh
/opt/project_llm/projects/Travel/scripts/preflight_travel_bot.sh
/opt/project_llm/projects/Travel/scripts/provision_travel_bot.sh
```

Если dry-run resource helper показывает недостаток `/home` или swap, применить
его один раз с `--apply`, затем снова запустить preflight. Gate не обходить без
отдельного owner risk decision.

Скрипт скрыто читает новый токен, проверяет через Telegram `getMe`, что он
принадлежит `@travel_samurai_bot`, запускает `hermes-gateway-travel.service`
и выполняет полный smoke. Токен нельзя передавать аргументом CLI, писать в
Markdown или добавлять в Git.

Model-selection evidence и точные latency/correctness gates:
[`RELEASE_NOTES_v1.0.2.md`](RELEASE_NOTES_v1.0.2.md).
Durable resource-headroom patch:
[`RELEASE_NOTES_v1.0.3.md`](RELEASE_NOTES_v1.0.3.md).
Conversation UX release and live golden-set evidence:
[`RELEASE_NOTES_v1.0.4.md`](RELEASE_NOTES_v1.0.4.md).
