# 10 组可解释切分案例

## 1. 哈萨克语：`мемлекетаралық`

原句：Ғылыми конференцияда мемлекетаралық ынтымақтастықты дамытудың жаңа бағыттары кеңінен талқыланды.

- mBERT：`м | ##ем | ##лекет | ##аралық`
- XLM-R：`▁мемлекет | аралық`
- SentencePiece-BPE-8k：`▁м | ем | л | ек | ет | ар | алық`

切分数量：mBERT 4，XLM-R 2，SentencePiece 7。

## 3. 哈萨克语：`қатысушыларымыздың`

原句：Қатысушыларымыздың ұсыныстары бойынша білім беру бағдарламасына бірнеше маңызды өзгерістер енгізілді.

- mBERT：`қ | ##аты | ##су | ##шылар | ##ым | ##ыз | ##дың`
- XLM-R：`▁қатысушылар | ымыздың`
- SentencePiece-BPE-8k：`▁қат | ыс | ушы | лар | ым | ыз | дың`

切分数量：mBERT 7，XLM-R 2，SentencePiece 7。

## 5. 哈萨克语：`мүмкіндіктеріміздің`

原句：Мүмкіндіктеріміздің кеңеюіне байланысты халықаралық ынтымақтастық барысында жаңа тәжірибе жинақталды.

- mBERT：`мүмкін | ##дік | ##тері | ##мі | ##зді | ##ң`
- XLM-R：`▁мүмкіндіктері | м | іздің`
- SentencePiece-BPE-8k：`▁мүмкін | ді | кт | ер | ім | із | дің`

切分数量：mBERT 6，XLM-R 3，SentencePiece 7。

## 8. 柯尔克孜语：`кызматташтыгыбыздын`

原句：Эл аралык конференцияда кызматташтыгыбыздын жаңы багыттары жана биргелешкен долбоорлор талкууланды.

- mBERT：`к | ##ыз | ##мат | ##та | ##шт | ##ыг | ##ы | ##бы | ##зды | ##н`
- XLM-R：`▁кызмат | та | шты | г | ыбызды | н`
- SentencePiece-BPE-8k：`▁к | ыз | мат | та | ш | ты | гы | б | ыз | дын`

切分数量：mBERT 10，XLM-R 6，SentencePiece 10。

## 10. 柯尔克孜语：`катышуучуларыбыздын`

原句：Катышуучуларыбыздын сунуштарынын негизинде билим берүү программасына маанилүү өзгөртүүлөр киргизилди.

- mBERT：`ка | ##тыш | ##уучу | ##лары | ##бы | ##зды | ##н`
- XLM-R：`▁катышуучулар | ыбызды | н`
- SentencePiece-BPE-8k：`▁кат | ыш | уучу | лары | б | ыз | дын`

切分数量：mBERT 7，XLM-R 3，SentencePiece 7。

## 13. 柯尔克孜语：`маалыматтардын`

原句：Маалыматтардын коопсуздугу граждандардын жеке жашоосуна жана улуттук коопсуздукка түздөн-түз таасир этет.

- mBERT：`ма | ##алы | ##мат | ##тарды | ##н`
- XLM-R：`▁маалыматтарды | н`
- SentencePiece-BPE-8k：`▁маалымат | тар | дын`

切分数量：mBERT 5，XLM-R 2，SentencePiece 3。

## 15. 乌兹别克语：`mustaqilligimizning`

原句：Xalqaro konferensiyada mustaqilligimizning tarixiy ahamiyati arxiv hujjatlari va ilmiy manbalar asosida keng tahlil qilindi.

- mBERT：`must | ##aq | ##ill | ##igi | ##mi | ##zni | ##ng`
- XLM-R：`▁mustaqil | lig | imizning`
- SentencePiece-BPE-8k：`▁m | us | t | aq | il | li | g | imiz | ning`

切分数量：mBERT 7，XLM-R 3，SentencePiece 9。

## 16. 乌兹别克语：`tadqiqotchilarimizning`

原句：Tadqiqotchilarimizning natijalari nufuzli jurnalda e'lon qilinib, ilmiy jamoatchilik tomonidan ijobiy baholandi.

- mBERT：`tad | ##qi | ##q | ##ot | ##chi | ##lari | ##mi | ##zni | ##ng`
- XLM-R：`▁ | tadqiqot | chilar | imizning`
- SentencePiece-BPE-8k：`▁t | ad | q | iq | ot | ch | il | ar | imiz | ning`

切分数量：mBERT 9，XLM-R 4，SentencePiece 10。

## 18. 乌兹别克语：`hamkorligimizni`

原句：Hamkorligimizni yanada mustahkamlash uchun ta’lim, texnologiya va innovatsiya sohalarida qo‘shma loyihalar amalga oshiriladi.

- mBERT：`ham | ##kor | ##ligi | ##mi | ##zni`
- XLM-R：`▁ham | kor | lig | imiz | ni`
- SentencePiece-BPE-8k：`▁h | am | k | or | li | g | imiz | ni`

切分数量：mBERT 5，XLM-R 5，SentencePiece 8。

## 20. 乌兹别克语：`rivojlantirishimiz`

原句：Rivojlantirishimiz uchun ilmiy tadqiqotlar sifatini oshirish va yangi avlod mutaxassislarini tayyorlash muhim ahamiyatga ega.

- mBERT：`ri | ##voj | ##lanti | ##rish | ##imi | ##z`
- XLM-R：`▁rivojlantirish | imiz`
- SentencePiece-BPE-8k：`▁ | ri | v | o | j | lan | tirish | imiz`

切分数量：mBERT 6，XLM-R 2，SentencePiece 8。
