# NotificationFrequency

要素数が確定されたシーケンスの途中で処理を挟むタイミングの判定を補助します。  

## 使い方

1. `n回毎`あるいは`n%毎`など、頻度を指定してインスタンス`nf`を生成します。
1. `nf.length`に管理するシーケンスの要素数を与えます。
1. `enumerate`付きの`for文`などで(`通知を行うか否か(bool)`, `進捗率(int)`)を取得できます。

```Python

from otsunotificationfrequency import NotificationFrequency

# 2212個の要素を持つリストで実行する例
data = [x * 2 for x in range(2212)]
length = len(data)

# 25%毎に表示を行う
nf25per = NotificationFrequency('25%')
nf25per.set_length(length)

# 20個毎に表示を行う
# nf20 = NotificationFrequency(20)
# nf20.length = length

for i, d in enumerate(data):
    i += 1
    sa, per = nf25per.check_and_get_percentage(i)
    # sa, per = nf20(i)
    if sa:
        print(f'{d}: {per}% ({i}/{length})')
```

`25%`毎に表示する例  

```console

1104: 25% (553/2212)
2210: 50% (1106/2212)
3316: 75% (1659/2212)
4422: 100% (2212/2212)
```

`20個`毎に表示する例

```console

38: 0% (20/2212)
78: 1% (40/2212)
118: 2% (60/2212)
158: 3% (80/2212)
198: 4% (100/2212)
238: 5% (120/2212)
278: 6% (140/2212)
318: 7% (160/2212)
358: 8% (180/2212)
398: 9% (200/2212)
438: 9% (220/2212)
...
4158: 94% (2080/2212)
4198: 94% (2100/2212)
4238: 95% (2120/2212)
4278: 96% (2140/2212)
4318: 97% (2160/2212)
4358: 98% (2180/2212)
4398: 99% (2200/2212)
4422: 100% (2212/2212)
```

## otsunotificationfrequency.validatorモジュール

`otsuvalidator`ライブラリがインストールされていない場合インポートできず、`ImportError`が発生します。  
`otsucfgmng`などでバリデータやコンバータが必要な場合に利用してください。  
`NotificationFrequency`を使用するだけの場合、このモジュールは何の機能も持ちません。
