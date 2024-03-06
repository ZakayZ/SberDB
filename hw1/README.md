# Домашняя работа #2

---

## Поднимаем образ

`docker-compose -f mongo.yml up -d`

## Загружаем датасет

Я выбрал [датасет](https://archive.ics.uci.edu/ml/datasets/wine+quality), так как он содержит много различных полей и не содержит картинки.

Он содержит 2 `.csv` файла, которые я разместил в коллекции `white`, `red`.

```sql
use winesDB

db.createCollection('red')

db.createCollection('white')
```

А затем загружаем данные:

```shell
artyasen-osx:hw1 artyasen$ mongoimport --authenticationDatabase admin -u admin -p admin --host=127.0.0.1 -d winesDB -c red --type csv --file winequality-red.csv --headerline
2024-03-06T23:14:02.580+0300	connected to: mongodb://127.0.0.1/
2024-03-06T23:14:02.610+0300	1599 document(s) imported successfully. 0 document(s) failed to import.

artyasen-osx:hw1 artyasen$ mongoimport --authenticationDatabase admin -u admin -p admin --host=127.0.0.1 -d winesDB -c white --type csv --file winequality-white.csv --headerline
2024-03-06T23:17:11.785+0300	connected to: mongodb://127.0.0.1/
2024-03-06T23:17:11.871+0300	4898 document(s) imported successfully. 0 document(s) failed to import.
```

## CRUD запросы

### Find запросы

```sql
winesDB> db.red.find({'pH': {$gt: 4}})
[
  {
    _id: ObjectId('65e8ce8a64d0649f9c5eefcf'),
    'fixed acidity': 5.4,
    'volatile acidity': 0.74,
    'citric acid': 0,
    'residual sugar': 1.2,
    chlorides: 0.041,
    'free sulfur dioxide': 16,
    'total sulfur dioxide': 46,
    density: 0.99258,
    pH: 4.01,
    sulphates: 0.59,
    alcohol: 12.5,
    quality: 6
  },
  {
    _id: ObjectId('65e8ce8a64d0649f9c5eefd7'),
    'fixed acidity': 5,
    'volatile acidity': 0.74,
    'citric acid': 0,
    'residual sugar': 1.2,
    chlorides: 0.041,
    'free sulfur dioxide': 16,
    'total sulfur dioxide': 46,
    density: 0.99258,
    pH: 4.01,
    sulphates: 0.59,
    alcohol: 12.5,
    quality: 6
  }
]
```

```sql
winesDB> db.red.findOne({'alcohol': 12, 'quality': 5})
{
  _id: ObjectId('65e8ce8a64d0649f9c5ef0b0'),
  'fixed acidity': 6.2,
  'volatile acidity': 0.64,
  'citric acid': 0.09,
  'residual sugar': 2.5,
  chlorides: 0.081,
  'free sulfur dioxide': 15,
  'total sulfur dioxide': 26,
  density: 0.99538,
  pH: 3.57,
  sulphates: 0.63,
  alcohol: 12,
  quality: 5
}
```

### Update

```sql
winesDB> db.red.updateOne({'fixed acidity': 6.2}, {$set: { 'my_filed': 'best field', 'quality': 1000 }})
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
winesDB> db.red.findOne({'fixed acidity': 6.2})
{
  _id: ObjectId('65e8ce8a64d0649f9c5eeafc'),
  'fixed acidity': 6.2,
  'volatile acidity': 0.45,
  'citric acid': 0.2,
  'residual sugar': 1.6,
  chlorides: 0.069,
  'free sulfur dioxide': 3,
  'total sulfur dioxide': 15,
  density: 0.9958,
  pH: 3.41,
  sulphates: 0.56,
  alcohol: 9.2,
  quality: 1000,
  my_filed: 'best field'
}
```

```sql
winesDB> db.red.updateOne({'fixed acidity': 6.2}, {$set: { 'my_filed': 'best field', 'quality': 1000 }})
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
winesDB> db.red.findOne({'fixed acidity': 6.2})
{
  _id: ObjectId('65e8ce8a64d0649f9c5eeafc'),
  'fixed acidity': 6.2,
  'volatile acidity': 0.45,
  'citric acid': 0.2,
  'residual sugar': 1.6,
  chlorides: 0.069,
  'free sulfur dioxide': 3,
  'total sulfur dioxide': 15,
  density: 0.9958,
  pH: 3.41,
  sulphates: 0.56,
  alcohol: 9.2,
  quality: 1000,
  my_filed: 'best field'
}
```

```sql
winesDB> db.red.replaceOne({'chlorides': 0.06}, { 'new_field': 123, 'xxx_field_xxx': 'kek' })
{
  acknowledged: true,
  insertedId: null,
  matchedCount: 1,
  modifiedCount: 1,
  upsertedCount: 0
}
winesDB> db.red.findOne({'new_field': 123})
{
  _id: ObjectId('65e8ce8a64d0649f9c5eeb2f'),
  new_field: 123,
  xxx_field_xxx: 'kek'
}
```

### Delete

```sql
winesDB> db.red.deleteOne({'new_field': {$exists: 1}})
{ acknowledged: true, deletedCount: 1 }
```

### Create

```sql
winesDB> db.red.insertOne({_id: "xxx", 'value': "my value", 'num': 412412})
{ acknowledged: true, insertedId: 'xxx' }
winesDB> db.red.find({_id: "xxx"})
[ { _id: 'xxx', value: 'my value', num: 412412 } ]
```

## Оптимизация индексами

Возьмем произвольный большой запрос:

```sql
winesDB> db.white.find({alcohol: {$gt: 9}, chlorides: {$lt: 0.1}, pH: {$lt: 3.3, $gt: 3.1}, quality: 4}).explain("executionStats")
{
  executionStats: {
    executionSuccess: true,
    nReturned: 52,
    executionTimeMillis: 5,
    totalKeysExamined: 0,
    totalDocsExamined: 4898,
  },
  ok: 1
}
```

Занимает 5 мс на выполнения.

Добавим индексы:

`db.white.createIndex({alcohol: 1, chlorides: 1, pH: 1, quality: 1})`

Повторим запрос:

```sql
winesDB> db.white.find({alcohol: {$gt: 9}, chlorides: {$lt: 0.1}, pH: {$lt: 3.3, $gt: 3.1}, quality: 4}).explain("executionStats")
{
  executionStats: {
    executionSuccess: true,
    nReturned: 52,
    executionTimeMillis: 7,
    totalKeysExamined: 2944,
    totalDocsExamined: 52,
    }
  },
  ok: 1
}
```

Получаем замедление на 2 мс. Успех!

Скорее всего данных мало, чтобы проход по индексам был эффективнее, чем проход по всем элементам. Стоит заметить, что число просмотренных документов `totalDocsExamined` упало в 10 раз, что говорит о повышенной производительности для больших обьемов данных.
