# Платежный гейтвей

## Структура проекта и особенности
- api - REST API
- billing - основное приложение связанное с биллингом
- config - конфигурация проекта
- users - приложение с пользователями
- billing-gateway.json - файл для Insomnia
- линия 120 символов


## Модели
* Account:
  - валютный счет для юзера
  - может быть несколько счетов в одной и той же валюте для одного юзера
  - существуют "технические" счета - к примеру, для внешних переводов
  - технические счета используются, когда юзер пополняет баланс банковским переводом, к примеру.
  - технические счета позволяют фильтровать внешние операции - к примеру, можно узнать, сколько мы взяли комиссии или сколько было пополнений через банковский перевод
  или когда выводит деньги с лицевого счета на электронный кошелек.
* Operation:
  - стандартная бухгалтерская проводка по счетам
  - используется для двойного начисления
  - операции идут относительно текущего аккаунта
  - в базовой реализации, операции бывают двух типов - перевод и комиссия
* Payment:
  - по-сути, является объединяющей сущностью для операций
  - показывает кто кому переводил, сколько и с какой комиссией
  - также, активно используется для фоновой проводки платежа (отдаем клиенту Payment.id, 
  далее он может поллить либо соединиться через WebSocket, дожидаясь обработки платежа)
  - если во время обработки платежа что-то пошло не так - можно добавить воркера, который по-расписанию 
  будет обрабатывать платежи в INITIATED и будет переводить их в COMPLETED либо в FAILED
  
  
## Минусы
- только 1 авторизационный токен на юзера
- не сделано подтверждение аккаунта
- не сделана конвертацию валют между разными счетами
- фильтрация и сортировка не по всем полям
- избыточность в связях Payment - Operation
- не оптимизированы запросы к БД
- инлайновый импорт в задачах
- много дефолтных коментов django
- большой размер образа


# Плюсы
- реализован подход с фоновой обработкой долгих задач
- маленькая, но расширяемая схема моделей
- использована кастомная модель пользователя
- приложение и среда докеризованы и готовы к деплою
- соблюден PEP8
- можно добавить разные валюты для счетов (если потребуется - можно создать даже отдельную модель)
- можно сделать конвертацию валюты (модель с 3-мя полями: from, to, rate)
