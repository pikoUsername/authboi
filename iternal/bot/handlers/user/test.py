from aiogram import types

from iternal.bot.loader import dp
from iternal.bot.utils.embed import Paginator

__all__ = "paginator_test",

slug = ["""Доброго времени суток, уважаемое хабрасообщество! Как я и обещал после прошлой статьи по теории струн, сегодня мы попробуем приоткрыть завесу тайн и пробежаться по костылям новым веяниям в космологии — попробуем взглянуть на тернистый путь, который прошли ученые, и разобраться, к чему же они в конце концов пришли в попытке описать происхождение, жизнь и будущее нашей Вселенной. В процессе написания статья немало разрослась, поэтому я все-таки решил разделить её на две части.

Космологическая постоянная
""", """
В 1916 году Альберт Эйнштейн при создании общей теории относительности (ОТО) полагал, что наша Вселенная должна быть стационарной, то есть по большей части недвижной. Или, другими словами, расстояние между двумя разными звёздами и даже галактиками с течением времени должно оставаться одним и тем же. Однако из уравнений его же собственной теории выходило, что Вселенная по ним никак не может быть стационарной. Тогда Эйнштейн дополнил уравнения так называемым «лямбда-членом», который был призван гарантировать то, что Вселенная таки стационарна. Лямбда-член в дальнейшем назвали «космологической постоянной».

Практический смысл космологической постоянной заключался в том, что пустое пространство на самом деле не пустое — в нём имеется некое поле, которое оказывает воздействие на находящееся в нём вещество, извлекая нужную для этого энергию из ниоткуда. Подобные выводы вызывали у современников недоумение, и коллеги не преминули обрушиться на Эйнштейна с критикой.

В 1922 году Александр Фридман представил собственную модель Вселенной, которая не использовала космологическую постоянную. Но по его модели получалось, что Вселенная должна либо постоянно расширяться, либо постоянно сжиматься. Изначально Эйнштейн к данной модели отнесся отрицательно.

Но в 1929 году Эдвин Хаббл поставил точку в данном вопросе, экспериментально подтвердив, что Вселенная расширяется — то есть, расстояние между двумя любыми галактиками с течением времени постоянно увеличивается, а не остаётся неизменным. Эйнштейн признал свою неправоту, сказав, что введение космологической постоянной было его величайшей ошибкой.

Открытие расширяющейся Вселенной стало новым толчком для науки — привело к созданию теории Большого взрыва. Да и современная Лямбда-CDM модель Вселенной базируется именно на модели Фридмана, включая в себя помимо нее и космологическую постоянную, и тёмную материю, и тёмную энергию.

Тёмная материя

До 1998 года учёные усердно работали над теорией Большого взрыва, которая постепенно все больше и больше развивалась. Но общая суть оставалась неизменной: изначально вся материя была сосредоточена в одной-единственной точке, и много лет назад произошел Большой взрыв, дав начало нашей Вселенной.

Математически теория базировалась на ОТО, но она не была в состоянии описать все наблюдаемые явления. Например, было установлено, что края всех галактик вращаются гораздо быстрее, чем это следует из законов Ньютона, которые являются предельным случаем ОТО.
""", """
Объяснений этому явлению могло быть два: либо массы галактик больше, чем кажутся, либо гравитация убывает с расстоянием не так быстро, как предсказывает ОТО, а как-то очень хитро — не нарушая уже проверенные кейсы, но и объясняя кривые вращений галактик. В данном случае ученые остановились на первом варианте, и добавили к космологической модели недостающую массу, которую назвали «тёмной материей».

На тот момент у тёмной материи не было экспериментальных подтверждений, и для объяснения этого факта было предложено два варианта:

Тёмную материю просто не видно. Черные дыры, коричневые карлики, нейтронные звезды, кварковые звезды, преонные звезды, многочисленные планеты в телескоп не узреть на таких расстояниях, а они вполне себе обычные объекты во Вселенной. Хотя согласно различным космологическим теориям и наблюдениям за древними космическими объектами — так много подобных объектов быть не должно.
Тёмная материя состоит из невидимых частиц. Хотя сама возможность существования подобных частиц в науке сейчас под большим вопросом. Тем не менее тёмная материя должна состоять не только из слабо взаимодействующих, но и довольно массивных частиц. Подпадающие под такие характеристики частицы усиленно ищутся, но пока безуспешно.
""", """
На данный момент учёные предполагают, что если тёмная материя представляет собой некий новый тип частиц, то они могут, помимо гравитации, взаимодействовать ещё каким-либо образом (например, посредством слабого взаимодействия — того самого, из-за которого распадаются радиоактивные элементы). На практике это означает, что эти частицы могут рассеиваться на ядрах атомов; поэтому, если взять большое количество активного вещества, то со временем какая-нибудь частица тёмной материи с ним провзаимодействует, что можно будет зафиксировать чувствительной аппаратурой.

На данный момент исследователи по всему миру проводят эксперименты с огромными объёмами вещества в расчёте на то, что удастся что-нибудь зарегистрировать, и хотя, временами, поступают новости о положительных результатах, все они довольно спорны.
"""]


@dp.message_handler(commands="test", is_authed=True)
async def paginator_test(m: types.Message):
    p = Paginator(slug)

    await p.start(m)
