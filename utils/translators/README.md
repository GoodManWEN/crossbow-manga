# 翻译模块

目前效果比较好的翻译模型都是云翻，transformer普及以后现在的序列到序列技术用的模型也不会小，我其实也比较怀疑就算有本地能用的翻译器用户是否能跑得起来。所以总之方案是云翻就对了。

BaseTranslator类实现了一个超时和重复获取的基类，插件应在此之上引用基类，并实现自己的业务逻辑即可。base会在失败时重新请求，失败多了会报告失败。